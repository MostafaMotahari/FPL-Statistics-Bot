from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message
from decouple import config

from src.sql.session import get_db
from src.sql.methods import get_user


@Client.on_message(filters.private & filters.regex("^⚽️ Predictions 🎲$"))
async def prediction_menu(client: Client, message: Message):
    db_session = get_db().__next__()
    user = get_user(db_session, message.from_user.id)

    if config("BOT_PREDICTION_MODE") == "ON":
        if user.phone_number:
            # Here we should send the prediction WebApp.
            await message.reply_text(
                "✅ You can now predict the results of the matches."
            )
            return
        
        await message.reply_text(
            "❌ First, you need to verify your phone number."
            "For this, you can use the **📱 Veify Phone Number** button in the main menu."
        )
        return

    await message.reply_text(
        "❌ Predictions are currently disabled."
    )
    