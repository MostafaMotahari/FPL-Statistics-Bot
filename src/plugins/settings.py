import os

from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from decouple import config

from src.sql.session import get_db
from src.sql.methods import get_all_users
from src.plugins.custom_filters import admin_filter

# Message templates
SETTING_MESSAGE = """
Bot settings:
Power mode: {}

- Users: {}
- Admins: {}
- Banned: {}
"""

@Client.on_message(admin_filter & filters.private & filters.command(["settings"]))
async def settings(client: Client, message: Message):
    await message.reply_text(
        SETTING_MESSAGE.format(
            "⬜️🟩" if config("BOT_POWER_MODE") == "ON" else "🟥⬜️",
            len(get_all_users(get_db().__next__())),
            len([user for user in get_all_users(get_db().__next__()) if user.status == "admin"]),
            len([user for user in get_all_users(get_db().__next__()) if user.status == "banned"]),
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

# TODO this snippet is hardcoded, it should be dynamic
# Power mode snippet
@Client.on_callback_query(filters.regex("power_(on|off)"))
async def power_mode(client: Client, callback_query):
    if callback_query.data == "power_on":
        # Power mode is off, turn it on
        os.environ["BOT_POWER_MODE"] = "ON"

        await callback_query.edit_message_text(
            SETTING_MESSAGE.format(
                "⬜️🟩",
                len(get_all_users(get_db().__next__())),
                len([user for user in get_all_users(get_db().__next__()) if user.status == "admin"]),
                len([user for user in get_all_users(get_db().__next__()) if user.status == "banned"]),
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(
                        "⚡️Power mode⚡️",
                        callback_data="power_off"
                    )],
                ]
            )
        )
    else:
        # Power mode is on, turn it off
        os.environ["BOT_POWER_MODE"] = "OFF"
        
        await callback_query.edit_message_text(
            SETTING_MESSAGE.format(
                "🟥⬜️",
                len(get_all_users(get_db().__next__())),
                len([user for user in get_all_users(get_db().__next__()) if user.status == "admin"]),
                len([user for user in get_all_users(get_db().__next__()) if user.status == "banned"]),
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(
                        "⚡️Power mode⚡️",
                        callback_data="power_on"
                    )],
                ]
            )
        )