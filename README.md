# 🚀 Marketing RAG Agent (Track A – Research + Prototype)

[![GitHub Repo](https://img.shields.io/badge/GitHub-MarketingRAG-blue?logo=github)](https://github.com/Pranavbh1/marketing-rag-agent)

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
* ✅ Lightweight **Knowledge Graph enrichment** for marketing terms

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/Pranavbh1/marketing-rag-agent.git
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
uvicorn app.main:app --reload
```

Then open in browser: [http://localhost:8000/docs](http://localhost:8000/docs)

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

Returns statistics from feedback logs.

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

* **LangGraph** manages multi-step reasoning: Retrieve → Generate
* **Chroma** stores vectorized blog content
* **LangChain** powers embeddings, memory, and data loading
* **Gemini Flash** LLM generates contextual answers
* **Knowledge Graph** enriches the query context
* Feedback saved to `feedback_log.json` is used for ROUGE and metrics

---

## 🗂️ File Overview

```
app/
├── __init__.py
├── main.py                 # FastAPI app with endpoints
├── agent.py                # LangGraph-based RAG pipeline
├── routes/
│   └── feedback.py         # Optional: feedback API endpoint
├── utils/
│   ├── __init__.py
│   ├── utils.py            # Chroma vector store & embedding logic
│   ├── save_feedback.py    # Feedback logger
│   ├── rouge_eval.py       # ROUGE scoring
│   ├── metrics.py          # Feedback stats
│   └── kg.py               # Lightweight marketing knowledge graph enrichment
chroma_db/                  # Chroma vector DB storage
chroma_langchain_db/        # Optional LangChain version DB
sample_data/                # Example CSV for testing
feedback_log.json           # Feedback records
requirements.txt            # Dependencies
.env                        # Google API key
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
  -F 'file=@sample_data/ad_data.csv'
```

### Rewrite Ad

```bash
curl -X POST http://localhost:8000/rewrite-ad \
  -H "Content-Type: application/json" \
  -d '{"ad_text": "Huge discounts today!", "tone": "professional", "platform": "LinkedIn"}'
```

---

## 📊 Evaluation Strategy

* **ROUGE-1 / ROUGE-L**: for comparing responses to ground truth
* **Manual review**: hallucinations, tone, relevance
* **Feedback loop**: Logs `is_hallucinated`, `relevance_score`, `comments`

---

## 🧩 Agentic Pattern + Knowledge Graph

* ✅ LangGraph-based multi-step flow
* ✅ Prompt enrichment via `enrich_with_knowledge_graph()` in `kg.py`
* ✅ Easily extensible with LangSmith, LangChain memory, or frontend UI

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
