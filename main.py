import asyncio
import logging

from aiogram import Bot, Dispatcher
import config

from app.handlers import router
from app.light_handlers import light_router
from app.question_and_answer import qa_router
from database.models import async_main

bot = Bot(token=config.TOKEN)
dp = Dispatcher()

async def main():
    await async_main()
    dp.include_router(router)
    dp.include_router(light_router)
    dp.include_router(qa_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())