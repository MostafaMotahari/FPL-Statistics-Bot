from collections import Counter
import aiohttp
from PIL import Image, ImageDraw, ImageFont

from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from fpl import FPL
from decouple import config
from prettytable import PrettyTable

# Get leage captains
async def get_captains(league_id: int):

    # Get league data
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        await fpl.login(
            config("FPL_EMAIL"),
            config("FPL_PASSWORD"),
        )

        classic_league = await fpl.get_classic_league(league_id)
        # Export user IDs
        user_ids = [user["entry"] for user in classic_league.standings["results"]]

        # Get user data and captains
        users = [await fpl.get_user(user_id) for user_id in user_ids]

        # Exporting players
        users_picks = [await user.get_picks(6) for user in users]
        all_pick_lists = [pick_list_json[6] for pick_list_json in users_picks]
        # Seperate captains
        captains = []
        for pick_list in all_pick_lists:
            for pick in pick_list:
                captains.append(pick["element"]) if pick["is_captain"] else None

        top_three_captains = Counter(captains).most_common(3)

        # Insert in table
        captains_table = PrettyTable()
        captains_table.add_column("League", [classic_league.league["name"]])

        for captain in top_three_captains:
            captain_player_obj = await fpl.get_player(captain[0])
            captains_table.add_column(captain_player_obj.web_name, [captain[1]])

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
    font = ImageFont.truetype("src/static/cour.ttf", 30)

    margin = int(image.size[1] / 5)
    for index, captains_table in enumerate(leagues_captains_tables):
        draw.text((36, index * margin), str(captains_table), font=font, fill="black")

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