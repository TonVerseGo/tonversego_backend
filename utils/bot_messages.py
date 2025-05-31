import os
from aiogram import Bot

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))

async def send_message(text: str, user: int):
    await bot.send_message(user, text)