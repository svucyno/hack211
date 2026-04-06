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

# Save contact
def save_contact(name, phone):
    contacts = load_contacts()
    contacts.append({"name": name, "phone": phone})
    with open("contacts.json", "w") as f:
        json.dump(contacts, f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_contact', methods=['POST'])
def add_contact():
    name = request.form['name']
    phone = request.form['phone']
    save_contact(name, phone)
    return render_template('index.html', message="Contact Added!")

@app.route('/predict', methods=['POST'])
def predict():
    heart_rate = int(request.form['heart_rate'])
    bp = int(request.form['bp'])
    oxygen = int(request.form['oxygen'])

    # 📍 Get location
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    result = predict_risk(heart_rate, bp, oxygen)

    alert_msg = ""

    if result == "High Risk":
        contacts = load_contacts()

        location_link = f"https://www.google.com/maps?q={latitude},{longitude}"

        for contact in contacts:
            try:
                client.messages.create(
                    body=f"🚨 Emergency! Health risk detected.\nLocation: {location_link}",
                    from_=twilio_number,
                    to=contact["phone"]
                )
            except Exception as e:
                print("SMS Error:", e)

        alert_msg = f"🚨 Alert sent to {len(contacts)} contacts!"

    return render_template(
        'index.html',
        prediction=result,
        alert=alert_msg,
        hr=heart_rate,
        bp=bp,
        ox=oxygen
    )

if __name__ == "__main__":
    app.run(debug=True)