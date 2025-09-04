import streamlit as st
import requests
import time

 


# FastAPI backend URL
API_URL = "http://127.0.0.1:8000/ask"
MAX_RETRIES = 10
WAIT_SECONDS = 2

r = None
for i in range(MAX_RETRIES):
    try:
        r = requests.get(API_URL)
        print("Connected to backend!")
        break
    except requests.exceptions.RequestException:
        print(f"Attempt {i+1}/{MAX_RETRIES} failed, retrying in {WAIT_SECONDS}s...")
        time.sleep(WAIT_SECONDS)

if r is None:
    raise Exception(f"Could not connect to FastAPI backend at {API_URL}")



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
        

