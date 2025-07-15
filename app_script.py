import requests
from dotenv import load_dotenv
from pyrogram import Client, filters
import os
load_dotenv()
FILE_CHANNEL_ID = int(os.getenv("FILE_CHANNEL_ID",-1002739721923))
user_status = {}
admin_app_details = {}
SEARCH_URL = "https://sainipankaj12.serv00.net/App/Pre/get.php?query="
admins = {6150091802: "Owner", 5943119285: "Admin"}  # Example Admin Dictionary


def send_telegram_message(chat_id, text, bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    return response.json()
