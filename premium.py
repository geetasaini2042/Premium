"""
JAY SHREE RAM
"""
"""
FUNCTIONS Here 
#search_and_send_inline,search_and_send_app,send_document
"""
##Imports
import app_admin
import requests
import json
import sys
import time
import os
##Imports#From Pyrogran 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton,Message,InputMediaPhoto, CallbackQuery,WebAppInfo
from pyrogram import Client, filters
from filters.status_filters import StatusFilter,NoStatusFilter
from common_data  import BOT_TOKEN,APP_DATA_FILE
from app_script import SEARCH_URL,send_telegram_message,FILE_CHANNEL_ID
from script import app,flask_app,upload_users
import logging
temp_data = {}
saveii = {}
from threading import Lock



# Lock for file safety
file_lock = Lock()
#Main Functions Started
from flask import Flask, request, jsonify
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import re
CHECK_CHANNEL_ID = int(os.getenv("CHECK_CHANNEL_ID", "-1002536426442"))
from urllib.parse import quote
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
def clean_file_name(name: str) -> str:
    name = re.sub(r'@\w+', '', name)                  # Remove all @usernames
    name = re.sub(r'(?i)modded by', '', name)         # Remove 'modded by' case-insensitive
    name = re.sub(r'\s+', ' ', name).strip()          # Clean extra spaces
    name = re.sub(r'(?i)Getmodpc', ' ', name).strip()
    return name


@app.on_message(filters.command("start") & filters.regex(r"^/start\s+APK_\w+") & filters.private)
async def handle_start_with_uniq_id(client: Client, message: Message):
    try:
        # Extract uniq_id from message
        param_text = message.text.split(maxsplit=1)[1]
        match = re.match(r"APK_(\w+)", param_text)

        if not match:
            await message.reply("⚠️ Invalid link format. Please use a valid link.")
            return

        uniq_id = match.group(1)

        # 🔍 JSON से file_id और app details निकालें
        try:
            with file_lock:
                with open(APP_DATA_FILE, "r") as f:
                    all_data = json.load(f)
        except Exception as e:
            await message.reply("⚠️ Unable to access data. Please try later.")
            print(f"JSON Read Error: {e}")
            return

        app_item = next((item for item in all_data if item.get("uniq_id") == uniq_id), None)

        if not app_item:
            await message.reply("❌ App not found or expired.")
            return

        file_id = app_item.get("file_id")
        original_file_name = app_item.get("file_name", "Unknown")

        # ✅ Send document to check validity
        try:
            sent_doc = await client.send_document(
                chat_id=CHECK_CHANNEL_ID,
                document=file_id,
                caption="🔍 Validating file..."
            )

            doc = sent_doc.document
            cleaned_file_name = clean_file_name(doc.file_name or original_file_name)
            file_size = round(doc.file_size / (1024 * 1024), 2)
            mime_type = doc.mime_type or "N/A"

        except Exception as e:
            await message.reply("❌ The file link seems to be invalid or expired.")
            print(f"File check failed: {e}")
            return

        # 🧑‍💻 User Info
        user = message.from_user
        user_details = f"""
📥 **New File Accessed!**

👤 **User Details:**
• ID: `{user.id}`
• Name: {user.first_name} {user.last_name or ""}
• Username: @{user.username or 'N/A'}
• Language: {user.language_code or 'N/A'}

📄 **File Info:**
• Name: `{original_file_name}`
• Cleaned: `{cleaned_file_name}`
• Type: `{mime_type}`
• Size: `{file_size} MB`
• File ID: `{file_id}`
""".strip()

        # 🔄 Edit caption in check channel
        try:
            await sent_doc.edit_caption(user_details)
        except Exception as e:
            print("Caption edit failed:", e)

        # 🌐 WebApp button
        encoded_file_name = quote(cleaned_file_name)
        link123 = f"https://geetasaini2042.github.io/17uio/APPS/NewVersion/index.html?file_id={file_id}&uniq_id={uniq_id}&file_size={file_size}&file_name={encoded_file_name}"

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("📲 Get Your App Now", web_app=WebAppInfo(url=link123))]
            ]
        )

        # ✅ Final message to user
        response_text = f"""
✅ **Your file is ready!**

• **App Name:** `{cleaned_file_name}`
• **Size:** `{file_size} MB`
Click the button below to open the app 👇
"""

        await message.reply(response_text, reply_markup=keyboard)

    except Exception as e:
        await message.reply("🚫 An unexpected error occurred. Please try again.")
        print(f"Unexpected error: {e}")
