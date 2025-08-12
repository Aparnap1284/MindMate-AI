# MindMate AI

**Generative AI-powered youth mental wellness companion** that provides empathetic conversations, real-time mood tracking, and crisis detection for young adults.  
Built using **Google Cloud Vertex AI** and **HuggingFace Transformers** for advanced natural language understanding and emotion detection.

---

## 🌟 Features
- 🤖 **Empathetic AI Chatbot** – Friendly, confidential, and culturally relevant conversations.
- 📊 **Mood Detection & Tracking** – AI-based sentiment analysis with daily emotional logs.
- 🚨 **Crisis Detection & Support** – Detects signs of distress and provides verified helpline contacts.
- 💡 **Personalized Coping Activities** – Tailored tips based on emotional history and user interests.
- 📈 **Mood History Visualization** – Interactive graphs showing emotional trends over time.

---

## 🎯 Target Audience
Students and young adults aged **15–25** seeking a private, non-judgmental mental wellness companion.

---

## 🛠 Tech Stack
**Frontend:** Streamlit  
**Backend:** FastAPI  
**Database:** Google Firestore  
**AI/ML Tools:** Google Cloud Vertex AI, HuggingFace Transformers  
**Other Tools:** Plotly, Firebase Auth, GitHub, Google Cloud Run, Figma

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Google Cloud account (Vertex AI + Firestore enabled)
- HuggingFace account (optional for hosted models)

### Installation

# Clone this repo
git clone https://github.com/Aparnap1284/MindMate-AI.git

# Go to project folder
cd MindMate-AI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
Run Backend

cd backend
uvicorn main:app --reload
Run Frontend

cd frontend
streamlit run app.py

📌 Roadmap
 Backend setup with FastAPI

 AI model integration (Vertex AI + HuggingFace)

 Firestore database for mood history

 Streamlit frontend with chat UI

 Crisis detection & helpline integration

 Deployment on Google Cloud Run

