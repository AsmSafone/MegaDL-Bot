# (c) Asm Safone
# A Part of MegaDL-Bot <https://github.com/AsmSafone/MegaDL-Bot>

import os
import asyncio
from pyrogram import Client, idle
from config import Config

if __name__ == "__main__" :
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)
    plugins = dict(root="megadl")
    app = Client(
        "MegaDL-Bot",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        plugins=plugins
    )
    app.start()
    print('\n\n>>> MegaDL-Bot Started. Join @AsmSafone!')
    idle()
    app.stop()
    print('\n\n>>> MegaDL-Bot Stopped. Join @AsmSafone!')
