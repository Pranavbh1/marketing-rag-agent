📝 Track A – Agentic RAG Prototype Write-up
🧱 Architecture & Tools Used
This project implements an Agentic RAG system built with:

FastAPI for a robust and modular backend

LangGraph to manage multi-step workflows (Retrieve → Generate)

LangChain components for embeddings, document loaders, and memory

Gemini 2.0 Flash for fast and contextual generation

Chroma as the vector store, storing marketing blog chunks

GoogleGenerativeAI embeddings for semantic vectorization

Knowledge Graph enrichment via kg.py to expand user queries

ROUGE evaluation to track response quality

The solution is served as a fully working FastAPI backend with multiple endpoints that support RAG-based question answering, CSV analysis, ad rewriting, and evaluation logging.

🧠 Use of Graph RAG (Agentic RAG)
This project utilizes LangGraph, which enables declarative control over agent workflows. The RAG pipeline is modeled as a directed graph:

Node 1: Retrieve → Retrieves top-k relevant chunks from Chroma DB using vector similarity

Node 2: Generate → Passes retrieved content, query history, and context to Gemini for answering

This graph-based structure allows for better debugging, extensibility (e.g., adding a critique or summarization node), and memory tracking. Unlike simple chains, LangGraph supports multi-turn, multi-hop reasoning in a modular, scalable way.

📚 Knowledge Graph Integration
A lightweight enrich_with_knowledge_graph() function enhances user queries before retrieval. For example:

Query: “Best campaigns for skincare”
→ Enriched: “Best campaigns for skincare ads, beauty products, Instagram influencer promotions”

This enrichment simulates a knowledge graph by adding domain-relevant entities and synonyms, increasing the recall during document retrieval and improving answer relevance. In future iterations, this can be expanded into a formal knowledge graph using ontologies like schema.org or advertising taxonomies.

📏 Evaluation Strategy
We use a combination of manual and automated evaluation methods:

ROUGE-1 and ROUGE-L via rouge_eval.py to evaluate overlap with reference summaries

Feedback Logging: Each interaction is logged to feedback_log.json with:

is_hallucinated: Boolean flag

relevance_score: 1–5 rating

comments: Optional feedback

Metrics Endpoint (/metrics): Aggregates relevance scores and hallucination rate

This allows us to quantitatively monitor agent performance and iterate over time.

🔁 Pattern Recognition & Improvement Loop
The system supports a continuous improvement loop:

Logged feedback data can be analyzed to fine-tune prompts or rerank responses

The LangGraph structure allows easy integration of future nodes like:

Critic agents

Memory nodes for user-specific long-term context

Retrieval re-ranking based on feedback

As a next step, feedback signals can drive prompt rewriting or automated retraining, simulating a learning system.

🔧 Challenges & Resolutions
Chroma persistence conflicts: Solved using a startup routine to check/create the vector DB

Slow CSV file handling: Optimized by computing CTR/CPC inline and summarizing top-5 rows

Query hallucinations: Reduced via prompt engineering and context grounding

Limited context in user questions: Addressed with KG-based enrichment

🚀 Next Steps
Add frontend (Streamlit or React) for visual interaction

Use LangSmith for trace visualization and debugging

Expand KG with entity linking + vector search hybrids

Add LangGraph memory nodes to personalize across sessions



Author: Pranav Bhawsar
Repository: [GitHub Link Placeholder]