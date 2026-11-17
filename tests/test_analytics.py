from datetime import datetime, timedelta, timezone

import pandas as pd

from mindmate import analytics


def rec(days_ago, sentiment, emotion="sadness", hour=12):
    base = datetime(2026, 11, 17, hour, 0, tzinfo=timezone.utc)
    return {"user_id": "u", "timestamp": base - timedelta(days=days_ago), "emotion": emotion,
            "emotion_score": 0.9, "sentiment": "negative" if sentiment < 0 else "positive",
            "sentiment_score": sentiment, "text_length": 20}


def test_empty_frame_is_safe():
    df = analytics.to_frame([])
    assert analytics.daily_mood(df).empty
    assert analytics.weekly_mood(df).empty
    assert analytics.emotion_distribution(df).empty
    assert not analytics.support_signal(df).triggered
    assert analytics.trend_note(df) == "No mood history yet."


def test_daily_and_weekly_aggregation():
    df = analytics.to_frame([rec(0, -0.5), rec(0, -0.3), rec(1, 0.4, "joy")])
    daily = analytics.daily_mood(df)
    assert len(daily) == 2
    today = daily.iloc[-1]
    assert round(today["avg_sentiment"], 2) == -0.40 and today["messages"] == 2
    weekly = analytics.weekly_mood(df)
    assert weekly["messages"].sum() == 3
    assert all(w.weekday() == 0 for w in weekly["week"])  # Monday start


def test_emotion_distribution_shares_sum_to_one():
    df = analytics.to_frame([rec(0, -0.5), rec(0, -0.5), rec(1, 0.6, "joy")])
    dist = analytics.emotion_distribution(df)
    assert dist.iloc[0]["emotion"] == "sadness" and dist.iloc[0]["count"] == 2
    assert abs(dist["share"].sum() - 1) < 1e-9


def test_three_day_negative_streak_triggers():
    df = analytics.to_frame([rec(2, -0.6), rec(1, -0.5), rec(0, -0.7)])
    sig = analytics.support_signal(df)
    assert sig.triggered and "3 days" in sig.reason and sig.emotion == "sadness"


def test_gap_breaks_streak():
    df = analytics.to_frame([rec(3, -0.6), rec(1, -0.5), rec(0, -0.7)])  # day 2 missing
    assert analytics.negative_streak(analytics.daily_mood(df)) == 2


def test_recent_heavy_messages_trigger_without_streak():
    df = analytics.to_frame([rec(0, -0.9, hour=8), rec(0, -0.8, hour=9), rec(0, -0.7, hour=10)])
    sig = analytics.support_signal(df)
    assert sig.triggered and "last few messages" in sig.reason


def test_positive_history_does_not_trigger():
    df = analytics.to_frame([rec(2, 0.5, "joy"), rec(1, 0.3, "joy"), rec(0, 0.6, "joy")])
    assert not analytics.support_signal(df).triggered
    assert analytics.dominant_negative_emotion(df) is None


def test_timezone_day_boundary_is_ist():
    # 20:00 UTC on 16 Nov is 01:30 IST on 17 Nov
    r = rec(0, -0.5)
    r["timestamp"] = datetime(2026, 11, 16, 20, 0, tzinfo=timezone.utc)
    df = analytics.to_frame([r])
    assert df["day"].iloc[0] == pd.Timestamp("2026-11-17")
