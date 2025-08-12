from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Your WhatsApp Cloud API credentials
VERIFY_TOKEN = "my_wp_bot_token"
ACCESS_TOKEN = "EAA6ijAIaH6MBPDHX2CeXlQle870wZC21ZCvZCzx5xuwOMPZAAjb8mIuGYjsnH8W5ZAZBZAK1HDXJxmhYqZCZCPWZCZChNrJsQP1o1it2LqZAEipZCMFudXz9EM1vfqj1vnqVyK4UlbgAejTDrJZBzWTk7ZBpHWlbqyeZBtrjaw1r6pVy9hVk2yYMqgobDPlkp2qZBn9b2ofktZBONtO3facl3ZC2pB2eg91mSM9ymT9Ryl1ow0KUVP7ZAdLqegZDZD"
PHONE_NUMBER_ID = "764448353413111"

# Webhook verification (GET request)
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("✅ Webhook verified successfully!")
            return challenge, 200
        else:
            return "❌ Verification token mismatch", 403
    return "❌ No mode/token found", 400

# Handle incoming messages (POST request)
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📩 Incoming data:", data)

    try:
        # Navigate JSON to get sender & message text
        entry = data["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        messages = value.get("messages", [])

        if messages:
            message = messages[0]
            sender_id = message["from"]
            msg_text = message.get("text", {}).get("body", "")

            # Send an auto-reply
            reply_text = f"Hi! You said: {msg_text}"
            send_whatsapp_message(sender_id, reply_text)

    except Exception as e:
        print("⚠ Error processing message:", e)

    return "EVENT_RECEIVED", 200

# Function to send WhatsApp messages via Cloud API
def send_whatsapp_message(to, text):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    response = requests.post(url, headers=headers, json=payload)
    print("📤 Reply sent:", response.status_code, response.text)
    return response

if __name__ == "__main__":
    # Local run
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
