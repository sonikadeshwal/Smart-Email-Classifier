"""
Smart Email Classifier — White & Emerald Theme
Clean white background, Arial font, emerald & teal accents
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
:root {
  --bg:        #ffffff;
  --bg-1:      #f8fffe;
  --bg-2:      #f0faf7;
  --bg-3:      #e6f7f2;
  --bg-4:      #d0f0e8;

  --emerald:   #059669;
  --emerald-2: #047857;
  --emerald-lt:#d1fae5;
  --emerald-md:#a7f3d0;

  --teal:      #0891b2;
  --teal-lt:   #cffafe;
  --teal-md:   #a5f3fc;

  --border:    #e2e8f0;
  --border-2:  #cbd5e1;
  --border-3:  #94a3b8;

  --red:       #dc2626;
  --red-lt:    #fee2e2;
  --amber:     #d97706;
  --amber-lt:  #fef3c7;
  --purple:    #7c3aed;
  --purple-lt: #ede9fe;

  --text-1:    #0f172a;
  --text-2:    #475569;
  --text-3:    #94a3b8;

  --radius:    10px;
  --radius-sm: 7px;
  --radius-xs: 5px;
  --shadow:    0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.04);
}

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
  font-family: Arial, Helvetica, sans-serif !important;
  background: var(--bg) !important;
  color: var(--text-1) !important;
}

.stApp { background: var(--bg) !important; }

[data-testid="stSidebar"] {
  background: var(--bg-1) !important;
  border-right: 1px solid var(--border) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.8rem 2.2rem; max-width: 1180px; }

/* ── HEADER ── */
.hdr {
  padding: 1.8rem 0 1.6rem;
  margin-bottom: 1.6rem;
  border-bottom: 2px solid var(--emerald-lt);
  position: relative;
}
.hdr::after {
  content: '';
  position: absolute;
  bottom: -2px; left: 0;
  width: 120px; height: 2px;
  background: var(--emerald);
}
.hdr-tag {
  font-size: 0.68rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--emerald);
  font-weight: 700;
  margin-bottom: 0.6rem;
  display: flex;
  align-items: center;
  gap: 6px;
}
.hdr-tag::before {
  content: '';
  width: 14px; height: 2px;
  background: var(--emerald);
  border-radius: 1px;
}
.hdr-h1 {
  font-size: 2.2rem;
  font-weight: 700;
  color: var(--text-1);
  line-height: 1.1;
  margin-bottom: 0.5rem;
}
.hdr-h1 em {
  font-style: normal;
  color: var(--emerald);
}
.hdr-sub {
  font-size: 0.8rem;
  color: var(--text-2);
}

/* ── STAT ROW ── */
.stat-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 1.6rem;
}
.stat-tile {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.1rem 1.3rem;
  box-shadow: var(--shadow);
  position: relative;
  overflow: hidden;
  transition: box-shadow 0.2s, transform 0.2s;
}
.stat-tile:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}
.stat-tile::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  border-radius: var(--radius) var(--radius) 0 0;
}
.st-em::before { background: var(--emerald); }
.st-tl::before { background: var(--teal); }
.st-am::before { background: var(--amber); }
.st-pu::before { background: var(--purple); }

.stat-lbl {
  font-size: 0.65rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-3);
  font-weight: 700;
  margin-bottom: 0.45rem;
}
.stat-num { font-size: 1.8rem; font-weight: 700; line-height: 1; }
.st-em .stat-num { color: var(--emerald); }
.st-tl .stat-num { color: var(--teal); }
.st-am .stat-num { color: var(--amber); }
.st-pu .stat-num { color: var(--purple); }
.stat-hint { font-size: 0.68rem; color: var(--text-3); margin-top: 0.3rem; }

/* ── CARD ── */
.card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: var(--shadow);
  margin-bottom: 1rem;
}
.card-hdr {
  background: var(--bg-2);
  border-bottom: 1px solid var(--border);
  padding: 0.7rem 1.2rem;
  display: flex;
  align-items: center;
  gap: 8px;
}
.card-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--emerald);
}
.card-title {
  font-size: 0.7rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--emerald);
  font-weight: 700;
}
.sample-lbl {
  font-size: 0.65rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-3);
  font-weight: 700;
  margin-bottom: 0.5rem;
}

/* ── TEXTAREA ── */
.stTextArea textarea {
  background: #fff !important;
  border: 1px solid var(--border-2) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text-1) !important;
  font-family: Arial, Helvetica, sans-serif !important;
  font-size: 0.88rem !important;
  line-height: 1.7 !important;
  caret-color: var(--emerald) !important;
  transition: border-color 0.2s, box-shadow 0.2s !important;
  box-shadow: var(--shadow) !important;
}
.stTextArea textarea:focus {
  border-color: var(--emerald) !important;
  box-shadow: 0 0 0 3px rgba(5,150,105,0.12) !important;
  outline: none !important;
}
.stTextArea label { display: none !important; }

/* ── BUTTONS ── */
.stButton button {
  background: #fff !important;
  color: var(--text-2) !important;
  border: 1px solid var(--border-2) !important;
  border-radius: var(--radius-xs) !important;
  font-family: Arial, Helvetica, sans-serif !important;
  font-size: 0.78rem !important;
  font-weight: 600 !important;
  padding: 0.44rem 1rem !important;
  transition: all 0.18s !important;
  box-shadow: var(--shadow) !important;
}
.stButton button:hover {
  background: var(--bg-2) !important;
  border-color: var(--emerald) !important;
  color: var(--emerald) !important;
}
.run-btn button {
  background: var(--emerald) !important;
  color: #fff !important;
  border: none !important;
  border-radius: var(--radius-sm) !important;
  font-family: Arial, Helvetica, sans-serif !important;
  font-size: 0.92rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.03em !important;
  padding: 0.72rem 2rem !important;
  width: 100% !important;
  transition: all 0.2s !important;
  box-shadow: 0 4px 14px rgba(5,150,105,0.25) !important;
}
.run-btn button:hover {
  background: var(--emerald-2) !important;
  box-shadow: 0 6px 20px rgba(5,150,105,0.35) !important;
  transform: translateY(-1px) !important;
}

/* ── RESULT ── */
.result-anim { animation: fadeUp 0.35s ease-out; }
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}
.result-card {
  border-radius: var(--radius);
  border: 1px solid;
  padding: 1.5rem;
  box-shadow: var(--shadow-md);
}
.rc-spam      { border-color: #fca5a5; background: var(--red-lt);    color: var(--red);    }
.rc-promotion { border-color: var(--emerald-md); background: var(--emerald-lt); color: var(--emerald); }
.rc-important { border-color: var(--teal-md);    background: var(--teal-lt);    color: var(--teal);    }
.rc-urgent    { border-color: #fcd34d; background: var(--amber-lt);  color: var(--amber);  }

.rc-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.62rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  padding: 3px 10px;
  border-radius: 999px;
  border: 1px solid currentColor;
  background: rgba(255,255,255,0.7);
  margin-bottom: 0.8rem;
  font-weight: 700;
}
.rc-label {
  font-size: 2rem;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 0.35rem;
}
.rc-conf-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 1rem;
}
.rc-bar-bg {
  flex: 1; height: 6px;
  background: rgba(0,0,0,0.08);
  border-radius: 3px;
  overflow: hidden;
}
.rc-bar-fill {
  height: 100%;
  border-radius: 3px;
  background: currentColor;
  transition: width 0.8s ease;
}
.rc-conf-val {
  font-size: 0.78rem;
  font-weight: 700;
  min-width: 40px;
  text-align: right;
}
.rc-desc {
  font-size: 0.82rem;
  color: var(--text-2);
  line-height: 1.65;
  border-top: 1px solid rgba(0,0,0,0.07);
  padding-top: 0.8rem;
  margin-bottom: 0.8rem;
}
.rc-action {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 5px 12px;
  border-radius: var(--radius-xs);
  border: 1px solid currentColor;
  background: rgba(255,255,255,0.6);
}

/* ── PROB ── */
.prob-wrap {
  background: #fff;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.2rem;
  box-shadow: var(--shadow);
}
.prob-title {
  font-size: 0.62rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--text-3);
  font-weight: 700;
  margin-bottom: 1rem;
  padding-bottom: 0.6rem;
  border-bottom: 1px solid var(--border);
}
.prob-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}
.prob-icon { font-size: 0.9rem; width: 22px; text-align: center; }
.prob-name {
  width: 80px;
  font-size: 0.7rem;
  text-transform: uppercase;
  font-weight: 600;
  color: var(--text-2);
  letter-spacing: 0.04em;
}
.prob-name.active { color: var(--emerald); }
.prob-bg {
  flex: 1; height: 7px;
  background: var(--border);
  border-radius: 4px;
  overflow: hidden;
}
.prob-fill { height: 100%; border-radius: 4px; transition: width 0.8s ease; }
.pf-spam      { background: var(--red); }
.pf-promotion { background: var(--emerald); }
.pf-important { background: var(--teal); }
.pf-urgent    { background: var(--amber); }
.prob-pct {
  width: 38px; text-align: right;
  font-size: 0.7rem; font-weight: 700;
}
.pf-spam-t      { color: var(--red);     }
.pf-promotion-t { color: var(--emerald); }
.pf-important-t { color: var(--teal);    }
.pf-urgent-t    { color: var(--amber);   }

/* ── ANALYSIS ── */
.analysis {
  margin-top: 1rem;
  background: var(--bg-2);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 1rem;
}
.analysis-hdr {
  font-size: 0.62rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-3);
  font-weight: 700;
  margin-bottom: 0.7rem;
}
.analysis-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.72rem;
  padding: 4px 0;
  border-bottom: 1px solid var(--border);
}
.analysis-row:last-child { border: none; }
.ak { color: var(--text-2); }
.av { color: var(--emerald); font-weight: 700; }

/* ── PIPELINE ── */
.pipe-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-top: 1.4rem;
}
.pipe-card {
  background: #fff;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.3rem;
  box-shadow: var(--shadow);
  transition: box-shadow 0.2s, transform 0.2s, border-color 0.2s;
}
.pipe-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-3px);
  border-color: var(--emerald-md);
}
.pipe-num {
  font-size: 2.2rem;
  font-weight: 700;
  color: var(--emerald-lt);
  line-height: 1;
  margin-bottom: 0.55rem;
  transition: color 0.2s;
}
.pipe-card:hover .pipe-num { color: var(--emerald); }
.pipe-title { font-size: 0.9rem; font-weight: 700; color: var(--text-1); margin-bottom: 0.4rem; }
.pipe-desc  { font-size: 0.76rem; color: var(--text-2); line-height: 1.65; }

/* ── SIDEBAR ── */
.sb-logo {
  padding: 1rem 0 0.8rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 0.8rem;
}
.sb-logo-tag {
  font-size: 0.6rem;
  letter-spacing: 0.14em;
  color: var(--emerald);
  text-transform: uppercase;
  font-weight: 700;
  margin-bottom: 0.3rem;
}
.sb-logo-name { font-size: 1.1rem; font-weight: 700; color: var(--text-1); }
.sb-logo-name span { color: var(--emerald); }

.sb-section {
  font-size: 0.6rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--text-3);
  font-weight: 700;
  margin: 1.1rem 0 0.5rem;
  padding-bottom: 0.4rem;
  border-bottom: 1px solid var(--border);
}
.sb-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.38rem 0;
  font-size: 0.72rem;
  border-bottom: 1px solid var(--border);
}
.sb-key { color: var(--text-2); }
.sb-val { font-weight: 700; font-size: 0.72rem; }
.v-em { color: var(--emerald); }
.v-tl { color: var(--teal);    }
.v-am { color: var(--amber);   }
.v-pu { color: var(--purple);  }

.cat-row {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 0.4rem 0;
  border-bottom: 1px solid var(--border);
}
.cat-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.cd-spam      { background: var(--red);     }
.cd-promotion { background: var(--emerald); }
.cd-important { background: var(--teal);    }
.cd-urgent    { background: var(--amber);   }
.cat-name { font-size: 0.74rem; font-weight: 700; }
.cn-spam      { color: var(--red);     }
.cn-promotion { color: var(--emerald); }
.cn-important { color: var(--teal);    }
.cn-urgent    { color: var(--amber);   }
.cat-sub { font-size: 0.64rem; color: var(--text-3); margin-left: auto; font-weight: 600; }

.hist-row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0.45rem 0.65rem;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: var(--radius-xs);
  margin-bottom: 5px;
  font-size: 0.68rem;
  transition: border-color 0.18s, box-shadow 0.18s;
}
.hist-row:hover { border-color: var(--emerald); box-shadow: var(--shadow); }
.hist-txt { flex: 1; color: var(--text-2); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 130px; }
.hist-lbl { font-weight: 700; font-size: 0.62rem; letter-spacing: 0.06em; text-transform: uppercase; }
.hl-spam      { color: var(--red);     }
.hl-promotion { color: var(--emerald); }
.hl-important { color: var(--teal);    }
.hl-urgent    { color: var(--amber);   }
.hist-t { color: var(--text-3); font-size: 0.6rem; margin-left: auto; }

/* ── FOOTER ── */
.footer {
  margin-top: 3rem;
  padding: 1.2rem 0;
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.66rem;
  color: var(--text-3);
}
.footer strong { color: var(--emerald); }

/* ── SECTION LABEL ── */
.section-lbl {
  font-size: 0.65rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--text-3);
  font-weight: 700;
  margin-top: 2.2rem;
  margin-bottom: 0.2rem;
}
</style>
""", unsafe_allow_html=True)

