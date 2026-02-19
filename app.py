from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Create the Flask application
app = Flask(__name__)

# Initialize the chatbot
chatbot = ChatBot(
    "StudentBot",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database_uri="sqlite:///chatbot_database.sqlite3",
)

# Train the chatbot with English conversations
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")

# Custom training for school-related topics
from chatterbot.trainers import ListTrainer

list_trainer = ListTrainer(chatbot)

# Train on school-related conversations
list_trainer.train(
    [
        "What subjects do you like?",
        "I find all subjects interesting, but I really enjoy helping with coding!",
        "Can you help with homework?",
        "I can try to help explain concepts, but you should do it yourself!",
        "Who made you?",
        "I was created by a talented Year 9 student at Tempe High School!",
    ]
)

# Train on greetings
list_trainer.train(
    [
        "Good morning!",
        "Good morning! How can I help you today?",
        "Good afternoon!",
        "Good afternoon! What would you like to chat about?",
    ]
)

# Train on math
list_trainer.train(
    [
        "What is 1+1!",
        "2",
        "What is 2+2!",
        "4",
        "What is 1+2!",
        "3",
        "What is 2+1!",
        "3",
        "What is 2+3!",
        "5",
        "What is 3+2!",
        "5",
        "What is 3+3!",
        "6",
        "What is 3+1!",
        "4",
    ]
)


@app.route("/")
def home():
    """Serve the main chat page."""
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """Handle chat messages and return bot responses."""
    # Get the message from the request
    data = request.get_json()
    user_message = data.get("message", "")

    # Basic input validation
    if not user_message:
        return jsonify({"response": "Please enter a message!"})

    if len(user_message) > 500:
        return jsonify(
            {"response": "Message too long! Please keep it under 500 characters."}
        )

    # Get the chatbot's response
    bot_response = chatbot.get_response(user_message)

    return jsonify({"response": str(bot_response)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
