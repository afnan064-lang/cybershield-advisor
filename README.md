# 🛡️ CyberShield Advisor
**Cybersecurity & Phishing Detection Advisor** - a rule-based Expert System built with Python + Streamlit.

| Requirement | Where |
|---|---|
| Knowledge base: **100 rules** | `kb.py` (`_RULE_DEFS`) |
| Knowledge base: **300 assertions** (200 observed + 40 derived + 60 verdicts) | `kb.py` |
| Inference engine (forward chaining + explanation) | `engine.py` |
| Natural-language interface (chat, ready-made problems, custom picker) | `app.py`, `engine.parse_text` |

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
python check_kb.py   # validates 100 rules / 300 assertions
```

## Deploy on Streamlit Community Cloud
1. Create a GitHub repo and upload all files in this folder (keep the folder structure).
2. Go to https://share.streamlit.io, click **Create app**, choose your repo, branch `main`, main file `app.py`.
3. Click **Deploy**.

## Files
- `app.py` - web interface (Home, Advisor chat, Knowledge Base, How It Works)
- `engine.py` - forward-chaining inference engine + text parser
- `kb.py` - assertions, rules, verdict advice, ready-made problems
- `style.py` - theme CSS
- `docs/PRESENTATION_NOTES.md` - notes for your presentation

## Add your own problem
Add a row to `PRESETS` in `kb.py`: `("E", "your short problem text", ["E01", "E04"])`.
