from fastapi import FastAPI, Request
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

API_URL = "https://api-inference.huggingface.co/models/cosmosai471/Luna-v2"
HEADERS = {"Authorization": "Bearer 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"}

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_input = body.get("message", "")
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": user_input})
    result = response.json()
    return {"reply": result[0]['generated_text'] if isinstance(result, list) else "Sorry, Luna didn’t respond."}
