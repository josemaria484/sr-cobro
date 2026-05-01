from flask import Flask, request, jsonify
import app

app_flask = Flask(__name__)

@app_flask.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    print("[DEBUG] mensaje entrante:", data)

    # Simulación simple (después lo adaptamos a WhatsApp real)
    mensaje = data.get("text", "")
    numero = data.get("from", "")

    if not mensaje:
        return jsonify({"error": "sin mensaje"}), 400

    respuesta = app.procesar_mensaje(mensaje)

    print("[DEBUG] respuesta:", respuesta)

    return jsonify({
        "reply": respuesta
    })

@app_flask.route("/status", methods=["GET"])
def status():
    return "OK", 200

if __name__ == "__main__":
    app_flask.run(host="0.0.0.0", port=5000, debug=True)
