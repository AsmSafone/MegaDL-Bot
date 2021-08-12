# (c) Asm Safone
# A Part of MegaDL-Bot <https://github.com/AsmSafone/MegaDL-Bot>

import os
import math
import time
import shutil
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from megadl.forcesub import handle_force_subscribe
from config import Config, TEXT


@Client.on_message(filters.command("help") & filters.private & filters.incoming)
async def help(bot, message, cb=False):
    if Config.UPDATES_CHANNEL:
      fsub = await handle_force_subscribe(bot, message)
      if fsub == 400:
        return
    me = await bot.get_me()
    button = [[
        InlineKeyboardButton(f'🏠 HOME', callback_data='back'),
        InlineKeyboardButton(f'ABOUT 👨', callback_data='about')
        ],[
        InlineKeyboardButton(f'📦 SOURCE', url='https://github.com/AsmSafone/MegaDL-Bot'),
        InlineKeyboardButton(f'CLOSE 🔐', callback_data='close')
        ]]
    reply_markup = InlineKeyboardMarkup(button)
    if cb:
        await message.message.edit(
            text=TEXT.HELP_USER.format(bot_name=me.mention(style='md')),
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )
    else:
        await message.reply_text(
            text=TEXT.HELP_USER.format(bot_name=me.mention(style='md')),
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            quote=True
        )


@Client.on_message(filters.command("start") & filters.private & filters.incoming)
async def start(bot, message, cb=False):
    if Config.UPDATES_CHANNEL:
      fsub = await handle_force_subscribe(bot, message)
      if fsub == 400:
        return
    me = await bot.get_me()
    owner = await bot.get_users(Config.OWNER_ID)
    owner_username = owner.username if owner.username else 'AsmSafone'
    button = [[
        InlineKeyboardButton(f'💡 HELP', callback_data='help'),
        InlineKeyboardButton(f'ABOUT 👨', callback_data="about")
        ],[
        InlineKeyboardButton(f'📦 SOURCE', url='https://github.com/AsmSafone/MegaDL-Bot'),
        InlineKeyboardButton(f'CLOSE 🔐', callback_data="close")
        ]]
    reply_markup = InlineKeyboardMarkup(button)
    if cb:
        await message.message.edit(
            text=TEXT.START_TEXT.format(user_mention=message.from_user.mention, bot_name=me.mention(style='md'), bot_owner=owner.mention(style="md")), 
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )
    else:
        await message.reply_text(
            text=TEXT.START_TEXT.format(user_mention=message.from_user.mention, bot_name=me.mention(style='md'), bot_owner=owner.mention(style="md")), 
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            quote=True
        ) 


@Client.on_message(filters.command("about") & filters.private & filters.incoming)
async def about(bot, message, cb=False):
    if Config.UPDATES_CHANNEL:
      fsub = await handle_force_subscribe(bot, message)
      if fsub == 400:
        return
    me = await bot.get_me()
    button = [[
        InlineKeyboardButton(f'🏠 HOME', callback_data='back'),
        InlineKeyboardButton(f'HELP 💡', callback_data='help')
        ],[
        InlineKeyboardButton(f'📦 SOURCE', url='https://github.com/AsmSafone/MegaDL-Bot'),
        InlineKeyboardButton(f'CLOSE 🔐', callback_data="close")
        ]]
    reply_markup = InlineKeyboardMarkup(button)
    if cb:
        await message.message.edit(
            text=TEXT.ABOUT.format(bot_name=me.mention(style='md')),
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )
    else:
        await message.reply_text(
            text=TEXT.ABOUT.format(bot_name=me.mention(style='md')),
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            quote=True
        )


@Client.on_callback_query(filters.regex('^help$'))
async def help_cb(bot, message):
    await message.answer()
    await help(bot, message, True)


@Client.on_callback_query(filters.regex('^close$'))
async def close_cb(bot, message):
    await message.message.delete()
    await message.message.reply_to_message.delete()


@Client.on_callback_query(filters.regex('^back$'))
async def back_cb(bot, message):
    await message.answer()
    await start(bot, message, True)


@Client.on_callback_query(filters.regex('^about$'))
async def about_cb(bot, message):
    await message.answer()
    await about(bot, message, True)


@Client.on_callback_query(filters.regex('^refreshmeh$'))
async def refreshmeh_cb(bot, message):
    if Config.UPDATES_CHANNEL:
        invite_link = await bot.create_chat_invite_link(int(Config.UPDATES_CHANNEL))
        try:
            user = await bot.get_chat_member(int(Config.UPDATES_CHANNEL), message.from_user.id)
            if user.status == "kicked":
                await message.message.edit(
                    text="Sorry Sir, You are Banned. Contact My [Support Group](https://t.me/safothebot).",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await message.message.edit(
                text="**You Still Didn't Join ☹️, Please Join My Updates Channel To Use Me!**\n\nDue to Overload, Only Channel Subscribers Can Use Me!",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🤖 Join Updates Channel 🤖", url=invite_link.invite_link)
                        ],
                        [
                            InlineKeyboardButton("🔄 Refresh 🔄", callback_data="refreshmeh")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await message.message.edit(
                text="Something Went Wrong. Contact My [Support Group](https://t.me/safothebot).",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    await message.answer()
    await start(bot, message, True)



@Client.on_callback_query(filters.regex('^cancel_mega$'))
async def cancel_cb(bot, message):
    basedir = Config.DOWNLOAD_LOCATION
    userpath = str(message.from_user.id)
    try:
        await message.answer(
            "Trying To Cancel... 🤒",
                show_alert=True
            )
        await asyncio.sleep(5)
        shutil.rmtree(basedir + "/" + userpath)
        await message.message.delete()
        await message.message.reply_text("**Process Cancelled By User 😡!**", reply_to_message_id=message.message_id)
    except Exception as e:
        await print(e)
        await message.answer(
            "Can't Cancel Right Now! 😡",
                show_alert=True
            )
