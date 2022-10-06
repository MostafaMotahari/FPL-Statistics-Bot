from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from src.sql.session import get_db
from src.sql.methods import get_user
from src.sql.models import UserModel


@Client.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    await message.reply_text(
        "Hi! I'm a bot created by @FBI_Coach.\n"
        "I'm created by @Mousiol.\n"
        "I'm a bot that can help you to get the latest stats from the Fantasy Premier League.\n"
        "You can use /help to get the list of commands.\n",
        
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("📊 Stats"), KeyboardButton("⚽️ Predictions 🎲")],
                [KeyboardButton("👤 Profile")],
                [KeyboardButton("📱 Verify Phone Number", True)],
            ],
            resize_keyboard=True
        )
    )

    # Register a user
    db_session = get_db().__next__()

    if get_user(db_session, message.from_user.id) is None:
        db_session.add(UserModel(telegram_id=message.from_user.id))
        db_session.commit()