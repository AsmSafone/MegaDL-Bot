# (c) Asm Safone
# A Part of MegaDL-Bot <https://github.com/AsmSafone/MegaDL-Bot>

import os
import time
import asyncio
import logging
import subprocess
import shutil
import filetype
import moviepy.editor
from mega import Mega
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from hurry.filesize import size
from functools import partial
from asyncio import get_running_loop
from genericpath import isfile
from posixpath import join
from megadl.progress import progress_for_pyrogram, humanbytes
from megadl.forcesub import handle_force_subscribe
from config import Config

# Logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Mega Client
mega = Mega()
m = mega.login()

# Temp Download Directory
basedir = Config.DOWNLOAD_LOCATION

# Telegram's Max File Size
TG_MAX_FILE_SIZE = Config.TG_MAX_SIZE

# Automatic Url Detection
MEGA_REGEX = (r"^((?:https?:)?\/\/)"
              r"?((?:www)\.)"
              r"?((?:mega\.nz))"
              r"(\/)([-a-zA-Z0-9()@:%_\+.~#?&//=]*)([\w\-]+)(\S+)?$")

# Download Mega Link
def DownloadMegaLink(url, alreadylol, download_msg):
    try:
        m.download_url(url, alreadylol, statusdl_msg=download_msg)
    except Exception as e:
        #await download_msg.edit(f"**Error:** `{e}`")
        print(e)


