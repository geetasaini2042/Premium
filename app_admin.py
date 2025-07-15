"""JAY SHREE RAM"""

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton , CallbackQuery, ReplyKeyboardRemove , ForceReply
import time
import json
import requests
from datetime import datetime, timedelta
import asyncio
import re
import os
from app_script import FILE_CHANNEL_ID,admin_app_details,admins
from script import app
from pyrogram import Client, filters
from filters.status_filters import StatusFilter
from common_data import status_user_file


def set_user_status(user_id: int, status: str):
    try:
        with open(status_user_file, "r") as f:
            data = json.load(f)
    except:
        data = {}

    data[str(user_id)] = status

    with open(status_user_file, "w") as f:
        json.dump(data, f)
        
def get_user_status(user_id: int) -> str:
    try:
        with open(status_user_file, "r") as f:
            data = json.load(f)
        return data.get(str(user_id), "")
    except:
        return ""
def delete_user_1status(user_id: int):
    try:
        with open(status_user_file, "r") as f:
            data = json.load(f)
    except:
        data = {}

    if str(user_id) in data:
        del data[str(user_id)]

    with open(status_user_file, "w") as f:
        json.dump(data, f)




API_URL = "https://sainipankaj12.serv00.net/App/Pre/index.php"
cancel12 = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚫Cancel", callback_data="cancel")]])
admin_keyboard  = InlineKeyboardMarkup([
        [InlineKeyboardButton("Upload App", callback_data="adm_upload_premium_app")]
        
    ])
cancelkro = ReplyKeyboardMarkup(
    [[KeyboardButton("🚫CANCEL")]],
    resize_keyboard=True
)
upload_premium  = InlineKeyboardMarkup([
        [InlineKeyboardButton("Upload Menually", callback_data="adm_upload_menual")],
        [InlineKeyboardButton("GET FROM CHANNEL", callback_data="adm_get_from_channel")]])

def is_admin(_, __, message):
    return message.from_user and message.from_user.id in admins


@app.on_message(filters.command("app_admin") & filters.private & filters.create(is_admin))
def adminCommand(client,message):
    user_id = message.from_user.id
    if user_id not in admins:
        return message.reply_text("⛔ आपको इस कमांड का उपयोग करने की अनुमति नहीं है!")
    else:
      message.reply_text(f"Welcome {admins[user_id]}, Your Most Welcome",reply_markup=admin_keyboard)

@app.on_callback_query(filters.regex("^adm_upload_ok_"))
async def admin_callback456(client, callback_query):
    user_id = callback_query.from_user.id
    
    if user_id not in admins:
        return await callback_query.answer("⛔ आपको इस एक्शन की अनुमति नहीं है!", show_alert=True)
    
    callback_data = callback_query.data  # e.g., "adm_upload_ok_file1"
    file_key = callback_data.replace("adm_upload_ok_", "", 1)  # Extracting file_key (e.g., file1, file2)

    if user_id in admin_app_details and file_key in admin_app_details[user_id]:
        file_id = admin_app_details[user_id][file_key]['file_id']
        file_name = admin_app_details[user_id][file_key]['file_name']

        await callback_query.message.edit_text("Please Wait...")
        await send_data(file_id, file_name)
        
        await callback_query.message.edit_text(
            "Uploaded successfully! Thanks for uploading this file. 😊",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🚫Delete", callback_data="delete")],
                [InlineKeyboardButton("⚜ Home", callback_data="home")]
            ])
        )
    else:
        await callback_query.answer("No file details", show_alert=True)
 
@app.on_callback_query(filters.regex("^adm_"))
def adminCallback(client, callback_query):
    user_id = callback_query.from_user.id
    first_name =callback_query.from_user.first_name
    if user_id not in admins:
        return callback_query.answer("⛔ आपको इस एक्शन की अनुमति नहीं है!", show_alert=True)
    callback_data = callback_query.data  # e.g., "adm_upload_premium_app"
    real_msg = callback_data.replace("adm_", "", 1)  # Removes "adm_" prefix
    #callback_query.message.reply_text(f"🔹 Real Message: {real_msg}")
    if real_msg =="upload_premium_app":
      callback_query.message.edit_text(f"Hey {first_name}, How do you want to add premium app",reply_markup=upload_premium)
    elif real_msg == "get_from_channel":
      callback_query.message.edit_text(f"Hey {first_name}, Please send me Channel Id Without @ .",reply_markup=cancelkro)
      sta1tus = "adm_upload_app_from_channel"
      set_user_status(user_id, sta1tus)
    elif real_msg =="upload_menual":
      callback_query.message.reply_text(f"Hey {first_name}, Please send me a App to add that in database.",reply_markup=cancelkro)
      sta1tus = "adm_upload_premium_app"
      set_user_status(user_id, sta1tus)
    
    elif real_msg =="upload_ar":
      callback_query.message.edit_text("Not Sending...",reply_markup=admin_keyboard)
      del admin_app_details[user_id]
    
