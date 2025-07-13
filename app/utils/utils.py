# 📁 app/utils.py

import os
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader

# ✅ Load environment variables
load_dotenv()

# ✅ Create Gemini embedding model ONCE
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def create_vectorstore():
    # ✅ Skip rebuilding if vectorstore already exists
    if os.path.exists("chroma_langchain_db/index"):
        print("🟢 Vectorstore already exists. Skipping rebuild.")
        return

    print("⚙️ Creating Chroma vectorstore...")

    all_docs = []
    for filename in os.listdir("data"):
        if filename.endswith(".txt"):
            loader = TextLoader(
                os.path.join("data", filename),
                encoding="utf-8",
                autodetect_encoding=True
            )
            docs = loader.load()
            all_docs.extend(docs)

    # ✅ Split documents into chunks
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(all_docs)

    # ✅ Initialize Chroma vectorstore
    vectorstore = Chroma(
        collection_name="marketing_blog_chunks",
        embedding_function=embeddings,
        persist_directory="chroma_langchain_db"
    )

    # ✅ Add chunks and persist
    vectorstore.add_documents(split_docs)

    print("✅ Vector store created and documents added.")
    return vectorstore
