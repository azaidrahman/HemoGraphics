from os import getenv
from dotenv import load_dotenv
import asyncio
import logging, sys

from aiogram import Bot, Dispatcher, types 
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold
from setuptools import Command

# from aiogram.types import (
#     KeyboardButton,
#     Message,
#     ReplyKeyboardMarkup,
#     ReplyKeyboardRemove,
# )

from message_handler import register_handlers

load_dotenv()
TOKEN = getenv("TELEGRAM_TOKEN")
bot = None
if TOKEN is not None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
else:
    logging.error("TELEGRAM_TOKEN not found in environment. Bot cannot start.")
    sys.exit(1)

dp = Dispatcher()
monthly_donation, seasonal_chart, retention_chart = register_handlers(dp,bot)



@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    intro_message = (
        f"Hello, Thevesh (and others)!\n\n"
        "Welcome to the Blood Donation Trends Bot (HemoGraphics). This bot provides insights into blood donation trends. All the data is updated daily! \n\n"
        "You can use the following commands to interact with the bot:\n\n"
        
        f"{hbold('/monthly_donation')}: \nView trends of blood donations in different states. This feature allows you to visualize donation trends on a monthly basis, helping you understand the comparison of numbers from each state.\n"
        
        f"{hbold('/seasonal')}: \nAnalyze seasonal components of blood donation trends for the top 2 and bottom 2 performing (donations) states. Break down the donation data into seasonal trends, trend cycles, and residuals, providing a deeper understanding of the underlying patterns.\n"
        
        f"{hbold('/retention')}: \nExamine donor retention rates and patterns. This command helps you understand how effectively donors are being retained over time, which is crucial for planning and improving donor engagement strategies.\n\n"
        
        f"Click here to print out all the charts immediately! : {hbold('/chart')}"
    )
    await message.answer(intro_message)



async def main() -> None:

    await dp.start_polling(bot)




if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())