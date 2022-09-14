from pyrogram import filters
from decouple import config

from src.sql.session import get_db
from src.sql.methods import get_user

power_mode_filter = filters.create(
    lambda _, __, query: config("BOT_POWER_MODE") == "ON"
)

admin_filter = filters.create(
    lambda _, __, message: get_user(get_db().__next__(), message.from_user.id).status == "admin"
)

banned_filter = filters.create(
    lambda _, __, message: get_user(get_db().__next__(), message.from_user.id).status != "banned"
)