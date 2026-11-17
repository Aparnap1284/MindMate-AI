"""Pandas analytics over the mood log: daily/weekly trends, emotion mix, support signal."""
from dataclasses import dataclass

import pandas as pd

from . import config

COLUMNS = ["user_id", "timestamp", "emotion", "emotion_score",
           "sentiment", "sentiment_score", "text_length"]


def to_frame(records: list[dict]) -> pd.DataFrame:
    """Records -> clean DataFrame with local time, calendar day and week-start columns."""
    if not records:
        return pd.DataFrame(columns=COLUMNS + ["local_time", "day", "week"])
    df = pd.DataFrame(records)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df["sentiment_score"] = pd.to_numeric(df["sentiment_score"], errors="coerce")
    df = df.dropna(subset=["timestamp", "sentiment_score", "emotion"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    df["local_time"] = df["timestamp"].dt.tz_convert(config.TIMEZONE)
    df["day"] = df["local_time"].dt.tz_localize(None).dt.normalize()
    df["week"] = df["day"] - pd.to_timedelta(df["day"].dt.weekday, unit="D")  # Monday start
    return df


def daily_mood(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["day", "avg_sentiment", "messages"])
    return (df.groupby("day")
              .agg(avg_sentiment=("sentiment_score", "mean"), messages=("sentiment_score", "size"))
              .reset_index())


def weekly_mood(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["week", "avg_sentiment", "messages"])
    return (df.groupby("week")
              .agg(avg_sentiment=("sentiment_score", "mean"), messages=("sentiment_score", "size"))
              .reset_index())


def emotion_distribution(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["emotion", "count", "share"])
    out = df["emotion"].value_counts().rename_axis("emotion").reset_index(name="count")
    out["share"] = out["count"] / out["count"].sum()
    return out


def negative_streak(daily: pd.DataFrame, threshold: float = config.STREAK_THRESHOLD) -> int:
    """Number of consecutive calendar days, ending at the latest day, with avg sentiment < threshold."""
    if daily.empty:
        return 0
    streak, prev = 0, None
    for _, row in daily.sort_values("day", ascending=False).iterrows():
        consecutive = prev is None or (prev - row["day"]).days == 1
        if row["avg_sentiment"] < threshold and consecutive:
            streak += 1
            prev = row["day"]
        else:
            break
    return streak


def dominant_negative_emotion(df: pd.DataFrame, days: int = 7):
    """Most frequent negative emotion over the last `days` days (None if there is none)."""
    if df.empty:
        return None
    recent = df[df["day"] >= df["day"].max() - pd.Timedelta(days=days - 1)]
    negatives = recent[recent["emotion"].isin(config.NEGATIVE_EMOTIONS)]
    if negatives.empty:
        return None
    return negatives["emotion"].value_counts().idxmax()


@dataclass(frozen=True)
class SupportSignal:
    triggered: bool
    reason: str
    emotion: str | None


def support_signal(df: pd.DataFrame) -> SupportSignal:
    """Rule used to trigger personalised coping suggestions.

    Triggered if either:
      * the last STREAK_DAYS calendar days are all below STREAK_THRESHOLD, or
      * the last RECENT_WINDOW messages average below RECENT_THRESHOLD.
    """
    if df.empty:
        return SupportSignal(False, "", None)
    streak = negative_streak(daily_mood(df))
    if streak >= config.STREAK_DAYS:
        return SupportSignal(True, f"your mood has been low for {streak} days in a row",
                             dominant_negative_emotion(df))
    recent = df.tail(config.RECENT_WINDOW)
    if len(recent) >= 3 and recent["sentiment_score"].mean() < config.RECENT_THRESHOLD:
        return SupportSignal(True, "your last few messages sounded quite heavy",
                             dominant_negative_emotion(df))
    return SupportSignal(False, "", None)


def trend_note(df: pd.DataFrame) -> str:
    """One-line mood summary passed to the chat model as context (no raw text involved)."""
    if df.empty:
        return "No mood history yet."
    daily = daily_mood(df)
    last = daily["avg_sentiment"].iloc[-1]
    note = f"Latest daily average sentiment {last:+.2f} over {len(daily)} day(s) of history."
    emo = dominant_negative_emotion(df)
    if emo:
        note += f" Most frequent negative emotion this week: {emo}."
    return note