async def admin_session_av(client, message):
    user_id = message.from_user.id
    user_state = get_user_status(user_id)
    real_msg = user_state.replace("adm_", "", 1)

    if real_msg == "upload_premium_app":
        await message.reply_text("⚠️Please Cancel this Session first!", reply_markup=cancel12)
    else:
        await message.reply_text(f"There is a Session : {real_msg} \n**Please Cancel this session first!", reply_markup=cancel12)
@app.on_callback_query(filters.regex("^cancle"))        
def cancle_session_query(client,query):
  message=query.message
  user_id = query.from_user.id
  user_state = get_user_status(user_id)
  real_msg = user_state.replace("adm_", "", 1) 
  if real_msg == "upload_premium_app":
      delete_user_1status(user_id)
      msg12 = message.reply_text("Session Canceled!", reply_markup=ReplyKeyboardRemove())
      time.sleep(0.7)
      msg12.delete()
  else:
      delete_user_1status(user_id)
      msg12 = message.reply_text("SESSION Canceled", reply_markup=ReplyKeyboardRemove())
      msg12.reply_text("Hello Admin Session Cancled Now Choose Next Option..",reply_markup=admin_keyboard)
      time.sleep(0.7)
      msg12.delete()
@app.on_message(filters.text  & filters.regex(r"^🚫CANCEL$"))
def cancle_session_msg(client,message):
  user_id = message.from_user.id
  user_state = get_user_status(user_id)
  real_msg = user_state.replace("adm_", "", 1) 
  if real_msg == "upload_premium_app":
      delete_user_1status(user_id)
      msg12 = message.reply_text("Session Canceled!", reply_markup=ReplyKeyboardRemove())
      time.sleep(0.7)
      msg12.delete()

  elif real_msg.startswith("enter_app"):
     del admin_app_details[user_id]
     msg12.edit("Hello Admin Session Cancled Now Choose Next Option..",reply_markup=admin_keyboard)
  else:
      delete_user_1status(user_id)
      msg12 = message.reply_text("Session Canceled!", reply_markup=ReplyKeyboardRemove())
      msg12.reply_text("Hello Admin Session Cancled Now Choose Next Option..",reply_markup=admin_keyboard)
      time.sleep(0.7)
      msg12.delete()


# Helper function to extract channel username and message ID from a Telegram link
def extract_from_link(link):
    match = re.match(r'https://t\.me/([\w\d_]+)/(\d+)', link)
    if match:
        return match.group(1), int(match.group(2))
    return None, None

@app.on_message(filters.text 
    & ~filters.me & ~filters.group 
    & ~filters.command("start")
    & ~filters.regex(r"^🚫CANCEL$")
    & filters.create(is_admin)
    & StatusFilter("adm_")
)
async def process_adm_text_messages(client, message):  
    user_id = message.from_user.id  
    user_text = message.text.strip()  
    user_state = get_user_status(user_id)  
    real_msg = user_state.replace("adm_", "", 1)

    if real_msg == "upload_app_from_channel":  
        username, msg_id = extract_from_link(user_text)
        if not username or not msg_id:
            await message.reply_text("❌ Invalid link! Please send a valid Telegram message link like:\n`https://t.me/channel/1234`")
            return
        try:  
            chat = await client.get_chat(username)
            await message.reply_text(f"""This Channel Details :  
📢 **{chat.title}**  
🆔 ID: `{chat.id}`  
👤 Members: {chat.members_count if chat.members_count else 'Unknown'}  
📜 Description: {chat.description if chat.description else 'No Description'}  
  
Now send me the **LAST message link**...  
            """)  
            sta1tus = "adm_channel_last_id"  
            set_user_status(user_id, sta1tus)
            admin_app_details[user_id] = {
                'channel_id': chat.id,
                'channel_username': username,
                'first_id': msg_id
            }
        except Exception as e:  
            await message.reply_text("Failed to fetch channel details.")
  
    elif real_msg == "channel_last_id":
        username, msg_id = extract_from_link(user_text)
        if not username or not msg_id:
            await message.reply_text("❌ Invalid link! Please send a valid Telegram message link like:\n`https://t.me/channel/5678`")
            return
        admin_app_details[user_id]['last_id'] = msg_id
        await message.reply_text(f"✅ Last Message ID saved: {msg_id} \n\nNow saving files to database...")
        await fetch_and_save_files(client, user_id, message)
        delete_user_1status(user_id)



async def send_data(file_id, file_name):
    data = {
        "file_id": file_id,
        "file_name": file_name
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(data))
        response_json = response.json()  # API का JSON रिस्पॉन्स
        
        if response.status_code == 200 and response_json.get("success") is True:
            print(f"Sent: {file_name} - OK")
            return "OK"
        else:
            print(f"Sent: {file_name} - ER")
            return "ER"

    except Exception as e:
        print(f"Error sending {file_name}: {e}")
        return "ER"

