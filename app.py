from flask import Flask, render_template, request
from model import predict_risk
import json
from twilio.rest import Client

app = Flask(__name__)

# 🔑 ADD YOUR TWILIO DETAILS
account_sid = "AC5c45bac3dd0b3e452066fc1d35eb9c8c"
auth_token = "3b3e33d5ab930a4a7cac6e55811b702e"
twilio_number = "+16812844328"

client = Client(account_sid, auth_token)

# Load contacts
def load_contacts():
    try:
        with open("contacts.json", "r") as f:
            return json.load(f)
    except:
        return []
