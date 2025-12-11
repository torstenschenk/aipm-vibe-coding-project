import os
from typing import List, Dict

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

FASTAPI_BASE_URL = os.getenv("FASTAPI_BASE_URL", "http://localhost:8001").rstrip("/")
GENERATE_ENDPOINT = f"{FASTAPI_BASE_URL}/generate"

st.set_page_config(page_title="Groq Chat Relay", layout="centered")
st.title("Groq Chat Relay")

if "messages" not in st.session_state:
    st.session_state.messages: List[Dict[str, str]] = []

st.markdown(
    """
    <style>
        .history-pane {
            background-color: #f9fafb;
            color: #111827;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 16px;
            max-height: 320px;
            overflow-y: auto;
        }
        .history-pane p {
            margin-bottom: 12px;
        }
        .history-pane span {
            font-weight: 600;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

history = reversed(st.session_state.messages)
history_html = "".join(
    f"<p><span>You:</span> {entry['prompt']}</p>"
    f"<p><span>Groq:</span> {entry['response']}</p>"
    for entry in history
)

st.markdown(
    f'<div class="history-pane">{history_html or "<p>No messages yet.</p>"}</div>',
    unsafe_allow_html=True,
)

with st.form("prompt-form"):
    prompt = st.text_input("Enter your prompt")
    submitted = st.form_submit_button("Send")

    if submitted:
        if not prompt.strip():
            st.error("Please enter a prompt before sending.")
        else:
            try:
                response = requests.post(
                    GENERATE_ENDPOINT,
                    json={"prompt": prompt},
                    timeout=60,
                )
                response.raise_for_status()
                data = response.json()
                result = data.get("result")
                if not result:
                    st.error("FastAPI did not return a result.")
                else:
                    st.session_state.messages.append({"prompt": prompt, "response": result})
                    st.rerun()
            except requests.RequestException as exc:
                st.error(f"Request failed: {exc}")
