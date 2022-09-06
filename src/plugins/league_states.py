from importlib.util import decode_source
import aiohttp
from PIL import Image, ImageDraw, ImageFont

from decouple import config
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from fpl import FPL
from prettytable import PrettyTable


@Client.on_message(filters.private & filters.command(["leagues"]))
async def send_leagues(client: Client, message: Message):

    leagues = config("LEAGUES_ID", cast=lambda v: [s.strip() for s in v.split(',')])

    await message.reply_text(
        "Please choose one of the following leagues:\n\n",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(league.split("-")[0], callback_data=league.split("-")[1])] for league in leagues
        ])
    )


@Client.on_callback_query(filters.regex("^[0-9]+$"))
async def get_league_state(client: Client, callback_query: Message):

    league_id = int(callback_query.data)

    # Get league data
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        await fpl.login(
            config("FPL_EMAIL"),
            config("FPL_PASSWORD"),
        )
        classic_league = await fpl.get_classic_league(league_id)

    classic_league = await classic_league.get_standings(page=1, page_new_entries=1, phase=1)

    # Sort standings data
    standings_table = PrettyTable(["Rank", "Team", "Full Name", "Points"])
    standings_table.max_table_width = 600

    for team in classic_league["results"]:
        standings_table.add_row([
            team["rank"],
            team["entry_name"],
            team["player_name"],
            team["event_total"]
        ])

    print(standings_table.__dict__)

    # Delete the message. later we will send the league state as edited message
    await callback_query.message.delete()

    image = Image.new("RGB", (600, 400), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("FreeMono.ttf", 15)
    draw.text((10, 10), str(standings_table), font=font, fill="black")
    image.save("src/media/standings.png")

    # Send the league state as new message
    await client.send_photo(
        chat_id=callback_query.from_user.id,
        photo="src/media/standings.png",
        caption="Table",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Next Page", callback_data=callback_query.data), 
                InlineKeyboardButton("Previous Page", callback_data=callback_query.data)
            ],
        ])
    )