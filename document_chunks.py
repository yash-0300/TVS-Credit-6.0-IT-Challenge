from document_loader import *
from langchain.text_splitter import RecursiveCharacterTextSplitter

docs = get_web_documents()

def get_document_chunks():
    r_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 150,
        length_function = len,
        separators = ["\n\n\n", "\n\n", "\n", " ", ""]
    )
    texts = r_splitter.split_documents(docs)
    return texts