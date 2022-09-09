from pyrogram import filters
from pyrogram.client import Client


@Client.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    await message.reply_text(
        "Hi! I'm a bot created by @FBI_Coach.\n"
        "I'm created by @Mousiol.\n"
        "I'm a bot that can help you to get the latest stats from the Fantasy Premier League.\n"
        "You can use /help to get the list of commands.\n")