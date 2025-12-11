import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from groq import Groq
from pydantic import BaseModel

load_dotenv()

GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is missing. Add it to your .env file.")

groq_client = Groq(api_key=GROQ_API_KEY)

app = FastAPI(
    title="Groq Relay API",
    description="Simple FastAPI service that forwards prompts to Groq models.",
    version="0.1.0",
)


class PromptRequest(BaseModel):
    prompt: str


class LLMResponse(BaseModel):
    result: str


@app.post("/generate", response_model=LLMResponse)
async def generate_response(payload: PromptRequest) -> LLMResponse:
    """Send the user's prompt to Groq and return the model's reply."""
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a concise assistant that explains concepts clearly."
                    ),
                },
                {"role": "user", "content": payload.prompt},
            ],
            temperature=0.2,
            max_tokens=512,
        )
    except Exception as exc:  # pragma: no cover - groq client handles specifics
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    content = completion.choices[0].message.content if completion.choices else ""
    if not content:
        raise HTTPException(status_code=500, detail="Empty response from Groq.")

    return LLMResponse(result=content)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)