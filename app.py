from flask import Flask, request, jsonify, render_template
from interpreter import interpreter
import logging
import os
from datetime import datetime

# Initialize Flask application
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure the interpreter
def configure_interpreter():
    """Configure the interpreter settings."""
    interpreter.offline = True  # Offline mode enabled
    interpreter.llm.model = "openai/sin"
    interpreter.llm.temperature = 0.7
    interpreter.llm.context_window = 100000
    interpreter.llm.max_tokens = 1000
    interpreter.llm.max_output = 10000
    interpreter.llm.api_base = "https://chat.musicheardworldwide.com/api"
    interpreter.llm.api_key = "sk-715370e4191e460ebb96ad7e3c748cbc"
    interpreter.llm.api_version = "2.0.2"
    interpreter.llm.supports_functions = True
    interpreter.llm.supports_vision = False
    interpreter.system_message = "You are Open Interpreter..."
    interpreter.custom_instructions = "This is a custom instruction."
    interpreter.verbose = True
    interpreter.safe_mode = 'ask'
    interpreter.auto_run = True
    interpreter.anonymized_telemetry = False  # Disable telemetry

    # Interpreter execution instructions
    interpreter.llm.execution_instructions = (
        "To execute code on the user's machine, write a markdown code block. "
        "Specify the language after the ```. You will receive the output. Use any programming language."
    )

# Configure the interpreter on startup
configure_interpreter()

# In-memory storage for conversations (replace with a database for persistence)
conversations = {}
current_conversation_id = None  # Tracks the active conversation

@app.route('/')
def index():
    """Serve the chat interface."""
    return render_template('index.html')

@app.route('/conversations', methods=['GET'])
def get_conversations():
    """Return a list of past conversations."""
    return jsonify([{"id": id, "title": conv["title"]} for id, conv in conversations.items()])

@app.route('/conversation/<conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    """Return a specific conversation by ID."""
    if conversation_id in conversations:
        return jsonify(conversations[conversation_id])
    else:
        return jsonify({"error": "Conversation not found"}), 404

@app.route('/new_chat', methods=['POST'])
def new_chat():
    """Start a new conversation."""
    global current_conversation_id
    if current_conversation_id:
        # Save the current conversation before starting a new one
        conversations[current_conversation_id]["end_time"] = datetime.now().strftime('%Y-%m-%d %H:%M')
    current_conversation_id = str(len(conversations) + 1)
    conversations[current_conversation_id] = {
        "title": f"Conversation {current_conversation_id} - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "start_time": datetime.now().strftime('%Y-%m-%d %H:%M'),
        "messages": []
    }
    return jsonify({"conversation_id": current_conversation_id})

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests and store messages in the current conversation."""
    global current_conversation_id
    try:
        data = request.get_json()
        prompt = data.get('prompt')

        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        # If no conversation exists, start a new one
        if not current_conversation_id:
            new_chat()

        # Process the prompt using the interpreter
        full_response = ""
        for chunk in interpreter.chat(prompt, stream=True, display=False):
            if isinstance(chunk, dict):
                if chunk.get("type") == "message":
                    full_response += chunk.get("content", "")
                elif chunk.get("type") == "code":
                    full_response += f"```\n{chunk.get('content', '')}\n```\n"
            elif isinstance(chunk, str):
                full_response += chunk
            else:
                logger.warning(f"Unexpected chunk type: {type(chunk)}")

        # Clean up the response (remove unnecessary backticks)
        full_response = full_response.replace("``` ``` ```", "```").replace("``` ```", "```")

        # Store the prompt and response in the current conversation
        conversations[current_conversation_id]["messages"].append(
            {"role": "user", "content": prompt}
        )
        conversations[current_conversation_id]["messages"].append(
            {"role": "bot", "content": full_response.strip()}
        )

        return jsonify({"response": full_response.strip(), "conversation_id": current_conversation_id})

    except Exception as e:
        logger.error(f"Error during chat processing: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    logger.info(f"Open Interpreter server is running on http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
