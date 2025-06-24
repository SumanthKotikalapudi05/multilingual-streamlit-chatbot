import streamlit as st
import os
from constants import google_key 

st.title(" Sumanth's First Chat-Bot")

if not os.environ.get("Google_API_Key"):
    os.environ['Google_API_Key'] = google_key

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

model = init_chat_model(
    "gemini-2.0-flash",
      model_provider="google_genai"
      )

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_area("Enter text in any language to english", "")

if st.button("Enter"):
    if user_input.strip():
        st.session_state.chat_history.append(HumanMessage(content=user_input))

        with st.chat_message("user"):
            st.markdown(user_input)

        messages = [SystemMessage("Answer the following in the given language and also in english"),
                    HumanMessage("hello!!")] + st.session_state.chat_history

        with st.chat_message("assistant"):
            response_container = st.empty()
            response = ""

            for token in model.stream(messages):
                response += token.content
                response_container.markdown(response + "▌")

            # Remove the cursor
            response_container.markdown(response)
            st.session_state.chat_history.append(HumanMessage(content=user_input))
            st.session_state.chat_history.append(HumanMessage(content=response))

if st.button("Clear Chat"):
    st.session_state.chat_history = []
