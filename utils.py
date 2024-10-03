import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
import base64

load_dotenv()
search = GoogleSerperAPIWrapper()

api_key = os.getenv("openai_api_key")
client = OpenAI(api_key = api_key)

def get_answer(messages):
    # system_message = [{"role": "system", "content": "You are an helpful AI Chatbot, that answers questions asked by Users based on the previous chathistory. You have to retrieve the similar question and answer exactly as the user answered it previously"}]
    
    query_asked = st.session_state.messages[-1]["content"]
    query_asked += ". Always search on TVS Credit website. https://www.tvscredit.com/"
    context = search.run(query_asked)
    system_prompt = f"""
    You are an helpful Financial AI Assistant. 
    Your role is to assist customers by answering their queries regarding personal loans, two-wheeler loans, and several other financial services available on TVS Credit, using a combination of past conversation history and real-time information fetched from TVS Credit website https://www.tvscredit.com/.
    If you don't get answers from the conversation history. You can use the given context fetched from TVS Credit website to answer customer query.
    {context}
    """
    system_message = [{"role": "system", "content": system_prompt}]
    messages = system_message + messages
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    return response.choices[0].message.content

def speech_to_text(audio_data):
    with open(audio_data, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model = "whisper-1",
            response_format = "text",
            file = audio_file
        )
    return transcript

def text_to_speech(input_text):
    response = client.audio.speech.create(
        model = "tts-1",
        voice = "nova",
        input = input_text
    )
    webm_file_path = "temp_audio_play.mp3"
    with open(webm_file_path, "wb") as f:
        response.stream_to_file(webm_file_path)
    return webm_file_path

def autoplay_audio(file_path : str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src = "data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html = True)