async def fetch_and_save_files(client, user_id, message):
    try:
        details = admin_app_details.get(user_id, {})  
        source_channel = details.get('channel_id')
        target_channel = FILE_CHANNEL_ID  # Private Channel ID
        first_msg_id = details.get('first_id')
        last_msg_id = details.get('last_id')

        if not source_channel or not target_channel or not first_msg_id or not last_msg_id:
            return await message.reply_text("❌ Missing required details!")

        total_files = last_msg_id - first_msg_id + 1  
        saved_files = 0
        skipped_files = 0
        error_count = 0

        status_msg = await message.reply_text(
            f"📢 **Processing Started**\n\n"
            f"📂 **Total Files to Process:** {total_files}\n"
            f"📥 **Saved Files:** {saved_files}\n"
            f"⏭ **Skipped Files:** {skipped_files}\n"
            f"⚠ **Errors Encountered:** {error_count}"
        )

        for index, msg_id in enumerate(range(first_msg_id, last_msg_id + 1), start=1):
            try:
                fetched_message = await client.get_messages(source_channel, msg_id)  

                if fetched_message and fetched_message.document:
                    file_name = fetched_message.document.file_name

                    if file_name.endswith(".apk"):  # ✅ सिर्फ .apk फाइल ही सेव करें
                        copied_msg = await fetched_message.copy(target_channel)  # ✅ Forward Without Tag
                        file_id = copied_msg.document.file_id
                        
                        response = await send_data(file_id, file_name)  # ✅ File ID सेव करें

                        if response == "OK":
                            saved_files += 1
                        else:
                            error_count += 1  # अगर API से "OK" न मिले तो एरर काउंट बढ़ाएं

                        await asyncio.sleep(3)  
                    else:
                        skipped_files += 1  # .apk न होने पर स्किप करें

                else:
                    skipped_files += 1  
                
            except Exception as e:
                print(f"Skipping message {msg_id} due to error: {e}")
                error_count += 1  
                continue  

            if index % 50 == 0 or index == total_files:  
                await status_msg.edit(
                    f"📢 **Processing Update**\n\n"
                    f"📂 **Total Files to Process:** {total_files}\n"
                    f"📥 **Saved Files:** {saved_files}\n"
                    f"⏭ **Skipped Files:** {skipped_files}\n"
                    f"⚠ **Errors Encountered:** {error_count}"
                )

        await status_msg.edit(
            f"✅ **Processing Completed!**\n\n"
            f"📂 **Total Files Processed:** {total_files}\n"
            f"📥 **Successfully Saved:** {saved_files}\n"
            f"⏭ **Skipped Files:** {skipped_files}\n"
            f"⚠ **Errors Encountered:** {error_count}"
        )

    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

@app.on_message(filters.private & filters.document & ~filters.me & StatusFilter("adm_upload_premium_app"))
async def get_file_id(client, message):
    user_id = message.from_user.id
    if get_user_status(user_id)   == "chatting_with_ai":
      await message.reply_text("Sorry I cant see your sended Document",reply_markup=cancel12)
    elif get_user_status(user_id)   == "enter_roll_number":
       await message.reply_text("⚠️Please Provide a Valid Roll number Or Cancel this session!",reply_markup=cancel12)
    elif get_user_status(user_id)   == "search_premium_app":
       await message.reply_text("⚠️Please Provide a App name I Will Find Out Premium app for you...",reply_markup=cancel12)
    elif get_user_status(user_id)   and get_user_status(user_id).startswith("adm_"):
      forwarded = await message.copy(FILE_CHANNEL_ID)
      file_id = forwarded.document.file_id
      file_name = forwarded.document.file_name
      user_state = get_user_status(user_id)  
      real_msg = user_state.replace("adm_", "", 1) 
      if real_msg =="upload_premium_app":
         await message.reply_text(f"""
Saved Successfully in database : 
**FILE NAME :** `{file_name}`
**FILE ID : ** `{file_id}` .
      """,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙Back", callback_data="adm_upload_premium_app")]]))
         await send_data(file_id, file_name)
         delete_user_status(user_id)
  
    else:
      if user_id in admins:
         forwarded = await message.copy(FILE_CHANNEL_ID)
         file_id = forwarded.document.file_id
         file_name = forwarded.document.file_name  # फाइल का नाम
      
         if ".apk" in file_name.lower(): 
             if user_id not in admin_app_details:
                 admin_app_details[user_id] = {}  # हर एडमिन के लिए अलग डिक्शनरी
        
             # नई फाइल के लिए अगला क्रमांक निकालें
             file_count = len(admin_app_details[user_id]) + 1
             file_key = f"file{file_count}"

             admin_app_details[user_id][file_key] = {
                 "file_id": file_id,
                 "file_name": file_name
             }
             verify_premium_upload  = InlineKeyboardMarkup([
                [InlineKeyboardButton("Upload Premium App", callback_data=f"adm_upload_ok_{file_key}"),
                InlineKeyboardButton("Don't Upload", callback_data="adm_upload_ar")]])
             await message.reply_text(
                 f"**File Name :**\n `{file_name}`\n\n**File Id** :\n`{file_id}`\n\n UPLOAD THIS APP TO PREMIUM APPS DATABASE",
                 reply_markup=verify_premium_upload
             )
         else:
             await message.reply_text(
                 f"**File Name :**\n `{file_name}`\n\n**File Id :**\n `{file_id}`",
                 reply_markup=home_keyboard
             )
      else:
          await message.reply_text("Unsupport Media Type...",reply_markup=home_keyboard)