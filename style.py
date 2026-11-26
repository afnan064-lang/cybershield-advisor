CSS = """
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800&family=Manrope:wght@400;500;600;700&display=swap');
:root{--ink:#071826;--ink2:#0C2A44;--mint:#14D9B5;--cyan:#22B8F0;--bg:#F2F6FA;--card:#fff;
--line:#E1EAF2;--muted:#5B6B7C;--crit:#E5384F;--high:#F2791B;--med:#E5A900;--low:#16B672;}
html,body,[class*="css"],.stApp{font-family:'Manrope',sans-serif;}
.stApp{background:var(--bg);}
#MainMenu,footer,header[data-testid="stHeader"]{visibility:hidden;height:0;}
.block-container{max-width:1180px;padding-top:1rem;padding-bottom:5rem;}
h1,h2,h3,h4{font-family:'Sora',sans-serif;color:var(--ink);letter-spacing:-.02em;}

/* top bar + nav */
.topstrip{background:var(--ink);color:#B8CBDD;font-size:.8rem;padding:.45rem 1rem;border-radius:12px;
 text-align:center;margin-bottom:.8rem;}
.logo{display:flex;align-items:center;gap:.6rem;font-family:'Sora',sans-serif;font-weight:800;
 font-size:1.35rem;color:var(--ink);padding-top:.35rem;}
.logo i{display:inline-flex;width:38px;height:38px;border-radius:11px;align-items:center;justify-content:center;
 background:linear-gradient(135deg,var(--mint),var(--cyan));font-style:normal;font-size:1.1rem;}
.st-key-nav div[role="radiogroup"],.st-key-cat div[role="radiogroup"]{gap:.3rem;flex-wrap:wrap;}
.st-key-nav div[role="radiogroup"]{justify-content:flex-end;}
.st-key-nav label,.st-key-cat label{padding:.45rem 1.05rem;border-radius:999px;cursor:pointer;border:1px solid transparent;}
.st-key-cat label{border-color:var(--line);background:#fff;padding:.3rem .8rem;}
.st-key-nav label>div:first-child,.st-key-cat label>div:first-child{display:none;}
.st-key-nav label p,.st-key-cat label p{font-weight:600;font-size:.92rem;margin:0;}
.st-key-nav label:has(input:checked){background:var(--ink);}
.st-key-nav label:has(input:checked) p{color:#fff;}
.st-key-cat label:has(input:checked){background:var(--mint);border-color:var(--mint);}
.st-key-cat label:has(input:checked) p{color:var(--ink);}

/* hero */
.st-key-hero{background:radial-gradient(900px 400px at 85% 10%,rgba(20,217,181,.22),transparent 60%),
 linear-gradient(135deg,#061522 0%,#0C2A44 65%,#0E3B52 100%);border-radius:26px;padding:3.2rem 3rem;
 position:relative;overflow:hidden;}
.st-key-hero:before{content:"";position:absolute;inset:0;opacity:.35;
 background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);
 background-size:38px 38px;pointer-events:none;}
.hero-tag{display:inline-block;background:rgba(20,217,181,.14);color:var(--mint);border:1px solid rgba(20,217,181,.4);
 padding:.3rem .8rem;border-radius:999px;font-size:.82rem;font-weight:600;}
.hero-h{font-family:'Sora',sans-serif;font-weight:800;color:#fff;font-size:3rem;line-height:1.08;margin:1rem 0;}
.hero-p{color:#B8CBDD;font-size:1.08rem;line-height:1.6;max-width:30rem;}
.scan{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14);border-radius:20px;padding:1.3rem;
 backdrop-filter:blur(6px);position:relative;}
.scan-line{height:3px;border-radius:3px;background:linear-gradient(90deg,transparent,var(--mint),transparent);
 animation:sweep 2.6s ease-in-out infinite;margin-bottom:1rem;}
@keyframes sweep{0%,100%{opacity:.2;transform:translateX(-20%)}50%{opacity:1;transform:translateX(20%)}}
.scan-msg{color:#DCE8F3;font-size:.92rem;background:rgba(0,0,0,.25);border-radius:12px;padding:.8rem;margin-bottom:.8rem;}
.scan-row{display:flex;justify-content:space-between;align-items:center;color:#fff;font-weight:700;margin-top:.5rem;}
.pill{border-radius:999px;padding:.2rem .7rem;font-size:.78rem;font-weight:700;color:#fff;}
.bar{height:8px;border-radius:8px;background:rgba(255,255,255,.12);margin-top:.5rem;overflow:hidden;}
.bar b{display:block;height:100%;background:linear-gradient(90deg,var(--mint),var(--cyan));}
@media (prefers-reduced-motion:reduce){.scan-line{animation:none}}

/* buttons */
.stButton>button,.stDownloadButton>button{border-radius:12px;font-weight:700;border:1px solid var(--line);}
button[kind="primary"],button[data-testid="stBaseButton-primary"]{
 background:linear-gradient(135deg,var(--mint),var(--cyan))!important;color:var(--ink)!important;border:none!important;
 padding:.6rem 1.4rem;box-shadow:0 8px 20px rgba(20,217,181,.3);}
.stButton>button:focus-visible{outline:3px solid var(--cyan);}

/* sections */
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin:1.4rem 0;}
.stat{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:1.2rem 1.4rem;}
.stat b{font-family:'Sora',sans-serif;font-size:2rem;color:var(--ink);display:block;}
.stat span{color:var(--muted);font-size:.9rem;}
.sec-h{font-size:1.8rem;font-weight:800;margin:2.2rem 0 .3rem;}
.sec-p{color:var(--muted);margin-bottom:1.2rem;}
.grid5{display:grid;grid-template-columns:repeat(5,1fr);gap:1rem;}
.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;}
.cardx{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:1.2rem;}
.cardx .ic{font-size:1.6rem;width:46px;height:46px;border-radius:13px;background:#E8FAF6;display:flex;
 align-items:center;justify-content:center;margin-bottom:.7rem;}
.cardx h4{margin:.1rem 0 .3rem;font-size:1.02rem;}
.cardx p{color:var(--muted);font-size:.88rem;margin:0;line-height:1.5;}
.band{background:linear-gradient(135deg,var(--ink),var(--ink2));border-radius:22px;padding:2rem 2.4rem;margin-top:2rem;
 color:#fff;}
.band h3{color:#fff;margin:0 0 .3rem;}
.band p{color:#B8CBDD;margin:0;}
.foot{text-align:center;color:var(--muted);font-size:.85rem;margin-top:3rem;}

/* advisor */
.panel-h{font-family:'Sora',sans-serif;font-weight:700;font-size:1.15rem;color:var(--ink);margin-bottom:.2rem;}
.prob{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:.7rem .9rem;font-size:.93rem;
 line-height:1.4;min-height:3.2rem;display:flex;align-items:center;}
.chip{display:inline-block;background:#E8FAF6;color:#0A6B5B;border-radius:999px;padding:.22rem .7rem;font-size:.8rem;
 font-weight:600;margin:.15rem .2rem .15rem 0;}
.banner{border-radius:16px;padding:1rem 1.2rem;color:#fff;display:flex;justify-content:space-between;
 align-items:center;flex-wrap:wrap;gap:.4rem;margin-bottom:.8rem;}
.banner b{font-family:'Sora',sans-serif;font-size:1.1rem;}
.vcard{background:var(--card);border:1px solid var(--line);border-left:6px solid;border-radius:16px;
 padding:1rem 1.2rem;margin-bottom:.8rem;}
.vtop{display:flex;justify-content:space-between;align-items:center;gap:.6rem;flex-wrap:wrap;}
.vtop h4{margin:0;font-size:1.05rem;}
.vcat{color:var(--muted);font-size:.8rem;}
.vcard ol{margin:.6rem 0 0 1.1rem;padding:0;color:#23384D;font-size:.93rem;line-height:1.6;}
.r-Critical{--c:var(--crit);}.r-High{--c:var(--high);}.r-Medium{--c:var(--med);}.r-Low{--c:var(--low);}
.banner{background:var(--c);}.vcard{border-left-color:var(--c);}.pill{background:var(--c);}
.poss{background:#FFF9E6;border:1px solid #F4E3A1;border-radius:14px;padding:.7rem 1rem;font-size:.88rem;margin-bottom:.5rem;}
.rtrace{font-size:.85rem;color:#23384D;border-bottom:1px dashed var(--line);padding:.35rem 0;}
.rtrace code{background:#E8FAF6;color:#0A6B5B;border-radius:6px;padding:.05rem .4rem;}
@media(max-width:900px){.stats,.grid4{grid-template-columns:repeat(2,1fr)}.grid5{grid-template-columns:repeat(2,1fr)}
 .hero-h{font-size:2.1rem}.st-key-hero{padding:1.6rem}}

/* ---- force readable light theme (even if the browser/Streamlit is in dark mode) ---- */
:root,.stApp{color-scheme:light;}
.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"]{background:var(--bg)!important;}
.stApp p,.stApp span,.stApp li,.stApp label,.stApp div,.stApp summary,.stApp code,
[data-testid="stMarkdownContainer"] *,[data-testid="stChatMessage"] *{color:#071826;}
.stApp h1,.stApp h2,.stApp h3,.stApp h4{color:#071826!important;}
/* keep light text only where the background is dark */
.st-key-hero .hero-h,.band h3{color:#fff!important;}
.st-key-hero .hero-p,.band p,.topstrip{color:#B8CBDD!important;}
.hero-tag{color:#14D9B5!important;}
.scan *{color:#DCE8F3;} .scan .pill,.banner,.banner *,.pill{color:#fff!important;}
.st-key-nav label:has(input:checked) *{color:#fff!important;}
.st-key-cat label:has(input:checked) *{color:#071826!important;}
.chip{color:#0A6B5B!important;}
button[kind="primary"] *,button[data-testid="stBaseButton-primary"] *{color:#071826!important;}
/* secondary buttons: white with dark text */
button[data-testid="stBaseButton-secondary"],.stButton>button[kind="secondary"],.stDownloadButton>button{
 background:#fff!important;border:1px solid #C9D6E2!important;}
button[data-testid="stBaseButton-secondary"] *,.stDownloadButton>button *{color:#071826!important;}
/* radio circles hidden for pill menus */
.st-key-nav label[data-baseweb="radio"]>div:first-child,.st-key-cat label[data-baseweb="radio"]>div:first-child,
.st-key-nav label>span:first-child,.st-key-cat label>span:first-child{display:none!important;}
/* inputs and expanders */
.stTextInput input,.stTextArea textarea,[data-baseweb="select"]>div,[data-baseweb="input"]{
 background:#fff!important;color:#071826!important;border-color:#C9D6E2!important;}
[data-baseweb="tag"]{background:#E8FAF6!important;} [data-baseweb="tag"] *{color:#0A6B5B!important;}
[data-testid="stExpander"]{background:#fff;border:1px solid #C9D6E2;border-radius:14px;}
[data-testid="stChatMessage"]{background:#fff;border:1px solid var(--line);border-radius:16px;}
.prob{color:#071826!important;background:#fff;}
"""
