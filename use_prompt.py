import streamlit as st
import os
from constants import google_key

st.title("Sumanth's First Chat-Bot")

if not os.environ.get("Google_API_Key"):
    os.environ['Google_API_Key'] = google_key

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate

model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_area("Enter text in any language to translate to English", "")

instruction_template = PromptTemplate(
    input_variables=["user_text"],
    template="""
You are a smart Multilingual assistant.

identify the language given by the user as message.
when the user asks something in  any language), reply fully in **that language** with **English transliteration in brackets**, wherever needed.

if the user's message is in English, still respond in English , and do **not** repeat the message in English again.

if the answer involves code, only show the code once in that language context — do **not** repeat it in English.
Message: {user_text}
"""
)

# On Translate button
if st.button("GO!!!"):
    if user_input.strip():
        # Show user message
        with st.chat_message("user"):
            st.markdown(user_input)

        # Format system instruction using the template
        system_prompt = instruction_template.format(user_text=user_input)

        # Prepare messages
        messages = [
            SystemMessage(system_prompt),
            HumanMessage(user_input)
        ]

        # Append to history
        st.session_state.chat_history.append(HumanMessage(user_input))

        # Assistant message container
        with st.chat_message("assistant"):
            response_container = st.empty()
            response = ""

            for token in model.stream(messages):
                response += token.content
                response_container.markdown(response + "▌")

            # Final response
            response_container.markdown(response)
            st.session_state.chat_history.append(HumanMessage(response))

# Clear button
if st.button("Clear Chat"):
    st.session_state.chat_history = []
