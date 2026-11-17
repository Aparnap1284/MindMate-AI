"""Emotion + sentiment classification with Hugging Face models."""
from dataclasses import dataclass

from . import config


@dataclass(frozen=True)
class MoodReading:
    emotion: str            # top emotion label
    emotion_score: float    # model confidence for that label
    sentiment: str          # negative / neutral / positive
    sentiment_score: float  # signed score in [-1, 1] = P(positive) - P(negative)


def load_pipelines():
    """Load both classifiers once (heavy: cache this in the caller)."""
    from transformers import pipeline  # imported lazily so tests don't need torch

    emotion = pipeline("text-classification", model=config.EMOTION_MODEL,
                       top_k=None, truncation=True, max_length=512)
    sentiment = pipeline("text-classification", model=config.SENTIMENT_MODEL,
                         top_k=None, truncation=True, max_length=512)
    return emotion, sentiment


def _flatten(result):
    """HF pipelines return [{...}] or [[{...}]] depending on version/top_k."""
    if result and isinstance(result[0], list):
        return result[0]
    return result


def signed_sentiment(scores) -> float:
    by_label = {s["label"].lower(): float(s["score"]) for s in scores}
    return by_label.get("positive", 0.0) - by_label.get("negative", 0.0)


def analyze(text: str, emotion_pipe, sentiment_pipe) -> MoodReading:
    emo_scores = _flatten(emotion_pipe(text))
    sen_scores = _flatten(sentiment_pipe(text))
    top_emo = max(emo_scores, key=lambda s: s["score"])
    top_sen = max(sen_scores, key=lambda s: s["score"])
    return MoodReading(
        emotion=top_emo["label"].lower(),
        emotion_score=float(top_emo["score"]),
        sentiment=top_sen["label"].lower(),
        sentiment_score=round(signed_sentiment(sen_scores), 4),
    )
