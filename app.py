"""CyberShield Advisor - Cybersecurity & Phishing Detection Expert System (Streamlit UI)."""
import html
import json

import streamlit as st

import engine
from kb import (ASSERTIONS, CATEGORIES, ICONS, PRESETS, RULES, VERDICTS)
from style import CSS

st.set_page_config(page_title="CyberShield Advisor", page_icon="🛡️", layout="wide")
st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

PAGES = ["Home", "Advisor", "Knowledge Base", "How It Works"]
N_RULES, N_ASSERT = len(RULES), len(ASSERTIONS)
OBS_IDS = [k for k, a in ASSERTIONS.items() if a["kind"] == "Observed"]

# ------------------------------------------------------------------ state
st.session_state.setdefault("messages", [])
st.session_state.setdefault("edit_open", False)
st.session_state.setdefault("custom_text", "")
st.session_state.setdefault("custom_facts", [])


def go(page):
    st.session_state["nav"] = page


def run_analysis(text, facts):
    label = text.strip() or "Selected signs: " + ", ".join(ASSERTIONS[f]["text"] for f in facts[:4])
    st.session_state.messages.append({"role": "user", "text": label})
    st.session_state.messages.append({"role": "assistant", "result": engine.analyze(text, facts)})


def send_preset(i):
    _, text, facts = PRESETS[i]
    st.session_state.edit_open = False
    run_analysis(text, facts)


def edit_preset(i):
    _, text, facts = PRESETS[i]
    st.session_state.custom_text = text
    st.session_state.custom_facts = list(facts)
    st.session_state.edit_open = True


def send_custom():
    run_analysis(st.session_state.custom_text, st.session_state.custom_facts)


# ------------------------------------------------------------------ header
st.markdown('<div class="topstrip">🔒 Free educational tool &nbsp;|&nbsp; Expert System with '
            f'{N_RULES} rules and {N_ASSERT} assertions</div>', unsafe_allow_html=True)
c1, c2 = st.columns([2, 5])
c1.markdown('<div class="logo"><i>🛡️</i>CyberShield</div>', unsafe_allow_html=True)
page = c2.radio("Menu", PAGES, horizontal=True, label_visibility="collapsed", key="nav")


# ------------------------------------------------------------------ helpers
def chips(ids):
    return "".join(f'<span class="chip">{html.escape(ASSERTIONS[i]["text"])}</span>' for i in ids)


def render_result(res):
    if not res["observed"]:
        st.markdown("I could not find a warning sign in that message. Try describing what you saw "
                    "(for example: *an email asked for my password*) or pick a ready-made problem on the left.")
        return
    st.markdown("**I understood these signs:**")
    st.markdown(chips(res["observed"]), unsafe_allow_html=True)
    vs = res["verdicts"]
    if not vs:
        st.markdown('<div class="banner r-Low"><b>No known threat pattern matched</b>'
                    f'<span>{len(res["observed"])} signs checked</span></div>', unsafe_allow_html=True)
        st.markdown("Add more details to get a sharper answer. Meanwhile: use unique passwords, turn on "
                    "two-factor authentication, and never share OTP codes.")
    else:
        st.markdown(f'<div class="banner r-{res["overall"]}"><b>Overall risk: {res["overall"]}</b>'
                    f'<span>{len(vs)} threat pattern(s) found</span></div>', unsafe_allow_html=True)
        for v in vs[:3]:
            steps = "".join(f"<li>{html.escape(s)}</li>" for s in v["steps"])
            st.markdown(
                f'<div class="vcard r-{v["risk"]}"><div class="vtop"><h4>{html.escape(v["title"])}</h4>'
                f'<span class="pill">{v["risk"]} &middot; {v["confidence"]}% match</span></div>'
                f'<div class="vcat">{ICONS[v["cat"]]} {CATEGORIES[v["cat"]]}</div><ol>{steps}</ol></div>',
                unsafe_allow_html=True)
        if len(vs) > 3:
            with st.expander(f"{len(vs) - 3} more threat pattern(s)"):
                for v in vs[3:]:
                    st.markdown(f"**{v['title']}** ({v['risk']}): " + " ".join(v["steps"]))
        with st.expander("Why did I say this? (rules used)"):
            for v in vs[:3]:
                st.markdown(f"**{v['title']}**")
                for r in engine.explain(res, v["id"]):
                    st.markdown(f'<div class="rtrace"><code>{r["id"]}</code> IF {html.escape(engine.describe_rule(r))} '
                                f'&rarr; <b>{html.escape(ASSERTIONS[r["then"]]["text"])}</b></div>',
                                unsafe_allow_html=True)
    for p in res["possible"]:
        st.markdown(f'<div class="poss"><b>Could also be: {html.escape(p["title"])}</b> ({p["risk"]}). '
                    f'Check if: {html.escape(" / ".join(p["missing"]))}</div>', unsafe_allow_html=True)


