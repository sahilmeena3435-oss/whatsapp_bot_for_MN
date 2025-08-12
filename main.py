from flask import Flask, request
import requests

app = Flask(__name__)

# Hardcoded values (NOT recommended for production)
ACCESS_TOKEN = "EAA6ijAIaH6MBPDGRiR4Ju3KG5O1YIj2Wb0sRPk0BLvE57NnQhe6y07x8MxJN35tuNuBgMwf5E9dHOJHZALXZBeTMLStAXNowcteTubU0mXNDfOL0hOC2NZBfzCt8rqmVUT7OV9qK5ZBRP8hbt2mJcS2APZBekWP2k0Vqeq522bI9QwdcchKvv1M15HBD9zuraFViZBoWyV8OEofdoan3kw90Hqb2nfhOsZCH4nM6CcwGHttK4QZD"
PHONE_NUMBER_ID = "764448353413111"
VERIFY_TOKEN = "testwebhook"  # You can change this to any string, but remember it for Meta verification

# Function to send messages
def send_message(to, text):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    response = requests.post(url, headers=headers, json=data)
    print("Send message response:", response.text)

# Webhook verification (Meta setup)
@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Error", 403

# Handle incoming messages
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Incoming webhook data:", data)  # Debug log
    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        from_number = message["from"]
        text = message["text"]["body"]
        send_message(from_number, f"You said: {text}")
    except Exception as e:
        print("Error:", e)
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
