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
   import random

def get_brent_price():
    """
    Simulazione logica intraday (2 ore)
    Versione base senza API reali
    """

    # Simulazione dati (poi li sostituiremo con dati reali)
    trend = random.choice(["rialzista", "ribassista", "neutrale"])
    rsi = random.randint(30, 70)
    volatilita = random.choice(["bassa", "media", "alta"])

    risposta = "📊 Analisi petrolio (2H)\n\n"

    risposta += f"Trend breve: {trend}\n"
    risposta += f"RSI: {rsi}\n"
    risposta += f"Volatilità: {volatilita}\n\n"

    # Logica decisionale
    if trend == "rialzista" and 40 < rsi < 65 and volatilita != "alta":
        risposta += "🟢 POSSIBILE LONG (compra)\n"
        risposta += "👉 Solo se il prezzo conferma il movimento\n"
        risposta += "⚠️ Rischio: medio"
    elif trend == "ribassista" and 35 < rsi < 60 and volatilita != "alta":
        risposta += "🔴 POSSIBILE SHORT (vendi)\n"
        risposta += "👉 Solo su conferma\n"
        risposta += "⚠️ Rischio: medio"
    else:
        risposta += "⛔ NESSUNA OPERAZIONE\n"
        risposta += "👉 Mercato instabile o senza vantaggio"

    return risposta


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