# ------------------------------------------------------------------ HOME
if page == "Home":
    with st.container(key="hero"):
        l, r = st.columns([6, 5], gap="large")
        with l:
            st.markdown('<span class="hero-tag">Expert System &middot; Phishing Detection</span>'
                        '<div class="hero-h">Spot phishing before it spots you.</div>'
                        '<div class="hero-p">Describe what happened in plain words. CyberShield checks it against '
                        f'{N_RULES} expert rules and tells you the threat and what to do next.</div>',
                        unsafe_allow_html=True)
            st.write("")
            st.button("Check a problem now", type="primary", on_click=go, args=("Advisor",))
        with r:
            st.markdown(
                '<div class="scan"><div class="scan-line"></div>'
                '<div class="scan-msg">&ldquo;Your account is suspended. Verify now or it will be closed.&rdquo;</div>'
                '<div class="scan-row"><span>Credential Phishing Email</span>'
                '<span class="pill r-High">High risk</span></div>'
                '<div class="bar"><b style="width:87%"></b></div>'
                '<div style="color:#B8CBDD;font-size:.82rem;margin-top:.4rem">87% match &middot; 3 rules fired</div>'
                '</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="stats"><div class="stat"><b>{N_RULES}</b><span>Expert rules</span></div>'
                f'<div class="stat"><b>{N_ASSERT}</b><span>Assertions</span></div>'
                f'<div class="stat"><b>{len(CATEGORIES)}</b><span>Topic areas</span></div>'
                f'<div class="stat"><b>{len(VERDICTS)}</b><span>Threats it can name</span></div></div>',
                unsafe_allow_html=True)
    st.markdown('<div class="sec-h">What it checks</div><div class="sec-p">Ten areas of everyday cyber safety.</div>',
                unsafe_allow_html=True)
    desc = {"E": "Fake and risky emails", "L": "Dangerous links and QR codes", "S": "Scam texts and calls",
            "W": "Fake shops and login pages", "A": "Passwords and hacked accounts", "M": "Viruses and ransomware",
            "N": "Unsafe WiFi and routers", "F": "Job, love and investment scams", "B": "Card and bank fraud",
            "D": "Leaks and identity theft"}
    cards = "".join(f'<div class="cardx"><div class="ic">{ICONS[k]}</div><h4>{CATEGORIES[k]}</h4>'
                    f'<p>{desc[k]}</p></div>' for k in CATEGORIES)
    st.markdown(f'<div class="grid5">{cards}</div>', unsafe_allow_html=True)
    st.markdown('<div class="band"><h3>Not sure what is wrong?</h3>'
                '<p>Pick a ready-made problem or type your own. You get an answer in seconds.</p></div>',
                unsafe_allow_html=True)
    st.write("")
    st.button("Open the Advisor", type="primary", on_click=go, args=("Advisor",), key="cta2")

# ------------------------------------------------------------------ ADVISOR
elif page == "Advisor":
    prompt = st.chat_input("Describe your problem, e.g. I got an email asking for my password")
    if prompt:
        run_analysis(prompt, [])

    st.markdown('<div class="sec-h" style="margin-top:.6rem">Cyber Safety Advisor</div>'
                '<div class="sec-p">Pick a ready-made problem, edit it, or type your own in the chat box below.</div>',
                unsafe_allow_html=True)
    left, right = st.columns([5, 6], gap="large")

    with left:
        st.markdown('<div class="panel-h">Ready-made problems</div>', unsafe_allow_html=True)
        cat = st.radio("Topic", list(CATEGORIES), format_func=lambda k: f"{ICONS[k]} {CATEGORIES[k]}",
                       horizontal=True, label_visibility="collapsed", key="cat")
        for i, (c, text, facts) in enumerate(PRESETS):
            if c != cat:
                continue
            a, b, d = st.columns([6, 1.3, 1.3], vertical_alignment="center")
            a.markdown(f'<div class="prob">{html.escape(text)}</div>', unsafe_allow_html=True)
            b.button("Send", key=f"s{i}", on_click=send_preset, args=(i,), type="primary")
            d.button("Edit", key=f"e{i}", on_click=edit_preset, args=(i,))
        with st.expander("Customize a problem", expanded=st.session_state.edit_open):
            st.text_area("Your description", key="custom_text", height=90,
                         placeholder="Write what happened in your own words")
            st.multiselect("Warning signs (add or remove)", OBS_IDS, key="custom_facts",
                           format_func=lambda k: f"{CATEGORIES[ASSERTIONS[k]['cat']]}: {ASSERTIONS[k]['text']}")
            st.button("Analyze my problem", on_click=send_custom, type="primary", key="go_custom")

    with right:
        st.markdown('<div class="panel-h">Advisor chat <span style="font-weight:500;color:#5B6B7C;'
                    'font-size:.85rem">(newest first)</span></div>', unsafe_allow_html=True)
        msgs = st.session_state.messages
        if not msgs:
            with st.chat_message("assistant", avatar="🛡️"):
                st.markdown("Hi! I am **CyberShield**. Tell me what happened, for example *a caller asked for my OTP*. "
                            "Or choose a ready-made problem on the left.")
        pairs = [msgs[i:i + 2] for i in range(0, len(msgs), 2)][::-1]
        for u, a in pairs:
            with st.chat_message("user", avatar="🧑"):
                st.markdown(u["text"])
            with st.chat_message("assistant", avatar="🛡️"):
                render_result(a["result"])
        if msgs:
            st.button("Clear chat", on_click=lambda: st.session_state.messages.clear())