@app.on_message(filters.command("start") & filters.regex(r"^/start\s+ID_\w+") & filters.private)
async def handle_start_with_file_id(client: Client, message: Message):
    try:
        # Extract file_id from parameter
        param_text = message.text.split(maxsplit=1)[1]
        match = re.match(r"ID_(\w+)", param_text)

        if not match:
            await message.reply("⚠️ Invalid link format. Please use a valid link.")
            return

        file_id = match.group(1)

        # Try sending file to check validity
        try:
            sent_doc = await client.send_document(
                chat_id=CHECK_CHANNEL_ID,
                document=file_id,
                caption="🔍 Validating file..."
            )

            doc = sent_doc.document
            original_file_name = doc.file_name or "Unknown"
            cleaned_file_name = clean_file_name(original_file_name)
            file_size = round(doc.file_size / (1024 * 1024), 2)  # in MB
            mime_type = doc.mime_type or "N/A"

        except Exception as e:
            await message.reply("❌ The file link seems to be invalid or expired.")
            print(f"File check failed: {e}")
            return

        # User Info
        user = message.from_user
        user_details = f"""
📥 **New File Accessed!**

👤 **User Details:**
• ID: `{user.id}`
• Name: {user.first_name} {user.last_name or ""}
• Username: @{user.username or 'N/A'}
• Language: {user.language_code or 'N/A'}

📄 **File Info:**
• Name: `{original_file_name}`
• Cleaned: `{cleaned_file_name}`
• Type: `{mime_type}`
• Size: `{file_size} MB`
• File ID: `{file_id}`
""".strip()

        # Edit caption in check channel
        try:
            await sent_doc.edit_caption(user_details)
        except Exception as e:
            print("Caption edit failed:", e)

        # WebApp button
        encoded_file_name = quote(cleaned_file_name)
        link123 = f"https://geetasaini2042.github.io/17uio/APPS/NewVersion/index.html?file_id={file_id}&file_size={file_size}&file_name={encoded_file_name}"
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("📲 Get Your App Now", web_app=WebAppInfo(url=link123))]
            ]
        )

        # Message to user
        response_text = f"""
✅ **Your file is ready!**

• **App Name:** `{cleaned_file_name}`
• ** Size: ** `{file_size} MB`
Click the button below to open the app 👇
"""

        await message.reply(
            response_text,
            reply_markup=keyboard
        )

    except Exception as e:
        await message.reply("🚫 An unexpected error occurred. Please try again.")
        print(f"Unexpected error: {e}")
def not_a_command(_, __, message):
    return not message.text.startswith("/")

@app.on_message(
    filters.text
    & ~filters.me
    & ~filters.group
    & ~filters.regex(r"^🚫CANCEL$")
    & filters.create(not_a_command)
    & filters.create(lambda _, __, msg: len(msg.text.strip().encode("utf-8")) <= 55)
    & NoStatusFilter()
)
async def process_text_messages(client: Client, message: Message):
       msg = await message.reply_text("Searching app...")
       user_id = message.from_user.id
       user_msg = message.text
       user_name = message.from_user.first_name
       Search_Query = user_msg
       await search_and_send_inline(msg,Search_Query)
import re

import json
import os
from datetime import datetime
from threading import Lock
from difflib import SequenceMatcher


file_lock = Lock()

