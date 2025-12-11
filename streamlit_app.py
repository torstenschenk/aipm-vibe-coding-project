import os
from typing import List

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("FASTAPI_BASE_URL", "http://localhost:8001")
GENERATE_ENDPOINT = f"{API_BASE_URL.rstrip('/')}/generate"

st.set_page_config(page_title="Groq Streamlit Demo", layout="centered")
st.title("Groq Chat Relay")

if "messages" not in st.session_state:
    st.session_state.messages: List[dict] = []

st.markdown(
    """
    <style>
        .result-pane {
            max-height: 320px;
            overflow-y: auto;
            padding: 1rem;
            border: 1px solid #d1d5db;
            border-radius: 0.5rem;
            background-color: #f9fafb;
            color: #0f172a;
        }
        .result-pane p {
            margin-bottom: 0.5rem;
        }
        .result-pane hr {
            border: none;
            border-top: 1px solid #cbd5f5;
            margin: 0.75rem 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

history_html = ""
for entry in reversed(st.session_state.messages):
    history_html += (
        f"<p><strong>You:</strong> {entry['prompt']}</p>"
        f"<p><strong>Groq:</strong> {entry['response']}</p><hr />"
    )

st.markdown(
    f"<div class='result-pane'>{history_html or 'Awaiting your first prompt.'}</div>",
    unsafe_allow_html=True,
)

with st.form("prompt_form"):
    prompt = st.text_input("Ask the model", placeholder="Type your message here...")
    submitted = st.form_submit_button("Send")

if submitted:
    if not prompt.strip():
        st.warning("Please enter a prompt before sending.")
    else:
        with st.spinner("Contacting FastAPI backend…"):
            try:
                response = requests.post(
                    GENERATE_ENDPOINT,
                    json={"prompt": prompt},
                    timeout=60,
                )
                response.raise_for_status()
                data = response.json()
                answer = data.get("result", "(No content returned)")
            except requests.RequestException as exc:
                st.error(f"Request failed: {exc}")
            else:
                st.session_state.messages.append(
                    {"prompt": prompt.strip(), "response": answer.strip()}
                )
                st.rerun()
