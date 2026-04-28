import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from gradio_client import Client

app = Flask(__name__)
CORS(app)

HF_SPACE = os.environ.get("HF_SPACE_ID", "cosmosai471/come_onnn")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_text = data.get("text")
    
    print(f">>> Received prompt: {user_text}", flush=True)

    try:
        client = Client(HF_SPACE)
        # Your API documentation says /chat_generator takes (str, list)
        result = client.predict(
            message_from_input=user_text,
            history=[], 
            api_name="/chat_generator"
        )
        
        print(f">>> Raw Result from HF: {result}", flush=True)

        # AGGRESSIVE SEARCH FOR THE RESPONSE TEXT
        ai_response = None

        if isinstance(result, (list, tuple)):
            # Check Index 2 first (Your docs say this is the Textbox string)
            if len(result) > 2 and isinstance(result[2], str) and len(result[2]) > 0:
                ai_response = result[2]
            # Check Index 0 (The Chatbot history list)
            elif len(result) > 0 and isinstance(result[0], list) and len(result[0]) > 0:
                last_msg = result[0][-1]
                if isinstance(last_msg, dict) and 'content' in last_msg:
                    ai_response = last_msg['content']
                elif isinstance(last_msg, (list, tuple)) and len(last_msg) > 1:
                    ai_response = last_msg[1] # Older Gradio format

        if ai_response:
            print(f">>> Success! Sending: {ai_response[:50]}...", flush=True)
            return jsonify({"response": ai_response})
        
        return jsonify({"response": "Luna reached Hugging Face, but the AI didn't send back text. Check if the Space is working manually."})

    except Exception as e:
        print(f"!!! CRITICAL ERROR: {str(e)}", flush=True)
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    return "Luna is Online", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
