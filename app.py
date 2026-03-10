"""
Smart Email Classifier — Streamlit App
Author: Built from resume project description
"""

import streamlit as st
import pickle
import re
import os
import numpy as np
import pandas as pd
from datetime import datetime

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Email Classifier",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

  html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
  }

  /* Dark background */
  .stApp {
    background: #0d0f14;
    color: #e8eaf0;
  }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background: #13151c !important;
    border-right: 1px solid #1e2130;
  }

  /* Hero banner */
  .hero-banner {
    background: linear-gradient(135deg, #1a1d2e 0%, #0f1420 50%, #1a1d2e 100%);
    border: 1px solid #2a2d40;
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin-bottom: 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
  }
  .hero-banner::before {
    content: '';
    position: absolute;
    top: -40%;
    left: -20%;
    width: 60%;
    height: 200%;
    background: radial-gradient(ellipse, rgba(99,102,241,0.08) 0%, transparent 70%);
    pointer-events: none;
  }
  .hero-banner h1 {
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #818cf8, #c084fc, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 0.5rem 0;
  }
  .hero-banner p {
    color: #8b93a8;
    font-size: 1rem;
    margin: 0;
  }

  /* Category badge */
  .badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.05em;
  }
  .badge-spam      { background: #2d1515; color: #f87171; border: 1px solid #7f1d1d; }
  .badge-promotion { background: #1a2d15; color: #86efac; border: 1px solid #14532d; }
  .badge-important { background: #15202d; color: #93c5fd; border: 1px solid #1e3a5f; }
  .badge-urgent    { background: #2d2015; color: #fbbf24; border: 1px solid #7f3d00; }

  /* Result card */
  .result-card {
    border-radius: 14px;
    padding: 1.8rem;
    margin: 1rem 0;
    border: 1px solid;
  }
  .result-spam      { background: #1a0f0f; border-color: #7f1d1d; }
  .result-promotion { background: #0f1a0f; border-color: #14532d; }
  .result-important { background: #0f1520; border-color: #1e3a5f; }
  .result-urgent    { background: #1a150a; border-color: #7f3d00; }

  .result-label {
    font-size: 1.6rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
  }
  .result-spam      .result-label { color: #f87171; }
  .result-promotion .result-label { color: #86efac; }
  .result-important .result-label { color: #93c5fd; }
  .result-urgent    .result-label { color: #fbbf24; }

  .result-confidence {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: #8b93a8;
    margin-bottom: 0.8rem;
  }
  .result-description {
    font-size: 0.9rem;
    color: #b0b8cc;
    line-height: 1.5;
  }

  /* Probability bar */
  .prob-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 8px;
    font-size: 0.82rem;
  }
  .prob-label {
    width: 90px;
    color: #8b93a8;
    font-family: 'JetBrains Mono', monospace;
  }
  .prob-bar-bg {
    flex: 1;
    background: #1e2130;
    border-radius: 4px;
    height: 8px;
    overflow: hidden;
  }
  .prob-bar-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.4s ease;
  }
  .prob-value {
    width: 42px;
    text-align: right;
    color: #8b93a8;
    font-family: 'JetBrains Mono', monospace;
  }

  /* Metric card */
  .metric-box {
    background: #13151c;
    border: 1px solid #1e2130;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
  }
  .metric-box .metric-val {
    font-size: 1.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  .metric-box .metric-lbl {
    font-size: 0.75rem;
    color: #5a6170;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 4px;
  }

  /* Sample email button */
  .stButton button {
    background: #1e2130 !important;
    color: #b0b8cc !important;
    border: 1px solid #2a2d40 !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.82rem !important;
    padding: 0.4rem 0.9rem !important;
    transition: all 0.2s !important;
  }
  .stButton button:hover {
    background: #252838 !important;
    border-color: #818cf8 !important;
    color: #e8eaf0 !important;
  }

  /* Primary button */
  .classify-btn button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.7rem 2rem !important;
    width: 100% !important;
  }
  .classify-btn button:hover {
    background: linear-gradient(135deg, #4f52d9, #7c3aed) !important;
    transform: translateY(-1px) !important;
  }

  /* Text area */
  .stTextArea textarea {
    background: #13151c !important;
    border: 1px solid #2a2d40 !important;
    border-radius: 10px !important;
    color: #e8eaf0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.92rem !important;
    caret-color: #818cf8;
  }
  .stTextArea textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99,102,241,0.15) !important;
  }

  /* Section header */
  .section-hdr {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #4a5168;
    margin-bottom: 0.8rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e2130;
  }

  /* History item */
  .hist-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.6rem 0.8rem;
    background: #13151c;
    border: 1px solid #1e2130;
    border-radius: 8px;
    margin-bottom: 6px;
    font-size: 0.82rem;
  }
  .hist-text { color: #8b93a8; flex: 1; margin: 0 10px;
               white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 160px; }
  .hist-time { color: #4a5168; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; }

  /* Footer */
  .footer {
    text-align: center;
    color: #3a4155;
    font-size: 0.75rem;
    padding: 2rem 0 1rem;
    border-top: 1px solid #1a1d28;
    margin-top: 3rem;
  }

  /* Hide streamlit default elements */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 2rem; max-width: 1100px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Load Model
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), "model", "email_classifier.pkl")
    with open(model_path, "rb") as f:
        return pickle.load(f)

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────
CATEGORY_META = {
    "spam": {
        "icon": "🚫",
        "color": "#f87171",
        "description": "This email shows strong indicators of spam — unsolicited, deceptive, or malicious content. It's safe to delete or move to your spam folder.",
        "action": "Delete or mark as spam"
    },
    "promotion": {
        "icon": "🛍️",
        "color": "#86efac",
        "description": "This appears to be a promotional or marketing email from a brand or service. Check if it's relevant to you before acting.",
        "action": "Review and archive"
    },
    "important": {
        "icon": "📋",
        "color": "#93c5fd",
        "description": "This email likely requires your attention — it may contain an invoice, appointment, update, or action item.",
        "action": "Read and respond"
    },
    "urgent": {
        "icon": "⚡",
        "color": "#fbbf24",
        "description": "This email contains time-sensitive content that demands immediate attention. Act promptly to avoid missing a critical deadline.",
        "action": "Act immediately"
    }
}

BAR_COLORS = {
    "spam": "#f87171",
    "promotion": "#86efac",
    "important": "#93c5fd",
    "urgent": "#fbbf24"
}

SAMPLE_EMAILS = {
    "🚫 Spam": "CONGRATULATIONS! You've been selected as our lucky winner! Claim your FREE $1000 gift card now. Click here immediately before it expires!",
    "🛍️ Promo": "Flash sale this weekend only! Up to 60% off all items. Use code SAVE60 at checkout. Free shipping on orders over $50. Shop now!",
    "📋 Important": "Hi, your invoice #INV-2024-0892 for October services is attached. Payment is due by November 30th. Please review and confirm receipt.",
    "⚡ Urgent": "CRITICAL ALERT: Our production server is down. All services affected. Immediate action required. Please join the emergency call in 5 minutes."
}

# ─────────────────────────────────────────────
# Session State
# ─────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "email_text" not in st.session_state:
    st.session_state.email_text = ""

# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 0.5rem 0 1.5rem'>
      <div style='font-size:1.3rem; font-weight:700; color:#e8eaf0'>📧 Email Classifier</div>
      <div style='font-size:0.75rem; color:#4a5168; margin-top:4px'>NLP · Naive Bayes · TF-IDF</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-hdr">Model Stats</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="metric-box"><div class="metric-val">89%</div><div class="metric-lbl">CV Accuracy</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-box"><div class="metric-val">4</div><div class="metric-lbl">Categories</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="metric-box"><div class="metric-val">5×</div><div class="metric-lbl">Cross-Val</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-box"><div class="metric-val">50+</div><div class="metric-lbl">Daily Emails</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-hdr">Categories</div>', unsafe_allow_html=True)
    for cat, meta in CATEGORY_META.items():
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">'
            f'<span style="font-size:1rem">{meta["icon"]}</span>'
            f'<div><div style="font-size:0.82rem;font-weight:600;color:{meta["color"]}">{cat.capitalize()}</div>'
            f'<div style="font-size:0.72rem;color:#4a5168">{meta["action"]}</div></div>'
            f'</div>',
            unsafe_allow_html=True
        )

    if st.session_state.history:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-hdr">Recent</div>', unsafe_allow_html=True)
        for item in reversed(st.session_state.history[-5:]):
            meta = CATEGORY_META[item["label"]]
            st.markdown(
                f'<div class="hist-item">'
                f'<span>{meta["icon"]}</span>'
                f'<span class="hist-text">{item["preview"]}</span>'
                f'<span class="hist-time">{item["time"]}</span>'
                f'</div>',
                unsafe_allow_html=True
            )

# ─────────────────────────────────────────────
# Main Content
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <h1>📧 Smart Email Classifier</h1>
  <p>NLP-powered classification using TF-IDF vectorization & Naive Bayes · 89% accuracy · 5-fold cross-validated</p>
</div>
""", unsafe_allow_html=True)

# Load model
try:
    model = load_model()
    model_loaded = True
except Exception as e:
    st.error(f"❌ Could not load model: {e}")
    model_loaded = False

# ── Sample buttons ──
st.markdown('<div class="section-hdr">Try a sample email</div>', unsafe_allow_html=True)
cols = st.columns(4)
for i, (label, sample) in enumerate(SAMPLE_EMAILS.items()):
    with cols[i]:
        if st.button(label, use_container_width=True):
            st.session_state.email_text = sample
            st.rerun()

# ── Input ──
st.markdown("<br>", unsafe_allow_html=True)
email_input = st.text_area(
    "Email Content",
    value=st.session_state.email_text,
    placeholder="Paste your email text here — subject line, body, or both...",
    height=160,
    label_visibility="collapsed"
)

left, right = st.columns([3, 1])
with left:
    st.markdown('<div class="classify-btn">', unsafe_allow_html=True)
    classify_clicked = st.button("🔍  Classify Email", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with right:
    if st.button("🗑️  Clear", use_container_width=True):
        st.session_state.email_text = ""
        st.rerun()

# ── Prediction ──
if classify_clicked and email_input.strip() and model_loaded:
    clean = preprocess_text(email_input)
    prediction = model.predict([clean])[0]
    probabilities = model.predict_proba([clean])[0]
    classes = model.classes_
    prob_dict = dict(zip(classes, probabilities))
    confidence = prob_dict[prediction]

    # Save to history
    st.session_state.history.append({
        "label": prediction,
        "preview": email_input[:50] + "..." if len(email_input) > 50 else email_input,
        "confidence": confidence,
        "time": datetime.now().strftime("%H:%M")
    })

    meta = CATEGORY_META[prediction]

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-hdr">Classification Result</div>', unsafe_allow_html=True)

    col_result, col_probs = st.columns([1.2, 1])

    with col_result:
        st.markdown(f"""
        <div class="result-card result-{prediction}">
          <div style="margin-bottom:0.8rem">
            <span class="badge badge-{prediction}">{meta['icon']} {prediction.upper()}</span>
          </div>
          <div class="result-label">{meta['icon']} {prediction.capitalize()}</div>
          <div class="result-confidence">Confidence: {confidence:.1%}</div>
          <div class="result-description">{meta['description']}</div>
          <div style="margin-top:1rem;padding-top:0.8rem;border-top:1px solid rgba(255,255,255,0.06)">
            <span style="font-size:0.75rem;color:#4a5168;text-transform:uppercase;letter-spacing:0.08em">Suggested action</span><br>
            <span style="font-size:0.85rem;color:{meta['color']};font-weight:600">→ {meta['action']}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_probs:
        st.markdown('<div class="section-hdr">Probability Breakdown</div>', unsafe_allow_html=True)
        for cls in ["spam", "promotion", "important", "urgent"]:
            prob = prob_dict.get(cls, 0)
            bar_color = BAR_COLORS[cls]
            highlight = "font-weight:600" if cls == prediction else ""
            st.markdown(f"""
            <div class="prob-row">
              <span class="prob-label" style="{highlight}">{CATEGORY_META[cls]['icon']} {cls}</span>
              <div class="prob-bar-bg">
                <div class="prob-bar-fill" style="width:{prob*100:.1f}%;background:{bar_color}"></div>
              </div>
              <span class="prob-value">{prob:.0%}</span>
            </div>
            """, unsafe_allow_html=True)

        # Word count & processing info
        word_count = len(email_input.split())
        clean_word_count = len(clean.split())
        st.markdown(f"""
        <div style="margin-top:1.2rem;padding:0.8rem;background:#0d0f14;border-radius:8px;border:1px solid #1e2130">
          <div style="font-size:0.72rem;color:#4a5168;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.5rem">Text Analysis</div>
          <div style="font-size:0.8rem;color:#8b93a8;font-family:'JetBrains Mono',monospace">
            Raw words: {word_count}<br>
            After preprocessing: {clean_word_count}<br>
            Char count: {len(email_input)}
          </div>
        </div>
        """, unsafe_allow_html=True)

elif classify_clicked and not email_input.strip():
    st.warning("⚠️ Please enter some email text to classify.")

# ─────────────────────────────────────────────
# About Section
# ─────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<div class="section-hdr">How It Works</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
steps = [
    ("01", "Text Preprocessing", "Email text is cleaned — URLs, addresses and special characters removed, then lowercased and whitespace-normalized."),
    ("02", "TF-IDF Vectorization", "Clean text is transformed into numerical features using Term Frequency–Inverse Document Frequency with bigrams."),
    ("03", "Naive Bayes Classifier", "A Multinomial Naive Bayes model predicts the category, returning class probabilities for full transparency."),
]
for col, (num, title, desc) in zip([c1, c2, c3], steps):
    with col:
        st.markdown(f"""
        <div class="metric-box" style="text-align:left;padding:1.4rem">
          <div style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:#4a5168;margin-bottom:0.5rem">STEP {num}</div>
          <div style="font-size:0.95rem;font-weight:600;color:#e8eaf0;margin-bottom:0.5rem">{title}</div>
          <div style="font-size:0.8rem;color:#5a6170;line-height:1.5">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">
  Smart Email Classifier · Built with Python, Scikit-learn & Streamlit · NLP Pipeline · 89% CV Accuracy
</div>
""", unsafe_allow_html=True)
