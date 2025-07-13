# 📁 main.py

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from app.agent import run_query
# from app.utils import create_vectorstore
from app.utils.utils import create_vectorstore

from dotenv import load_dotenv
import os
from fastapi import UploadFile, File
import pandas as pd
from app.agent import model  # reuse your existing Gemini model
from app.routes.feedback import router as feedback_router
from app.utils.kg import enrich_with_knowledge_graph
from app.utils.metrics import get_feedback_metrics



# ✅ Load environment variables (e.g., GOOGLE_API_KEY)
load_dotenv()

# ✅ Initialize FastAPI app
app = FastAPI(title="Marketing RAG Agent", version="1.0")
app.include_router(feedback_router, prefix="/api")

# ✅ Create Chroma Vector Store on startup (if not already persisted)
@app.on_event("startup")
def build_vectorstore():
    print("⚙️ Building/Validating vector store...")
    create_vectorstore()
    print("✅ Vector store ready.")

# ✅ Request Body Schema
from typing import Optional
from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    history: Optional[list[str]] = []



class RewriteRequest(BaseModel):
    ad_text: str
    tone: str
    platform: str

# # ✅ Main Agent Endpoint
# @app.post("/run-agent")
# def run_agent(req: QueryRequest):
#     print("🟡 Received query:", req.query)

#     try:
#         response, updated_history = run_query(req.query)
#         return {
#             "response": response,
#             "history": updated_history
#         }

#     except Exception as e:
#         # print("🔴 Error:", str(e))
#         return {"error": str(e)}

from app.utils.save_feedback import auto_log_feedback  # ✅ new helper

@app.post("/run-agent")
def run_agent(req: QueryRequest):
    query_enriched = enrich_with_knowledge_graph(req.query)
    response, updated_history = run_query(query_enriched, req.history)

    # ✅ Automatically save initial feedback entry
    auto_log_feedback(req.query, response)

    return {"response": response, "history": updated_history}




@app.post("/analyze-csv")
async def analyze_csv(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)

        df["CTR"] = df["clicks"] / df["impressions"].replace(0, 1)
        df["CPC"] = df["spend"] / df["clicks"].replace(0, 1)

        summary = df[["ad_name", "impressions", "clicks", "spend", "CTR", "CPC"]] \
            .sort_values(by="CTR", ascending=False) \
            .head(5)

        summary_str = summary.to_string(index=False)

        prompt = f"""
You're a marketing performance analyst AI.

The table below shows the top 5 performing ads from a Meta or Google Ads campaign:

{summary_str}

Your tasks:
1. Suggest 3 improvements to ad performance.
2. Highlight any unusual trends or outliers.
3. Give actionable tips for better engagement or conversions.
"""

        response = model.generate_content(prompt)

        return {
            "insights": response.text.strip(),
            "data_preview": summary_str
        }

    except Exception as e:
        return {"error": str(e)}



@app.post("/rewrite-ad")
def rewrite_ad(req: RewriteRequest):
    try:
        prompt = f"""
You are an expert ad copywriter.

Rewrite the following ad in a {req.tone} tone, optimized for {req.platform}.

Make sure it fits platform best practices (character limits, hashtags, tone of voice).

Original Ad:
{req.ad_text}

Rewritten Ad:
"""

        response = model.generate_content(prompt)
        return {"rewritten_ad": response.text.strip()}
    except Exception as e:
        return {"error": str(e)}
    

@app.get("/metrics")
def metrics():
    return get_feedback_metrics()
