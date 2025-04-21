from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)

model_path = "cosmosai471/Luna-v2"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path).to("cpu")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message", "")
        prompt = f"User: {user_input}\nLuna:"
        inputs = tokenizer(prompt, return_tensors="pt", padding=True)
        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            do_sample=True,
            top_p=0.9,
            temperature=0.7
        )
        decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Extract only Luna's response
        if "Luna:" in decoded_output:
            response = decoded_output.split("Luna:")[-1].strip()
        else:
            response = decoded_output
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

@app.route("/")
def home():
    return "Luna backend is running!"
    
