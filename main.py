import asyncio
import logging

from aiogram import Bot, Dispatcher
import config

from app.handlers import router
from database.models import async_main

bot = Bot(token=config.TOKEN)
dp = Dispatcher()

async def main():
    await async_main()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())