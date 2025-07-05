
import requests
import os

def send_telegram_message(text, token, chat_id):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    response = requests.post(url, data=data)
    response.raise_for_status()
