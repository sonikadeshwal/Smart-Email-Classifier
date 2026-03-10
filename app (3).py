"""
Smart Email Classifier — Emerald & Teal Theme
Clean, professional dark UI with emerald greens and teal accents
"""

import streamlit as st
import pickle
import re
import os
from datetime import datetime

st.set_page_config(
    page_title="Smart Email Classifier",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

:root {
  --bg-0:#050f0c; --bg-1:#080f0d; --bg-2:#0b1510; --bg-3:#0f1c14; --bg-4:#122018;
  --emerald:#10d9a0; --emerald-2:#0eb889; --emerald-dim:#0a7a5c;
  --emerald-glow:rgba(16,217,160,0.13); --emerald-soft:rgba(16,217,160,0.06);
  --teal:#14c8c8; --teal-2:#0fa8a8; --teal-dim:#0a7070;
  --teal-glow:rgba(20,200,200,0.13); --teal-soft:rgba(20,200,200,0.06);
  --border:#0d2218; --border-2:#133328; --border-3:#1a4535;
  --red:#f05070; --amber:#f0a030; --purple:#a070e0;
  --text-1:#d0ede4; --text-2:#6a9e88; --text-3:#2a5040;
  --radius:12px; --radius-sm:8px; --radius-xs:5px;
}
*,*::before,*::after{box-sizing:border-box;}
html,body,[class*="css"]{font-family:'Plus Jakarta Sans',sans-serif!important;background:var(--bg-0)!important;color:var(--text-1);}
.stApp{background:radial-gradient(ellipse 80% 50% at 10% 0%,rgba(16,217,160,0.04) 0%,transparent 60%),radial-gradient(ellipse 60% 40% at 90% 100%,rgba(20,200,200,0.04) 0%,transparent 60%),var(--bg-0)!important;}
[data-testid="stSidebar"]{background:var(--bg-1)!important;border-right:1px solid var(--border-2)!important;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding:1.8rem 2.2rem;max-width:1180px;}

/* HEADER */
.hdr{padding:2rem 0 1.8rem;margin-bottom:1.8rem;border-bottom:1px solid var(--border-2);position:relative;}
.hdr::after{content:'';position:absolute;bottom:-1px;left:0;width:220px;height:1px;background:linear-gradient(90deg,var(--emerald),transparent);}
.hdr-tag{font-family:'DM Mono',monospace;font-size:.62rem;letter-spacing:.22em;text-transform:uppercase;color:var(--emerald);margin-bottom:.7rem;display:flex;align-items:center;gap:7px;}
.hdr-tag::before{content:'';width:18px;height:1px;background:var(--emerald);}
.hdr-h1{font-size:2.5rem;font-weight:800;color:#fff;letter-spacing:-.03em;line-height:1;margin-bottom:.5rem;}
.hdr-h1 em{font-style:normal;background:linear-gradient(135deg,var(--emerald),var(--teal));-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.hdr-sub{font-size:.78rem;color:var(--text-2);font-family:'DM Mono',monospace;}

/* STATS */
.stat-row{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:1.8rem;}
.stat-tile{background:var(--bg-2);border:1px solid var(--border-2);border-radius:var(--radius);padding:1.1rem 1.3rem;position:relative;overflow:hidden;transition:border-color .25s,transform .2s;}
.stat-tile:hover{border-color:var(--border-3);transform:translateY(-2px);}
.stat-tile::after{content:'';position:absolute;top:0;left:0;right:0;height:2px;border-radius:var(--radius) var(--radius) 0 0;}
.st-em::after{background:linear-gradient(90deg,var(--emerald),var(--teal));}
.st-tl::after{background:linear-gradient(90deg,var(--teal),var(--emerald));}
.st-am::after{background:var(--amber);}
.st-pu::after{background:var(--purple);}
.stat-lbl{font-size:.6rem;letter-spacing:.18em;text-transform:uppercase;color:var(--text-3);font-family:'DM Mono',monospace;margin-bottom:.5rem;}
.stat-num{font-size:1.9rem;font-weight:800;line-height:1;letter-spacing:-.02em;}
.st-em .stat-num{background:linear-gradient(135deg,var(--emerald),var(--teal));-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.st-tl .stat-num{background:linear-gradient(135deg,var(--teal),var(--emerald));-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.st-am .stat-num{color:var(--amber);}
.st-pu .stat-num{color:var(--purple);}
.stat-hint{font-size:.65rem;color:var(--text-2);margin-top:.3rem;}

/* CARD */
.card{background:var(--bg-2);border:1px solid var(--border-2);border-radius:var(--radius);overflow:hidden;margin-bottom:1rem;}
.card-hdr{background:var(--bg-3);border-bottom:1px solid var(--border-2);padding:.75rem 1.3rem;display:flex;align-items:center;gap:8px;}
.card-dot{width:7px;height:7px;border-radius:50%;background:var(--emerald);box-shadow:0 0 8px var(--emerald);animation:gpulse 2.2s ease-in-out infinite;}
@keyframes gpulse{0%,100%{opacity:1;box-shadow:0 0 8px var(--emerald);}50%{opacity:.5;box-shadow:0 0 3px var(--emerald);}}
.card-title{font-size:.62rem;letter-spacing:.18em;text-transform:uppercase;color:var(--emerald);font-family:'DM Mono',monospace;}
.sample-lbl{font-family:'DM Mono',monospace;font-size:.58rem;letter-spacing:.18em;text-transform:uppercase;color:var(--text-3);margin-bottom:.55rem;padding:0 1.3rem;}

/* TEXTAREA */
.stTextArea textarea{background:var(--bg-1)!important;border:1px solid var(--border-2)!important;border-radius:var(--radius-sm)!important;color:var(--text-1)!important;font-family:'DM Mono',monospace!important;font-size:.84rem!important;line-height:1.75!important;caret-color:var(--emerald)!important;transition:border-color .2s,box-shadow .2s!important;}
.stTextArea textarea:focus{border-color:var(--emerald-dim)!important;box-shadow:0 0 0 3px var(--emerald-soft)!important;outline:none!important;}
.stTextArea label{display:none!important;}

/* BUTTONS */
.stButton button{background:var(--bg-3)!important;color:var(--text-2)!important;border:1px solid var(--border-3)!important;border-radius:var(--radius-xs)!important;font-family:'Plus Jakarta Sans',sans-serif!important;font-size:.75rem!important;font-weight:500!important;padding:.42rem 1rem!important;transition:all .2s!important;}
.stButton button:hover{background:var(--bg-4)!important;border-color:var(--emerald-dim)!important;color:var(--emerald)!important;box-shadow:0 0 14px var(--emerald-glow)!important;}
.run-btn button{background:linear-gradient(135deg,var(--emerald-dim),var(--teal-dim))!important;color:#fff!important;border:none!important;border-radius:var(--radius-sm)!important;font-family:'Plus Jakarta Sans',sans-serif!important;font-size:.9rem!important;font-weight:700!important;letter-spacing:.04em!important;padding:.72rem 2rem!important;width:100%!important;transition:all .25s!important;box-shadow:0 4px 20px rgba(16,217,160,.2)!important;}
.run-btn button:hover{background:linear-gradient(135deg,#0dc890,#12b8b8)!important;box-shadow:0 6px 28px rgba(16,217,160,.35)!important;transform:translateY(-1px)!important;}

/* RESULT */
.result-anim{animation:fadeUp .45s cubic-bezier(.16,1,.3,1);}
@keyframes fadeUp{from{opacity:0;transform:translateY(14px);}to{opacity:1;transform:translateY(0);}}
.result-card{border-radius:var(--radius);border:1px solid;padding:1.6rem;position:relative;overflow:hidden;}
.result-card::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 80% 60% at 0% 50%,currentColor,transparent 65%);opacity:.05;pointer-events:none;}
.rc-spam{border-color:rgba(240,80,112,.35);background:rgba(240,80,112,.04);color:var(--red);}
.rc-promotion{border-color:rgba(16,217,160,.35);background:rgba(16,217,160,.04);color:var(--emerald);}
.rc-important{border-color:rgba(20,200,200,.35);background:rgba(20,200,200,.04);color:var(--teal);}
.rc-urgent{border-color:rgba(240,160,48,.35);background:rgba(240,160,48,.04);color:var(--amber);}
.rc-tag{display:inline-flex;align-items:center;gap:6px;font-family:'DM Mono',monospace;font-size:.6rem;letter-spacing:.2em;text-transform:uppercase;padding:3px 10px;border-radius:999px;border:1px solid currentColor;background:rgba(255,255,255,.04);margin-bottom:.85rem;opacity:.9;}
.rc-label{font-size:2.1rem;font-weight:800;letter-spacing:-.025em;line-height:1;margin-bottom:.35rem;}
.rc-conf-row{display:flex;align-items:center;gap:10px;margin-bottom:1rem;}
.rc-bar-bg{flex:1;height:5px;background:rgba(255,255,255,.06);border-radius:3px;overflow:hidden;}
.rc-bar-fill{height:100%;border-radius:3px;background:currentColor;box-shadow:0 0 8px currentColor;transition:width .9s cubic-bezier(.16,1,.3,1);}
.rc-conf-val{font-family:'DM Mono',monospace;font-size:.75rem;font-weight:500;opacity:.9;min-width:40px;text-align:right;}
.rc-desc{font-size:.8rem;color:var(--text-2);line-height:1.7;border-top:1px solid rgba(255,255,255,.05);padding-top:.85rem;margin-bottom:.85rem;}
.rc-action{display:inline-flex;align-items:center;gap:5px;font-size:.65rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;padding:5px 12px;border-radius:var(--radius-xs);border:1px solid currentColor;background:rgba(255,255,255,.04);}

/* PROB */
.prob-wrap{background:var(--bg-2);border:1px solid var(--border-2);border-radius:var(--radius);padding:1.3rem;}
.prob-title{font-family:'DM Mono',monospace;font-size:.58rem;letter-spacing:.2em;text-transform:uppercase;color:var(--text-3);margin-bottom:1.1rem;padding-bottom:.6rem;border-bottom:1px solid var(--border-2);}
.prob-row{display:flex;align-items:center;gap:10px;margin-bottom:13px;}
.prob-icon{font-size:.9rem;width:22px;text-align:center;}
.prob-name{width:80px;font-family:'DM Mono',monospace;font-size:.66rem;letter-spacing:.05em;text-transform:uppercase;color:var(--text-2);}
.prob-name.active{color:var(--emerald);font-weight:600;}
.prob-bg{flex:1;height:7px;background:var(--border-2);border-radius:4px;overflow:hidden;}
.prob-fill{height:100%;border-radius:4px;transition:width .85s cubic-bezier(.16,1,.3,1);}
.pf-spam{background:linear-gradient(90deg,#7a1830,var(--red));}
.pf-promotion{background:linear-gradient(90deg,var(--emerald-dim),var(--emerald));}
.pf-important{background:linear-gradient(90deg,var(--teal-dim),var(--teal));}
.pf-urgent{background:linear-gradient(90deg,#7a5010,var(--amber));}
.prob-pct{width:38px;text-align:right;font-family:'DM Mono',monospace;font-size:.68rem;font-weight:500;}
.pf-spam-t{color:var(--red);}.pf-promotion-t{color:var(--emerald);}.pf-important-t{color:var(--teal);}.pf-urgent-t{color:var(--amber);}

/* ANALYSIS */
.analysis{margin-top:1rem;background:var(--bg-1);border:1px solid var(--border-2);border-radius:var(--radius-sm);padding:1rem;}
.analysis-hdr{font-family:'DM Mono',monospace;font-size:.58rem;letter-spacing:.18em;text-transform:uppercase;color:var(--text-3);margin-bottom:.75rem;}
.analysis-row{display:flex;justify-content:space-between;font-family:'DM Mono',monospace;font-size:.68rem;padding:4px 0;border-bottom:1px solid rgba(255,255,255,.03);}
.analysis-row:last-child{border:none;}
.ak{color:var(--text-2);}.av{color:var(--emerald);font-weight:500;}

/* PIPELINE */
.pipe-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:1.6rem;}
.pipe-card{background:var(--bg-2);border:1px solid var(--border-2);border-radius:var(--radius);padding:1.4rem;transition:border-color .25s,transform .2s;position:relative;overflow:hidden;}
.pipe-card:hover{border-color:var(--emerald-dim);transform:translateY(-3px);box-shadow:0 8px 30px rgba(16,217,160,.08);}
.pipe-card::after{content:'';position:absolute;bottom:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,var(--emerald),transparent);opacity:0;transition:opacity .3s;}
.pipe-card:hover::after{opacity:.4;}
.pipe-num{font-size:2.6rem;font-weight:800;line-height:1;margin-bottom:.6rem;background:linear-gradient(135deg,var(--border-3),var(--bg-4));-webkit-background-clip:text;-webkit-text-fill-color:transparent;transition:all .3s;}
.pipe-card:hover .pipe-num{background:linear-gradient(135deg,var(--emerald),var(--teal));-webkit-background-clip:text;}
.pipe-title{font-size:.88rem;font-weight:700;color:var(--text-1);margin-bottom:.45rem;}
.pipe-desc{font-size:.73rem;color:var(--text-2);line-height:1.7;}

/* SIDEBAR */
.sb-logo{padding:1rem 0 .8rem;border-bottom:1px solid var(--border-2);margin-bottom:.8rem;}
.sb-logo-tag{font-family:'DM Mono',monospace;font-size:.55rem;letter-spacing:.22em;color:var(--emerald);text-transform:uppercase;margin-bottom:.3rem;}
.sb-logo-name{font-size:1.05rem;font-weight:800;color:#fff;}
.sb-logo-name span{color:var(--emerald);}
.sb-section{font-family:'DM Mono',monospace;font-size:.55rem;letter-spacing:.22em;text-transform:uppercase;color:var(--text-3);margin:1.1rem 0 .5rem;padding-bottom:.4rem;border-bottom:1px solid var(--border-2);}
.sb-row{display:flex;justify-content:space-between;align-items:center;padding:.4rem 0;font-size:.7rem;border-bottom:1px solid rgba(255,255,255,.02);}
.sb-key{color:var(--text-2);}.sb-val{font-weight:600;font-family:'DM Mono',monospace;font-size:.68rem;}
.v-em{color:var(--emerald);}.v-tl{color:var(--teal);}.v-am{color:var(--amber);}.v-pu{color:var(--purple);}
.cat-row{display:flex;align-items:center;gap:9px;padding:.42rem 0;border-bottom:1px solid rgba(255,255,255,.02);}
.cat-dot{width:6px;height:6px;border-radius:50%;flex-shrink:0;}
.cd-spam{background:var(--red);box-shadow:0 0 5px var(--red);}.cd-promotion{background:var(--emerald);box-shadow:0 0 5px var(--emerald);}
.cd-important{background:var(--teal);box-shadow:0 0 5px var(--teal);}.cd-urgent{background:var(--amber);box-shadow:0 0 5px var(--amber);}
.cat-name{font-size:.72rem;font-weight:600;}
.cn-spam{color:var(--red);}.cn-promotion{color:var(--emerald);}.cn-important{color:var(--teal);}.cn-urgent{color:var(--amber);}
.cat-sub{font-size:.62rem;color:var(--text-3);margin-left:auto;font-family:'DM Mono',monospace;}
.hist-row{display:flex;align-items:center;gap:8px;padding:.45rem .65rem;background:var(--bg-2);border:1px solid var(--border-2);border-radius:var(--radius-xs);margin-bottom:5px;font-size:.66rem;transition:border-color .2s;}
.hist-row:hover{border-color:var(--border-3);}
.hist-txt{flex:1;color:var(--text-2);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:130px;}
.hist-lbl{font-weight:700;font-size:.6rem;letter-spacing:.06em;text-transform:uppercase;}
.hl-spam{color:var(--red);}.hl-promotion{color:var(--emerald);}.hl-important{color:var(--teal);}.hl-urgent{color:var(--amber);}
.hist-t{color:var(--text-3);font-family:'DM Mono',monospace;font-size:.58rem;margin-left:auto;}

/* FOOTER */
.footer{margin-top:3rem;padding:1.2rem 0;border-top:1px solid var(--border-2);display:flex;justify-content:space-between;align-items:center;font-size:.63rem;color:var(--text-3);font-family:'DM Mono',monospace;}
.footer strong{color:var(--emerald);}
</style>
""", unsafe_allow_html=True)

# ── Constants ──
CATEGORY_META = {
    "spam":      {"icon":"⛔","label":"SPAM",      "desc":"High-confidence spam detected. Unsolicited or potentially malicious content — safe to discard without reading.","action":"→ DELETE / MARK SPAM"},
    "promotion": {"icon":"🛍","label":"PROMOTION", "desc":"Marketing or promotional content identified. Review relevance before acting on any offers or links inside.","action":"→ ARCHIVE / REVIEW"},
    "important": {"icon":"📋","label":"IMPORTANT", "desc":"Requires your attention — likely an invoice, confirmation, update, or action item needing a timely response.","action":"→ READ & RESPOND"},
    "urgent":    {"icon":"⚡","label":"URGENT",    "desc":"Time-critical content detected. This email demands immediate attention — delays may cause missed deadlines.","action":"→ ACT IMMEDIATELY"},
}
SAMPLES = {
    "⛔ Spam":      "CONGRATULATIONS! You've won a FREE $1000 gift card! Click here to claim before it expires. Limited time only!",
    "🛍 Promo":     "Flash sale — up to 60% off this weekend. Use code SAVE60 at checkout. Free shipping on all orders over $50!",
    "📋 Important": "Hi, your invoice #INV-2024-0892 for October is attached. Payment due by November 30. Please review and confirm.",
    "⚡ Urgent":    "CRITICAL: Production server is down. All services affected. Immediate action required — join the emergency call NOW.",
}

@st.cache_resource
def load_model():
    path = os.path.join(os.path.dirname(__file__), "model", "email_classifier.pkl")
    with open(path, "rb") as f:
        return pickle.load(f)

def preprocess(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'[^a-z\s]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

for k, v in [("history",[]),("email_text",""),("result",None)]:
    if k not in st.session_state: st.session_state[k] = v

try:    model = load_model(); model_ok = True
except: model_ok = False

# ── Sidebar ──
with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
      <div class="sb-logo-tag">NLP System · Active</div>
      <div class="sb-logo-name">Email<span> Intel</span></div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sb-section">Model Metrics</div>', unsafe_allow_html=True)
    for k,v,c in [("CV Accuracy","89%","v-em"),("Precision","~91%","v-tl"),("Recall","~88%","v-em"),
                  ("F1 Score","~89%","v-tl"),("CV Folds","5×","v-am"),("Vectorizer","TF-IDF","v-em"),
                  ("Classifier","NB","v-tl"),("Categories","4","v-pu")]:
        st.markdown(f'<div class="sb-row"><span class="sb-key">{k}</span><span class="sb-val {c}">{v}</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-section">Categories</div>', unsafe_allow_html=True)
    for cat,icon,action in [("spam","⛔","Delete"),("promotion","🛍","Archive"),("important","📋","Respond"),("urgent","⚡","Act Now")]:
        st.markdown(f'<div class="cat-row"><div class="cat-dot cd-{cat}"></div><span class="cat-name cn-{cat}">{icon} {cat.capitalize()}</span><span class="cat-sub">{action}</span></div>', unsafe_allow_html=True)

    if st.session_state.history:
        st.markdown('<div class="sb-section">Recent</div>', unsafe_allow_html=True)
        for item in reversed(st.session_state.history[-5:]):
            st.markdown(f'<div class="hist-row"><div class="cat-dot cd-{item["label"]}"></div><span class="hist-txt">{item["preview"]}</span><span class="hist-lbl hl-{item["label"]}">{item["label"][:4].upper()}</span><span class="hist-t">{item["time"]}</span></div>', unsafe_allow_html=True)

# ── Header ──
st.markdown("""
<div class="hdr">
  <div class="hdr-tag">NLP Intelligence · Real-Time Classification</div>
  <div class="hdr-h1">Smart <em>Email</em> Classifier</div>
  <div class="hdr-sub">TF-IDF · Multinomial Naive Bayes · 5-Fold CV · 89% Accuracy</div>
</div>""", unsafe_allow_html=True)

# ── Stats ──
st.markdown("""
<div class="stat-row">
  <div class="stat-tile st-em"><div class="stat-lbl">CV Accuracy</div><div class="stat-num">89%</div><div class="stat-hint">5-fold validated</div></div>
  <div class="stat-tile st-tl"><div class="stat-lbl">Categories</div><div class="stat-num">4</div><div class="stat-hint">Spam · Promo · Imp · Urgent</div></div>
  <div class="stat-tile st-am"><div class="stat-lbl">Daily Volume</div><div class="stat-num">50+</div><div class="stat-hint">Emails classified</div></div>
  <div class="stat-tile st-pu"><div class="stat-lbl">Algorithm</div><div class="stat-num" style="font-size:1rem;padding-top:.3rem">Naive<br>Bayes</div><div class="stat-hint">Multinomial NB</div></div>
</div>""", unsafe_allow_html=True)

# ── Input ──
st.markdown('<div class="card"><div class="card-hdr"><div class="card-dot"></div><div class="card-title">Email Input</div></div></div>', unsafe_allow_html=True)
st.markdown('<div class="sample-lbl">Quick load sample →</div>', unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)
for col,(label,text) in zip([c1,c2,c3,c4], SAMPLES.items()):
    with col:
        if st.button(label, use_container_width=True):
            st.session_state.email_text = text
            st.session_state.result = None
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)
email_input = st.text_area("email", value=st.session_state.email_text,
    placeholder="Paste email content here — subject line, body, or both...",
    height=148, label_visibility="collapsed")

b1,b2 = st.columns([5,1])
with b1:
    st.markdown('<div class="run-btn">', unsafe_allow_html=True)
    classify = st.button("📧  Classify Email", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with b2:
    if st.button("Clear", use_container_width=True):
        st.session_state.email_text = ""
        st.session_state.result = None
        st.rerun()

# ── Classify ──
if classify:
    if not email_input.strip():
        st.warning("⚠ Please paste some email content first.")
    elif not model_ok:
        st.error("✗ Model not found — make sure model/email_classifier.pkl exists.")
    else:
        clean = preprocess(email_input)
        pred  = model.predict([clean])[0]
        probs = model.predict_proba([clean])[0]
        pd_   = dict(zip(model.classes_, probs))
        conf  = pd_[pred]
        st.session_state.result = {"pred":pred,"conf":conf,"pd":pd_,
            "chars":len(email_input),"words":len(email_input.split()),"tokens":len(clean.split())}
        st.session_state.history.append({"label":pred,
            "preview":email_input[:46]+"…" if len(email_input)>46 else email_input,
            "time":datetime.now().strftime("%H:%M")})
        st.rerun()

# ── Result ──
if st.session_state.result:
    r    = st.session_state.result
    pred = r["pred"]; conf = r["conf"]; meta = CATEGORY_META[pred]; pd_ = r["pd"]
    icons = {"spam":"⛔","promotion":"🛍","important":"📋","urgent":"⚡"}

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([1.1,1])

    with left:
        st.markdown(f"""
        <div class="result-anim">
          <div class="result-card rc-{pred}">
            <div class="rc-tag">{meta['icon']} Classification Result</div>
            <div class="rc-label">{meta['label']}</div>
            <div class="rc-conf-row">
              <div class="rc-bar-bg"><div class="rc-bar-fill" style="width:{int(conf*100)}%"></div></div>
              <div class="rc-conf-val">{conf:.1%}</div>
            </div>
            <div class="rc-desc">{meta['desc']}</div>
            <div class="rc-action">{meta['action']}</div>
          </div>
        </div>""", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="prob-wrap"><div class="prob-title">Probability Distribution</div>', unsafe_allow_html=True)
        for cat in ["spam","promotion","important","urgent"]:
            p = pd_.get(cat,0); pct = int(p*100)
            active = "active" if cat==pred else ""
            st.markdown(f"""
            <div class="prob-row">
              <span class="prob-icon">{icons[cat]}</span>
              <span class="prob-name {active}">{cat}</span>
              <div class="prob-bg"><div class="prob-fill pf-{cat}" style="width:{pct}%"></div></div>
              <span class="prob-pct pf-{cat}-t">{p:.0%}</span>
            </div>""", unsafe_allow_html=True)

        tier = "HIGH" if conf>.75 else "MEDIUM" if conf>.5 else "LOW"
        st.markdown(f"""
        <div class="analysis">
          <div class="analysis-hdr">Text Analysis</div>
          <div class="analysis-row"><span class="ak">Characters</span><span class="av">{r['chars']:,}</span></div>
          <div class="analysis-row"><span class="ak">Raw words</span><span class="av">{r['words']}</span></div>
          <div class="analysis-row"><span class="ak">Clean tokens</span><span class="av">{r['tokens']}</span></div>
          <div class="analysis-row"><span class="ak">Confidence tier</span><span class="av">{tier}</span></div>
        </div></div>""", unsafe_allow_html=True)

# ── Pipeline ──
st.markdown("""
<div style="font-family:'DM Mono',monospace;font-size:.58rem;letter-spacing:.2em;text-transform:uppercase;color:#2a5040;margin-top:2.5rem">How It Works</div>
<div class="pipe-grid">
  <div class="pipe-card"><div class="pipe-num">01</div><div class="pipe-title">Text Preprocessing</div><div class="pipe-desc">Raw email text is lowercased, stripped of URLs, email addresses, and special characters — producing clean, normalized token sequences for analysis.</div></div>
  <div class="pipe-card"><div class="pipe-num">02</div><div class="pipe-title">TF-IDF Vectorization</div><div class="pipe-desc">Tokens are encoded into an 8,000-feature matrix using Term Frequency–Inverse Document Frequency across unigram and bigram ranges.</div></div>
  <div class="pipe-card"><div class="pipe-num">03</div><div class="pipe-title">Naive Bayes Inference</div><div class="pipe-desc">A Multinomial Naive Bayes classifier — validated across 5 stratified folds at 89% accuracy — outputs a full probability distribution in real time.</div></div>
</div>""", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
  <span><strong>Smart Email Classifier</strong> · NLP Pipeline</span>
  <span>Python · Scikit-learn · TF-IDF · Naive Bayes · Streamlit</span>
  <span>89% CV Accuracy</span>
</div>""", unsafe_allow_html=True)
