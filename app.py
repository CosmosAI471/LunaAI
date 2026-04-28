import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from gradio_client import Client

app = Flask(__name__)
CORS(app) # Allows your GitHub Pages to talk to this server

# The Hugging Face Space you want to protect
HF_SPACE = os.environ.get("HF_SPACE_ID", "cosmosai471/come_onnn")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_text = data.get("text")
    
    if not user_text:
        return jsonify({"error": "No message provided"}), 400

    try:
        # We initialize the client inside the request to handle wake-ups better
        client = Client(HF_SPACE)
        
        # This matches the specific way your 'come_onnn' space works
        result = client.predict(
            user_text,    # The message
            None,         # System prompt (None = default)
            [],           # Chat history (Empty = new chat)
            False,        # Parameter 1
            False,        # Parameter 2
            api_name="/chat_generator"
        )
        
        # Extract the AI's response from the Gradio history list
        if isinstance(result, (list, tuple)) and len(result) > 0:
            history = result[0]
            ai_response = history[-1]['content']
            return jsonify({"response": ai_response})
        
        return jsonify({"response": str(result)})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Luna is waking up or busy. Please try again in 10 seconds."}), 503

@app.route('/health')
def health():
    return "Backend is Live", 200

if __name__ == "__main__":
    # Render binds to the PORT environment variable automatically
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
