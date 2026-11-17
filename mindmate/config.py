"""Central configuration. Everything secret comes from environment variables / .env."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Gemini (chat). Model IDs get retired often, so keep it configurable.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

# Hugging Face models (run locally via transformers)
EMOTION_MODEL = "j-hartmann/emotion-english-distilroberta-base"  # anger, disgust, fear, joy, neutral, sadness, surprise
SENTIMENT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"  # negative, neutral, positive

# Storage
FIRESTORE_COLLECTION = "mood_logs"
FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS", "")  # path to service-account JSON
LOCAL_LOG = Path(os.getenv("MINDMATE_LOCAL_LOG", "data/mood_log.csv"))  # fallback when Firestore is not configured

# Analytics
TIMEZONE = "Asia/Kolkata"
NEGATIVE_EMOTIONS = ("sadness", "fear", "anger", "disgust")
STREAK_THRESHOLD = -0.2   # a day counts as "negative" if its average sentiment is below this
STREAK_DAYS = 3           # consecutive negative days that trigger coping suggestions
RECENT_WINDOW = 5         # last N messages used for the short-term check
RECENT_THRESHOLD = -0.4
