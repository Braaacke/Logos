import base64
import json
import random
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "logos.json"
LOGO_DIR = BASE_DIR / "logos"

st.set_page_config(page_title="Logo-Quiz", page_icon="🎯", layout="centered")


@st.cache_data
def load_logos():
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


def normalize(text: str) -> str:
    return " ".join(text.casefold().strip().split())


def make_options(item, all_items, n_wrong=3):
    wrong = [i["name"] for i in all_items if i["name"] != item["name"]]
    options = random.sample(wrong, min(n_wrong, len(wrong))) + [item["name"]]
    random.shuffle(options)
    return options


def start_quiz(n_questions, mode):
    logos = load_logos()
    items = random.sample(logos, n_questions)
    st.session_state.quiz = {
        "items": items,
        "i": 0,
        "score": 0,
        "mode": mode,
        "answered": False,
        "correct": None,
        "given": None,
        "options": make_options(items[0], logos),
    }


def next_question():
    q = st.session_state.quiz
    q["i"] += 1
    q["answered"] = False
    q["correct"] = None
    q["given"] = None
    if q["i"] < len(q["items"]):
        q["options"] = make_options(q["items"][q["i"]], load_logos())


def reset_quiz():
    st.session_state.pop("quiz", None)


def check_answer(given: str):
    q = st.session_state.quiz
    item = q["items"][q["i"]]
    accepted = [normalize(item["name"])] + [normalize(a) for a in item.get("aliases", [])]
    q["given"] = given
    q["correct"] = normalize(given) in accepted
    q["answered"] = True
    if q["correct"]:
        q["score"] += 1


def show_logo(item):
    path = LOGO_DIR / item["image"]
    if not path.exists():
        st.warning(f"Bild fehlt: logos/{item['image']}")
        return
    if path.suffix.lower() == ".svg":
        b64 = base64.b64encode(path.read_bytes()).decode()
        st.markdown(
            f'<div style="background:#fff;border-radius:16px;padding:32px;'
            f'border:1px solid #e5e5e5;text-align:center">'
            f'<img src="data:image/svg+xml;base64,{b64}" '
            f'style="max-width:100%;height:180px"></div>',
            unsafe_allow_html=True,
        )
    else:
        st.image(str(path), use_container_width=True)


# ---------------------------------------------------------------- Start
st.title("🎯 Logo-Quiz")

logos = load_logos()

if "quiz" not in st.session_state:
    st.write("Erkennst du die Marken an ihren Logos?")
    mode = st.radio(
        "Modus",
        ["Multiple Choice", "Freitext"],
        horizontal=True,
    )
    max_q = len(logos)
    if max_q < 2:
        st.error("Bitte mindestens 2 Logos in data/logos.json eintragen.")
        st.stop()
    n = st.slider("Anzahl Fragen", 1, max_q, min(10, max_q)) if max_q > 1 else 1
    st.button("Quiz starten", type="primary", on_click=start_quiz, args=(n, mode))
    st.stop()

# ---------------------------------------------------------------- Ergebnis
q = st.session_state.quiz
total = len(q["items"])

if q["i"] >= total:
    st.header("Geschafft! 🎉")
    st.metric("Ergebnis", f"{q['score']} / {total}")
    share = q["score"] / total
    if share == 1:
        st.success("Perfekt – du bist ein Logo-Profi!")
    elif share >= 0.7:
        st.info("Sehr stark!")
    elif share >= 0.4:
        st.info("Solide, da geht noch mehr.")
    else:
        st.info("Übung macht den Meister – versuch es nochmal!")
    st.button("Nochmal spielen", type="primary", on_click=reset_quiz)
    st.stop()

# ---------------------------------------------------------------- Frage
item = q["items"][q["i"]]
st.progress(q["i"] / total, text=f"Frage {q['i'] + 1} von {total} · Punkte: {q['score']}")

col_l, col_m, col_r = st.columns([1, 2, 1])
with col_m:
    show_logo(item)

if not q["answered"]:
    with st.form(key=f"form_{q['i']}"):
        if q["mode"] == "Multiple Choice":
            answer = st.radio("Welche Marke ist das?", q["options"], index=None)
        else:
            answer = st.text_input("Welche Marke ist das?")
        submitted = st.form_submit_button("Antworten", type="primary")
    if submitted:
        if answer:
            check_answer(answer)
            st.rerun()
        else:
            st.warning("Bitte gib eine Antwort ein.")
else:
    if q["correct"]:
        st.success(f"Richtig! Das ist **{item['name']}**.")
    else:
        st.error(f"Leider falsch. Richtig wäre: **{item['name']}** (deine Antwort: {q['given']})")
    if item.get("info"):
        st.caption(item["info"])
    label = "Nächste Frage" if q["i"] + 1 < total else "Ergebnis anzeigen"
    st.button(label, type="primary", on_click=next_question)

st.divider()
st.button("Quiz abbrechen", on_click=reset_quiz)
