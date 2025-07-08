import os
from aiogram import Bot
from typing import Optional

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN", ""))

async def send_message(text: str, user: int, ipfs_link: Optional[str] = None) -> None:
    if ipfs_link:
        ipfs_url = ipfs_link.replace("ipfs://", "https://ipfs.io/ipfs/")
        await bot.send_photo(chat_id=user, photo=ipfs_url, caption=text)
    else:
        await bot.send_message(chat_id=user, text=text)

    return None
