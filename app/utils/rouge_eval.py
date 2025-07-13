from rouge_score import rouge_scorer

def compute_rouge(predicted: str, reference: str):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, predicted)
    return {
    "rouge1": scores["rouge1"].fmeasure,
    "rougeL": scores["rougeL"].fmeasure
    }