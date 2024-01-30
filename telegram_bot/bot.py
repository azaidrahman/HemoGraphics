from aiohttp import web
from os import getenv
from dotenv import load_dotenv
import asyncio

from aiogram import Bot, Dispatcher, Router, types
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

load_dotenv()
TOKEN = getenv("TELEGRAM_TOKEN")
bot = None
if TOKEN is not None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

async def main():
    global bot
    bot = Bot(TOKEN, parse_mode=types.ParseMode.HTML)  # Initialize bot
    dp = Dispatcher()

    @dp.message(commands=['hello'])
    async def send_hello(message: types.Message):
        group_chat_id = 'your_group_chat_id'  # Replace with your actual group chat ID
        await bot.send_message(group_chat_id, "Hello, World!")

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())