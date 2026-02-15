from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
import streamlit as st

load_dotenv()

llm = ChatGroq(
  model_name = "openai/gpt-oss-120b"
)


st.title("Ask question")
st.markdown("your bot ask question which you want")

if "messages" not in st.session_state:
  st.session_state.messages = []

query = st.chat_input("Ask anything?")

for m in st.session_state.messages:
  role = m["role"]
  content = m["content"]
  st.chat_message(role).markdown(content)

if query:
  st.session_state.messages.append({
    "role":"user",
    "content": query
  })
  st.chat_message("user").markdown(query)

  with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        for chunk in llm.stream(st.session_state.messages):
          if chunk.content:
                full_response += chunk.content
                message_placeholder.markdown(full_response)

  st.session_state.messages.append({
    "role":"ai",
    "content": full_response
  })
