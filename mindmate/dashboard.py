"""Plotly figures for the mood dashboard."""
import plotly.graph_objects as go

from . import analytics

EMOTION_COLORS = {
    "joy": "#F4B400", "surprise": "#AB47BC", "neutral": "#9E9E9E",
    "sadness": "#4285F4", "fear": "#7E57C2", "anger": "#DB4437", "disgust": "#0F9D58",
}


def mood_trend_figure(df, granularity: str = "Daily") -> go.Figure:
    """Line chart of average sentiment over time (Daily or Weekly)."""
    if granularity == "Weekly":
        data, x = analytics.weekly_mood(df), "week"
    else:
        data, x = analytics.daily_mood(df), "day"
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data[x], y=data["avg_sentiment"], mode="lines+markers", name="Avg sentiment",
        customdata=data["messages"],
        hovertemplate="%{x|%d %b}<br>Sentiment %{y:+.2f}<br>%{customdata} message(s)<extra></extra>",
    ))
    fig.add_hline(y=0, line_dash="dot", line_color="gray")
    fig.update_layout(
        title=f"Mood over time ({granularity.lower()} average)",
        yaxis=dict(title="Sentiment (-1 negative to +1 positive)", range=[-1, 1]),
        xaxis_title="Date", margin=dict(l=10, r=10, t=50, b=10), height=380,
    )
    return fig


def emotion_distribution_figure(df) -> go.Figure:
    """Bar chart of how often each emotion was detected."""
    dist = analytics.emotion_distribution(df)
    fig = go.Figure(go.Bar(
        x=dist["emotion"], y=dist["count"],
        marker_color=[EMOTION_COLORS.get(e, "#607D8B") for e in dist["emotion"]],
        text=[f"{s:.0%}" for s in dist["share"]], textposition="outside",
        hovertemplate="%{x}: %{y} message(s)<extra></extra>",
    ))
    fig.update_layout(title="Emotion distribution", yaxis_title="Messages",
                      margin=dict(l=10, r=10, t=50, b=10), height=380)
    return fig
