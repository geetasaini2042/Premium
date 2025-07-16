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
from common_data  import BOT_TOKEN
from app_script import SEARCH_URL,send_telegram_message
from script import app,flask_app,upload_users
temp_data = {}
saveii = {}
#Main Functions Started
from flask import Flask, request, jsonify
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import re
CHECK_CHANNEL_ID = int(os.getenv("CHECK_CHANNEL_ID", "-1002536426442"))
from urllib.parse import quote

def clean_file_name(name: str) -> str:
    name = re.sub(r'@\w+', '', name)                  # Remove all @usernames
    name = re.sub(r'(?i)modded by', '', name)         # Remove 'modded by' case-insensitive
    name = re.sub(r'\s+', ' ', name).strip()          # Clean extra spaces
    return name

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
📥 *New File Accessed!*

👤 *User Details:*
• ID: `{user.id}`
• Name: {user.first_name} {user.last_name or ""}
• Username: @{user.username or 'N/A'}
• Language: {user.language_code or 'N/A'}

📄 *File Info:*
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
✅ *Your file is ready!*

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
    & NoStatusFilter()  # 👈 यही line जोड़ा गया है
)
async def process_text_messages(client: Client, message: Message):
       msg = await message.reply_text("Please Wait...")
       time.sleep(5)
       await msg.edit_text("Searching app...")
       user_id = message.from_user.id
       user_msg = message.text
       user_name = message.from_user.first_name
       Search_Query = user_msg
       await search_and_send_inline(msg,Search_Query)

async def search_and_send_inline(msg, search_query, page=1):
    response = requests.get(SEARCH_URL + search_query)
    user_id = msg.chat.id
    if user_id not in saveii:
        saveii[user_id] = {}
    if response.status_code != 200:
        await msg.edit("Error Searching App")
        return
    saveii[user_id]['page'] = page
    saveii[user_id]['search_query'] = search_query
    apps = response.json()
    if not apps:
        await msg.edit("No App found")
        return

    results_per_page = 10
    total_pages = (len(apps) + results_per_page - 1) // results_per_page  # कुल पेज
    
    # पेज इंडेक्स सेट करें
    start_idx = (page - 1) * results_per_page
    end_idx = start_idx + results_per_page
    apps = apps[start_idx:end_idx]  # सिर्फ़ 10 परिणाम फ़िल्टर करें
    buttons = []
    row = []

    for idx, app in enumerate(apps):
        short_id = f"app_{start_idx + idx}"  # यूनिक Short ID
        temp_data[short_id] = app["file_id"]

        row.append(InlineKeyboardButton(app["file_name"], callback_data=f"pre_{short_id}"))

        if len(row) == 2:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    # पेज नेविगेशन बटन
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton("⬅ Previous", callback_data=f"page_{page-1}_{search_query}"))
    if total_pages > 1:
      nav_buttons.append(InlineKeyboardButton(f"{page}/{total_pages}", callback_data=f"premium_apps"))
    if page < total_pages:
        nav_buttons.append(InlineKeyboardButton("Next ➡", callback_data=f"page_{page+1}_{search_query}"))

    if nav_buttons:
        buttons.append(nav_buttons)

    await msg.edit(
        f"**Here is your Search Result For :** \n`{search_query}`",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

    return temp_data  # Short IDs को बाद में एक्सेस करने के लिए रिटर्न करें


from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import re


async def search_and_send_app(client, msg, file_id):
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
        link123 = f"https://geetasaini2042.github.io/17uio/APPS/NewVersion/index.html?file_id={file_id}&file_size={file_size}&file_name={encoded_file_name}"
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("📲 Get Your App Now", web_app=WebAppInfo(url=link123))]
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
def send_document(chat_id, file_id, caption="", protect_content=True, parse_mode="HTML"):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    user_id = chat_id
    #print(saveii)
    #print(saveii[user_id])
    search_query = saveii[user_id]['search_query'] 
    page = saveii[user_id]['page']
    keyboard = {
        "inline_keyboard": [
            [{"text": "🔍Search Again", "callback_data": "123_premium_apps"}],
            [{"text": "🔙Back", "callback_data": f"page_{page}_{search_query}"},
            {"text": "🏠 Home", "callback_data": "home"}]
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
      user_id = query.from_user.id  # Get user ID
      user_name = query.from_user.first_name  # Extract user name
      if query.data.startswith("pre_"):
        short_id = query.data[4:]  # "pre_" के बाद का टेक्स्ट निकालें
        file_id = temp_data.get(short_id)  # Short ID से असली File ID प्राप्त करें
        if not file_id:
           await query.answer("File not found!", show_alert=True)
           return
        msg = await query.message.reply_text("Please Wait...")
        await query.message.delete()
        await search_and_send_app(client, msg, file_id)

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

        if not file_id:
            print("❌ Missing file_id")
            return jsonify({"status": "error", "message": "Missing file_id"}), 400

        try:
            res = send_document(
                chat_id,
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
