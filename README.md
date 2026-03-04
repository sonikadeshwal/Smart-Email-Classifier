# 📧 Smart Email Classifier

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0+-orange.svg)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

&gt; An intelligent NLP pipeline that automatically categorizes emails into **Spam**, **Promotion**, **Important**, and **Urgent** with 89% accuracy using TF-IDF vectorization and Naive Bayes classification.

![Demo](https://img.shields.io/badge/Live-Demo-green?logo=streamlit)

---

## ✨ Features

- 🎯 **89% Classification Accuracy** with 5-fold cross-validation
- ⚡ **Real-time Predictions** processing 50+ emails daily
- 📊 **Interactive Web Dashboard** built with Streamlit
- 📁 **Batch Processing** support for CSV uploads
- 🚨 **Urgent Alert System** with priority notifications
- 📈 **Visual Analytics** with confidence metrics and probability distributions
- 🔧 **Production-Ready** with Docker support and REST API

---

## 🧠 Model Workflow

1. Text Cleaning (lowercasing, punctuation removal)
2. Tokenization & Stopword Removal
3. TF-IDF Vectorization
4. Multinomial Naive Bayes Training
5. 5-Fold Cross Validation
6. Real-Time Prediction


## 📌 Example Prediction

Input:
"Your account has been credited. Please verify immediately."

Output:
Category: Urgent  
Confidence: 0.92
## 🚀 Quick Start
smart-email-classifier/
├── 📁 .streamlit/
│   └── config.toml              # Streamlit configuration
├── 📁 api/
│   ├── app.py                   # Flask REST API
│   └── fastapi_app.py           # FastAPI async API
├── 📁 src/
│   ├── __init__.py
│   ├── data_preprocessing.py    # Text cleaning & tokenization
│   ├── feature_extraction.py    # TF-IDF vectorization
│   ├── model.py                 # Naive Bayes with CV
│   ├── evaluate.py              # Precision/recall analysis
│   └── predict.py               # Real-time prediction API
├── 📁 models/                   # Trained models (generated)
├── 📁 notebooks/
│   └── model_selection.ipynb    # Rationale documentation
├── 📁 data/
│   └── sample_emails.csv        # Synthetic dataset
├── app.py                       # Streamlit web app
├── train.py                     # Training pipeline
├── config.yaml                  # Model configuration
├── requirements.txt
├── Dockerfile
└── README.md

## 📸 Screenshots

![Dashboard](assets/screenshot1.png)
![Batch Processing](assets/screenshot2.png)

```bash
# Clone the repository
git clone https://github.com/yourusername/smart-email-classifier.git
cd smart-email-classifier

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
