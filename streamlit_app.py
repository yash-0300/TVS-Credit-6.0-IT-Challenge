import streamlit as st
import os
import pandas as pd
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *
from utils import *


# Page configuration
st.set_page_config(page_title="TVS Chatbot", page_icon="🤖", layout="wide")

# Float feature intialization
float_init()

# st.sidebar.title("Flipkart Chatbot")
st.sidebar.image("https://pimwp.s3.ap-south-1.amazonaws.com/2024/05/TVS-Credit-Logo-01.png", use_column_width=True)
st.sidebar.markdown("### Welcome to TVS CredAssist AI Assistant!")
st.sidebar.markdown(
    """
    This chatbot is here to assist you with all your financial needs. 
    Whether you're looking for loan details, tracking your applications, or exploring the best credit options, we're here to help!
    """
)
st.sidebar.markdown("---")
st.sidebar.markdown("### How to use:")
st.sidebar.markdown(
    """
    - Click on the record button to start your conversation.
    - The chatbot will respond to your queries instantly.
    """
)
st.sidebar.markdown("### Feedback")
st.sidebar.text_area("We value your feedback!", placeholder="Type here...")


def generate_conversation_history():
    df = pd.read_csv('./Tvs_Credit.csv')
    conversation_history = []
    for index, row in df.iterrows():
        conversation_history.append({
            'role': 'user',
            'content': row['Questions']
        })
        conversation_history.append({
            'role': 'assistant',
            'content': row['Answer']
        })

    conversation_history.append({
        'role': 'assistant',
        'content': 'Hi! How may I assist you today'
    })

    return conversation_history

conversation_history = generate_conversation_history()
len_conversation_history = len(conversation_history) - 1

def intialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = conversation_history

    # if "audio_intitalized" not in st.session_state:
    #     st.session_state.audio_intialized = False

intialize_session_state()

st.title(":green[TVS CredAssist] AI Assistant 🤖")

# Create footer container for the microphone
footer_container = st.container()
with footer_container:
    audio_bytes = audio_recorder()

count_messages = 0
for message in st.session_state.messages:
    if count_messages >= len_conversation_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    count_messages += 1

# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.write(message["content"])


if audio_bytes:
    # Write the audio bytes to a file
    with st.spinner("Transcribing..."):
        webm_file_path = "temp_audio.mp3"
        with open(webm_file_path, "wb") as f:
            f.write(audio_bytes)
        
        transcript = speech_to_text(webm_file_path)
        if transcript:
            st.session_state.messages.append({"role": "user", "content": transcript})
            with st.chat_message("user"):
                st.write(transcript)
            os.remove(webm_file_path)


if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking🤔..."):
            final_response = get_answer(st.session_state.messages)
        with st.spinner("Generating audio response..."):
            audio_file = text_to_speech(final_response)
            autoplay_audio(audio_file)
        
        st.write(final_response)
        st.session_state.messages.append({"role": "assistant", "content": final_response})
        os.remove(audio_file)

# Float the footer container and provide CSS to target it with 
footer_container.float("bottom: 0rem;")
