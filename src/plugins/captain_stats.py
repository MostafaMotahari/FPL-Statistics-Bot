from collections import Counter
import requests
from PIL import Image, ImageDraw, ImageFont

from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from decouple import config
from prettytable import PrettyTable
from src.__main__ import BASE_API_URL

# Get leage captains
async def get_captains(league_id: int):

    # Get classic league from api
    classic_league = requests.get(f"{BASE_API_URL}leagues-classic/{league_id}/standings/?page_standings=1")
    classic_league = classic_league.json()

    # Export user IDs
    user_ids = [user["entry"] for user in classic_league["standings"]["results"]]

    # Exporting players
    users_picks = [requests.get(f"{BASE_API_URL}entry/{user_id}/event/6/picks/").json() for user_id in user_ids]
    # users_picks = [await user.json() for user in users_picks]

    all_pick_lists = [pick_list_json["picks"] for pick_list_json in users_picks]
    # Seperate captains
    captains = []
    for pick_list in all_pick_lists:
        for pick in pick_list:
            captains.append(pick["element"]) if pick["is_captain"] else None

    top_three_captains = Counter(captains).most_common(3)

    # Insert in table
    captains_table = PrettyTable()
    captains_table.add_column("League", [classic_league["league"]["name"]])

    captain_player_obj = requests.get(f"{BASE_API_URL}bootstrap-static/").json()

    for captain in top_three_captains:
        # captain_player_obj = await captain_player_obj.json()
        captains_table.add_column(captain_player_obj["elements"][captain[0]]["second_name"], [captain[1]])

    return captains_table

# Captains Stats
@Client.on_message(filters.private & filters.command("captainstats"))
async def captain_stats(client: Client, message: Message):

    # Get local leagues ids
    leagues = config("LEAGUES_ID", cast=lambda v: [s.strip() for s in v.split(',')])

    # Get number of captains in each league
    leagues_captains_tables = [await get_captains(int(league_id.split("-")[1])) for league_id in leagues]

    # Draw on picture
    image = Image.open("src/static/captain_table_bg.jpg")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("src/static/cour.ttf", 27)

    margin = int(image.size[1] / 5)
    for index, captains_table in enumerate(leagues_captains_tables):
        draw.text((55, (index * margin) + 30), str(captains_table), font=font, fill="black")

    image.save("src/static/captains_table.png") # Saving the created image

    await client.send_photo(
        chat_id=message.chat.id,
        photo="src/static/captains_table.png",
        caption="🏆 **Captains Stats**\n",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Overall", callback_data="overall_captains")],
            [InlineKeyboardButton("Top 10", callback_data="top10_captains")],
            [InlineKeyboardButton("Iran", callback_data="iran_captains")],
        ])

    )