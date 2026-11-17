"""Mood-log storage: Firestore when configured, local CSV otherwise.

Privacy: only the *analysis* of a message is stored (emotion, sentiment, timestamp,
length). The raw message text is never written to the database.
"""
import csv
from datetime import datetime, timezone
from pathlib import Path

from . import config
from .nlp import MoodReading

FIELDS = ["user_id", "timestamp", "emotion", "emotion_score",
          "sentiment", "sentiment_score", "text_length"]


class MoodStore:
    def __init__(self, local_path=None):
        self._db = None
        self._local_path = Path(local_path or config.LOCAL_LOG)
        if config.FIREBASE_CREDENTIALS:
            from google.cloud import firestore
            self._db = firestore.Client.from_service_account_json(config.FIREBASE_CREDENTIALS)

    @property
    def backend_name(self) -> str:
        return "Firestore" if self._db is not None else "Local CSV (Firestore not configured)"

    # ---- write ----
    def log(self, user_id: str, reading: MoodReading, text_length: int, timestamp=None) -> dict:
        record = {
            "user_id": user_id,
            "timestamp": timestamp or datetime.now(timezone.utc),
            "emotion": reading.emotion,
            "emotion_score": reading.emotion_score,
            "sentiment": reading.sentiment,
            "sentiment_score": reading.sentiment_score,
            "text_length": text_length,
        }
        if self._db is not None:
            self._db.collection(config.FIRESTORE_COLLECTION).add(record)
        else:
            self._append_csv(record)
        return record

    def _append_csv(self, record: dict) -> None:
        self._local_path.parent.mkdir(parents=True, exist_ok=True)
        new_file = not self._local_path.exists()
        with self._local_path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            if new_file:
                writer.writeheader()
            row = dict(record)
            row["timestamp"] = record["timestamp"].isoformat()
            writer.writerow(row)

    # ---- read ----
    def fetch(self, user_id: str) -> list[dict]:
        if self._db is not None:
            from google.cloud.firestore_v1.base_query import FieldFilter
            docs = (self._db.collection(config.FIRESTORE_COLLECTION)
                    .where(filter=FieldFilter("user_id", "==", user_id)).stream())
            return [d.to_dict() for d in docs]
        if not self._local_path.exists():
            return []
        with self._local_path.open(newline="", encoding="utf-8") as f:
            rows = [r for r in csv.DictReader(f) if r["user_id"] == user_id]
        for r in rows:
            for k in ("emotion_score", "sentiment_score"):
                r[k] = float(r[k])
            r["text_length"] = int(r["text_length"])
        return rows
