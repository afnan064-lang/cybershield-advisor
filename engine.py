"""Inference engine (forward chaining) + natural-language parser."""
import math
import re
from difflib import get_close_matches

from kb import ASSERTIONS, RULES, VERDICTS, HINTS, RISK_ORDER

STOP = set("i me my a an the to of in on at is are was were be it its and or for from with that "
           "this by as so do does did am im ive have has had got get just very really also than "
           "then there they them he she we you your our us can could would will".split())
SYN = {"mail": "email", "mails": "email", "emails": "email", "txt": "sms", "text": "sms",
       "message": "sms", "messages": "sms", "pwd": "password", "pass": "password",
       "urgently": "urgent", "immediately": "urgent", "scam": "fake", "fraud": "fake",
       "wi-fi": "wifi", "hacker": "hack", "hacked": "hack", "phished": "phishing",
       "website": "site", "web": "site", "webpage": "site", "pretending": "pretend",
       "pretends": "pretend", "called": "caller", "calling": "caller", "calls": "caller", "phoned": "caller", "rang": "caller", "deadline": "urgent", "hurry": "urgent", "asked": "ask", "asking": "ask", "asks": "ask", "popup": "pop-up", "popups": "pop-up", "encrypted": "locked", "slowly": "slow", "hot": "overheat", "claims": "say", "claim": "say", "says": "say", "said": "say"}


def _stem(w):
    for suf in ("ing", "ed", "es", "s"):
        if len(w) > len(suf) + 2 and w.endswith(suf):
            return w[: -len(suf)]
    return w


def tokens(text):
    t = text.lower().replace("log in", "login").replace("sign in", "login").replace("cannot", "cant")
    t = t.replace("wi-fi", "wifi")
    words = re.findall(r"[a-z0-9']+", t)
    out = []
    for w in words:
        w = SYN.get(w, w)
        if w in STOP:
            continue
        out.append(_stem(SYN.get(_stem(w), w)))
    return out


# --- pre-compute token sets and IDF weights for observed assertions
_OBS_TOK = {i: set(tokens(a["text"])) for i, a in ASSERTIONS.items() if a["kind"] == "Observed"}
_DF = {}
for _s in _OBS_TOK.values():
    for _w in _s:
        _DF[_w] = _DF.get(_w, 0) + 1
_N = len(_OBS_TOK)
_W = {w: math.log(_N / d) + 1 for w, d in _DF.items()}


def parse_text(text, threshold=0.6):
    """Natural language -> list of observed assertion ids."""
    words = tokens(text)
    wset = set(words)
    found = {}
    for w in words:
        for i in HINTS.get(w, []):
            found[i] = 1.0
    for i, toks in _OBS_TOK.items():
        if not toks:
            continue
        got, total, hit = 0.0, 0.0, 0
        for t in toks:
            wt = _W[t]
            total += wt
            if t in wset or get_close_matches(t, wset, n=1, cutoff=0.85):
                got += wt
                hit += 1
        score = got / total
        if score >= threshold and hit >= 2:
            found[i] = max(found.get(i, 0), score)
    return [i for i, _ in sorted(found.items(), key=lambda x: -x[1])]


# --- forward chaining
def infer(facts):
    """Repeat: fire every rule whose groups all hold; add its conclusion. Stop when nothing new."""
    memory = set(facts)
    fired = {}
    changed = True
    while changed:
        changed = False
        for r in RULES:
            if r["id"] in fired or r["then"] in memory:
                continue
            matched = []
            for g in r["groups"]:
                hit = [x for x in g if x in memory]
                if not hit:
                    break
                matched.append(hit)
            else:
                memory.add(r["then"])
                fired[r["id"]] = matched
                changed = True
    return memory, fired


def _support(concl, rules_by_then, fired, cache):
    """Observed facts that led to a conclusion (for the confidence score)."""
    if concl in cache:
        return cache[concl]
    if ASSERTIONS[concl]["kind"] == "Observed":
        cache[concl] = {concl}
        return cache[concl]
    r = rules_by_then.get(concl)
    s = set()
    if r and r["id"] in fired:
        for hit in fired[r["id"]]:
            for x in hit:
                s |= _support(x, rules_by_then, fired, cache)
    cache[concl] = s
    return s


def explain(result, vid):
    """Rules that were used to reach verdict vid, in order (dependencies first)."""
    by_then = {r["then"]: r for r in RULES}
    order, seen = [], set()

    def walk(x):
        r = by_then.get(x)
        if not r or r["id"] not in result["fired"] or r["id"] in seen:
            return
        seen.add(r["id"])
        for hit in result["fired"][r["id"]]:
            for y in hit:
                walk(y)
        order.append(r)

    walk(vid)
    return order


def describe_rule(r):
    parts = []
    for g in r["groups"]:
        txt = " OR ".join(ASSERTIONS[x]["text"] for x in g)
        parts.append(f"({txt})" if len(g) > 1 else txt)
    return " AND ".join(parts)


def analyze(text, facts=()):
    """Full pipeline: parse text, merge facts, infer, rank verdicts."""
    parsed = parse_text(text) if text else []
    observed = list(dict.fromkeys(list(facts) + parsed))
    memory, fired = infer(observed)
    by_then = {r["then"]: r for r in RULES}
    cache = {}
    verdicts = []
    for vid, (title, cat, risk, adv) in VERDICTS.items():
        rule = by_then[vid]
        if rule["id"] in fired:
            n = len(_support(vid, by_then, fired, cache))
            verdicts.append({"id": vid, "title": title, "cat": cat, "risk": risk,
                             "steps": adv.split("|"), "confidence": min(97, 55 + 8 * n),
                             "signs": n})
    verdicts.sort(key=lambda v: (-RISK_ORDER[v["risk"]], -v["confidence"]))
    possible = []
    for vid, (title, cat, risk, adv) in VERDICTS.items():
        rule = by_then[vid]
        if rule["id"] in fired:
            continue
        miss = [g for g in rule["groups"] if not any(x in memory for x in g)]
        if len(miss) == 1 and len(rule["groups"]) > 1:
            possible.append({"id": vid, "title": title, "risk": risk,
                             "missing": [ASSERTIONS[x]["text"] for x in miss[0][:3]]})
    possible.sort(key=lambda v: -RISK_ORDER[v["risk"]])
    overall = verdicts[0]["risk"] if verdicts else None
    return {"text": text, "observed": observed, "parsed": parsed, "memory": memory,
            "fired": fired, "verdicts": verdicts, "possible": possible[:3], "overall": overall}
