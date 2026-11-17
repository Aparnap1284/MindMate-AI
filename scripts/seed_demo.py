"""Write ~2 weeks of SYNTHETIC mood data for the nickname 'demo_user' (local CSV only).

Use it to preview the dashboard. Do not present the resulting charts as real user data.
Run:  python scripts/seed_demo.py   then open the app with nickname  demo_user
"""
import hashlib
import random
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mindmate import config  # noqa: E402
from mindmate.nlp import MoodReading  # noqa: E402
from mindmate.storage import MoodStore  # noqa: E402

random.seed(7)
uid = hashlib.sha256(b"demo_user").hexdigest()[:12]
store = MoodStore()
now = datetime.now(timezone.utc)
for d in range(14, -1, -1):
    low_phase = d <= 3  # last 3 days trend negative to demo the coping trigger
    for _ in range(random.randint(2, 4)):
        if low_phase:
            emo, sent = random.choice([("sadness", -0.7), ("fear", -0.5), ("sadness", -0.6)])
        else:
            emo, sent = random.choice([("joy", 0.6), ("neutral", 0.0), ("surprise", 0.3), ("sadness", -0.4)])
        sent = max(-1, min(1, sent + random.uniform(-0.15, 0.15)))
        reading = MoodReading(emo, 0.9, "negative" if sent < -0.1 else "positive" if sent > 0.1 else "neutral", round(sent, 3))
        store.log(uid, reading, random.randint(15, 120), timestamp=now - timedelta(days=d, hours=random.randint(0, 8)))
print(f"Seeded demo data into {store.backend_name}. Use nickname: demo_user")
