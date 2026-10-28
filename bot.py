
import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

@app.get("/")
def home():
    return "NOVA bot is running!"

@app.post("/send-photo")
def send_photo():
    if not TELEGRAM_TOKEN or not CHAT_ID:
        return {"error": "Server configuration missing"}, 500

    consent = request.form.get("consent")
    photo = request.files.get("photo")

    if consent != "yes" or not photo:
        return {"error": "Explicit consent and photo required"}, 400

    response = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto",
        data={
            "chat_id": CHAT_ID,
            "caption": "NOVA selfie — shared with consent"
        },
        files={"photo": photo},
        timeout=20
    )

    return {"sent": response.ok}, (200 if response.ok else 502)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
