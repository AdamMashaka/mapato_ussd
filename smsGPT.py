from flask import Flask, request
import openai
import requests
import traceback
import os

app = Flask(__name__)

# Set your API keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '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')  # Replace with your OpenAI API key
AFRICASTALKING_API_KEY = os.getenv('AFRICASTALKING_API_KEY', 'atsk_ad1374226cbf8177b2374f7375a805f176765eb5542d40cbcf3dd2cf6e69eed9d120a589')  # Replace with your Africa's Talking API key

# Bot's name
bot_name = "SHAMBA BOT"

# Language for the bot
bot_language = "sw"  # Swahili

# Topic for the conversation
conversation_topic = "kilimo cha mahindi, mabadiliko ya hali ya kwenye kilimo, wadudu na magonjwa ya mazao, mbinu bora za kilimo"

# Greeting message in Swahili
greeting = f"{bot_name}: Karibu! Mimi ni {bot_name} nipo kwa ajili ya kukupa taarifa kuhusiana na kilimo, wadudu waharibifu na magonjwa ya mazao Tafadhali niambie unahitaji msaada wa aina gani."

# Function to interact with the bot
def chat_with_bot(bot_name, language, topic, user_message, conversation_history=None):
    # Create system and user messages
    system_message = f"{bot_name}: Karibu! Mimi ni {bot_name}. Nipo kwa ajili ya kukupa taarifa kuhusiana na kilimo, wadudu waharibifu na magonjwa ya mazao. Tafadhali niambie unahitaji msaada wa aina gani."
    user_message = f"User: {user_message}"

    # Combine system and user messages with existing conversation history
    messages = [{"role": "system", "content": system_message}]
    
    if conversation_history:
        messages += conversation_history
    
    messages.append({"role": "user", "content": user_message})

    # Make the API call for chat completion
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=150,
        api_key=OPENAI_API_KEY  # Add OpenAI API Key here
    )

    # Extract and return the assistant's reply
    assistant_reply = response['choices'][0]['message']['content']

    return assistant_reply


@app.route('/')
def smart_shamba():
    return 'Lima Kijanja'

@app.route('/sms_callback', methods=['POST'])  # Revert back to /sms_callback
def sms_callback():
    try:
        user_message = request.form.get("text")
        sender = request.form.get("from")

        # Check for common greetings and respond with the greeting message
        if user_message.lower() in ["habari", "hello", "mambo"]:
            bot_response = greeting
        else:
            # Use the user's SMS message with the bot's name, language, and topic as the prompt
            bot_response = chat_with_bot(
                bot_name, bot_language, conversation_topic, user_message)

        # Send the bot response to the user via Africa's Talking SMS API
        response_to_sms(sender, bot_response)

        return "Success", 201

    except Exception as e:
        # Log the error
        traceback.print_exc()
        return "Internal Server Error", 500

def response_to_sms(recipient_phone_number, message):
    url = "https://api.sandbox.africastalking.com/version1/messaging"
    data = {
        "username": "sandbox",
        "to": recipient_phone_number,  # Use the recipient_phone_number from the callback
        "message": message,
        "from": "45407"
    }
    headers = {
        "apikey": AFRICASTALKING_API_KEY,  # Add Africa's Talking API Key here
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(url, data=data, headers=headers)
        print(f"API Request: {data}")
        print(f"API Response: {response.text}")

        # Check if the SMS was sent successfully
        if response.status_code != 201:
            raise Exception(f"Failed to send SMS. Status code: {response.status_code}")

    except Exception as e:
        print(f"Failed to send SMS: {str(e)}")
        raise Exception(f"Failed to send SMS: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)

