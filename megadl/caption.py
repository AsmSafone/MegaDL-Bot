# (c) Asm Safone
# A Part of MegaDL-Bot <https://github.com/AsmSafone/MegaDL-Bot>

from config import Config
from pyrogram import Client, filters

@Client.on_message(filters.reply & filters.text & filters.private & ~filters.edited)
async def caption(bot, message):
    file = message.reply_to_message
    if file.media and not file.video_note and not file.sticker:
        await file.copy(message.chat.id, caption=message.text)
    else:
        return
