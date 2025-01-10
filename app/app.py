from flask import Flask, request, jsonify
from interpreter import interpreter
import logging
import os

# Initialize Flask application
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Interpreter configuration
def configure_interpreter():
    settings = {
        'offline': True,
        'llm': {
            'model': "gpt-3.5-turbo",
            'temperature': 0.7,
            'context_window': 16000,
            'max_tokens': 100,
            'max_output': 1000,
            'api_base': "https://api.example.com",
            'api_key': os.getenv("INTERPRETER_API_KEY", "your_api_key_here"),
            'api_version': "2.0.2",
            'supports_functions': True,
            'supports_vision': True,
            'execution_instructions': (
                "To execute code on the user's machine, write a markdown code block. "
                "Specify the language after the ```. You will receive the output. Use any programming language."
            )
        },
        'system_message': "You are Open Interpreter...",
        'custom_instructions': "This is a custom instruction.",
        'verbose': True,
        'safe_mode': 'ask',
        'auto_run': True,
        'max_budget': 0.01,
        'anonymized_telemetry': False  # Disable telemetry
    }
    
    for key, value in settings.items():
        if key == 'llm':
            for llm_key, llm_value in value.items():
                setattr(interpreter.llm, llm_key, llm_value)
        else:
            setattr(interpreter, key, value)

configure_interpreter()

# Create an endpoint for chat
@app.route('/chat', methods=['POST'])
def chat():
    """
    Endpoint for handling chat requests.
    Expects a JSON payload with a 'prompt' key.
    """
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            logger.warning("Invalid request: No 'prompt' provided.")
            return jsonify({"error": "Invalid request. Please provide a 'prompt'."}), 400
        
        prompt = data['prompt']
        if not isinstance(prompt, str):
            logger.warning("Invalid 'prompt' type. Expected string.")
            return jsonify({"error": "Invalid 'prompt' type. Expected string."}), 400
        
        if len(prompt) > 10000:
            logger.warning("Prompt too long. Maximum allowed length is 10000 characters.")
            return jsonify({"error": "Prompt too long. Maximum allowed length is 10000 characters."}), 400
        
        logger.info(f"Processing prompt: {prompt}")
        full_response = ""
        
        for chunk in interpreter.chat(prompt, stream=True, display=False):
            if isinstance(chunk, dict):
                if chunk.get("type") == "message":
                    full_response += chunk.get("content", "")
                elif chunk.get("type") == "code":
                    full_response += f"```\n{chunk.get('content', '')}\n```"
            elif isinstance(chunk, str):
                full_response += chunk
            else:
                logger.warning(f"Unexpected chunk type: {type(chunk)}")
        
        logger.info("Response generated successfully.")
        return jsonify({"response": full_response.strip()})
    
    except json.JSONDecodeError as e:
        logger.warning(f"Invalid JSON payload: {str(e)}")
        return jsonify({"error": "Invalid JSON payload."}), 400
    except Exception as e:
        logger.error(f"Error during chat processing: {str(e)}")
        return jsonify({"error": "Internal server error."}), 500

if __name__ == '__main__':
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    logger.info(f"Open Interpreter server is running on http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
