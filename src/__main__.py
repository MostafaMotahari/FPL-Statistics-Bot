""""This files is the main file of the bot"""
import sys

from pyrogram.client import Client
from decouple import config

from src.sql.base_class import Base
from src.sql.session import engine
from src.sql.migrations import make_migrations

PLUGINS = dict(root='src/plugins')
BASE_API_URL = "https://fantasy.premierleague.com/api/"

app = Client(
    "FplBot",
    api_id=config("API_ID"),
    api_hash=config("API_HASH"),
    bot_token=config("BOT_TOKEN"),
    plugins=PLUGINS
)

if __name__ == "__main__":
    # Make migrations
    if len(sys.argv) == 2:
        if sys.argv[1] == "migrate":
            # Create tables
            Base.metadata.create_all(bind=engine)
            make_migrations()
            print("Migrations done!")
        else:
            print("Invalid argument!")

    # Run the bot
    app.run()