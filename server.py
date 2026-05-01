from flask import Flask, request
import requests
import os
import json
from app import procesar

app = Flask(__name__)

VERIFY_TOKEN = "123456"
ACCESS_TOKEN = os.getenv("WA_TOKEN")
PHONE_NUMBER_ID = "1047050545162823"

def enviar_whatsapp(to, text):
    url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"
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

    r = requests.post(url, headers=headers, json=payload)
    print("RESPUESTA META:", r.status_code, r.text)

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        return "ERROR", 403

    data = request.json
    print("DATA:", json.dumps(data, indent=2))

    try:
        value = data["entry"][0]["changes"][0]["value"]

        if "messages" in value:
            msg = value["messages"][0]
            sender = msg["from"]
            texto = msg["text"]["body"]

            respuesta = procesar(texto)
            enviar_whatsapp(sender, respuesta)

    except Exception as e:
        print("ERROR:", e)

    return "OK", 200

@app.route("/status")
def status():
    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000)
