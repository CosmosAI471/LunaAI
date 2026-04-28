from flask import Flask, request, jsonify
from flask_cors import CORS
from gradio_client import Client
import threading
import time
import os

app = Flask(__name__)
# This allows your GitHub Pages frontend to talk to your Render backend
CORS(app) 

# We pull the Space ID from Render's Environment Variables (100% hidden from hackers)
HF_SPACE = os.environ.get("HF_SPACE_ID", "cosmosai471/come_onnn")
try:
    hf_client = Client(HF_SPACE)
except Exception as e:
    print(f"Failed to connect to HF: {e}")

def keep_hf_awake():
    """Background task to ping Hugging Face every 60 seconds."""
    while True:
        try:
            # We send a silent, hidden prompt to keep the instance warm
            hf_client.predict("/chat_generator", ["keep_alive", None, [{"role":"user", "content":"keep_alive"}], False, False])
            print("Successfully pinged Hugging Face.")
        except Exception as e:
            print(f"Ping failed: {e}")
        time.sleep(60)

# Start the keep-awake loop the moment the server boots
threading.Thread(target=keep_hf_awake, daemon=True).start()

@app.route('/chat', methods=['POST'])
def chat():
    """Receives message from your frontend, passes it to HF securely."""
    data = request.json
    user_text = data.get("text")
    
    if not user_text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # Call Gradio. We do this synchronously here to keep the API stable.
        result = hf_client.predict("/chat_generator", [user_text, None, [{"role":"user", "content":user_text}], False, False])
        
        # Extract the AI's response from the Gradio output format
        if isinstance(result, tuple) or isinstance(result, list):
            history = result[0]
            ai_response = history[-1]['content']
        else:
            ai_response = str(result)

        return jsonify({"response": ai_response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """A simple endpoint to prove Render is awake."""
    return "Luna Backend is running securely.", 200

if __name__ == '__main__':
    # Required for Render hosting
    app.run(host='0.0.0.0', port=10000)