def search_apps_from_json(query):
    try:
        with file_lock:
            if not os.path.exists(APP_DATA_FILE):
                print("❌ apps_data.json is not available")
                return []
            with open(APP_DATA_FILE, 'r', encoding='utf-8') as f:
                apps = json.load(f)
    except Exception as e:
        print(f"❌ Error reading JSON file: {e}")
        return []

    query = query.strip().lower()
    if not query:
        print("❌ Provide a search query")
        return []

    exact_matches = []
    substring_matches = []
    fuzzy_matches = []

    query_no_space = query.replace(" ", "")

    for app in apps:
        file_name = app.get("file_name", "").lower()
        file_name_no_space = file_name.replace(" ", "")

        # 1. Exact match (with or without space)
        if file_name == query or file_name_no_space == query_no_space:
            app["match_score"] = 100
            exact_matches.append(app)
            continue

        # 2. Substring match
        if query in file_name or query_no_space in file_name_no_space:
            app["match_score"] = 80
            substring_matches.append(app)
            continue

        # 3. Fuzzy match (similarity > 60%)
        similarity = SequenceMatcher(None, file_name, query).ratio()
        percent = similarity * 100
        if percent > 60:
            app["match_score"] = int(percent)
            fuzzy_matches.append(app)

    # Merge all results
    final_results = exact_matches + substring_matches + fuzzy_matches

    # Sort by timestamp (desc), then match_score (desc)
    def sort_key(app):
        timestamp = app.get("timestamp", "")
        try:
            dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except:
            dt = datetime.min
        return (-dt.timestamp(), -app.get("match_score", 0))

    final_results.sort(key=sort_key)

    # Return top 50
    return final_results[:50]

import requests
import json
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# 📤 Step 1: Send query to GPT-4 via Pollinations API
@app.on_callback_query(filters.regex("^pankaj_"))
async def premiumcall12(client, query: CallbackQuery):
  await premiumcall12345123(client, query)
  

async def premiumcall12345123(client, query):
  if query.data.startswith("pankaj_"):
        _, page, search_query = query.data.split("_")
        page = int(page)
    
        msg = query.message
        await search_and_send_inline(msg, search_query, page, is_ai_provided=True)
        #await search_and_send_inline(msg, search_query, page)  
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def get_ai_queries_with_requests(user_query):
    url = os.getenv("POLLINATIONS_API_URL", "")
    token = os.getenv("POLLINATIONS_API_KEY", "")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "Referer": "https://singodiya.tech/"
    }

    prompt = (
        "You are an intelligent assistant specialized in correcting and understanding app names. "
        "Your task is to help users who provide incorrect, misspelled, or vague app names by identifying "
        "the most likely intended app names.\n\n"
        "For example, if a user types \"youtueb\" or \"snap edit video\", you should intelligently infer "
        "that they probably meant apps like \"YouTube\", \"SnapEdit\", \"CapCut\", or \"YouCut\".\n\n"
        "Your response should be a pure JSON object containing an array of one or more possible corrected or related app names. "
        "Do not include any explanation, formatting, or extra text. Just return the result as a clean JSON object.\n\n"
        "Format:\n{\n  \"queries\": [\"corrected_app_name_1\", \"corrected_app_name_2\", ...]\n}\n\n"
        "Rules:\n"
        "1. Only return app names that actually exist or are commonly used.\n"
        "2. Try to keep the most relevant matches at the top of the list.\n"
        "3. Always respond only in the above JSON format.\n"
        "4. Keep at least 2 app name in json.\n"
        "5. If you are unsure, still try to suggest likely matches based on the words provided.\n"
        "6. Do not include unrelated suggestions or add any commentary or greetings.\n\n"
        "Your job is purely to assist in app search correction in a minimal and machine-readable way."
    )

    payload = {
        "model": "searchgpt",
        "system": prompt,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": user_query}]
            }
        ]
    }

    try:
        res = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        full_json = res.json()

        content = full_json["choices"][0]["message"]["content"]

        return json.loads(content).get("queries", [])

    except Exception as e:
        print("❌ AI Response Error:", e)
        return []
