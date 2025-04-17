from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_URL = "https://api-inference.huggingface.co/models/cosmosai471/Luna-v2"
HEADERS = {"Authorization": "Bearer hf_xxxYourTokenHerexxx"}  # Replace with your token

@app.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()
        user_input = body.get("message", "")

        response = requests.post(API_URL, headers=HEADERS, json={"inputs": user_input})
        result = response.json()

        print("Hugging Face result:", result)  # Debug line

        if isinstance(result, list) and len(result) > 0:
            return {"reply": result[0]["generated_text"]}
        else:
            return {"reply": "Sorry, Luna didn’t respond."}

    except Exception as e:
        print("Error:", str(e))
        return {"reply": "Sorry, Luna didn’t respond due to an internal error."}
