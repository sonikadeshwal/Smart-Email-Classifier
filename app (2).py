"""
Smart Email Classifier — Advanced UI
Cyber-intelligence terminal aesthetic with animated components
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
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# Advanced CSS — Cyber Intelligence Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@300;400;500;600&display=swap');

:root {
  --bg-primary:    #040608;
  --bg-secondary:  #080c10;
  --bg-card:       #0a0f16;
  --bg-elevated:   #0d1520;
  --border:        #0e2035;
  --border-bright: #0d3a5c;
  --cyan:          #00d4ff;
  --cyan-dim:      #0099cc;
  --cyan-glow:     rgba(0,212,255,0.12);
  --green:         #00ff88;
  --green-dim:     #00cc6a;
  --green-glow:    rgba(0,255,136,0.1);
  --red:           #ff3d5a;
  --red-glow:      rgba(255,61,90,0.12);
  --amber:         #ffaa00;
  --amber-glow:    rgba(255,170,0,0.12);
  --purple:        #9d4edd;
  --purple-glow:   rgba(157,78,221,0.12);
  --text-primary:  #c8d8e8;
  --text-secondary:#5a7a96;
  --text-dim:      #2a4a64;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
  font-family: 'IBM Plex Mono', monospace;
  background: var(--bg-primary) !important;
  color: var(--text-primary);
}

/* Animated scanline background */
.stApp {
  background: var(--bg-primary) !important;
}
.stApp::before {
  content: '';
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background:
    repeating-linear-gradient(
      0deg,
      transparent,
      transparent 2px,
      rgba(0,212,255,0.012) 2px,
      rgba(0,212,255,0.012) 4px
    );
  pointer-events: none;
  z-index: 0;
}

/* Sidebar */
[data-testid="stSidebar"] {
  background: var(--bg-secondary) !important;
  border-right: 1px solid var(--border-bright) !important;
}
[data-testid="stSidebar"]::before {
  content: '';
  position: absolute;
  top: 0; right: 0;
  width: 1px; height: 100%;
  background: linear-gradient(180deg, transparent, var(--cyan), transparent);
  opacity: 0.3;
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
  padding: 1.5rem 2rem;
  max-width: 1200px;
}

/* ── HEADER ── */
.site-header {
  position: relative;
  padding: 2rem 0 1.5rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid var(--border-bright);
}
.site-header::after {
  content: '';
  position: absolute;
  bottom: -1px; left: 0;
  width: 180px; height: 1px;
  background: linear-gradient(90deg, var(--cyan), transparent);
}
.header-eyebrow {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.65rem;
  font-weight: 500;
  letter-spacing: 0.25em;
  color: var(--cyan);
  text-transform: uppercase;
  margin-bottom: 0.6rem;
  display: flex;
  align-items: center;
  gap: 8px;
}
.header-eyebrow::before {
  content: '▶';
  font-size: 0.5rem;
  animation: blink 1.4s step-end infinite;
}
@keyframes blink { 50% { opacity: 0; } }

.header-title {
  font-family: 'Syne', sans-serif;
  font-size: 2.6rem;
  font-weight: 800;
  line-height: 1;
  color: #ffffff;
  letter-spacing: -0.02em;
}
.header-title span {
  color: var(--cyan);
  text-shadow: 0 0 30px rgba(0,212,255,0.5);
}
.header-subtitle {
  margin-top: 0.6rem;
  font-size: 0.78rem;
  color: var(--text-secondary);
  letter-spacing: 0.04em;
}

/* ── STAT CARDS ── */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1px;
  background: var(--border-bright);
  border: 1px solid var(--border-bright);
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 2rem;
}
.stat-card {
  background: var(--bg-card);
  padding: 1.2rem 1.4rem;
  position: relative;
  transition: background 0.2s;
}
.stat-card:hover { background: var(--bg-elevated); }
.stat-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  opacity: 0;
  transition: opacity 0.3s;
}
.stat-card:hover::before { opacity: 1; }
.stat-card.cyan::before  { background: var(--cyan); }
.stat-card.green::before { background: var(--green); }
.stat-card.amber::before { background: var(--amber); }
.stat-card.purple::before{ background: var(--purple); }

.stat-label {
  font-size: 0.6rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--text-dim);
  margin-bottom: 0.5rem;
}
.stat-value {
  font-family: 'Syne', sans-serif;
  font-size: 1.8rem;
  font-weight: 800;
  line-height: 1;
}
.stat-card.cyan  .stat-value { color: var(--cyan);   text-shadow: 0 0 20px rgba(0,212,255,0.4); }
.stat-card.green .stat-value { color: var(--green);  text-shadow: 0 0 20px rgba(0,255,136,0.4); }
.stat-card.amber .stat-value { color: var(--amber);  text-shadow: 0 0 20px rgba(255,170,0,0.4); }
.stat-card.purple.stat-value { color: var(--purple); text-shadow: 0 0 20px rgba(157,78,221,0.4); }
.stat-sub {
  font-size: 0.65rem;
  color: var(--text-secondary);
  margin-top: 0.3rem;
}

/* ── MAIN PANEL ── */
.panel {
  background: var(--bg-card);
  border: 1px solid var(--border-bright);
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 1.5rem;
}
.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.9rem 1.4rem;
  border-bottom: 1px solid var(--border);
  background: var(--bg-secondary);
}
.panel-title {
  font-size: 0.65rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--cyan);
  display: flex;
  align-items: center;
  gap: 8px;
}
.panel-title::before {
  content: '';
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--cyan);
  box-shadow: 0 0 8px var(--cyan);
  animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.5;transform:scale(0.8)} }

.panel-body { padding: 1.4rem; }

/* ── SAMPLE PILLS ── */
.sample-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  margin-bottom: 1.2rem;
}
.sample-pill {
  border-radius: 6px;
  padding: 0.5rem 0.8rem;
  font-size: 0.7rem;
  letter-spacing: 0.05em;
  cursor: pointer;
  border: 1px solid;
  text-align: center;
  font-family: 'IBM Plex Mono', monospace;
  transition: all 0.2s;
}
.pill-spam      { background: rgba(255,61,90,0.07);  border-color: rgba(255,61,90,0.3);   color: var(--red);    }
.pill-promo     { background: rgba(0,255,136,0.07);  border-color: rgba(0,255,136,0.3);   color: var(--green);  }
.pill-important { background: rgba(0,212,255,0.07);  border-color: rgba(0,212,255,0.3);   color: var(--cyan);   }
.pill-urgent    { background: rgba(255,170,0,0.07);  border-color: rgba(255,170,0,0.3);   color: var(--amber);  }
.sample-pill:hover { transform: translateY(-2px); filter: brightness(1.2); }

/* ── TEXTAREA ── */
.stTextArea textarea {
  background: var(--bg-secondary) !important;
  border: 1px solid var(--border-bright) !important;
  border-radius: 8px !important;
  color: var(--text-primary) !important;
  font-family: 'IBM Plex Mono', monospace !important;
  font-size: 0.85rem !important;
  line-height: 1.7 !important;
  caret-color: var(--cyan) !important;
  resize: vertical !important;
}
.stTextArea textarea:focus {
  border-color: var(--cyan) !important;
  box-shadow: 0 0 0 2px var(--cyan-glow), inset 0 0 20px rgba(0,212,255,0.03) !important;
  outline: none !important;
}
.stTextArea label { display: none !important; }

/* ── BUTTONS ── */
.stButton button {
  background: var(--bg-secondary) !important;
  color: var(--text-secondary) !important;
  border: 1px solid var(--border-bright) !important;
  border-radius: 6px !important;
  font-family: 'IBM Plex Mono', monospace !important;
  font-size: 0.72rem !important;
  letter-spacing: 0.05em !important;
  padding: 0.45rem 1rem !important;
  transition: all 0.2s !important;
}
.stButton button:hover {
  background: var(--bg-elevated) !important;
  border-color: var(--cyan) !important;
  color: var(--cyan) !important;
  box-shadow: 0 0 12px var(--cyan-glow) !important;
}

.classify-btn button {
  background: linear-gradient(135deg, #003d5c, #005a80) !important;
  color: var(--cyan) !important;
  border: 1px solid var(--cyan) !important;
  border-radius: 8px !important;
  font-family: 'Syne', sans-serif !important;
  font-size: 0.9rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.08em !important;
  text-transform: uppercase !important;
  padding: 0.75rem 2rem !important;
  width: 100% !important;
  transition: all 0.25s !important;
  box-shadow: 0 0 20px rgba(0,212,255,0.15), inset 0 0 20px rgba(0,212,255,0.05) !important;
}
.classify-btn button:hover {
  background: linear-gradient(135deg, #004d70, #006b99) !important;
  box-shadow: 0 0 35px rgba(0,212,255,0.35), inset 0 0 30px rgba(0,212,255,0.1) !important;
  transform: translateY(-1px) !important;
}

/* ── RESULT CARD ── */
.result-wrapper {
  animation: slideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes slideIn {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

.result-main {
  border-radius: 12px;
  padding: 1.8rem;
  border: 1px solid;
  position: relative;
  overflow: hidden;
}
.result-main::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  opacity: 0.04;
  pointer-events: none;
}
.result-spam     { border-color: rgba(255,61,90,0.4);   background: rgba(255,61,90,0.05); }
.result-spam::before     { background: radial-gradient(circle at 20% 50%, var(--red), transparent 60%); }
.result-promotion{ border-color: rgba(0,255,136,0.4);   background: rgba(0,255,136,0.04); }
.result-promotion::before{ background: radial-gradient(circle at 20% 50%, var(--green), transparent 60%); }
.result-important{ border-color: rgba(0,212,255,0.4);   background: rgba(0,212,255,0.04); }
.result-important::before{ background: radial-gradient(circle at 20% 50%, var(--cyan), transparent 60%); }
.result-urgent   { border-color: rgba(255,170,0,0.4);   background: rgba(255,170,0,0.04); }
.result-urgent::before   { background: radial-gradient(circle at 20% 50%, var(--amber), transparent 60%); }

.result-eyebrow {
  font-size: 0.6rem;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  margin-bottom: 0.8rem;
  display: flex;
  align-items: center;
  gap: 8px;
}
.result-spam      .result-eyebrow { color: var(--red);   }
.result-promotion .result-eyebrow { color: var(--green); }
.result-important .result-eyebrow { color: var(--cyan);  }
.result-urgent    .result-eyebrow { color: var(--amber); }

.result-category {
  font-family: 'Syne', sans-serif;
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  line-height: 1;
  margin-bottom: 0.4rem;
}
.result-spam      .result-category { color: var(--red);   text-shadow: 0 0 30px rgba(255,61,90,0.5); }
.result-promotion .result-category { color: var(--green); text-shadow: 0 0 30px rgba(0,255,136,0.5); }
.result-important .result-category { color: var(--cyan);  text-shadow: 0 0 30px rgba(0,212,255,0.5); }
.result-urgent    .result-category { color: var(--amber); text-shadow: 0 0 30px rgba(255,170,0,0.5); }

.result-confidence-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 1rem;
}
.confidence-bar-bg {
  flex: 1;
  height: 4px;
  background: rgba(255,255,255,0.06);
  border-radius: 2px;
  overflow: hidden;
}
.confidence-bar-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}
.result-spam      .confidence-bar-fill { background: linear-gradient(90deg, var(--red), #ff6b80); }
.result-promotion .confidence-bar-fill { background: linear-gradient(90deg, var(--green), #66ffbb); }
.result-important .confidence-bar-fill { background: linear-gradient(90deg, var(--cyan), #66e8ff); }
.result-urgent    .confidence-bar-fill { background: linear-gradient(90deg, var(--amber), #ffcc44); }

.confidence-val {
  font-size: 0.75rem;
  font-weight: 600;
  min-width: 42px;
  text-align: right;
}
.result-spam      .confidence-val { color: var(--red);   }
.result-promotion .confidence-val { color: var(--green); }
.result-important .confidence-val { color: var(--cyan);  }
.result-urgent    .confidence-val { color: var(--amber); }

.result-desc {
  font-size: 0.78rem;
  color: var(--text-secondary);
  line-height: 1.7;
  margin-bottom: 1rem;
  padding-top: 0.8rem;
  border-top: 1px solid rgba(255,255,255,0.05);
}
.result-action-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.65rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  padding: 4px 10px;
  border-radius: 4px;
  border: 1px solid;
  font-weight: 600;
}
.result-spam      .result-action-tag { color: var(--red);   border-color: rgba(255,61,90,0.3);   background: rgba(255,61,90,0.08); }
.result-promotion .result-action-tag { color: var(--green); border-color: rgba(0,255,136,0.3);   background: rgba(0,255,136,0.07); }
.result-important .result-action-tag { color: var(--cyan);  border-color: rgba(0,212,255,0.3);   background: rgba(0,212,255,0.07); }
.result-urgent    .result-action-tag { color: var(--amber); border-color: rgba(255,170,0,0.3);   background: rgba(255,170,0,0.07); }

/* ── PROBABILITY BREAKDOWN ── */
.prob-section-title {
  font-size: 0.6rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--text-dim);
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border);
}
.prob-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}
.prob-icon { font-size: 0.9rem; width: 20px; text-align: center; }
.prob-name {
  width: 75px;
  font-size: 0.68rem;
  letter-spacing: 0.05em;
  color: var(--text-secondary);
  text-transform: uppercase;
}
.prob-bar-bg {
  flex: 1;
  height: 6px;
  background: rgba(255,255,255,0.04);
  border-radius: 3px;
  overflow: hidden;
  border: 1px solid rgba(255,255,255,0.03);
}
.prob-bar-fill {
  height: 100%;
  border-radius: 3px;
  position: relative;
}
.prob-bar-fill::after {
  content: '';
  position: absolute;
  top: 0; right: 0;
  width: 4px; height: 100%;
  background: rgba(255,255,255,0.4);
  border-radius: 0 3px 3px 0;
}
.bar-spam      { background: linear-gradient(90deg, #7a1020, var(--red)); }
.bar-promotion { background: linear-gradient(90deg, #006644, var(--green)); }
.bar-important { background: linear-gradient(90deg, #004466, var(--cyan)); }
.bar-urgent    { background: linear-gradient(90deg, #7a4400, var(--amber)); }
.prob-pct {
  width: 38px;
  text-align: right;
  font-size: 0.68rem;
  font-weight: 600;
}
.pct-spam      { color: var(--red);   }
.pct-promotion { color: var(--green); }
.pct-important { color: var(--cyan);  }
.pct-urgent    { color: var(--amber); }

/* ── TEXT ANALYSIS BOX ── */
.analysis-box {
  margin-top: 1rem;
  padding: 1rem;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
}
.analysis-title {
  font-size: 0.58rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--text-dim);
  margin-bottom: 0.8rem;
}
.analysis-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.68rem;
  margin-bottom: 4px;
  padding-bottom: 4px;
  border-bottom: 1px solid rgba(255,255,255,0.03);
}
.analysis-key { color: var(--text-secondary); }
.analysis-val { color: var(--cyan); font-weight: 600; }

/* ── HISTORY ── */
.hist-entry {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0.55rem 0.8rem;
  border-radius: 6px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  margin-bottom: 6px;
  transition: border-color 0.2s;
}
.hist-entry:hover { border-color: var(--border-bright); }
.hist-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}
.dot-spam      { background: var(--red);   box-shadow: 0 0 6px var(--red);   }
.dot-promotion { background: var(--green); box-shadow: 0 0 6px var(--green); }
.dot-important { background: var(--cyan);  box-shadow: 0 0 6px var(--cyan);  }
.dot-urgent    { background: var(--amber); box-shadow: 0 0 6px var(--amber); }
.hist-text {
  flex: 1;
  font-size: 0.68rem;
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 130px;
}
.hist-label {
  font-size: 0.6rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-weight: 600;
}
.label-spam      { color: var(--red);   }
.label-promotion { color: var(--green); }
.label-important { color: var(--cyan);  }
.label-urgent    { color: var(--amber); }
.hist-time { font-size: 0.6rem; color: var(--text-dim); margin-left: auto; }

/* ── HOW IT WORKS ── */
.how-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1px;
  background: var(--border-bright);
  border: 1px solid var(--border-bright);
  border-radius: 10px;
  overflow: hidden;
  margin-top: 1.5rem;
}
.how-card {
  background: var(--bg-card);
  padding: 1.4rem;
  position: relative;
}
.how-num {
  font-family: 'Syne', sans-serif;
  font-size: 3rem;
  font-weight: 800;
  color: var(--border-bright);
  line-height: 1;
  margin-bottom: 0.6rem;
  transition: color 0.3s;
}
.how-card:hover .how-num { color: var(--cyan); }
.how-title {
  font-family: 'Syne', sans-serif;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.4rem;
  letter-spacing: -0.01em;
}
.how-desc {
  font-size: 0.72rem;
  color: var(--text-secondary);
  line-height: 1.65;
}

/* ── SIDEBAR EXTRAS ── */
.sidebar-section {
  font-size: 0.58rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--text-dim);
  margin: 1.2rem 0 0.6rem;
  padding-bottom: 0.4rem;
  border-bottom: 1px solid var(--border);
}
.sidebar-stat {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.45rem 0;
  font-size: 0.7rem;
  border-bottom: 1px solid rgba(255,255,255,0.03);
}
.sidebar-stat-key { color: var(--text-secondary); }
.sidebar-stat-val { font-weight: 600; }
.val-cyan   { color: var(--cyan);  }
.val-green  { color: var(--green); }
.val-amber  { color: var(--amber); }
.val-purple { color: var(--purple);}

/* ── FOOTER ── */
.site-footer {
  margin-top: 3rem;
  padding-top: 1.2rem;
  border-top: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.62rem;
  color: var(--text-dim);
  letter-spacing: 0.05em;
}
.footer-brand { color: var(--cyan); font-weight: 600; }

/* ── STREAMLIT OVERRIDES ── */
div[data-testid="stVerticalBlock"] > div { gap: 0 !important; }
.stAlert { border-radius: 8px !important; border-left: 3px solid var(--amber) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────
CATEGORY_META = {
    "spam": {
        "icon": "⛔", "color": "red",
        "description": "High-confidence spam signal detected. This email contains unsolicited or potentially malicious content. Safe to delete without reading.",
        "action": "DELETE / MARK SPAM",
    },
    "promotion": {
        "icon": "🛍", "color": "green",
        "description": "Marketing or promotional content identified. Sent by a brand or service — check relevance before acting on any offers.",
        "action": "ARCHIVE / REVIEW",
    },
    "important": {
        "icon": "📋", "color": "cyan",
        "description": "This email requires attention. Likely contains an invoice, appointment, update, or action item that warrants a timely response.",
        "action": "READ & RESPOND",
    },
    "urgent": {
        "icon": "⚡", "color": "amber",
        "description": "Time-critical content detected. This email demands immediate action — ignoring it may result in missed deadlines or escalations.",
        "action": "ACT IMMEDIATELY",
    },
}

SAMPLES = {
    "⛔ Spam":      "CONGRATULATIONS! You've been selected as our lucky winner! Claim your FREE $1000 gift card now. Click here immediately!",
    "🛍 Promo":     "Flash sale this weekend — up to 60% off everything. Use code SAVE60 at checkout. Free shipping on orders over $50!",
    "📋 Important": "Hi, your invoice #INV-2024-0892 for October services is attached. Payment is due by November 30. Please confirm receipt.",
    "⚡ Urgent":    "CRITICAL: Production server is down. All services affected. Immediate action required. Please join the emergency call NOW.",
}

# ─────────────────────────────────────────────
# Model + State
# ─────────────────────────────────────────────
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

if "history" not in st.session_state:
    st.session_state.history = []
if "email_text" not in st.session_state:
    st.session_state.email_text = ""
if "result" not in st.session_state:
    st.session_state.result = None

try:
    model = load_model()
    model_ok = True
except:
    model_ok = False

# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0 0.5rem">
      <div style="font-family:'IBM Plex Mono',monospace;font-size:0.58rem;letter-spacing:0.25em;color:#0099cc;text-transform:uppercase;margin-bottom:0.4rem">SYSTEM</div>
      <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:800;color:#fff">EMAIL<span style="color:#00d4ff"> INTEL</span></div>
      <div style="font-size:0.62rem;color:#2a4a64;margin-top:2px">v2.0 · NLP PIPELINE</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Model Metrics</div>', unsafe_allow_html=True)
    metrics = [
        ("CV Accuracy",   "89%",    "val-cyan"),
        ("Precision",     "~91%",   "val-green"),
        ("Recall",        "~88%",   "val-cyan"),
        ("F1 Score",      "~89%",   "val-green"),
        ("CV Folds",      "5×",     "val-amber"),
        ("Categories",    "4",      "val-purple"),
        ("Daily Emails",  "50+",    "val-cyan"),
        ("Vectorizer",    "TF-IDF", "val-green"),
    ]
    for key, val, cls in metrics:
        st.markdown(f"""
        <div class="sidebar-stat">
          <span class="sidebar-stat-key">{key}</span>
          <span class="sidebar-stat-val {cls}">{val}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Categories</div>', unsafe_allow_html=True)
    cat_rows = [
        ("⛔", "Spam",      "red",   "#ff3d5a"),
        ("🛍", "Promotion", "green", "#00ff88"),
        ("📋", "Important", "cyan",  "#00d4ff"),
        ("⚡", "Urgent",    "amber", "#ffaa00"),
    ]
    for icon, name, _, color in cat_rows:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;padding:0.4rem 0;border-bottom:1px solid rgba(255,255,255,0.03)">
          <span style="font-size:0.85rem">{icon}</span>
          <span style="font-size:0.72rem;color:{color};font-weight:600;letter-spacing:0.05em">{name}</span>
        </div>""", unsafe_allow_html=True)

    if st.session_state.history:
        st.markdown('<div class="sidebar-section">Recent</div>', unsafe_allow_html=True)
        for item in reversed(st.session_state.history[-6:]):
            st.markdown(f"""
            <div class="hist-entry">
              <div class="hist-dot dot-{item['label']}"></div>
              <span class="hist-text">{item['preview']}</span>
              <span class="hist-label label-{item['label']}">{item['label'][:4].upper()}</span>
              <span class="hist-time">{item['time']}</span>
            </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

