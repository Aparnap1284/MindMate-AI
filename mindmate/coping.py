"""Crisis keyword safety net + emotion-specific coping suggestions."""
import re

# Rough keyword net (English + romanised Hindi). It is a safety net, not a classifier.
_CRISIS = re.compile(
    r"(suicid|kill myself|end my life|want to die|wanna die|self[- ]?harm|hurt myself|"
    r"no reason to live|better off dead|khudkushi|marna chahta|marna chahti|jaan de)",
    re.IGNORECASE,
)

HELPLINES = [
    ("Tele-MANAS (Govt. of India, 24x7, free)", "14416"),
    ("Emergency services", "112"),
]

TIPS = {
    "sadness": [
        "Message or call one person you trust, even just to say 'rough day'.",
        "Step outside for a 10-minute walk in daylight.",
        "Write down three small things that went okay today, however minor.",
    ],
    "fear": [
        "Try box breathing: inhale 4s, hold 4s, exhale 4s, hold 4s, for 2 minutes.",
        "Write the worry down, then split it into 'can act on' and 'can't control'.",
        "Do one small step on the thing you are anxious about, just 10 minutes.",
    ],
    "anger": [
        "Pause before replying: take 10 slow breaths or a short walk.",
        "Vent in a note you won't send, then revisit it after an hour.",
        "Name what you actually need (rest, space, an apology) and plan one way to ask.",
    ],
    "disgust": [
        "Notice what triggered the feeling and whether you can limit exposure to it.",
        "Reset your senses: fresh air, water, a change of room.",
        "Talk it through with a friend instead of replaying it alone.",
    ],
    "default": [
        "Keep a regular sleep and meal schedule this week.",
        "Do 15 minutes of movement you enjoy.",
        "Take a short break from social media today.",
    ],
}


def detect_crisis(text: str) -> bool:
    return bool(_CRISIS.search(text or ""))


def suggestions(emotion: str | None) -> list[str]:
    return TIPS.get(emotion or "", TIPS["default"])


def helpline_text() -> str:
    lines = [f"- **{name}:** {number}" for name, number in HELPLINES]
    return "\n".join(lines)