# ⚙️ Step 2: Main function to call from your Pyrogram handler
async def ai_query_send(msg, search_query):
    await msg.edit("🔍 Please wait… AI is searching for your app.")

    ai_queries = get_ai_queries_with_requests(search_query)

    if not ai_queries:
        await msg.edit("❌ AI couldn't suggest anything. Please try another name.")
        return

    # 🧠 Show inline buttons
    buttons = [
        [InlineKeyboardButton(text=q, callback_data=f"pankaj_1_{q}")]
        for q in ai_queries
    ]

    await msg.edit(
        "Based on AI, your search might match one of these apps:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
async def search_and_send_inline(msg, search_query, page=1, is_ai_provided=False):
    user_id = msg.chat.id

    if user_id not in saveii:
        saveii[user_id] = {}

    all_results = search_apps_from_json(search_query)
    keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("REQUEST AN APP", url="https://t.me/mr_singodiyabot")]
            ]
        )
    if not all_results:
      if is_ai_provided:
        await msg.edit("❌ I couldn't find this app. Please try another app.",reply_markup=keyboard)
        return
      else:
        await ai_query_send(msg, search_query)
        return

    saveii[user_id]['page'] = page
    saveii[user_id]['search_query'] = search_query

    results_per_page = 10
    total_pages = (len(all_results) + results_per_page - 1) // results_per_page

    start_idx = (page - 1) * results_per_page
    end_idx = start_idx + results_per_page
    apps = all_results[start_idx:end_idx]

    buttons = []
    row = []

    for app in apps:
        uniq_id = app.get("uniq_id")
        original_file_name = app.get("file_name", "No Name")
        file_name = clean_file_name(original_file_name)
        row.append(InlineKeyboardButton(file_name, callback_data=f"pre_{uniq_id}"))

        if len(row) == 2:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    # Pagination Buttons
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton("⬅ Previous", callback_data=f"page_{page-1}_{search_query}"))
    if total_pages > 1:
        nav_buttons.append(InlineKeyboardButton(f"{page}/{total_pages}", callback_data="premium_apps"))
    if page < total_pages:
        nav_buttons.append(InlineKeyboardButton("Next ➡", callback_data=f"page_{page+1}_{search_query}"))

    if nav_buttons:
        buttons.append(nav_buttons)

    await msg.edit(
        f"**Here is your Search Result For:**\n`{search_query}`",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import re


async def search_and_send_app(client,uniq_id, msg, file_id):
    try:
        # Try sending the document to check if file_id is valid
        try:
            sent_doc = await client.send_document(
                chat_id=CHECK_CHANNEL_ID,
                document=file_id,
                caption="🔍 Validating file..."
            )
            doc = sent_doc.document
            original_file_name = doc.file_name or "Unknown"
            cleaned_file_name = clean_file_name(original_file_name)
            file_size = round(doc.file_size / (1024 * 1024), 2)  # Convert to MB
            mime_type = doc.mime_type or "N/A"
        except Exception as e:
            await msg.edit_text("❌ Invalid or expired file. Please try again later.")
            print(f"File check failed: {e}")
            return

        # Edit the caption in the check channel with full file info
        caption_text = f"""
📥 **App Request Received!**

📄 **File Info:**
• Name: `{original_file_name}`
• Cleaned: `{cleaned_file_name}`
• Type: `{mime_type}`
• Size: `{file_size} MB`
• File ID: `{file_id}`
""".strip()
        try:
            await sent_doc.edit_caption(caption_text)
        except Exception as e:
            print("Caption edit failed:", e)

        # Create WebApp Button
        encoded_file_name = quote(cleaned_file_name)
        link123 = f"https://geetasaini2042.github.io/17uio/APPS/NewVersion/index.html?file_id={file_id}&uniq_id={uniq_id}&file_size={file_size}&file_name={encoded_file_name}"
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("📲 Get Your App Now", web_app=WebAppInfo(url=link123))],
                [InlineKeyboardButton("Create Share Link",callback_data=f"create_link_{uniq_id}")]
            ]
        )

        # Send message to user
        response_text = f"""
✅ **Your app is ready!**

📁 **File Name:** `{cleaned_file_name}`  
📦 **Size:** `{file_size} MB`

Tap the button below to open the app 👇
""".strip()

        await msg.edit_text(response_text, reply_markup=keyboard)

    except Exception as e:
        await msg.edit_text("🚫 Failed to send the file. Please Try again Later")
        print(f"Error: {e}")
def send_document(chat_id,uniq_id, file_id, caption="", protect_content=True, parse_mode="HTML"):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    user_id = chat_id
    keyboard = {
        "inline_keyboard": [
            [{"text": "🔍Search a App", "callback_data": "123_premium_apps"}],
            [{"text": "🔗 Create Link", "callback_data": f"create_link_{uniq_id}"}]
        ]
    }
    
    payload = {
        "chat_id": chat_id,
        "document": file_id,
        "caption": caption,
        "protect_content": protect_content,
        "parse_mode": parse_mode,
        "reply_markup": json.dumps(keyboard)  
    }
    
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        return "OK"
    else:
        return "ER"