# ------------------------------------------------------------------ KNOWLEDGE BASE
elif page == "Knowledge Base":
    st.markdown('<div class="sec-h" style="margin-top:.6rem">Knowledge Base</div>'
                f'<div class="sec-p">{N_ASSERT} assertions and {N_RULES} rules. Search and filter below.</div>',
                unsafe_allow_html=True)
    q = st.text_input("Search", placeholder="Search a word, e.g. password", label_visibility="collapsed")
    t1, t2, t3 = st.tabs([f"Rules ({N_RULES})", f"Assertions ({N_ASSERT})", "Threat advice"])
    with t1:
        rows = []
        for r in RULES:
            row = {"Rule": r["id"], "IF": engine.describe_rule(r),
                   "THEN": ASSERTIONS[r["then"]]["text"],
                   "Type": "Verdict" if r["then"].startswith("V") else "Signal"}
            if q.lower() in " ".join(map(str, row.values())).lower():
                rows.append(row)
        st.dataframe(rows, width="stretch", hide_index=True, height=480)
    with t2:
        rows = [{"ID": k, "Assertion": a["text"], "Type": a["kind"],
                 "Topic": CATEGORIES.get(a["cat"], "Derived")}
                for k, a in ASSERTIONS.items() if q.lower() in (a["text"] + a["kind"]).lower()]
        st.dataframe(rows, width="stretch", hide_index=True, height=480)
    with t3:
        rows = [{"ID": k, "Threat": v[0], "Topic": CATEGORIES[v[1]], "Risk": v[2],
                 "Advice": " ".join(v[3].split("|"))} for k, v in VERDICTS.items()
                if q.lower() in (v[0] + v[3]).lower()]
        st.dataframe(rows, width="stretch", hide_index=True, height=480)
    st.download_button("Download knowledge base (JSON)",
                       json.dumps({"assertions": ASSERTIONS, "rules": RULES}, indent=1),
                       "knowledge_base.json", "application/json")

# ------------------------------------------------------------------ HOW IT WORKS
else:
    st.markdown('<div class="sec-h" style="margin-top:.6rem">How it works</div>'
                '<div class="sec-p">A classic rule-based expert system in four steps.</div>', unsafe_allow_html=True)
    steps = [("1", "Understand", "The natural-language interface reads your words and matches them to known warning signs."),
             ("2", "Remember", "Matched signs are stored as facts in working memory."),
             ("3", "Reason", "The inference engine uses forward chaining: it fires every rule whose conditions are true, "
                             "adds new facts, and repeats until nothing new appears."),
             ("4", "Explain", "You get the threat, a risk level, a match score, simple steps, and the rules used.")]
    cards = "".join(f'<div class="cardx"><div class="ic">{n}</div><h4>{t}</h4><p>{d}</p></div>' for n, t, d in steps)
    st.markdown(f'<div class="grid4">{cards}</div>', unsafe_allow_html=True)
    st.markdown("#### Example")
    st.code("Facts:  E01 asks to verify account, E02 account suspended, E07 'Dear Customer'\n"
            "R001..R040 (signals)  ->  I02 pressure tactics\n"
            "R042 IF E02 AND (E01 OR E14) AND (I01 OR E07)  ->  V02 Fake Account-Suspension Email (High)",
            language="text")
    st.markdown("#### Parts of the system")
    st.markdown("- **Knowledge base** (`kb.py`): 200 observed + 40 derived + 60 verdict assertions, 100 IF-THEN rules\n"
                "- **Inference engine** (`engine.py`): forward chaining with an explanation facility\n"
                "- **Natural-language interface**: free text, ready-made problems, and a custom sign picker\n"
                "- **User interface** (`app.py`, `style.py`): Streamlit with a custom theme")

st.markdown('<div class="foot">CyberShield Advisor &middot; Educational expert system. '
            'For serious incidents, contact your bank or a security professional.</div>', unsafe_allow_html=True)
