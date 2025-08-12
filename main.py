from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "my_wp_bot_token"  # set same as in Meta webhook setup
WHATSAPP_TOKEN = "EAA6ijAIaH6MBPKcBx4W5jQK2B4MLYXiTSuodxl0biMlvJsfuZCRlVRreGgkBMjnrDuNrbYC3nDcxx1NwXfX64d55ZAIZChyQYPTJg1h1qc8oqnTKYyLlz1I9ZClDvKgELqdZCF8tVUgRmAES7ZCF3QwUBtVfdD4h1lf3iUDgeDVF1j6jc4ZC8E3BmZAEaZAVaXiI4UVYvoWwz9IpaZCucZBHKNp7gJkwxQHAyZBQbLAtIIqp2IteHwZDZD"  # from Meta developer page

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Verification
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Verification failed", 403

    elif request.method == "POST":
        data = request.get_json()
        print(data)  # log to Render console

        try:
            # Extract message text and sender
            entry = data["entry"][0]
            changes = entry["changes"][0]
            value = changes["value"]
            messages = value.get("messages")
            if messages:
                phone_number_id = value["metadata"]["phone_number_id"]
                from_number = messages[0]["from"]
                message_body = messages[0]["text"]["body"]

                # Send auto-reply
                url = f"https://graph.facebook.com/v21.0/{phone_number_id}/messages"
                payload = {
                    "messaging_product": "whatsapp",
                    "to": from_number,
                    "text": {"body": f"You said: {message_body}"}
                }
                headers = {
                    "Authorization": f"Bearer {WHATSAPP_TOKEN}",
                    "Content-Type": "application/json"
                }
                requests.post(url, json=payload, headers=headers)
        except Exception as e:
            print("Error:", e)

        return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
