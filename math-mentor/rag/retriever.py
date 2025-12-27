from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os

def retrieve_context(query, k=4):
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    INDEX_PATH = os.path.join(PROJECT_ROOT, "rag", "faiss_index")

    vectorstore = FAISS.load_local(
        INDEX_PATH,
        OpenAIEmbeddings(),
        allow_dangerous_deserialization=True
    )
    return vectorstore.similarity_search(query, k=k)
