# 🧠 MindMate AI  
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)  
[![GitHub stars](https://img.shields.io/github/stars/username/MindMate-AI?style=social)](https://github.com/username/MindMate-AI/stargazers)  

> **An AI-powered companion** that supports youth mental wellness through empathetic conversations, mood tracking, and personalized coping suggestions — built for Indian youth aged 15–25.

---

## 🌟 Core Features

1. 🤖 **AI Chatbot** – Empathetic, culturally relevant conversations.  
2. 📊 **Mood Detection & Logging** – Daily emotional state tracking using AI sentiment analysis.  
3. 🚨 **Crisis Detection & Support** – Identifies distress patterns, connects to helplines.  
4. 💡 **Personalized Coping Suggestions** – Recommendations based on emotional history.  

---

## 🎯 Target Audience
Students and young adults aged **15–25** seeking **confidential**, **youth-friendly**, and **culturally relevant** mental wellness support.

---

## 📌 Unique Selling Proposition (USP)
Combines **empathetic AI responses** with **real-time mood tracking** and **early crisis alerts**, powered by **Google Cloud’s AI tools** and **HuggingFace models** — all in a single platform designed for **Indian youth**.

---

## 🔍 Gaps in Existing Solutions & How MindMate AI Fills Them

| Existing App/Project | Gap in Current Solution | How MindMate AI Fills the Gap |
|----------------------|------------------------|--------------------------------|
| **Woebot**           | Western style, lacks Indian cultural context | Uses culturally relevant tone & examples for Indian students |
| **Wysa**             | CBT exercises but limited personalization | Dynamic coping suggestions from mood history |
| **Replika**          | Fun chat but no crisis detection | Mental health–focused, detects distress, connects to helplines |
| **Moodfit**          | Strong mood tracking, no empathetic AI | Combines mood tracking + real-time AI emotional support |
| **General AI Bots**  | Generic advice, no wellness analytics | AI tuned for youth mental wellness + analytics + personalized plans |

---

## 🛠 Tech Stack

**Frontend:** Streamlit *(fast prototyping, Python-native, responsive)*  
**Backend:** FastAPI *(lightweight, async, built-in API docs)*  
**Database:** Google Firestore *(real-time, fully managed, integrates with GCP)*  
**AI/ML Tools:** Google Cloud Vertex AI *(LLM empathetic responses)*, HuggingFace Transformers *(emotion & sentiment detection)*  
**Other Tools:** Plotly *(mood history visualization)*, Firebase Auth *(optional authentication)*, GitHub *(version control)*, Google Cloud Run *(deployment)*, Figma *(UI wireframes)*  

---

## ⚡ Getting Started

### Prerequisites
- Python **3.10+**
- Google Cloud account *(Vertex AI + Firestore enabled)*
- HuggingFace account *(optional for hosted models)*

### Installation

# Clone the repo
git clone https://github.com/Aparnap1284/MindMate-AI.git

cd MindMate-AI

# Create virtual environment
python -m venv venv
# Activate (Windows)
venv\Scripts\activate
# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
▶️ Running the App
Backend:

cd backend
uvicorn main:app --reload
Frontend:

cd frontend
streamlit run app.py
🗺 Roadmap
 Backend setup with FastAPI

 AI model integration (Vertex AI + HuggingFace)

 Firestore database for mood history

 Streamlit frontend with chat UI

 Crisis detection & helpline integration

 Deployment on Google Cloud Run

📜 License
This project is licensed under the MIT License – see the LICENSE file for details.

⚠ Disclaimer: MindMate AI is not a replacement for professional mental health services. In crisis situations, please contact a licensed professional or verified helpline.