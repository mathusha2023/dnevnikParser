from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import logging
import os
import config
from config import DATABASE_FILE
from handlers import main_router


async def main():
    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode="html"))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(main_router)
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    except asyncio.exceptions.CancelledError:
        logging.info("The polling cycle was interrupted")


if __name__ == "__main__":

    # создаем пустой файл базы данных, если его не существует
    if not os.path.exists("data.json"):
        with open(DATABASE_FILE, "w") as file:
            file.write("{}")

    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())