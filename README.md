# Open Interpreter Chat App

A simple web-based chat application powered by Open Interpreter. This app allows users to interact with an AI interpreter, save conversations, and start new chats. It features a clean UI with a sidebar for managing past conversations.

---

## Features

- **Chat with Open Interpreter**: Send prompts and receive responses from the AI interpreter.
- **Conversation Management**: 
  - Save all prompts and responses as part of a conversation.
  - Start a new conversation with the "New Chat" button.
- **Sidebar**: View and switch between past conversations.
- **Formatted Output**: Clean and readable responses from the AI interpreter.

---

## Prerequisites

Before running the app, ensure you have the following installed:

- Python 3.7 or higher
- Flask (`pip install flask`)
- Open Interpreter (`pip install open-interpreter`)

---

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/projectOne.git
   cd projectOne
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask server**:
   ```bash
   python app.py
   ```

4. **Access the app**:
   Open your browser and navigate to `http://localhost:5000`.

---

## Project Structure

```
projectOne/
├── app.py                # Main server script
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates
│   └── index.html        # Main UI template
├── static/               # Static files (CSS, JS)
│   ├── css/
│   │   └── styles.css    # Styles for the UI
│   └── js/
│       └── scripts.js    # JavaScript for interactivity
├── docs/                 # Documentation
│   └── README.md         # This file
└── tests/                # Unit tests (optional)
    └── test_app.py
```

---

## Usage

1. **Start a New Chat**:
   - Click the "New Chat" button in the sidebar to start a new conversation.

2. **Send a Prompt**:
   - Type your message in the input box and press "Enter" or click "Send".

3. **View Past Conversations**:
   - Click on a conversation in the sidebar to load it.

4. **Switch Conversations**:
   - Use the sidebar to switch between different conversations.

---

## Configuration

The app uses the following environment variables:

- `FLASK_PORT`: Port to run the Flask server (default: `5000`).
- `FLASK_DEBUG`: Set to `True` to enable debug mode (default: `False`).

Example:
```bash
export FLASK_PORT=5000
export FLASK_DEBUG=True
```

---

## Customizing the Interpreter

You can modify the interpreter settings in `app.py` under the `configure_interpreter` function. For example:

```python
interpreter.llm.model = "sin"
interpreter.llm.temperature = 0.7
interpreter.llm.api_key = "your-api-key"
```

---

## Contributing

Contributions are welcome! If you'd like to improve this project, please:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/).
- Powered by [Open Interpreter](https://github.com/KillianLucas/open-interpreter).

---

Enjoy chatting with Open Interpreter! 🚀
