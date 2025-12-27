from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os
from dotenv import load_dotenv
load_dotenv()

def build_index():
    # Resolve project root dynamically
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    KB_PATH = os.path.join(PROJECT_ROOT, "rag", "kb_docs")
    INDEX_PATH = os.path.join(PROJECT_ROOT, "rag", "faiss_index")

    docs = []

    for file in os.listdir(KB_PATH):
        if file.endswith(".md"):
            with open(os.path.join(KB_PATH, file), "r") as f:
                docs.append(f.read())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=50
    )

    documents = splitter.create_documents(docs)

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local(INDEX_PATH)

if __name__ == "__main__":
    build_index()
