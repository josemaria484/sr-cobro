from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = "123456"

ACCESS_TOKEN = "EAAUhwwsAtrYBRfXQCIjOmLDmS9zsi9e3aQTYokZCWjeTFZCWWXi6Dw3fUKw4xjAKUrsNswCpuQnjymgFZC56pw0bVfVcCU9G42x7zK2SZBdCn9ql6clGu9fRrZCPdyoOZB2WD4lchuLiN8FNqWcVaEC1MEfLU5WiuMB3obGl0y1FQ95P5kHdMTDL7QHf9SmjAAERm619FGtKZC22y5QHZAZBlc5NqyW4zzFZCkZCy62hvlih7hKZBekZCaNXEoWQf9n8ueNDbIEtetZAZAoznkuzDZBbNfwZD"
PHONE_NUMBER_ID = "991030984102226"

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

        print("DEBUG:", mode, token, challenge)

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        return "ERROR", 403

    if request.method == "POST":
        data = request.json
        print("Mensaje recibido:", data)

        try:
            value = data["entry"][0]["changes"][0]["value"]
            if "messages" in value:
                msg = value["messages"][0]
                sender = msg["from"]
                text = msg.get("text", {}).get("body", "").lower().strip()

                if text == "hola":
                    enviar_whatsapp(sender, "Hola, soy Sr Cobro. Bot conectado correctamente.")
                else:
                    enviar_whatsapp(sender, "Mensaje recibido por Sr Cobro.")
        except Exception as e:
            print("ERROR PROCESANDO:", e)

        return "OK", 200

@app.route("/status")
def status():
    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000)
