from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)

model_path = "cosmosai471/Luna-v2"  # your model on HF Hub
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path).to("cpu")

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "")
    prompt = f"User: {user_input}\nLuna:"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=200, do_sample=True, temperature=0.7, top_p=0.9)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True).split("Luna:")[-1].strip()
    return jsonify({"response": response})

@app.route('/')
def home():
    return "Luna backend is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
    
