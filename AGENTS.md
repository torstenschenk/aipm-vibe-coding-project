# Sample AGENTS.md file

You are Codex building a minimal FastAPI + Streamlit project that proxies prompts to Groq’s chat completions.

Requirements
1. FastAPI service (file `api/main.py`)
   - Load `GROQ_API_KEY` from `.env` (use python-dotenv).
   - Instantiate Groq client once.
   - Expose POST `/generate` accepting JSON `{"prompt": "<text>"}`.
   - Call model `llama3-70b-8192` with a short system prompt (“concise assistant…”), temperature 0.2, max_tokens 512.
   - Return JSON `{"result": "<first message content>"}`.
   - On Groq/API errors: raise HTTP 502 with Groq message; if response empty, raise HTTP 500.
   - Include `if __name__ == "__main__": uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)`.

2. Streamlit client (file `streamlit_app.py`)
   - Load `.env`, read `FASTAPI_BASE_URL` (default `http://localhost:8001`), set `GENERATE_ENDPOINT = <base>/generate`.
   - Keep session state list `messages` storing `prompt` + `response`.
   - Layout: title “Groq Chat Relay”, page config centered.
   - Custom CSS: history pane with light background (`#f9fafb`), dark text, rounded border, scrollable up to ~320px.
   - Show conversation history newest-first inside pane; message format “You:” / “Groq:”.
   - Form with text input + submit button. Validate non-empty prompt.
   - On submit: POST to FastAPI, 60s timeout, surface `requests` errors via `st.error`.
   - Append successful exchanges to session history and call `st.rerun()`.

3. Tooling
   - `requirements.txt` must contain: streamlit, fastapi, uvicorn, requests, python-dotenv, groq, plus pandas/scikit-learn if already listed.
   - Include `.env.example` showing `GROQ_API_KEY=` and optional `FASTAPI_BASE_URL=`.
   - Update README quickstart: create venv, install requirements, run API via `uvicorn api.main:app --reload --port 8001`, run Streamlit via `streamlit run streamlit_app.py`, explain GROQ key requirement.

Deliverables
- Fully working code for both files, ready to run locally.
- Concise comments only when necessary.
- No extra files beyond the ones specified.