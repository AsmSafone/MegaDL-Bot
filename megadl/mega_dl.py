# (c) @doreamonfans1 
# A Part of MegaDL-Bot <https://github.com/disneyteam77/MegaDL-Bot>

import os
import shutil
import filetype
import moviepy.editor
import time
import asyncio
import logging
import subprocess
import datetime
from mega import Mega
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from hurry.filesize import size
from megadl.progress import progress_for_pyrogram, humanbytes
from megadl.forcesub import handle_force_subscribe
from config import Config

# Logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Mega Client
mega = Mega()
m = mega.login()

# path we gonna give the download
basedir = Config.DOWNLOAD_LOCATION

# Automatic Url Detect (From OneDLBot)
MEGA_REGEX = (r"^((?:https?:)?\/\/)"
              r"?((?:www)\.)"
              r"?((?:mega\.nz))"
              r"(\/)([-a-zA-Z0-9()@:%_\+.~#?&//=]*)([\w\-]+)(\S+)?$")



@Client.on_message(filters.regex(MEGA_REGEX) & filters.private & filters.incoming & ~filters.edited)
async def megadl(bot, message):
    if Config.UPDATES_CHANNEL:
      fsub = await handle_force_subscribe(bot, message)
      if fsub == 400:
        return
    url = message.text
    user = f'[Upload Done!](tg://user?id={message.from_user.id})'
    userpath = str(message.from_user.id)
    alreadylol = basedir + "/" + userpath
    if not os.path.isdir(alreadylol):
        megadldir = os.makedirs(alreadylol)
    try:
        download_msg = await message.reply_text(text=f"**Downloading:** `{url}` \n\nThis Process May Take Some Time 🤷‍♂️!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancel Mega DL", callback_data="cancel")]]), reply_to_message_id=message.message_id)
        ist = (datetime.datetime.utcnow() + datetime.timedelta(minutes=30, hours=5)).strftime("%d/%m/%Y, %H:%M:%S")
        bst = (datetime.datetime.utcnow() + datetime.timedelta(minutes=00, hours=6)).strftime("%d/%m/%Y, %H:%M:%S")
        now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
        download_start = await bot.send_message(Config.LOG_CHANNEL, f"**Bot Become Busy Now !!** \n\nDownload Started at `{now}`", parse_mode="markdown")
        magapylol = m.download_url(url, alreadylol)
        await download_msg.edit("**Downloaded Successfully 😉!**")
    except Exception as e:
        await download_msg.edit(f"**Error:** `{e}`")
        ist = (datetime.datetime.utcnow() + datetime.timedelta(minutes=30, hours=5)).strftime("%d/%m/%Y, %H:%M:%S")
        bst = (datetime.datetime.utcnow() + datetime.timedelta(minutes=00, hours=6)).strftime("%d/%m/%Y, %H:%M:%S")
        now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
        await bot.send_message(Config.LOG_CHANNEL, f"**Bot Become Free Now !!** \n\nProcess Done at `{now}`", parse_mode="markdown")
        await download_start.delete()
        shutil.rmtree(basedir + "/" + userpath)
        return
    lmaocheckdis = os.stat(alreadylol).st_size
    readablefilesize = size(lmaocheckdis) # Convert Bytes into readable size
    if lmaocheckdis > Config.TG_MAX_SIZE:
        await download_msg.edit(f"**Detected File Size:** `{readablefilesize}` \n**Accepted File Size:** `2.0 GB` \n\nOops! File Is Too Large To Send In Telegram 🤒!")
        ist = (datetime.datetime.utcnow() + datetime.timedelta(minutes=30, hours=5)).strftime("%d/%m/%Y, %H:%M:%S")
        bst = (datetime.datetime.utcnow() + datetime.timedelta(minutes=00, hours=6)).strftime("%d/%m/%Y, %H:%M:%S")
        now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
        await bot.send_message(Config.LOG_CHANNEL, f"**Bot Become Free Now !!** \n\nProcess Done at `{now}`", parse_mode="markdown")
        await download_start.delete()
        shutil.rmtree(basedir + "/" + userpath)
        return
    else:
        start_time = time.time()
        guessedfilemime = filetype.guess(f"{magapylol}") # Detecting file type
        if not guessedfilemime.mime:
            await download_msg.edit("**Trying To Upload ...** \n**Can't Get File Type, Sending as Document!")
            await message.reply_document(magapylol, progress=progress_for_pyrogram, progress_args=("**Uploading ...**", download_msg, start_time), reply_to_message_id=message.message_id)
            await download_msg.edit(text=f"**{user}\nThanks For Using Me 😘!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🙌 SHARE 🙌", url=f"https://t.me/share/url?url=**Hey%20Guys!%20%20Check%20Out%20@AsmSafone's%20Bots%20Channel.%20%20Share%20His%20Bots%20And%20Support%20Him%20%F0%9F%98%89!%20%20Here%20Is%20The%20Bots%20List%20:-%20https://t.me/AsmSafone/173**")]]))
            ist = (datetime.datetime.utcnow() + datetime.timedelta(minutes=30, hours=5)).strftime("%d/%m/%Y, %H:%M:%S")
            bst = (datetime.datetime.utcnow() + datetime.timedelta(minutes=00, hours=6)).strftime("%d/%m/%Y, %H:%M:%S")
            now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
            await bot.send_message(Config.LOG_CHANNEL, f"**Bot Become Free Now !!** \n\nProcess Done at `{now}`", parse_mode="markdown")
            await download_start.delete()
            shutil.rmtree(basedir + "/" + userpath)
            return
        filemimespotted = guessedfilemime.mime
        # Checking If it's a gif
        if "image/gif" in filemimespotted:
            await download_msg.edit("**Trying To Upload ...**")
            await message.reply_animation(magapylol, progress=progress_for_pyrogram, progress_args=("**Uploading ...**", download_msg, start_time), reply_to_message_id=message.message_id)
            await download_msg.edit(text=f"**{user}\nThanks For Using Me 😘!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🙌 SHARE 🙌", url=f"https://t.me/share/url?url=**Hey%20Guys!%20%20Check%20Out%20@AsmSafone's%20Bots%20Channel.%20%20Share%20His%20Bots%20And%20Support%20Him%20%F0%9F%98%89!%20%20Here%20Is%20The%20Bots%20List%20:-%20https://t.me/AsmSafone/173**")]]))
            ist = (datetime.datetime.utcnow() + datetime.timedelta(minutes=30, hours=5)).strftime("%d/%m/%Y, %H:%M:%S")
            bst = (datetime.datetime.utcnow() + datetime.timedelta(minutes=00, hours=6)).strftime("%d/%m/%Y, %H:%M:%S")
            now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
            await bot.send_message(Config.LOG_CHANNEL, f"**Bot Become Free Now !!** \n\nProcess Done at `{now}`", parse_mode="markdown")
            await download_start.delete()
            shutil.rmtree(basedir + "/" + userpath)
            return
        # Checking if it's a image
        if "image" in filemimespotted:
            await download_msg.edit("**Trying To Upload ...**")
            await message.reply_photo(magapylol, progress=progress_for_pyrogram, progress_args=("**Uploading ...**", download_msg, start_time), reply_to_message_id=message.message_id)
            await download_msg.edit(text=f"**{user}\nThanks For Using Me 😘!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🙌 SHARE 🙌", url=f"https://t.me/share/url?url=**Hey%20Guys!%20%20Check%20Out%20@AsmSafone's%20Bots%20Channel.%20%20Share%20His%20Bots%20And%20Support%20Him%20%F0%9F%98%89!%20%20Here%20Is%20The%20Bots%20List%20:-%20https://t.me/AsmSafone/173**")]]))
            ist = (datetime.datetime.utcnow() + datetime.timedelta(minutes=30, hours=5)).strftime("%d/%m/%Y, %H:%M:%S")
            bst = (datetime.datetime.utcnow() + datetime.timedelta(minutes=00, hours=6)).strftime("%d/%m/%Y, %H:%M:%S")
            now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
            await bot.send_message(Config.LOG_CHANNEL, f"**Bot Become Free Now !!** \n\nProcess Done at `{now}`", parse_mode="markdown")
            await download_start.delete()
        # Checking if it's a video
        elif "video" in filemimespotted:
            await download_msg.edit("**Trying To Upload ...**")
            viddura = moviepy.editor.VideoFileClip(f"{magapylol}")
            vidduration = int(viddura.duration)
            thumbnail_path = f"{alreadylol}/thumbnail.jpg"
            subprocess.call(['ffmpeg', '-i', magapylol, '-ss', '00:00:10.000', '-vframes', '1', thumbnail_path])
            await message.reply_video(magapylol, duration=vidduration, thumb=thumbnail_path, progress=progress_for_pyrogram, progress_args=("**Uploading ...** \n", download_msg, start_time), reply_to_message_id=message.message_id)
            await download_msg.edit(text=f"**{user}\nThanks For Using Me 😘!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🙌 SHARE 🙌", url=f"https://t.me/share/url?url=**Hey%20Guys!%20%20Check%20Out%20@AsmSafone's%20Bots%20Channel.%20%20Share%20His%20Bots%20And%20Support%20Him%20%F0%9F%98%89!%20%20Here%20Is%20The%20Bots%20List%20:-%20https://t.me/AsmSafone/173**")]]))
            ist = (datetime.datetime.utcnow() + datetime.timedelta(minutes=30, hours=5)).strftime("%d/%m/%Y, %H:%M:%S")
            bst = (datetime.datetime.utcnow() + datetime.timedelta(minutes=00, hours=6)).strftime("%d/%m/%Y, %H:%M:%S")
            now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
            await bot.send_message(Config.LOG_CHANNEL, f"**Bot Become Free Now !!** \n\nProcess Done at `{now}`", parse_mode="markdown")
            await download_start.delete()
        # Checking if it's a audio
        elif "audio" in filemimespotted:
            await download_msg.edit("**Trying To Upload ...**")
            await message.reply_audio(magapylol, progress=progress_for_pyrogram, progress_args=("**Uploading ...**", download_msg, start_time), reply_to_message_id=message.message_id)
            await download_msg.edit(text=f"**{user}\nThanks For Using Me 😘!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🙌 SHARE 🙌", url=f"https://t.me/share/url?url=**Hey%20Guys!%20%20Check%20Out%20@AsmSafone's%20Bots%20Channel.%20%20Share%20His%20Bots%20And%20Support%20Him%20%F0%9F%98%89!%20%20Here%20Is%20The%20Bots%20List%20:-%20https://t.me/AsmSafone/173**")]]))
            ist = (datetime.datetime.utcnow() + datetime.timedelta(minutes=30, hours=5)).strftime("%d/%m/%Y, %H:%M:%S")
            bst = (datetime.datetime.utcnow() + datetime.timedelta(minutes=00, hours=6)).strftime("%d/%m/%Y, %H:%M:%S")
            now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
            await bot.send_message(Config.LOG_CHANNEL, f"**Bot Become Free Now !!** \n\nProcess Done at `{now}`", parse_mode="markdown")
            await download_start.delete()
        # If it's not a image/video or audio it'll reply it as doc
        else:
            await download_msg.edit("**Trying To Upload ...**")
            await message.reply_document(magapylol, progress=progress_for_pyrogram, progress_args=("**Uploading ...**", download_msg, start_time), reply_to_message_id=message.message_id)
            await download_msg.edit(text=f"**{user}\nThanks For Using Me 😘!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🙌 SHARE 🙌", url=f"https://t.me/share/url?url=**Hey%20Guys!%20%20Check%20Out%20@AsmSafone's%20Bots%20Channel.%20%20Share%20His%20Bots%20And%20Support%20Him%20%F0%9F%98%89!%20%20Here%20Is%20The%20Bots%20List%20:-%20https://t.me/AsmSafone/173**")]]))
            ist = (datetime.datetime.utcnow() + datetime.timedelta(minutes=30, hours=5)).strftime("%d/%m/%Y, %H:%M:%S")
            bst = (datetime.datetime.utcnow() + datetime.timedelta(minutes=00, hours=6)).strftime("%d/%m/%Y, %H:%M:%S")
            now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
            await bot.send_message(Config.LOG_CHANNEL, f"**Bot Become Free Now !!** \n\nProcess Done at `{now}`", parse_mode="markdown")
            await download_start.delete()
    try:
        shutil.rmtree(basedir + "/" + userpath)
        print("Successfully Removed Downloaded Files and Folders!")
    except Exception as e:
        print(e)
        return
