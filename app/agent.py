# 📁 app/agent.py

import os
from dotenv import load_dotenv
from typing import TypedDict, List

import uuid
import google.generativeai as genai

from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langgraph.graph import StateGraph, END
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnableConfig
from langchain_core.prompts import PromptTemplate



# ✅ Load environment variables
load_dotenv()

# ✅ Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel(model_name="gemini-2.0-flash-lite")

# ✅ Gemini Embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# ✅ Agent state type
class AgentState(TypedDict):
    query: str
    docs: List[Document]
    response: str
    history: List[str]

# ✅ Chroma retriever
def get_retriever():
    return Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    ).as_retriever(search_kwargs={"k": 3})

# ✅ Node: Document Retrieval
def retrieve_docs(state: AgentState) -> AgentState:
    print("🔍 Retrieving documents...")
    docs = get_retriever().invoke(state["query"])
    history = state.get("history", []) + [f"User: {state['query']}"]
    return {
        "query": state["query"],
        "docs": docs,
        "history": history,
        "response": ""
    }

# ✅ Node: Generate Gemini Response
def generate_answer(state: AgentState) -> AgentState:
    context = "\n\n".join(doc.page_content for doc in state["docs"])
    conversation = "\n".join(state.get("history", []))

    prompt = f"""
You're a helpful marketing AI assistant.

Here is the conversation so far:
{conversation}

Now, answer the user's latest query.

--- BLOG CONTENT ---
{context}
--- END ---

User Query: {state['query']}
Provide a clear, actionable response.
"""
    print("🤖 Querying Gemini...")
    response = model.generate_content(prompt)
    answer = response.text.strip()
    updated_history = state["history"] + [f"AI: {answer}"]
    return {
        "query": state["query"],
        "docs": state["docs"],
        "history": updated_history,
        "response": answer
    }

# ✅ Build LangGraph workflow
def build_agent():
    memory = ConversationBufferMemory(return_messages=True)

    workflow = StateGraph(AgentState)
    workflow.add_node("retrieve", RunnableLambda(retrieve_docs))
    workflow.add_node("generate", RunnableLambda(generate_answer))

    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)

    return workflow.compile()

# ✅ Compiled agent instance
agent = build_agent()

# ✅ Utility for visualizing the graph (optional)
def get_graph():
    return agent

# ✅ Public API to call the agent
def run_query(query: str, memory_session=None) -> str:
    if memory_session is None:
        memory_session = []

    result = agent.invoke({
        "query": query,
        "history": memory_session
    })
    return result["response"], result["history"]

