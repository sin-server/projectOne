from flask import Flask, request, jsonify
from interpreter import interpreter
import logging
import json
import os

# Initialize Flask application
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Interpreter configuration
interpreter.offline = True  # Offline mode enabled
interpreter.llm.model = "gpt-3.5-turbo"
interpreter.llm.temperature = 0.7
interpreter.llm.context_window = 16000
interpreter.llm.max_tokens = 100
interpreter.llm.max_output = 1000
interpreter.llm.api_base = "https://api.example.com"
interpreter.llm.api_key = "your_api_key_here"
interpreter.llm.api_version = "2.0.2"
interpreter.llm.supports_functions = True
interpreter.llm.supports_vision = True
interpreter.system_message = "You are Open Interpreter..."
interpreter.custom_instructions = "This is a custom instruction."
interpreter.verbose = True
interpreter.safe_mode = 'ask'
interpreter.auto_run = True
interpreter.max_budget = 0.01
interpreter.anonymized_telemetry = False  # Disable telemetry

# Interpreter execution instructions
interpreter.llm.execution_instructions = (
    "To execute code on the user's machine, write a markdown code block. Specify the language after the ```. You will receive the output. Use any programming language."
)

# Create an endpoint for chat
@app.route('/chat', methods=['POST'])
def chat():
    """
    Endpoint for handling chat requests.
    Expects a JSON payload with a 'prompt' key.
    """
    try:
        data = request.get_json()
    except Exception as e:
        logger.warning(f"Invalid JSON payload: {str(e)}")
        return jsonify({"error": "Invalid JSON payload."}), 400

    if not data or 'prompt' not in data:
        logger.warning("Invalid request: No 'prompt' provided.")
        return jsonify({"error": "Invalid request. Please provide a 'prompt'."}), 400

    prompt = data['prompt']
    full_response = ""

    try:
        logger.info(f"Received prompt: {prompt}")
        for chunk in interpreter.chat(prompt, stream=True, display=False):
            if isinstance(chunk, dict):
                if chunk.get("type") == "message":
                    full_response += chunk.get("content", "")
                elif chunk.get("type") == "code":
                    full_response += f"```
{chunk.get('content', '')}
```
"
            elif isinstance(chunk, str):
                full_response += chunk
            else:
                logger.warning(f"Unexpected chunk type: {type(chunk)}")
    except Exception as e:
        logger.error(f"Error during chat processing: {str(e)}")
        return jsonify({"error": str(e)}), 500

    logger.info("Response generated successfully.")
    return jsonify({"response": full_response.strip()})

if __name__ == '__main__':
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    logger.info(f"Open Interpreter server is running on http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=debug)