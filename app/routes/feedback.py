from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import os, json
from datetime import datetime
# from app.utils.rouge_eval import compute_rouge
from ..utils.rouge_eval import compute_rouge



router = APIRouter()

FEEDBACK_FILE = "feedback_log.json"

class Feedback(BaseModel):
    query: str
    response: str
    is_hallucinated: bool
    relevance_score: Optional[int] = None # 1–5
    comments: Optional[str] = None
    reference_summary: Optional[str] = None # For ROUGE

@router.post("/feedback")
def collect_feedback(feedback: Feedback):
    entry = feedback.dict()
    entry["timestamp"] = str(datetime.utcnow())

    # ✅ Auto-compute ROUGE if reference is provided
    if entry.get("reference_summary"):
        rouge_scores = compute_rouge(entry["response"], entry["reference_summary"])
        entry["rouge1"] = round(rouge_scores["rouge1"], 4)
        entry["rougeL"] = round(rouge_scores["rougeL"], 4)

    # Load existing feedback if it exists
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    # Append the new entry
    data.append(entry)

    # Write updated feedback back to file
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(data, f, indent=2)

    return {"message": "✅ Feedback recorded", "entry": entry}
