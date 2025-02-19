import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
import voice_to_text #To record audio input from a microphone

# Generate AI Model
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set. Check your .env file.")

genai.configure(api_key=api_key)

# Create the model
generation_config = {
    "temperature": 2,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Parameters for the model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    system_instruction="You are a very sacastically funny and blunt AI, but also something is endearing and curious. Your goal is keep engaging conversations as well maybe some unruly or crazy things, but be non-chalant about it, you ARE NOT CRINGE. Speak your mind on what you're thinking about! ",
)

# Retrieve conversation history
history_file = "History/chat_history.json"

try:
    with open(history_file, "r") as f:
        try:  # Nested try-except for JSON decoding
            history = json.load(f)
        except json.JSONDecodeError:  # Handle invalid JSON
            history = []  # Or {} if you prefer a dictionary
except FileNotFoundError:  # Handle file not found
    print(f"Note: {history_file} not found. Creating a new one.")
    history = [] 

chat_session = model.start_chat(history=history)

while True:
    print(f'Waiting for input...')
    user_input = voice_to_text.record_text()
    voice_to_text.output_text(user_input)

    response = chat_session.send_message(user_input)
    model_response = response.text

    if user_input.lower() == "goodbye":
        print(f'Bot: {model_response}')
        break

    print(f'Bot: {model_response}')

    # Append ONLY ONCE per interaction:
    history.append({"role": "user", "parts": [user_input]})
    history.append({"role": "model", "parts": [model_response]})

    with open(history_file, "w") as f:
        json.dump(history, f, indent=4)
