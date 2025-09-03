import streamlit as st
import requests

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(page_title="KrishiAI Assistant", page_icon="🌾")

st.title("🌾 KrishiAI - Agriculture Expert Assistant")
st.write("Ask me anything about Indian agriculture!")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for chat in st.session_state.messages:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# Input box
if question := st.chat_input("Type your agricultural question here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Call FastAPI backend
    try:
        response = requests.post(API_URL, json={"question": question})
        if response.status_code == 200:
            data = response.json()
            answer = data.get("answer", "⚠️ No response from server.")
        else:
            answer = f"⚠️ Error {response.status_code}: Could not connect to backend."

    except Exception as e:
        answer = f"⚠️ Exception: {str(e)}"

    # Add assistant response
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
