from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from decouple import config

from src.sql.session import get_db
from src.sql.methods import get_all_users

# Message templates
SETTING_MESSAGE = """
Bot settings:
Power mode: {}

- Users: {}
- Admins: {}
- Banned: {}
"""

@Client.on_message(filters.private & filters.command(["settings"]))
async def settings(client: Client, message: Message):
    await message.reply_text(
        SETTING_MESSAGE.format(
            "⬜️🟩" if config("BOT_POWER_MODE") == "ON" else "🟥⬜️",
            len(get_all_users(get_db().__next__())),
            "0",
            "0",
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(
                    "⚡️Power mode⚡️",
                    callback_data="power_off" if config("BOT_POWER_MODE") == "ON" else "power_on"
                )],
            ]
        )    
    )