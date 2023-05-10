import asyncio

from src.bot import bot

def run_bot():
    asyncio.run(bot.infinity_polling())