# (c) @doreamonfans1 
# A Part of MegaDL-Bot <https://github.com/disneyteam77/MegaDL-Bot>

import os
from pyrogram import Client, filters
from config import Config

@Client.on_message(filters.reply & filters.text & filters.private & ~filters.edited)
async def newcap(bot, message):
    nc = message.reply_to_message
    if nc.media and not (nc.video_note or nc.sticker):
        await nc.copy(message.chat.id, caption=message.text)
