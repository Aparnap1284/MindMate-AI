"""MindMate AI: Streamlit app (chat + mood analytics dashboard)."""
import hashlib

import streamlit as st

from mindmate import analytics, chat, config, coping, dashboard, nlp
from mindmate.storage import MoodStore

st.set_page_config(page_title="MindMate AI", page_icon="🧠", layout="centered")


@st.cache_resource(show_spinner="Loading emotion & sentiment models (first run downloads them)...")
def get_pipelines():
    return nlp.load_pipelines()


@st.cache_resource
def get_store():
    return MoodStore()


def user_id_from(nickname: str) -> str:
    # Pseudonymous id so the database never holds the nickname itself. (Not real auth.)
    return hashlib.sha256(nickname.strip().lower().encode()).hexdigest()[:12]


store = get_store()

# ---------------- sidebar ----------------
with st.sidebar:
    st.header("🧠 MindMate")
    nickname = st.text_input("Your nickname", placeholder="e.g. riya_21")
    page = st.radio("View", ["Chat", "Mood dashboard"])
    st.caption(f"Storage: {store.backend_name}")
    st.info("MindMate is a supportive companion, not a replacement for professional help.")
    with st.expander("Need to talk to someone now?"):
        st.markdown(coping.helpline_text())

st.title("🧠 MindMate AI")

if not nickname.strip():
    st.write("Pick a nickname in the sidebar to start. Only mood analysis is stored, "
             "never your message text.")
    st.stop()

user_id = user_id_from(nickname)
df = analytics.to_frame(store.fetch(user_id))

# ---------------- dashboard ----------------
if page == "Mood dashboard":
    if df.empty:
        st.info("No mood data yet. Chat for a bit and come back.")
        st.stop()
    c1, c2, c3 = st.columns(3)
    c1.metric("Messages analysed", len(df))
    c2.metric("Days tracked", df["day"].nunique())
    c3.metric("Avg sentiment", f"{df['sentiment_score'].mean():+.2f}")
    granularity = st.radio("Trend", ["Daily", "Weekly"], horizontal=True)
    st.plotly_chart(dashboard.mood_trend_figure(df, granularity), use_container_width=True)
    st.plotly_chart(dashboard.emotion_distribution_figure(df), use_container_width=True)
    signal = analytics.support_signal(df)
    if signal.triggered:
        st.warning(f"Heads up: {signal.reason}. A few ideas that may help:")
        for tip in coping.suggestions(signal.emotion):
            st.markdown(f"- {tip}")
    st.stop()

# ---------------- chat ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("How are you feeling today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if coping.detect_crisis(prompt):
            st.error("I'm really glad you told me. You deserve support right now. "
                     "Please reach out to someone who can help:\n\n" + coping.helpline_text())

        emotion_pipe, sentiment_pipe = get_pipelines()
        reading = nlp.analyze(prompt, emotion_pipe, sentiment_pipe)
        store.log(user_id, reading, text_length=len(prompt))
        df = analytics.to_frame(store.fetch(user_id))

        with st.spinner("Thinking..."):
            answer = chat.reply(st.session_state.messages[:-1], prompt, analytics.trend_note(df))
        st.markdown(answer)
        st.caption(f"Detected: {reading.emotion} ({reading.emotion_score:.0%}) · "
                   f"sentiment {reading.sentiment_score:+.2f}")

        signal = analytics.support_signal(df)
        if signal.triggered:
            st.info(f"I've noticed {signal.reason}. Some small things to try:\n\n"
                    + "\n".join(f"- {t}" for t in coping.suggestions(signal.emotion)))

    st.session_state.messages.append({"role": "assistant", "content": answer})
