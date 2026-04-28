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
    
    if not user_text:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Connect to the AI
        print(f"Connecting to {HF_SPACE}...", flush=True)
        client = Client(HF_SPACE)
        
        # EXACT parameters from your Gradio docs:
        # 1. message_from_input (str)
        # 2. history (list)
        result = client.predict(
            message_from_input=user_text,
            history=[], 
            api_name="/chat_generator"
        )
        
        # Your docs say it returns a tuple of 6 elements. 
        # Element [0] is the history list.
        if isinstance(result, (list, tuple)) and len(result) > 0:
            chat_history = result[0]
            # The last message in history is Luna's response
            if len(chat_history) > 0:
                ai_response = chat_history[-1]['content']
                return jsonify({"response": ai_response})
        
        return jsonify({"response": "Luna didn't return a text response."})

    except Exception as e:
        # This will now definitely show up in Render Logs
        print(f"!!! BACKEND ERROR: {str(e)}", flush=True) 
        return jsonify({"error": str(e)}), 503

@app.route('/health')
def health():
    return "Backend is Live", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
