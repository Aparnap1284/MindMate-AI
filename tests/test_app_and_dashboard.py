from datetime import datetime, timedelta, timezone
from pathlib import Path

from streamlit.testing.v1 import AppTest

from mindmate import analytics, chat, config, dashboard, nlp


def _df():
    now = datetime(2026, 11, 17, 12, tzinfo=timezone.utc)
    recs = [{"user_id": "u", "timestamp": now - timedelta(days=d), "emotion": e, "emotion_score": .9,
             "sentiment": "negative", "sentiment_score": s, "text_length": 10}
            for d, e, s in [(2, "sadness", -.6), (1, "fear", -.5), (0, "sadness", -.7)]]
    return analytics.to_frame(recs)


def test_figures_build():
    df = _df()
    assert len(dashboard.mood_trend_figure(df, "Daily").data[0].x) == 3
    assert len(dashboard.mood_trend_figure(df, "Weekly").data[0].x) >= 1
    assert list(dashboard.emotion_distribution_figure(df).data[0].x)[0] == "sadness"


def test_chat_contents_roles():
    c = chat.build_contents([{"role": "user", "content": "hi"}, {"role": "assistant", "content": "hello"}], "sad")
    assert [x.role for x in c] == ["user", "model", "user"]


def test_chat_without_key_is_graceful(monkeypatch):
    monkeypatch.setattr(config, "GEMINI_API_KEY", "")
    assert "GEMINI_API_KEY" in chat.reply([], "hi")


def test_full_app_flow(monkeypatch, tmp_path):
    monkeypatch.setattr(config, "LOCAL_LOG", tmp_path / "log.csv")
    monkeypatch.setattr(nlp, "load_pipelines", lambda: (None, None))
    monkeypatch.setattr(nlp, "analyze", lambda t, e, s: nlp.MoodReading("sadness", .92, "negative", -.8))
    monkeypatch.setattr(chat, "reply", lambda h, t, n="": "I hear you.")

    at = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py"), default_timeout=30).run()
    assert not at.exception
    at.sidebar.text_input[0].set_value("riya").run()
    for msg in ["I feel low", "still low", "very low"]:
        at.chat_input[0].set_value(msg).run()
        assert not at.exception, at.exception
    assert any("Detected: sadness" in c.value for c in at.caption)
    # 3 heavy messages -> support signal -> coping suggestions shown
    assert any("small things to try" in i.value for i in at.info)
    # crisis text shows helplines
    at.chat_input[0].set_value("I want to die").run()
    assert any("14416" in e.value for e in at.error)
    # dashboard renders
    at.sidebar.radio[0].set_value("Mood dashboard").run()
    assert not at.exception, at.exception
    assert len(at.metric) == 3 and at.metric[0].value == "4"
    assert (tmp_path / "log.csv").exists()
    assert "I feel low" not in (tmp_path / "log.csv").read_text()