@app.on_callback_query(filters.regex(r"^create_link_"))
async def create_telegram_link_handler(client, query: CallbackQuery):
    uniq_id = query.data.split("create_link_")[1]

    # JSON से app खोजें
    try:
        with file_lock:
            with open(APP_DATA_FILE, "r") as f:
                all_data = json.load(f)
    except Exception as e:
        await query.answer("⚠️ Unable to load data", show_alert=True)
        print("❌ JSON read error:", e)
        return

    app_item = next((item for item in all_data if item.get("uniq_id") == uniq_id), None)
    if not app_item:
        await query.answer("❌ App not found", show_alert=True)
        return

    # 🔧 Auto bot username
    bot_username = (await client.get_me()).username
    telegram_link = f"https://t.me/{bot_username}?start=APK_{uniq_id}"

    # Clean file name
    file_name = app_item.get("file_name", "Unknown")
    cleaned_file_name = clean_file_name(file_name)
    share = f"""**🔐Download Premium Unlocked app**
    
**APP NAME** : {cleaned_file_name}

Click on the Below Link:
{telegram_link}"""
    text =quote(share)
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📥 Open in Bot", url=telegram_link)],
        [InlineKeyboardButton("📤 Share Link", url=f"https://t.me/share/url?url=&text={text}")]
    ])

    await query.message.reply_text(
        f"🔗 **Link Generated!**\n\n📦 **App Name:** `{cleaned_file_name}`\n📎**Link:**\n {telegram_link}\n\n👇 Use button to access or share:",
        reply_markup=keyboard
    )

    await query.answer("Link ready ✅", show_alert=False)
@app.on_callback_query(filters.regex("^page_"))
async def premiumcall12(client, query: CallbackQuery):
  await premiumcall12345(client, query)

async def premiumcall12345(client, query):
  if query.data.startswith("page_"):
        _, page, search_query = query.data.split("_")
        page = int(page)
    
        msg = query.message
        await search_and_send_inline(msg, search_query, page)  

@app.on_callback_query(filters.regex("^pre_"))
async def premiumcall(client, query: CallbackQuery):
  await premium_app_send(client, query)
    
async def premium_app_send(client, query):
    user_id = query.from_user.id
    user_name = query.from_user.first_name

    if query.data.startswith("pre_"):
        uniq_id = query.data[4:]  # "pre_" के बाद वाला हिस्सा

        # 🔍 JSON से app ढूंढो
        try:
            with file_lock:
                with open(APP_DATA_FILE, 'r') as f:
                    all_data = json.load(f)
        except Exception as e:
            await query.answer("Error loading data", show_alert=True)
            print(f"❌ JSON read error: {e}")
            return

        # 🔎 uniq_id से app खोजो
        matched_app = next((item for item in all_data if item.get("uniq_id") == uniq_id), None)

        if not matched_app:
            await query.answer("File not found!", show_alert=True)
            return

        file_id = matched_app.get("file_id")
        msg = await query.message.reply_text("Please Wait...")
        await query.message.delete()
        await search_and_send_app(client,uniq_id, msg, file_id)

@app.on_callback_query(filters.regex("^123_premium_apps$"))
async def premium_app_sutffutftend(client, query):
     await query.message.reply_text("Please Provide a New app Name..")
     await query.message.delete()
from script import flask_app     
from flask import Flask, request, jsonify
from flask_cors import CORS

