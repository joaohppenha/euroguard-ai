import streamlit as st
import requests

# Page setup and header
st.set_page_config(
    page_title="EuroGuard AI",
    page_icon="🇪🇺",
    layout="centered"
)

st.title("🇪🇺 EuroGuard AI")
st.caption("RAG Compliance Assistant for GDPR & EU AI Act")

# Local FastAPI endpoint URL
API_URL = "http://127.0.0.1:8000/api/v1/query"

# Initialize chat message history state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render chat history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User chat input widget
if user_query := st.chat_input("Ask a question about GDPR or EU AI Act..."):
    # Display user input
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Send POST request to FastAPI backend
    with st.chat_message("assistant"):
        with st.spinner("Analyzing regulatory documentation..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"query": user_query},
                    timeout=30
                )
                
                if response.status_code == 200:
                    answer = response.json().get("response", "No response content.")
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    error_msg = f"API Error ({response.status_code}): {response.text}"
                    st.error(error_msg)
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to FastAPI server. Make sure Uvicorn is running on port 8000.")