# ── Constants ──
CATEGORY_META = {
    "spam":      {"icon": "⛔", "label": "SPAM",      "desc": "High-confidence spam detected. Unsolicited or potentially malicious content — safe to discard without reading.", "action": "→ DELETE / MARK SPAM"},
    "promotion": {"icon": "🛍", "label": "PROMOTION", "desc": "Marketing or promotional content identified. Review relevance before acting on any offers or links inside.",    "action": "→ ARCHIVE / REVIEW"},
    "important": {"icon": "📋", "label": "IMPORTANT", "desc": "Requires your attention — likely an invoice, confirmation, update, or action item needing a timely response.",   "action": "→ READ & RESPOND"},
    "urgent":    {"icon": "⚡", "label": "URGENT",    "desc": "Time-critical content detected. This email demands immediate attention — delays may cause missed deadlines.",    "action": "→ ACT IMMEDIATELY"},
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

for k, v in [("history", []), ("email_text", ""), ("result", None)]:
    if k not in st.session_state:
        st.session_state[k] = v

try:    model = load_model(); model_ok = True
except: model_ok = False

# ── Sidebar ──
with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
      <div class="sb-logo-tag">NLP System · Active</div>
      <div class="sb-logo-name">Email <span>Intel</span></div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sb-section">Model Metrics</div>', unsafe_allow_html=True)
    for k, v, c in [
        ("CV Accuracy", "89%",    "v-em"),
        ("Precision",   "~91%",   "v-tl"),
        ("Recall",      "~88%",   "v-em"),
        ("F1 Score",    "~89%",   "v-tl"),
        ("CV Folds",    "5×",     "v-am"),
        ("Vectorizer",  "TF-IDF", "v-em"),
        ("Classifier",  "NB",     "v-tl"),
        ("Categories",  "4",      "v-pu"),
    ]:
        st.markdown(f'<div class="sb-row"><span class="sb-key">{k}</span><span class="sb-val {c}">{v}</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-section">Categories</div>', unsafe_allow_html=True)
    for cat, icon, action in [("spam","⛔","Delete"),("promotion","🛍","Archive"),("important","📋","Respond"),("urgent","⚡","Act Now")]:
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
  <div class="hdr-sub">TF-IDF · Multinomial Naive Bayes · 5-Fold Cross-Validation · 89% Accuracy</div>
</div>""", unsafe_allow_html=True)

# ── Stats ──
st.markdown("""
<div class="stat-row">
  <div class="stat-tile st-em"><div class="stat-lbl">CV Accuracy</div><div class="stat-num">89%</div><div class="stat-hint">5-fold validated</div></div>
  <div class="stat-tile st-tl"><div class="stat-lbl">Categories</div><div class="stat-num">4</div><div class="stat-hint">Spam · Promo · Imp · Urgent</div></div>
  <div class="stat-tile st-am"><div class="stat-lbl">Daily Volume</div><div class="stat-num">50+</div><div class="stat-hint">Emails classified</div></div>
  <div class="stat-tile st-pu"><div class="stat-lbl">Algorithm</div><div class="stat-num" style="font-size:1rem;padding-top:.3rem">Naive<br>Bayes</div><div class="stat-hint">Multinomial NB</div></div>
</div>""", unsafe_allow_html=True)

# ── Input card ──
st.markdown('<div class="card"><div class="card-hdr"><div class="card-dot"></div><div class="card-title">Email Input</div></div></div>', unsafe_allow_html=True)
st.markdown('<div class="sample-lbl">Quick load sample →</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
for col, (label, text) in zip([c1, c2, c3, c4], SAMPLES.items()):
    with col:
        if st.button(label, use_container_width=True):
            st.session_state.email_text = text
            st.session_state.result = None
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)
email_input = st.text_area(
    "email",
    value=st.session_state.email_text,
    placeholder="Paste email content here — subject line, body, or both...",
    height=148,
    label_visibility="collapsed",
)

b1, b2 = st.columns([5, 1])
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
        st.session_state.result = {
            "pred": pred, "conf": conf, "pd": pd_,
            "chars": len(email_input), "words": len(email_input.split()), "tokens": len(clean.split()),
        }
        st.session_state.history.append({
            "label": pred,
            "preview": email_input[:46] + "…" if len(email_input) > 46 else email_input,
            "time": datetime.now().strftime("%H:%M"),
        })
        st.rerun()

# ── Result ──
if st.session_state.result:
    r    = st.session_state.result
    pred = r["pred"]; conf = r["conf"]; meta = CATEGORY_META[pred]; pd_ = r["pd"]
    icons = {"spam": "⛔", "promotion": "🛍", "important": "📋", "urgent": "⚡"}

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([1.1, 1])

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
        for cat in ["spam", "promotion", "important", "urgent"]:
            p = pd_.get(cat, 0)
            active = "active" if cat == pred else ""
            st.markdown(f"""
            <div class="prob-row">
              <span class="prob-icon">{icons[cat]}</span>
              <span class="prob-name {active}">{cat}</span>
              <div class="prob-bg"><div class="prob-fill pf-{cat}" style="width:{int(p*100)}%"></div></div>
              <span class="prob-pct pf-{cat}-t">{p:.0%}</span>
            </div>""", unsafe_allow_html=True)

        tier = "HIGH" if conf > 0.75 else "MEDIUM" if conf > 0.5 else "LOW"
        st.markdown(f"""
        <div class="analysis">
          <div class="analysis-hdr">Text Analysis</div>
          <div class="analysis-row"><span class="ak">Characters</span><span class="av">{r['chars']:,}</span></div>
          <div class="analysis-row"><span class="ak">Raw words</span><span class="av">{r['words']}</span></div>
          <div class="analysis-row"><span class="ak">Clean tokens</span><span class="av">{r['tokens']}</span></div>
          <div class="analysis-row"><span class="ak">Confidence tier</span><span class="av">{tier}</span></div>
        </div></div>""", unsafe_allow_html=True)

# ── Pipeline ──
st.markdown('<div class="section-lbl">How It Works</div>', unsafe_allow_html=True)
st.markdown("""
<div class="pipe-grid">
  <div class="pipe-card">
    <div class="pipe-num">01</div>
    <div class="pipe-title">Text Preprocessing</div>
    <div class="pipe-desc">Raw email text is lowercased, stripped of URLs, email addresses, and special characters — producing clean normalized tokens for analysis.</div>
  </div>
  <div class="pipe-card">
    <div class="pipe-num">02</div>
    <div class="pipe-title">TF-IDF Vectorization</div>
    <div class="pipe-desc">Tokens are encoded into an 8,000-feature matrix using Term Frequency–Inverse Document Frequency across unigram and bigram ranges.</div>
  </div>
  <div class="pipe-card">
    <div class="pipe-num">03</div>
    <div class="pipe-title">Naive Bayes Inference</div>
    <div class="pipe-desc">A Multinomial Naive Bayes classifier — validated across 5 stratified folds at 89% accuracy — outputs a full probability distribution in real time.</div>
  </div>
</div>""", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
  <span><strong>Smart Email Classifier</strong> · NLP Pipeline</span>
  <span>Python · Scikit-learn · TF-IDF · Naive Bayes · Streamlit</span>
  <span>89% CV Accuracy</span>
</div>""", unsafe_allow_html=True)
