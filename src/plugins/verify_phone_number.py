from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message

from src.sql.session import get_db
from src.sql.methods import get_user

# ToDo: add an option to change country code from env file or settings.
@Client.on_message(filters.private & filters.contact)
async def verify_phone_number(client: Client, message: Message):

    db_session = get_db().__next__()
    user = get_user(db_session, message.from_user.id)
    if user:
        if user.phone_number:
            await message.reply_text(
                "✅ You already have a phone number associated with your account."
            )
            return

        elif message.contact.phone_number.startswith("+98"):
            user.phone_number = message.contact.phone_number
            db_session.commit()
            await message.reply_text(
                "✅ Your phone number has been successfully verified."
            )
            return

        await message.reply_text(
            "❌ You can only use an Iranian phone number."
        )

    else:
        await message.reply_text(
            "❌ You don't have an account with us."
        )