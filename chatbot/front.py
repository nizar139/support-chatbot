import streamlit as st
import random
import time
from chatbot import RAG

rag_chatbot=RAG()

st.title("Madkudu Chatbot")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    answer, context = rag_chatbot.handle_user_input(prompt)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.write(answer)
    
    print(context)