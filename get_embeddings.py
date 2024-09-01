from document_chunks import *
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

texts = get_document_chunks()

def get_vectordb():
    persist_directory = './chromadb'
    vectordb = Chroma.from_documents(
        documents = texts,
        embedding = embeddings,
        persist_directory = persist_directory
    )
    return vectordb

