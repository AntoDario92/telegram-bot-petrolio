import os
import requests
from flask import Flask, request

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("Manca la variabile TELEGRAM_BOT_TOKEN")

TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"
app = Flask(__name__)


def send_message(chat_id, text):
    url = f"{TELEGRAM_API}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=data, timeout=20)


def get_brent_price():
    """
    Placeholder semplice.
    Per ora restituisce un messaggio fisso.
    Più avanti lo colleghiamo a un prezzo reale.
    """
    return "Prezzo petrolio: funzione in preparazione."


@app.route("/", methods=["GET"])
def home():
    return "Bot attivo!", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True)
    if not data:
        return "ok", 200

    message = data.get("message", {})
    chat = message.get("chat", {})
    text = message.get("text", "")
    chat_id = chat.get("id")

    if not chat_id:
        return "ok", 200

    text = text.strip()

    if text == "/start":
        send_message(
            chat_id,
            "Ciao! Sono il tuo bot petrolio.\n\nComandi disponibili:\n/start\n/help\n/petrolio"
        )
    elif text == "/help":
        send_message(
            chat_id,
            "Usa:\n/petrolio - stato del petrolio\n/help - aiuto"
        )
    elif text == "/petrolio":
        send_message(chat_id, get_brent_price())
    else:
        send_message(chat_id, "Comando non riconosciuto. Usa /help")

    return "ok", 200
