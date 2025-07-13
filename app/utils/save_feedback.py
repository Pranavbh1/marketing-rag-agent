# 📁 app/utils/save_feedback.py

import json
import os
from datetime import datetime

FEEDBACK_FILE = "feedback_log.json"

def auto_log_feedback(query, response):
    entry = {
        "timestamp": str(datetime.utcnow()),
        "query": query,
        "response": response,
        "is_hallucinated": False,
        "relevance_score": None,
        "comments": None,
        "reference_summary": None
    }

    try:
        with open(FEEDBACK_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(entry)

    with open(FEEDBACK_FILE, "w") as f:
        json.dump(data, f, indent=2)