@Client.on_message(filters.regex(MEGA_REGEX) & filters.private & filters.incoming & ~filters.edited)
async def megadl(bot, message):
    if Config.UPDATES_CHANNEL:
      fsub = await handle_force_subscribe(bot, message)
      if fsub == 400:
        return
    url = message.text
    user_info = f'**User ID:** #id{message.from_user.id} \n**User Name:** [{message.from_user.first_name}](tg://user?id={message.from_user.id})'
    userpath = str(message.from_user.id)
    alreadylol = basedir + "/" + userpath
    if os.path.isdir(alreadylol):
      await message.reply_text(f"**Already One Process is Going On! \nPlease Wait Until It's Get Finished 😕!**", reply_to_message_id=message.message_id)
      return
    else:
      os.makedirs(alreadylol)
    try:
      if 'folder' in url:
        await message.reply_text(f"**Mega Folder Isn't Supported Yet 🤒!**", reply_to_message_id=message.message_id)
        return
      else:
        logs_msg = await message.forward(Config.LOG_CHANNEL)
        trace_msg = await logs_msg.reply_text(f"#MegaDL: Download Started! \n\n{user_info}")
        download_msg = await message.reply_text(f"**Trying To Download ...** \n\nThis Process May Take Some Time 🤷‍♂️!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancel Mega DL", callback_data="cancel_mega")]]), reply_to_message_id=message.message_id)
        loop = get_running_loop()
        await loop.run_in_executor(None, partial(DownloadMegaLink, url, alreadylol, download_msg))
        getfiles = [f for f in os.listdir(alreadylol) if isfile(join(alreadylol, f))]
        files = getfiles[0]
        magapylol = f"{alreadylol}/{files}"
        await download_msg.edit(f"**Downloaded Successfully 😉!**")
        await trace_msg.edit(f"#MegaDL: Download Done! \n\n{user_info}")
    except Exception as e:
        await download_msg.edit(f"**Error:** `{e}`")
        await trace_msg.edit(f"#MegaDL: Download Failed! \nReason: `{e}` \n\n{user_info}")
        shutil.rmtree(basedir + "/" + userpath)
        return
    lmaocheckdis = os.stat(alreadylol).st_size
    readablefilesize = size(lmaocheckdis) # Convert Bytes into readable size
    if lmaocheckdis > TG_MAX_FILE_SIZE:
        await download_msg.edit(f"**Detected File Size:** `{readablefilesize}` \n**Accepted File Size:** `2.0 GB` \n\nOops! File Is Too Large To Send In Telegram 🤒!")
        await trace_msg.edit(f"#MegaDL: Upload Failed! \nReason: `File is Larger Than 2GB.` \n\n{user_info}")
        shutil.rmtree(basedir + "/" + userpath)
        return
    else:
        start_time = time.time()
        guessedfilemime = filetype.guess(f"{magapylol}") # Detecting file type
        if not guessedfilemime.mime:
            await download_msg.edit("**Trying To Upload ...** \n**Can't Get File Type, Sending as Document!")
            safone = await message.reply_document(magapylol, progress=progress_for_pyrogram, progress_args=("**Uploading ...** \n", download_msg, start_time), reply_to_message_id=message.message_id)
            await safone.reply_text(f"**Join @AsmSafone! \nThanks For Using Me 😘!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🙌 SHARE 🙌", url=f"https://t.me/share/url?url=**Hey%20Guys!%20%20Check%20Out%20@AsmSafone's%20Bots%20Channel.%20%20Share%20His%20Bots%20And%20Support%20Him%20%F0%9F%98%89!%20%20Here%20Is%20The%20Bots%20List%20:-%20https://t.me/AsmSafone/173**")]]), reply_to_message_id=safone.message_id)
            await download_msg.delete()
            await trace_msg.edit(f"#MegaDL: Upload Done! \n\n{user_info}")
            shutil.rmtree(basedir + "/" + userpath)
            return
        filemimespotted = guessedfilemime.mime
        # Checking If it's a gif
        if "image/gif" in filemimespotted:
            await download_msg.edit("**Trying To Upload ...**")
            safone = await message.reply_animation(magapylol, progress=progress_for_pyrogram, progress_args=("**Uploading ...** \n", download_msg, start_time), reply_to_message_id=message.message_id)
            await safone.reply_text(f"**Join @AsmSafone! \nThanks For Using Me 😘!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🙌 SHARE 🙌", url=f"https://t.me/share/url?url=**Hey%20Guys!%20%20Check%20Out%20@AsmSafone's%20Bots%20Channel.%20%20Share%20His%20Bots%20And%20Support%20Him%20%F0%9F%98%89!%20%20Here%20Is%20The%20Bots%20List%20:-%20https://t.me/AsmSafone/173**")]]), reply_to_message_id=safone.message_id)
            await download_msg.delete()
            await trace_msg.edit(f"#MegaDL: Upload Done! \n\n{user_info}")
        # Checking if it's a image
        elif "image" in filemimespotted:
            await download_msg.edit("**Trying To Upload ...**")
            safone = await message.reply_photo(magapylol, progress=progress_for_pyrogram, progress_args=("**Uploading ...** \n", download_msg, start_time), reply_to_message_id=message.message_id)
            await safone.reply_text(f"**Join @AsmSafone! \nThanks For Using Me 😘!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🙌 SHARE 🙌", url=f"https://t.me/share/url?url=**Hey%20Guys!%20%20Check%20Out%20@AsmSafone's%20Bots%20Channel.%20%20Share%20His%20Bots%20And%20Support%20Him%20%F0%9F%98%89!%20%20Here%20Is%20The%20Bots%20List%20:-%20https://t.me/AsmSafone/173**")]]), reply_to_message_id=safone.message_id)
            await download_msg.delete()
            await trace_msg.edit(f"#MegaDL: Upload Done! \n\n{user_info}")
        # Checking if it's a video
        elif "video" in filemimespotted:
            await download_msg.edit("**Trying To Upload ...**")
            viddura = moviepy.editor.VideoFileClip(f"{magapylol}")
            vidduration = int(viddura.duration)
            thumbnail_path = f"{alreadylol}/thumbnail.jpg"
            subprocess.call(['ffmpeg', '-i', magapylol, '-ss', '00:00:10.000', '-vframes', '1', thumbnail_path])
            safone = await message.reply_video(magapylol, duration=vidduration, thumb=thumbnail_path, progress=progress_for_pyrogram, progress_args=("**Uploading ...** \n", download_msg, start_time), reply_to_message_id=message.message_id)
            await safone.reply_text(f"**Join @AsmSafone! \nThanks For Using Me 😘!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🙌 SHARE 🙌", url=f"https://t.me/share/url?url=**Hey%20Guys!%20%20Check%20Out%20@AsmSafone's%20Bots%20Channel.%20%20Share%20His%20Bots%20And%20Support%20Him%20%F0%9F%98%89!%20%20Here%20Is%20The%20Bots%20List%20:-%20https://t.me/AsmSafone/173**")]]), reply_to_message_id=safone.message_id)
            await download_msg.delete()
            await trace_msg.edit(f"#MegaDL: Upload Done! \n\n{user_info}")
        # Checking if it's a audio
        elif "audio" in filemimespotted:
            await download_msg.edit("**Trying To Upload ...**")
            safone = await message.reply_audio(magapylol, progress=progress_for_pyrogram, progress_args=("**Uploading ...** \n", download_msg, start_time), reply_to_message_id=message.message_id)
            await safone.reply_text(f"**Join @AsmSafone! \nThanks For Using Me 😘!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🙌 SHARE 🙌", url=f"https://t.me/share/url?url=**Hey%20Guys!%20%20Check%20Out%20@AsmSafone's%20Bots%20Channel.%20%20Share%20His%20Bots%20And%20Support%20Him%20%F0%9F%98%89!%20%20Here%20Is%20The%20Bots%20List%20:-%20https://t.me/AsmSafone/173**")]]), reply_to_message_id=safone.message_id)
            await download_msg.delete()
            await trace_msg.edit(f"#MegaDL: Upload Done! \n\n{user_info}")
        # If it's not a image/video or audio it'll reply it as doc
        else:
            await download_msg.edit("**Trying To Upload ...**")
            safone = await message.reply_document(magapylol, progress=progress_for_pyrogram, progress_args=("**Uploading ...** \n", download_msg, start_time), reply_to_message_id=message.message_id)
            await safone.reply_text(f"**Join @AsmSafone! \nThanks For Using Me 😘!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🙌 SHARE 🙌", url=f"https://t.me/share/url?url=**Hey%20Guys!%20%20Check%20Out%20@AsmSafone's%20Bots%20Channel.%20%20Share%20His%20Bots%20And%20Support%20Him%20%F0%9F%98%89!%20%20Here%20Is%20The%20Bots%20List%20:-%20https://t.me/AsmSafone/173**")]]), reply_to_message_id=safone.message_id)
            await download_msg.delete()
            await trace_msg.edit(f"#MegaDL: Upload Done! \n\n{user_info}")
    try:
        shutil.rmtree(basedir + "/" + userpath)
        print("[ MegaDL-Bot ] Successfully Cleaned Temp Download Directory!")
    except Exception as e:
        print(e)
        return
