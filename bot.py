import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

BOT_TOKEN = "8407126683:AAHUOBGHJNyk3Q0_Q1y0qZ-Dq_5fC7pC4Q0"
API_ID = 32595789
API_HASH = "190a314f25c399f7f0708eb86e30f713"
CHANNEL_ID = -1004430081060
WEB_APP_URL = "https://drecopenal-gif.github.io/Adsgrm-/"

USER_SESSIONS = {}

app = Client("ad_file_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.private & (filters.document | filters.video | filters.photo | filters.audio))
async def save_file(client, message):
    forwarded = await message.forward(CHANNEL_ID)
    msg_id = forwarded.id
    bot_me = await client.get_me()
    share_link = f"https://t.me/{bot_me.username}?start=file_{msg_id}"
    await message.reply_text(
        f"✅ **File Saved!**\n\n"
        f"🔗 **Shareable Link:**\n`{share_link}`\n\n"
        f"કોઈ પણ યુઝર આ લિંક ઓપન કરશે એટલે એડ જોયા પછી તેને ફાઈલ મળશે."
    )

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    text = message.text
    if len(text.split()) > 1 and text.split()[1].startswith("file_"):
        file_id = int(text.split()[1].replace("file_", ""))
        USER_SESSIONS[message.chat.id] = file_id
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎬 Watch Ad to Unlock File", web_app=WebAppInfo(url=f"{WEB_APP_URL}?userid={message.chat.id}"))]
        ])
        
        await message.reply_text(
            "🔒 **File Locked!**\n\n"
            "ફાઇલ મેળવવા માટે નીચે બટન પર ક્લિક કરી જાહેરાત જુઓ.",
            reply_markup=keyboard
        )
    else:
        await message.reply_text("👋 મને કોઈ પણ વિડીયો કે ફાઇલ મોકલો લિંક બનાવવા માટે.")

@app.on_message(filters.service)
async def handle_webapp_data(client, message):
    if message.web_app_data and message.web_app_data.data == "ad_completed":
        chat_id = message.chat.id
        file_msg_id = USER_SESSIONS.get(chat_id)
        
        if file_msg_id:
            await message.reply_text("✅ Verification Successful! ફાઇલ મોકલાઈ રહી છે...")
            await client.copy_message(chat_id=chat_id, from_chat_id=CHANNEL_ID, message_id=file_msg_id)
        else:
            await message.reply_text("⚠️ કોઈ ફાઇલ મળી નથી. લિંક ફરીથી ઓપન કરો.")

async def main():
    async with app:
        print("Bot is running...")
        await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
