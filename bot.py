import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from config import BOT_TOKEN, POLL_INTERVAL, LOG_LEVEL
from services.storage import Storage
from services.sessions import SessionManager
from handlers.main import register_main
from handlers.downloaders import register_downloader
from handlers.payments import register_payments
from handlers.admin import register_admin
from handlers.ai import register_ai
from handlers.games import register_games
import logging
logging.basicConfig(level=LOG_LEVEL)
async def start():
    session = AiohttpSession()
    bot = Bot(token=BOT_TOKEN, session=session)
    dp = Dispatcher()
    storage = Storage()
    sessions = SessionManager()
    dp["storage"] = storage
    dp["sessions"] = sessions
    register_main(dp)
    register_downloader(dp)
    register_payments(dp)
    register_admin(dp)
    register_ai(dp)
    register_games(dp)
    try:
        await dp.start_polling(bot, polling_timeout=POLL_INTERVAL)
    finally:
        await bot.session.close()
if __name__ == "__main__":
    asyncio.run(start())
