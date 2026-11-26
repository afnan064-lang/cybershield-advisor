"""Run: python check_kb.py  -> validates the knowledge base counts and references."""
from kb import ASSERTIONS, RULES, VERDICTS, INTERMEDIATE, PRESETS
import engine

kinds = {}
for a in ASSERTIONS.values():
    kinds[a["kind"]] = kinds.get(a["kind"], 0) + 1
print("Assertions:", len(ASSERTIONS), kinds)
print("Rules:", len(RULES))
assert len(ASSERTIONS) == 300 and len(RULES) == 100
for r in RULES:
    assert r["then"] in ASSERTIONS, r
    for g in r["groups"]:
        for x in g:
            assert x in ASSERTIONS, (r["id"], x)
print("All references valid.")
for cat, text, facts in PRESETS:
    res = engine.analyze(text, facts)
    top = res["verdicts"][0]["title"] if res["verdicts"] else "NONE"
    print(f"{cat} | {top:35} | {text[:50]}")
