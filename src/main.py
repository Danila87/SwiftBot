import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from routers import (
    commands_router,
    events_router,
    messages_router,
    admin_commands_router
)

from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=BOT_TOKEN
)

dp = Dispatcher(
    storage=MemoryStorage(),
)

dp.include_routers(
    commands_router,
    admin_commands_router,
    events_router,
    # messages_router
)


async def main():
    logging.info("Бот запущен")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())