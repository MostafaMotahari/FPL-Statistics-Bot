from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message

# Send help message
@Client.on_message(filters.private & filters.command(["help"]) & filters.regex("^📊 Stats$"))
async def help(client: Client, message: Message):
    await message.reply_text(
        "Hi! I'm a bot created by @FBI_Coach.\n"
        "I'm created by @Mousiol.\n"
        "I'm a bot that can help you to get the latest stats from the Fantasy Premier League.\n"
        "You can use /help to get the list of commands.\n"
        "You can use /leagues to get the list of leagues.\n"
        "You can use /league_standings to get the standings of a league.\n"
        "You can use /league_fixtures to get the fixtures of a league.\n"
        "You can use /league_top_scorer to get the top scorer of a league.\n"
        "You can use /league_top_assists to get the top assists of a league.\n"
        "You can use /league_top_goals to get the top goals of a league.\n"
        "You can use /league_top_clean_sheets to get the top clean sheets of a league.\n"
        "You can use /league_top_goals_conceded to get the top goals conceded of a league.\n"
        "You can use /league_top_own_goals to get the top own goals of a league.\n"
        "You can use /league_top_penalties_saved to get the top penalties saved of a league.\n"
        "You can use /league_top_penalties_missed to get the top penalties missed of a league.\n"
        "You can use /league_top_yellow_cards to get the top yellow cards of a league.\n"
        "You can use /league_top_red_cards to get the top red cards of a league.\n"
        "You can use /league_top_saves to get the top saves of a league.\n"
        "You can use /league_top_bonus to get the top bonus of a league.\n"
        "You can use /league_top_bps to get the top bps of a league.\n"
    )