CORS(flask_app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
import traceback

@flask_app.route("/send_file", methods=["POST"])
def send_file():
    try:
        data = request.get_json()

        try:
            user_id = int(data.get("user_id", "0"))
            chat_id = user_id
        except ValueError:
            print("❌ Invalid user_id:")
            traceback.print_exc()
            return jsonify({"status": "error", "message": "Invalid user_id"}), 400

        file_id = data.get("file_id", "")
        file_name = data.get("file_name", "")
        file_size = data.get("file_size", "")
        uniq_id = data.get("uniq_id", "")

        if not file_id:
            print("❌ Missing file_id")
            return jsonify({"status": "error", "message": "Missing file_id"}), 400

        try:
            res = send_document(
                chat_id,
                uniq_id,
                file_id,
                caption=f"""📱 App Name: {file_name}
📦 Size: {file_size} MB

✅ 100% Safe & Tested
🔁 Shared via Telegram Bot
https://t.me/apps_premiumBot
@HOW_TO_INSTALL_APP
📲 Install and enjoy!""",
                protect_content=True,
                parse_mode="HTML"
            )

            if res == "OK":
                print("✅ File sent successfully.")
                return jsonify({"status": "success", "telegram_response": "ok"}), 200
            elif res == "ER":
                print("❌ send_document returned 'ER'")
                send_telegram_message(chat_id, "❌ फ़ाइल भेजने में समस्या आई। कृपया Admin से संपर्क करें।", BOT_TOKEN)
                return jsonify({"status": "error", "telegram_response": "er"}), 500
            else:
                print(f"⚠️ Unknown response from send_document: {res}")
                return jsonify({"status": "unknown", "telegram_response": res}), 500

        except Exception as e:
            print("❌ Exception while sending file:")
            traceback.print_exc()
            send_telegram_message(chat_id, "❌ फ़ाइल भेजने में त्रुटि हुई।", BOT_TOKEN)
            return jsonify({"status": "error", "telegram_response": str(e)}), 500

    except Exception as e:
        print("❌ Main exception in send_file():")
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500


RESTART_FLAG_FILE = ".restart_sent"

def send_message_to_channel(chat_id, message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message
        }
        res = requests.post(url, data=payload, timeout=10).json()
        if not res.get("ok"):
            logging.error(f"❌ Failed to send to {chat_id}: {res.get('description')}")
            return False
        return True
    except Exception as e:
        logging.exception(f"❌ Exception sending message to {chat_id}")
        return False

def check_and_send_restart():
    if os.path.exists(RESTART_FLAG_FILE):
        logging.info("✅ Restart message already sent. Skipping.")
        return

    # Get bot name
    try:
        bot_info = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getMe",
            timeout=10
        ).json()

        if not bot_info.get("ok"):
            logging.error(f"❌ Failed to get bot info: {bot_info.get('description')}")
            return

        bot_name = bot_info["result"].get("first_name", "Bot")

    except Exception:
        logging.exception("❌ Exception while fetching bot info")
        return

    # Message content
    message = f"I am Restarted. {bot_name}"

    # Send to both channels
    success1 = send_message_to_channel(CHECK_CHANNEL_ID, message)
    success2 = send_message_to_channel(FILE_CHANNEL_ID, message)

    if success1 or success2:
        with open(RESTART_FLAG_FILE, "w") as f:
            f.write("sent")
        logging.info("✅ Restart message sent to at least one channel.")
    else:
        logging.warning("⚠️ Restart message failed to send to both channels.")
        
from pyrogram import Client, filters
from pyrogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from urllib.parse import quote

@app.on_inline_query()
async def inline_search_handler(client: Client, query: InlineQuery):
    raw_query = query.query or ""
    search_text = raw_query.strip()
    bot_username = (await client.get_me()).username

    # 🔍 Debug log 1: Query received
    print(f"[🔍] Raw query: {repr(raw_query)} | Cleaned: {repr(search_text)}")

    # ✅ Case 1: Empty input

    if not search_text:
        print("[ℹ️] Query is empty. Sending 'Enter app name' fallback.")
        await query.answer(
            results=[],
            cache_time=0
        )
        return

    # 🔍 Perform search
    matched_apps = search_apps_from_json(search_text)

    # 🔍 Debug log 2: Search result count
    print(f"[🔍] Matches found: {len(matched_apps)} for query '{search_text}'")

    # ❌ Case 2: No match
    """
    if not matched_apps:
        print("[❌] No matching apps found. Sending fallback.")
        await query.answer(
            results=[],
            switch_pm_text=f"❌ No result for '{search_text}'",
            switch_pm_parameter="404",
            cache_time=0
        )
        return
"""
    # ✅ Case 3: Valid results
    results = []
    for app in matched_apps:
        title = app.get("file_name", "Unnamed App")
        uniq_id = app.get("uniq_id")
        start_link = f"https://t.me/{bot_username}?start=APK_{uniq_id}"
        encoded_name = quote(title)

        results.append(
            InlineQueryResultArticle(
                title=title,
                description="Click to open this app",
                input_message_content=InputTextMessageContent(
                    f"📦 **App:** `{title}`\n\n📲 Open this app:\n{start_link}"
                ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📲 Open App", url=start_link)]
                ])
            )
        )

    print(f"[✅] Sending {len(results)} results for query '{search_text}'")
    
    await query.answer(results=results[:20],#switch_pm_text="📝 app name",
             cache_time=0
            )
