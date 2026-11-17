# 🧠 MindMate AI

An AI wellness companion for Indian youth (15-25): empathetic chat plus a **mood-analytics pipeline** that classifies every message, logs the result, and turns the history into trends and personalised coping suggestions.

## How it works

```
message ─► Hugging Face emotion model ─┐
        └► Hugging Face sentiment model ┴─► MoodReading ─► Firestore (timestamped, no raw text)
                                                              │
        Gemini chat reply ◄── trend note ◄── Pandas (daily / weekly aggregation, streaks)
                                                              │
                                    Plotly dashboards in Streamlit + coping-suggestion trigger
```

| Piece | Implementation |
|---|---|
| Emotion | `j-hartmann/emotion-english-distilroberta-base` (anger, disgust, fear, joy, neutral, sadness, surprise) |
| Sentiment | `cardiffnlp/twitter-roberta-base-sentiment-latest`, stored as signed score `P(pos) - P(neg)` in [-1, 1] |
| Logging | Firestore collection `mood_logs` (`user_id`, `timestamp`, `emotion`, `emotion_score`, `sentiment`, `sentiment_score`, `text_length`). Falls back to a local CSV if Firebase isn't configured |
| Analytics | Pandas: IST-aware daily and weekly (Mon-start) averages, emotion distribution, negative-day streak |
| Dashboard | Plotly: mood-over-time (daily/weekly) and emotion distribution |
| Personalisation | Coping tips are triggered when the last 3 calendar days average below -0.2, or the last 5 messages average below -0.4; the tip set follows the dominant negative emotion of the week |
| Chat | Gemini via `google-genai`; the system prompt gets a one-line mood-trend note |
| Safety | Keyword net for self-harm phrases → shows Tele-MANAS 14416 / 112 immediately |

**Privacy by design:** only the analysis (emotion, sentiment, timestamp, message length) is stored, never the message text. Users are identified by a hashed nickname, which is *not* real authentication.

## Run it

```bash
python -m venv venv && source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # add GEMINI_API_KEY (and FIREBASE_CREDENTIALS for Firestore)
streamlit run app.py
```

First run downloads the two Hugging Face models (~600 MB total). Without `FIREBASE_CREDENTIALS` the app logs to `data/mood_log.csv`; the sidebar shows which backend is active.

**Firestore setup:** Firebase console → Project settings → Service accounts → generate key, save the JSON **outside the repo** (or keep it git-ignored), and point `FIREBASE_CREDENTIALS` to it.

Preview the dashboard with synthetic data (clearly not real usage): `python scripts/seed_demo.py`, then use nickname `demo_user`.

## Tests

```bash
pytest
```
Covers aggregation, streak/trigger rules, IST day boundaries, storage round-trip (and that raw text is never stored), crisis detection, dashboard figures and a full mocked app flow.

## Limitations

- Emotion/sentiment models are English-trained; Hinglish text will be classified less reliably.
- The crisis keyword net is a safety net, not a clinical tool.
- MindMate is not a replacement for professional mental health care. In an emergency call 112; Tele-MANAS (14416) offers free 24x7 support.

MIT License
