from aiohttp import web
from os import getenv
from dotenv import load_dotenv

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

async def on_startup(app: web.Application):
    webhook_url = 'https://your-cloud-function-url/hook'  # Replace with your Cloud Function URL
    await bot.set_webhook(webhook_url)

async def on_shutdown(app: web.Application):
    await bot.delete_webhook()

async def main():
    dp = Dispatcher()

    @dp.message(Command("hello"))
    async def send_hello(message: types.Message):
        current_chat_id = message.chat.id
        await bot.send_message(current_chat_id, "Hello, World!")

    app = web.Application()
    SimpleRequestHandler(dp, bot).register(app, path="/hook")
    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_shutdown)
    return app

if __name__ == "__main__":
    # For local testing, you might use web.run_app
    # For deployment, you'll use the server's method to run the app.
    web.run_app(main(), host='localhost', port=3000)