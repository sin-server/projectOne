from flask import Flask, request, jsonify, render_template
from interpreter import interpreter
import logging
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Conversation, Message, Embedding
import requests
import json

# Initialize Flask application
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup
DATABASE_URL = "sqlite:///sin.db"  # Replace with PostgreSQL URL if using Supabase
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Create tables
Base.metadata.create_all(engine)

# Configure the interpreter
def configure_interpreter():
    interpreter.offline = False
    interpreter.llm.model = "openai/sin"
    interpreter.llm.temperature = 0.7
    interpreter.llm.context_window = 100000
    interpreter.llm.max_tokens = 1000
    interpreter.llm.max_output = 10000
    interpreter.llm.api_base = "https://chat.musicheardworldwide.com/api"
    interpreter.llm.api_key = "sk-715370e4191e460ebb96ad7e3c748cbc"
    interpreter.system_message = "You are Open Interpreter for projectOne..."
    interpreter.verbose = True
    interpreter.auto_run = True

configure_interpreter()

# Embedding API setup
EMBEDDING_API_URL = "https://api.musicheardworldwide.com/embeddings"

def get_embedding(prompt):
    payload = {"model": "text", "prompt": prompt}
    response = requests.post(EMBEDDING_API_URL, json=payload)
    if response.status_code == 200:
        return response.json()["embedding"]
    else:
        raise Exception(f"Embedding API error: {response.text}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_chat', methods=['POST'])
def new_chat():
    global current_conversation_id
    if current_conversation_id:
        conversations[current_conversation_id]["end_time"] = datetime.now().strftime('%Y-%m-%d %H:%M')
    conversation = Conversation(
        title=f"Conversation {len(conversations) + 1}",
        start_time=datetime.now()
    )
    session.add(conversation)
    session.commit()
    current_conversation_id = conversation.id
    return jsonify({"conversation_id": current_conversation_id})

@app.route('/chat', methods=['POST'])
def chat():
    global current_conversation_id
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        if not current_conversation_id:
            new_chat()

        user_embedding = get_embedding(prompt)
        response = interpreter.chat(prompt)
        bot_embedding = get_embedding(response)

        conversation = session.query(Conversation).get(current_conversation_id)
        user_message = Message(conversation=conversation, role='user', content=prompt)
        bot_message = Message(conversation=conversation, role='bot', content=response)
        session.add_all([user_message, bot_message])

        session.add_all([
            Embedding(document=prompt, embedding=json.dumps(user_embedding), conversation=conversation),
            Embedding(document=response, embedding=json.dumps(bot_embedding), conversation=conversation)
        ])
        session.commit()

        return jsonify({"response": response, "conversation_id": current_conversation_id})
    except Exception as e:
        logger.error(f"Error during chat: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(host='0.0.0.0', port=port, debug=debug)
