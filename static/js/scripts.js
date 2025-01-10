// Fetch past conversations from the server
function fetchConversations() {
    fetch('/conversations')
        .then(response => response.json())
        .then(data => {
            const conversationList = document.getElementById('conversation-list');
            conversationList.innerHTML = ''; // Clear existing list
            data.forEach(conversation => {
                const li = document.createElement('li');
                li.textContent = conversation.title; // Use a title or snippet
                li.addEventListener('click', () => loadConversation(conversation.id));
                conversationList.appendChild(li);
            });
        })
        .catch(error => console.error('Error fetching conversations:', error));
}

// Load a specific conversation
function loadConversation(conversationId) {
    fetch(`/conversation/${conversationId}`)
        .then(response => response.json())
        .then(data => {
            // Display the conversation in the chat box
            const chatBox = document.getElementById('chat-box');
            chatBox.innerHTML = ''; // Clear existing chat
            data.messages.forEach(message => {
                const messageElement = document.createElement('div');
                messageElement.classList.add('message', message.role === 'user' ? 'user-message' : 'bot-message');
                messageElement.textContent = message.content;
                chatBox.appendChild(messageElement);
            });
            chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
        })
        .catch(error => console.error('Error loading conversation:', error));
}

// Start a new conversation
document.getElementById('new-chat-button').addEventListener('click', () => {
    fetch('/new_chat', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            // Clear the chat box
            document.getElementById('chat-box').innerHTML = '';
            // Refresh the conversation list
            fetchConversations();
        })
        .catch(error => console.error('Error starting new chat:', error));
});

// Send a new message
document.getElementById('send-button').addEventListener('click', sendMessage);
document.getElementById('prompt-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const promptInput = document.getElementById('prompt-input');
    const prompt = promptInput.value.trim();

    if (prompt) {
        // Display the user's message
        const chatBox = document.getElementById('chat-box');
        const userMessage = document.createElement('div');
        userMessage.classList.add('message', 'user-message');
        userMessage.textContent = prompt;
        chatBox.appendChild(userMessage);

        // Clear the input
        promptInput.value = '';

        // Send the prompt to the server
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: prompt }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(`Error: ${data.error}`);
            } else {
                // Display the bot's response
                const botMessage = document.createElement('div');
                botMessage.classList.add('message', 'bot-message');
                botMessage.textContent = data.response;
                chatBox.appendChild(botMessage);

                // Scroll to the bottom of the chat box
                chatBox.scrollTop = chatBox.scrollHeight;

                // Refresh the conversation list
                fetchConversations();
            }
        })
        .catch(error => {
            console.error('Error sending message:', error);
        });
    }
}

// Fetch conversations when the page loads
document.addEventListener('DOMContentLoaded', fetchConversations);
