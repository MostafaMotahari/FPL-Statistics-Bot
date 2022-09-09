from importlib.util import decode_source
import aiohttp
from PIL import Image, ImageDraw, ImageFont

from decouple import config
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from fpl import FPL
from prettytable import PrettyTable

# League data scraper
async def league_scraper(client: Client, chat_id: int, league_id: int):
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
    standings_table = PrettyTable(["Rank", "Team", "Full Name", "GW", "Points"])
    # standings_table.max_table_width = 63 # Limit the width for image

    for team in classic_league["results"]:
        standings_table.add_row([
            team["rank"],
            team["entry_name"],
            team["player_name"],
            team["event_total"],
            team["total"]
        ])

    # Make the league table image
    image = Image.open("src/static/table_bg.jpg")
    # image = Image.new("RGB", (600, (len(classic_league["results"]) * 15) + 200), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("src/static/cour.ttf", 20)
    draw.text((36, 20), str(standings_table), font=font, fill="black")
    image.save("src/static/standings.png") # Saving the created image

    # Send the league state as new message
    await client.send_photo(
        chat_id=chat_id,
        photo="src/static/standings.png",
        caption="**League Standings**\n"
        "__Page 1__",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Previous Page", callback_data="1"),
                InlineKeyboardButton("Next Page", callback_data="1"), 
            ],
        ])
    )

# Choosing a league to scrap
@Client.on_message(filters.private & filters.command(["leagues"]))
async def send_leagues(client: Client, message: Message):

    if len(message.text.split(" ")) == 1:
        leagues = config("LEAGUES_ID", cast=lambda v: [s.strip() for s in v.split(',')])

        await message.reply_text(
            "Please choose one of the following leagues:\n\n",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(league.split("-")[0], callback_data=league.split("-")[1])] for league in leagues
            ])
        )

    elif len(message.text.split(" ")) == 2:
        await message.reply_text("Please Wait...")
        await league_scraper(client, message.chat.id, int(message.text.split(" ")[1]))

    else:
        await message.reply_text("Wront command format.\n\nUsage: /leagues `[league_id]`")


# Main function that gets league data from fpl api and sort it
@Client.on_callback_query(filters.regex("^[0-9]+$"))
async def get_league_state(client: Client, callback_query: CallbackQuery):

    league_id = int(callback_query.data)

    # Delete the message. later we will send the league state as edited message
    await callback_query.message.delete()

    # Get league data
    await league_scraper(client, callback_query.message.chat.id, league_id)