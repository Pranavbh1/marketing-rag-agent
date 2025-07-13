# 🚀 Marketing RAG Agent (Track A – Research + Prototype)

An intelligent marketing agent built with **FastAPI**, **LangGraph**, and **Gemini Flash**, capable of:

* 🔎 Retrieving answers from a blog corpus (RAG via Chroma)
* 📈 Analyzing ad performance CSVs (CTR, CPC, actionable insights)
* ✍️ Rewriting ads with platform/tone optimization
* 🧠 Logging feedback and computing ROUGE metrics for quality evaluation

---

## ✨ Features

* ✅ Multi-step **Graph RAG agent** with memory
* ✅ **Chroma vector DB** with chunked marketing blog content
* ✅ **Gemini 2.0 Flash** for fast, high-quality responses
* ✅ CSV analysis route with ad performance metrics
* ✅ Ad rewriting with tone & platform optimization
* ✅ Feedback logging + hallucination & relevance fields
* ✅ ROUGE evaluation script for summaries

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/yourname/marketing-rag-agent.git
cd marketing-rag-agent
```

### 2. Create Virtual Environment & Install Requirements

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Set Up .env

Create a `.env` file:

```
GOOGLE_API_KEY=your-google-api-key
```

### 4. Run the FastAPI App

```bash
uvicorn main:app --reload
```

---

## 🔌 API Endpoints

### 🔁 `POST /run-agent`

Runs the marketing RAG agent on a query.

#### Request JSON

```json
{
  "query": "Best ad copy for summer sales",
}
```

#### Response JSON

```json
{
  "response": "Here’s a great example of summer ad copy...",
  "history": ["User: Best ad copy...", "AI: Here’s..."]
}
```

---

### 📊 `POST /analyze-csv`

Uploads ad performance CSV and returns analysis.

#### Sample CSV Format

| ad\_name | impressions | clicks | spend |
| -------- | ----------- | ------ | ----- |
| Ad A     | 1000        | 100    | 200   |

#### Response JSON

```json
{
  "insights": "Ad A has high CTR...",
  "data_preview": "Top 5 ads with CTR and CPC..."
}
```

---

### ✍️ `POST /rewrite-ad`

Rewrites ad copy for a specific platform and tone.

#### Request JSON

```json
{
  "ad_text": "Buy our product now!",
  "tone": "fun",
  "platform": "Instagram"
}
```

#### Response JSON

```json
{
  "rewritten_ad": "Grab it before it’s gone! 🌟 #InstaDeal"
}
```

---

### 📈 `GET /metrics`

Returns statistics from feedback logs (hallucination rate, etc).

```json
{
  "total": 20,
  "hallucinated": 2,
  "relevance_scores": {
    "avg": 4.2,
    "min": 3,
    "max": 5
  }
}
```

---

## 🧠 Behind the Scenes

* **LangGraph** manages multi-step reasoning: Retrieve → Generate.
* **Chroma** stores vectorized chunks of marketing blog articles.
* **LangChain** used for embeddings, loaders, memory.
* **Gemini Flash** LLM responds to queries using retrieved docs.
* Feedback is saved to `feedback_log.json`, used for metrics.

---

## 🗂️ File Overview

```
app/
├── agent.py              # LangGraph-based RAG pipeline
├── routes/
│   └── feedback.py       # Feedback rating API (optional)
├── utils/
│   ├── utils.py          # Chroma vector store logic
│   ├── save_feedback.py  # Logging feedback to JSON
│   ├── rouge_eval.py     # ROUGE scoring utility
│   ├──  metrics.py        # Aggregates metrics from feedback
│   └── kg.py             # Knowledge graph enrichment function
main.py                   # FastAPI app
requirements.txt          # All dependencies pinned
.env                      # API key
```

---

## 🧪 Example Usage

### Run Agent

```bash
curl -X POST http://localhost:8000/run-agent \
  -H "Content-Type: application/json" \
  -d '{"query": "Tips for holiday season ads"}'
```

### Analyze CSV

```bash
curl -X POST http://localhost:8000/analyze-csv \
  -F 'file=@sample_ads.csv'
```

---

## 📊 Evaluation Strategy

* **ROUGE-1 / ROUGE-L** for comparing generated text to reference summaries.
* **Manual review** for hallucinations, relevance, tone.
* **Feedback logs** capture `is_hallucinated`, `relevance_score`, and `comments`.

---

## 📈 Pattern Recognition & Feedback Loop

* Every interaction logs feedback in `feedback_log.json`
* Can be enhanced with LangGraph memory nodes or LangSmith traces
* Scope for fine-tuning prompts based on low relevance / hallucinations

---

## ✅ Agentic RAG + Knowledge Graph

* ✅ Implements **Graph-based RAG** with LangGraph
* ✅ Multi-step: Retrieval → Prompt Contextualization → Gemini Response
* ✅ Uses simple **Knowledge Graph enrichment** for marketing terms via `enrich_with_knowledge_graph()`

---

## 📌 To Do / Future Enhancements

* [ ] Frontend integration (Streamlit or React)
* [ ] Active learning via feedback tuning
* [ ] Entity linking via proper KG ontology (e.g., ad platform schemas)
* [ ] Evaluation dashboard with automated scoring 
* [ ] Entity-level knowledge graph with relationships (e.g., campaign → platform → CTA) 
* [ ] MongoDB/SQL logging for production readiness 
* [ ] LangSmith instrumentation
---

**Built with ❤️ for Track A (Agent + Research)**
