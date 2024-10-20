from flask import Flask, request
import africastalking
import requests
import os

AFRICASTALKING_API_KEY = "f9adeb64e252e6ab6ad32cfb36d68e924d6174baada05e58e37ce79aa7ac68d5"
STROLID_API_URL = "https://api.strolid.com/your-endpoint" # Here is where is my strolid credentials
STROLID_API_KEY = "your_strolid_api_key" 

app = Flask(__name__)
username = "sandbox"
api_key = AFRICASTALKING_API_KEY
africastalking.initialize(username, api_key)
sms = africastalking.SMS

def send_SMS(sms_phone_number):
    sms_response = sms.send(
        "Hello, I am your personal assistant. How may I help you?",
        sms_phone_number)

    print(sms_response)

    # Log the SMS details to Strolid
    log_to_strolid(sms_phone_number, sms_response)

def log_to_strolid(phone_number, sms_response):
    payload = {
        "phone_number": phone_number,
        "sms_response": sms_response,
        "message": "Hello, I am your personal assistant. How may I help you?",
    }

    headers = {
        "Authorization": f"Bearer {STROLID_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(STROLID_API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        print("Logged to Strolid successfully:", response.json())
    else:
        print("Failed to log to Strolid:", response.status_code, response.text)

# Example usage
send_SMS("+255694021848")

            

