# 🎯 Logo-Quiz

Ein einfaches Logo-Quiz mit [Streamlit](https://streamlit.io) – wahlweise als Multiple Choice oder mit Freitext-Eingabe.

## Projektstruktur

```
logo-quiz/
├── app.py              # Streamlit-App
├── requirements.txt    # Abhängigkeiten
├── data/logos.json     # Fragenkatalog
├── logos/              # Logo-Bilder (SVG/PNG/JPG)
└── .streamlit/config.toml
```

## Enthaltene Logos

Das Repository enthält 100 bekannte Marken als SVG-Logos aus dem Paket
[Simple Icons](https://simpleicons.org) (Lizenz: CC0, siehe `logos/LICENSE-simple-icons.md`).
Die Icons sind einfarbig in der jeweiligen Markenfarbe. Die **Marken selbst bleiben Eigentum
ihrer Inhaber** – die CC0-Lizenz betrifft nur die Zeichnung der Icons.

## Logos hinzufügen

1. Bilddatei in den Ordner `logos/` legen (z. B. `meine_marke.png`).
2. In `data/logos.json` einen Eintrag ergänzen:

```json
{"name": "Meine Marke", "image": "meine_marke.png", "aliases": ["MM"], "info": "Optionaler Hinweis"}
```

- `name`: korrekte Antwort (wird auch im Multiple-Choice-Modus angezeigt)
- `aliases`: weitere akzeptierte Schreibweisen im Freitext-Modus (Groß-/Kleinschreibung egal)
- `info`: optionaler Text nach der Antwort

> **Hinweis:** Marken sind rechtlich geschützt. Für eine öffentliche, nicht-kommerzielle Quiz-App
> ist die Nutzung meist unkritisch; prüfe sie bei kommerziellem Einsatz selbst.

## Lokal starten

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Auf GitHub hochladen

```bash
git init
git add .
git commit -m "Logo-Quiz"
git branch -M main
git remote add origin https://github.com/<DEIN-NAME>/logo-quiz.git
git push -u origin main
```

## Veröffentlichen mit Streamlit Community Cloud

1. Auf [share.streamlit.io](https://share.streamlit.io) mit GitHub anmelden.
2. **Create app** → Repository `logo-quiz`, Branch `main`, Main file path `app.py`.
3. **Deploy** klicken – nach ein paar Minuten ist die App unter einer öffentlichen URL erreichbar.

Jeder `git push` aktualisiert die App automatisch.
