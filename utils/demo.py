import os
import json
from datetime import datetime, timedelta

DEMO_FILE = "demo_status.json"
DEMO_DAYS = 7

def check_demo_expiry():
    today = datetime.today()

    if os.path.exists(DEMO_FILE):
        with open(DEMO_FILE, "r") as f:
            data = json.load(f)
        start_date = datetime.strptime(data["start_date"], "%Y-%m-%d")
        expired = data.get("expired", False)
    else:
        start_date = today
        expired = False
        with open(DEMO_FILE, "w") as f:
            json.dump({
                "start_date": start_date.strftime("%Y-%m-%d"),
                "expired": False
            }, f)

    # Check if already expired
    if expired:
        raise Exception("🚫 Demo period expired permanently. Contact support.")

    # Check if it *should* be expired now
    if today > start_date + timedelta(days=DEMO_DAYS):
        # Update file to prevent further access
        with open(DEMO_FILE, "w") as f:
            json.dump({
                "start_date": start_date.strftime("%Y-%m-%d"),
                "expired": True
            }, f)
        raise Exception("🚫 Demo period just expired. Contact support.")
