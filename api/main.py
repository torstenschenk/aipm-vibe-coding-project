import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from groq import Groq
from pydantic import BaseModel
import uvicorn

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY must be set in the environment.")

client = Groq(api_key=api_key)

app = FastAPI()


class PromptRequest(BaseModel):
    prompt: str


class GenerateResponse(BaseModel):
    result: str


@app.post("/generate", response_model=GenerateResponse)
async def generate(payload: PromptRequest):
    try:
        completion = client.chat.completions.create(
            #model="llama3-70b-8192",
            model="llama-3.1-8b-instant",
            temperature=0.2,
            max_tokens=512,
            messages=[
                {"role": "system", "content": "You are a concise assistant that responds clearly."},
                {"role": "user", "content": payload.prompt},
            ],
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    choices = completion.choices if completion else None
    first_message: Optional[str] = None
    if choices:
        message = choices[0].message
        if message and message.content:
            first_message = message.content.strip()

    if not first_message:
        raise HTTPException(status_code=500, detail="Empty response from Groq.")

    return GenerateResponse(result=first_message)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