# Header
st.markdown("""
<div class="site-header">
  <div class="header-eyebrow">NLP Intelligence System · Active</div>
  <div class="header-title">Smart <span>Email</span> Classifier</div>
  <div class="header-subtitle">
    TF-IDF Vectorization · Multinomial Naive Bayes · 5-Fold Cross-Validation · Real-Time Prediction
  </div>
</div>
""", unsafe_allow_html=True)

# Stats bar
st.markdown("""
<div class="stats-grid">
  <div class="stat-card cyan">
    <div class="stat-label">CV Accuracy</div>
    <div class="stat-value">89%</div>
    <div class="stat-sub">5-fold validated</div>
  </div>
  <div class="stat-card green">
    <div class="stat-label">Categories</div>
    <div class="stat-value">4</div>
    <div class="stat-sub">Spam · Promo · Important · Urgent</div>
  </div>
  <div class="stat-card amber">
    <div class="stat-label">Daily Volume</div>
    <div class="stat-value">50+</div>
    <div class="stat-sub">Emails processed</div>
  </div>
  <div class="stat-card purple">
    <div class="stat-label">Classifier</div>
    <div class="stat-value" style="font-size:1rem;padding-top:0.4rem;color:#9d4edd;text-shadow:0 0 20px rgba(157,78,221,0.4)">Naive<br>Bayes</div>
    <div class="stat-sub">Multinomial NB</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Input Panel ──
st.markdown("""
<div class="panel">
  <div class="panel-header">
    <div class="panel-title">Email Input Terminal</div>
  </div>
  <div class="panel-body" style="padding-bottom:0.5rem">
""", unsafe_allow_html=True)

# Sample buttons
st.markdown('<div style="font-size:0.6rem;letter-spacing:0.2em;text-transform:uppercase;color:#2a4a64;margin-bottom:0.6rem">Quick Load Sample</div>', unsafe_allow_html=True)

cols = st.columns(4)
labels = list(SAMPLES.keys())
for i, col in enumerate(cols):
    with col:
        if st.button(labels[i], use_container_width=True, key=f"sample_{i}"):
            st.session_state.email_text = list(SAMPLES.values())[i]
            st.session_state.result = None
            st.rerun()

st.markdown("</div></div>", unsafe_allow_html=True)

# Text input
email_input = st.text_area(
    "email",
    value=st.session_state.email_text,
    placeholder="// Paste email content here — subject, body, or both...\n// Press CLASSIFY to run NLP pipeline",
    height=155,
    label_visibility="collapsed",
    key="email_area"
)

# Action buttons
c1, c2 = st.columns([4, 1])
with c1:
    st.markdown('<div class="classify-btn">', unsafe_allow_html=True)
    classify = st.button("⚡  RUN CLASSIFIER", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with c2:
    if st.button("CLR", use_container_width=True):
        st.session_state.email_text = ""
        st.session_state.result = None
        st.rerun()

# ── Classify ──
if classify:
    if not email_input.strip():
        st.warning("⚠ Input buffer empty — paste email content to classify.")
    elif not model_ok:
        st.error("✗ Model file not found. Run setup_model.py first.")
    else:
        clean = preprocess(email_input)
        pred  = model.predict([clean])[0]
        probs = model.predict_proba([clean])[0]
        prob_dict = dict(zip(model.classes_, probs))
        conf = prob_dict[pred]
        st.session_state.result = {
            "pred": pred, "conf": conf,
            "prob_dict": prob_dict,
            "raw_len": len(email_input),
            "word_count": len(email_input.split()),
            "clean_words": len(clean.split()),
        }
        st.session_state.history.append({
            "label": pred,
            "preview": email_input[:45] + "…" if len(email_input) > 45 else email_input,
            "confidence": conf,
            "time": datetime.now().strftime("%H:%M"),
        })
        st.rerun()

# ── Result Display ──
if st.session_state.result:
    r    = st.session_state.result
    pred = r["pred"]
    conf = r["conf"]
    meta = CATEGORY_META[pred]
    prob_dict = r["prob_dict"]

    st.markdown("<br>", unsafe_allow_html=True)
    col_left, col_right = st.columns([1.1, 1])

    with col_left:
        conf_pct = int(conf * 100)
        st.markdown(f"""
        <div class="result-wrapper">
          <div class="result-main result-{pred}">
            <div class="result-eyebrow">{meta['icon']} CLASSIFICATION RESULT</div>
            <div class="result-category">{pred.upper()}</div>
            <div class="result-confidence-row">
              <div class="confidence-bar-bg">
                <div class="confidence-bar-fill" style="width:{conf_pct}%"></div>
              </div>
              <div class="confidence-val">{conf:.1%}</div>
            </div>
            <div class="result-desc">{meta['description']}</div>
            <div class="result-action-tag">→ {meta['action']}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="prob-section-title">Probability Distribution</div>', unsafe_allow_html=True)

        order = ["spam", "promotion", "important", "urgent"]
        icons = {"spam": "⛔", "promotion": "🛍", "important": "📋", "urgent": "⚡"}
        for cat in order:
            p = prob_dict.get(cat, 0)
            pct = int(p * 100)
            active = "font-weight:700;" if cat == pred else ""
            st.markdown(f"""
            <div class="prob-row">
              <span class="prob-icon">{icons[cat]}</span>
              <span class="prob-name" style="{active}">{cat}</span>
              <div class="prob-bar-bg">
                <div class="prob-bar-fill bar-{cat}" style="width:{pct}%"></div>
              </div>
              <span class="prob-pct pct-{cat}">{p:.0%}</span>
            </div>
            """, unsafe_allow_html=True)

        # Text analysis
        st.markdown(f"""
        <div class="analysis-box">
          <div class="analysis-title">Text Analysis</div>
          <div class="analysis-row">
            <span class="analysis-key">Raw characters</span>
            <span class="analysis-val">{r['raw_len']:,}</span>
          </div>
          <div class="analysis-row">
            <span class="analysis-key">Raw word count</span>
            <span class="analysis-val">{r['word_count']}</span>
          </div>
          <div class="analysis-row">
            <span class="analysis-key">After preprocessing</span>
            <span class="analysis-val">{r['clean_words']} tokens</span>
          </div>
          <div class="analysis-row" style="border:none;margin:0;padding:0">
            <span class="analysis-key">Confidence tier</span>
            <span class="analysis-val">{'HIGH' if conf > 0.75 else 'MEDIUM' if conf > 0.5 else 'LOW'}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ── How It Works ──
st.markdown("""
<div style="font-size:0.6rem;letter-spacing:0.2em;text-transform:uppercase;color:#2a4a64;margin-top:2.5rem;margin-bottom:0">Pipeline</div>
<div class="how-grid">
  <div class="how-card">
    <div class="how-num">01</div>
    <div class="how-title">Text Preprocessing</div>
    <div class="how-desc">Raw email text is lowercased, stripped of URLs, email addresses, and special characters, then whitespace-normalized into clean token sequences.</div>
  </div>
  <div class="how-card">
    <div class="how-num">02</div>
    <div class="how-title">TF-IDF Vectorization</div>
    <div class="how-desc">Clean tokens are encoded into an 8,000-feature numerical matrix using Term Frequency–Inverse Document Frequency with unigram and bigram ranges.</div>
  </div>
  <div class="how-card">
    <div class="how-num">03</div>
    <div class="how-title">Naive Bayes Inference</div>
    <div class="how-desc">A Multinomial Naive Bayes classifier, validated across 5 stratified folds, outputs a full probability distribution across all four categories in real time.</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="site-footer">
  <span><span class="footer-brand">Smart Email Classifier</span> · NLP Intelligence System</span>
  <span>Python · Scikit-learn · Streamlit · TF-IDF · Naive Bayes</span>
  <span style="color:#0e2035">89% CV ACCURACY</span>
</div>
""", unsafe_allow_html=True)
