import streamlit as st
from get_embeddings import *
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import AzureChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import os

load_dotenv()
openai_api_key = os.getenv("openai_api_key")
openai_api_version = os.getenv("openai_api_version")
openai_api_base = os.getenv("openai_api_base")
deployment_name = os.getenv("openai_api_key")

llm = AzureChatOpenAI(
    openai_api_key = openai_api_key,
    openai_api_version = "2024-02-01",
    openai_api_base = "https://gpt4o-adya.openai.azure.com/",
    deployment_name ="gpt4o_deployment",
    temperature = 0.4
)

def conversational_qa_chain():
    prompt = ChatPromptTemplate.from_template("""
        Answer the following question based only on the provided context.
        Think step by step before providing a detailed answer.
        I will tip you $1000 if the user finds the answer helpful
        If you don't know the answer, just say that you don't know.

        <context> {context} </context>
        Question: {input}
        """
    )

    document_chain = create_stuff_documents_chain(
        llm = llm,
        prompt = prompt
    )

    vectordb = get_vectordb()
    retriever = vectordb.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    return retrieval_chain

def main():
    st.title("TVS :violet[CredAssist] 💁")
    query = st.text_input("Ask TVS CredAssist, your ultimate financial companion!!!")
    if query:
        retrieval_chain = conversational_qa_chain()
        response = retrieval_chain.invoke({"input": query})
        st.text(response['answer'])

if __name__ == "__main__":
    main()