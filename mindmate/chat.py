"""Gemini-powered empathetic chat."""
from google import genai
from google.genai import types

from . import config

SYSTEM_PROMPT = (
    "You are MindMate, a warm, non-judgmental wellness companion for Indian youth aged 15-25. "
    "Reply in the user's language style (English, or Hinglish if they write that way). "
    "Be brief (3-5 sentences), validate feelings first, then offer at most one small, practical idea. "
    "You are not a therapist and must not diagnose. If the user mentions self-harm or suicide, "
    "respond with care and encourage them to contact a trusted person or a helpline such as "
    "Tele-MANAS (14416)."
)


def build_contents(history: list[dict], user_text: str) -> list[types.Content]:
    contents = []
    for turn in history:
        role = "user" if turn["role"] == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part(text=turn["content"])]))
    contents.append(types.Content(role="user", parts=[types.Part(text=user_text)]))
    return contents


def reply(history: list[dict], user_text: str, trend_note: str = "") -> str:
    if not config.GEMINI_API_KEY:
        return "GEMINI_API_KEY is not set, so I can't reply right now."
    system = SYSTEM_PROMPT + (f"\nContext about the user's recent mood: {trend_note}" if trend_note else "")
    try:
        client = genai.Client(api_key=config.GEMINI_API_KEY)
        response = client.models.generate_content(
            model=config.GEMINI_MODEL,
            contents=build_contents(history, user_text),
            config=types.GenerateContentConfig(system_instruction=system),
        )
        return (response.text or "").strip() or "I'm here with you. Could you tell me a little more?"
    except Exception as exc:  # network, quota, bad model id...
        return f"Sorry, I couldn't reach the AI service right now ({type(exc).__name__})."
