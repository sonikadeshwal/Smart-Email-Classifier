<div align="center">

<!-- Hero Banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=Smart%20Email%20Classifier&fontSize=48&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=AI-Powered%20Email%20Intelligence%20%7C%20Instant%20Classification&descAlignY=58&descSize=16" width="100%"/>

<!-- Badges Row 1 -->
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://smart-email-classifier-8qvos9kvaei2yvunqtomzc.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)

<!-- Badges Row 2 -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Maintained](https://img.shields.io/badge/Maintained-Yes-green.svg?style=for-the-badge)](https://github.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg?style=for-the-badge)](CONTRIBUTING.md)
[![Deployed](https://img.shields.io/badge/Status-Live-success?style=for-the-badge&logo=rocket&logoColor=white)](https://smart-email-classifier-8qvos9kvaei2yvunqtomzc.streamlit.app/)

<br/>

> **Instantly classify emails as Spam or Legitimate using machine learning — no setup needed.**

<a href="https://smart-email-classifier-8qvos9kvaei2yvunqtomzc.streamlit.app/">
  <img src="https://img.shields.io/badge/🚀%20Launch%20Live%20App-FF4B4B?style=for-the-badge" alt="Launch App" height="40"/>
</a>

</div>

---

## 📌 Table of Contents

- [✨ Overview](#-overview)
- [🎯 Features](#-features)
- [🖥️ Demo](#️-demo)
- [🛠️ Tech Stack](#️-tech-stack)
- [⚙️ Installation](#️-installation)
- [🚀 Usage](#-usage)
- [📊 Model Performance](#-model-performance)
- [📁 Project Structure](#-project-structure)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## ✨ Overview

**Smart Email Classifier** is a machine learning–powered web application that analyzes email content and instantly predicts whether it's **spam** or **legitimate (ham)**. Built with Streamlit for an interactive, no-friction experience, it leverages NLP preprocessing and a trained classification model to deliver fast, accurate results.

Whether you're exploring ML concepts, building a spam filter prototype, or just curious — this tool makes email intelligence accessible to everyone.

```
📧 Paste Email Content → 🤖 ML Model Analyzes → ✅ Instant Classification
```

---

## 🎯 Features

| Feature | Description |
|---|---|
| ⚡ **Real-Time Classification** | Instant spam/ham prediction with a single click |
| 🧹 **NLP Preprocessing** | Tokenization, stopword removal, stemming via NLTK |
| 📊 **Confidence Score** | See the model's prediction confidence |
| 🎨 **Clean UI** | Intuitive Streamlit interface, no technical knowledge needed |
| 🌐 **Live Deployment** | Hosted on Streamlit Community Cloud — zero install required |
| 🔄 **Reproducible** | Full pipeline from raw text to prediction |

---

## 🖥️ Demo

<div align="center">

### 🔗 [Try it live →](https://smart-email-classifier-8qvos9kvaei2yvunqtomzc.streamlit.app/)

</div>

**Example Inputs:**

<table>
<tr>
<th>📧 Spam Email Example</th>
<th>✅ Legitimate Email Example</th>
</tr>
<tr>
<td>

```
Congratulations! You've WON a $1,000 gift card!
Click here NOW to claim your FREE prize before
it EXPIRES. Limited time offer — ACT FAST!!!
```

</td>
<td>

```
Hi Sarah, just following up on the project 
proposal we discussed in Tuesday's meeting. 
Can we schedule a call for Thursday at 2pm?
```

</td>
</tr>
<tr>
<td align="center">🔴 Predicted: <b>SPAM</b></td>
<td align="center">🟢 Predicted: <b>HAM</b></td>
</tr>
</table>

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology |
|---|---|
| **Frontend** | ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white) |
| **Language** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) |
| **ML Model** | ![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white) |
| **NLP** | ![NLTK](https://img.shields.io/badge/NLTK-85C1E9?style=flat-square&logo=python&logoColor=white) |
| **Data** | ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white) ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white) |
| **Deployment** | ![Streamlit Cloud](https://img.shields.io/badge/Streamlit_Cloud-FF4B4B?style=flat-square&logo=streamlit&logoColor=white) |

</div>

---

## ⚙️ Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/smart-email-classifier.git
cd smart-email-classifier
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download NLTK data

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

---

## 🚀 Usage

### Run locally

```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`

### Or use the live app

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://smart-email-classifier-8qvos9kvaei2yvunqtomzc.streamlit.app/)

---

## 📊 Model Performance

The classifier was trained on the [SMS Spam Collection Dataset](https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset) and evaluated using standard classification metrics.

| Metric | Score |
|---|---|
| ✅ Accuracy | ~97–98% |
| 🎯 Precision | ~99% |
| 📈 Recall | ~94% |
| 📊 F1 Score | ~96% |

> *Results may vary by version. Run `model_training.ipynb` to reproduce.*

### How it works

```
Raw Email Text
     │
     ▼
📝 Text Preprocessing
   • Lowercasing
   • Punctuation removal
   • Tokenization
   • Stopword removal
   • Porter Stemming
     │
     ▼
🔢 TF-IDF Vectorization
     │
     ▼
🤖 Naive Bayes / ML Classifier
     │
     ▼
📊 Spam / Ham Prediction + Confidence Score
```

---

## 📁 Project Structure

```
smart-email-classifier/
│
├── 📄 app.py                    # Streamlit web application
├── 📓 model_training.ipynb      # Model training & evaluation notebook
├── 🤖 model.pkl                 # Serialized trained model
├── 🔢 vectorizer.pkl            # Serialized TF-IDF vectorizer
├── 📦 requirements.txt          # Python dependencies
└── 📖 README.md                 # You are here!
```

---

## 🤝 Contributing

Contributions are welcome! Here's how to get involved:

1. 🍴 **Fork** the repository
2. 🌿 **Create** a feature branch: `git checkout -b feature/your-feature-name`
3. 💾 **Commit** your changes: `git commit -m 'Add: your feature description'`
4. 📤 **Push** to the branch: `git push origin feature/your-feature-name`
5. 🔁 **Open** a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for code of conduct details.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

### ⭐ If you found this useful, give it a star!

[![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/smart-email-classifier?style=social)](https://github.com/YOUR_USERNAME/smart-email-classifier/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/smart-email-classifier?style=social)](https://github.com/YOUR_USERNAME/smart-email-classifier/network/members)
[![GitHub watchers](https://img.shields.io/github/watchers/YOUR_USERNAME/smart-email-classifier?style=social)](https://github.com/YOUR_USERNAME/smart-email-classifier/watchers)

---

Made with ❤️ and Python

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer" width="100%"/>

</div>
