from importlib.util import decode_source
import requests
from PIL import Image, ImageDraw, ImageFont

from decouple import config
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from prettytable import PrettyTable

from src.__main__ import BASE_API_URL
from src.plugins.custom_filters import power_mode_filter, banned_filter

# League data scraper
async def league_scraper(message: Message, league_id: int, standing_page: int = 1):
    # Get league data
    
        # Get classic league from api
    classic_league = requests.get(f"{BASE_API_URL}leagues-classic/{league_id}/standings/?page_standings={standing_page}")
    
    classic_league = classic_league.json()

    # Sort standings data
    standings_table = PrettyTable(["Rank", "Team", "Full Name", "GW", "Points"])
    # standings_table.max_table_width = 63 # Limit the width for image

    for team in classic_league["standings"]["results"]:
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

    # Inline Keyboard
    inline_keyboard = [[]]

    if standing_page != 1:
        inline_keyboard[0].append(InlineKeyboardButton("Previous Page", callback_data=f"{league_id}:{standing_page - 1}"))

    if classic_league["standings"]["has_next"]:
        inline_keyboard[0].append(InlineKeyboardButton("Next Page", callback_data=f"{league_id}:{standing_page + 1}"))

    # Send the league state as new message
    await message.edit_media(
        media=InputMediaPhoto(
            media="src/static/standings.png",

            caption=f"🏆 **{classic_league['league']['name']} Standings**\n"
            f"➕ Created Date: {classic_league['league']['created']}\n"
            f"▶️ Started GW: {classic_league['league']['start_event']}\n"
            f"📃 __Page {standing_page}__",
        ),

        reply_markup=InlineKeyboardMarkup(inline_keyboard) if len(inline_keyboard[0]) > 0 else None
    )

# Choosing a league to scrap
@Client.on_message(power_mode_filter & banned_filter & \
    filters.private & filters.command(["leagues"]))
async def send_leagues(client: Client, message: Message):

    if len(message.text.split(" ")) == 1:
        leagues = config("LEAGUES_ID", cast=lambda v: [s.strip() for s in v.split(',')])

        await client.send_animation(
            chat_id=message.chat.id,
            animation="src/static/loading_gif.gif",
            caption="Please choose one of the following leagues:\n\n",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(league.split("-")[0], callback_data=league.split("-")[1])] for league in leagues
            ])
        )

    elif len(message.text.split(" ")) == 2:
        table_message = await client.send_animation(
            chat_id=message.chat.id,
            animation="src/static/loading_gif.gif",
            caption="Please Wait..."
        )
        await league_scraper(table_message, int(message.text.split(" ")[1]))

    else:
        await message.reply_text("Wrong command format.\n\nUsage: /leagues `[league_id]`")


# Main function that gets league data from fpl api and sort it
@Client.on_callback_query(power_mode_filter & banned_filter & filters.regex("^[0-9]+"))
async def get_league_state(client: Client, callback_query: CallbackQuery):

    league_id = int(callback_query.data.split(":")[0])
    standing_page = 1 if len(callback_query.data.split(":")) == 1 else int(callback_query.data.split(":")[1])

    # Send Waiting message
    await callback_query.message.edit_caption("Please Wait...")

    # Get league data
    await league_scraper(callback_query.message, league_id, standing_page)