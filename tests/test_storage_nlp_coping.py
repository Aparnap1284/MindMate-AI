from mindmate import coping, nlp
from mindmate.storage import MoodStore


def test_signed_sentiment():
    scores = [{"label": "positive", "score": 0.1}, {"label": "neutral", "score": 0.2},
              {"label": "negative", "score": 0.7}]
    assert round(nlp.signed_sentiment(scores), 2) == -0.6


def test_analyze_handles_nested_pipeline_output():
    emo = lambda t: [[{"label": "joy", "score": 0.2}, {"label": "sadness", "score": 0.8}]]
    sen = lambda t: [{"label": "Negative", "score": 0.9}, {"label": "Positive", "score": 0.05}]
    r = nlp.analyze("x", emo, sen)
    assert r.emotion == "sadness" and r.sentiment == "negative" and r.sentiment_score < 0


def test_csv_roundtrip_and_user_isolation(tmp_path):
    store = MoodStore(local_path=tmp_path / "log.csv")
    reading = nlp.MoodReading("joy", 0.9, "positive", 0.8)
    store.log("alice", reading, 12)
    store.log("bob", reading, 5)
    rows = store.fetch("alice")
    assert len(rows) == 1 and rows[0]["emotion"] == "joy" and rows[0]["sentiment_score"] == 0.8
    assert "text" not in rows[0]  # raw message text is never stored
    assert store.fetch("nobody") == []


def test_crisis_detection():
    assert coping.detect_crisis("I want to die")
    assert coping.detect_crisis("sometimes I think about suicide")
    assert not coping.detect_crisis("exam stress is killing my sleep schedule lol")


def test_suggestions_fallback():
    assert coping.suggestions("sadness") != coping.suggestions(None)
    assert coping.suggestions("unknown") == coping.TIPS["default"]
