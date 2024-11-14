import asyncio
import time
import logging
import os
import sys


from decouple import config
from aiogram import Bot, Dispatcher, types
from app.handlers import router_main


async def main():
    bot = Bot(token=config('BOT_TOKEN'))
    await bot.delete_webhook()
    dp = Dispatcher()
    dp.include_router(router_main)
    await dp.start_polling(bot, polling_timeout=100)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
        print("Bot start")
    except KeyboardInterrupt:
        print('Bot stop')
    except Exception as e:
        print(e)



