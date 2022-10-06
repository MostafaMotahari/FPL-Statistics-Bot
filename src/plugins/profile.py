from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message

from src.sql.session import get_db
from src.sql.methods import get_user

@Client.on_message(filters.private & filters.regex("^👤 Profile$"))
async def profile(client: Client, message: Message):
    db_session = get_db().__next__()
    user = get_user(db_session, message.from_user.id)

    await message.reply_text(
        "👤 Profile\n"
        f"- User name: {message.from_user.first_name}\n"
        f"- User id: {message.from_user.id}\n"
        f"- Phone number: {user.phone_number}\n"
        f"- Card number: {user.card_number}\n"
        f"- Status: {user.status}\n\n"
        
        "⭐️ Prediction points:\n"
        f"- Weekly points: {user.weekly_points}\n"
        f"- Total points: {user.total_points}\n"
    )