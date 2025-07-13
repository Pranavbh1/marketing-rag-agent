# ✅ utils/metrics.py
import json
from rouge_score import rouge_scorer

FEEDBACK_FILE = "feedback_log.json"

def get_feedback_metrics():
    try:
        with open(FEEDBACK_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return {"error": "No feedback file found."}

    if not data:
        return {"error": "No feedback entries available."}

    total = len(data)
    hallucinated = sum(1 for entry in data if entry.get("is_hallucinated"))
    relevance_scores = [entry.get("relevance_score", 0) for entry in data if entry.get("relevance_score")]

    rouge1s, rougeLs = [], []
    scorer = rouge_scorer.RougeScorer(["rouge1", "rougeL"], use_stemmer=True)

    for entry in data:
        ref = entry.get("reference_summary")
        pred = entry.get("response")
        if ref and pred:
            scores = scorer.score(ref, pred)
            rouge1s.append(scores["rouge1"].fmeasure)
            rougeLs.append(scores["rougeL"].fmeasure)

    return {
        "total_feedback": total,
        "hallucination_rate": hallucinated / total,
        "avg_relevance": sum(relevance_scores) / len(relevance_scores) if relevance_scores else None,
        "avg_rouge1": sum(rouge1s) / len(rouge1s) if rouge1s else None,
        "avg_rougeL": sum(rougeLs) / len(rougeLs) if rougeLs else None
    }
