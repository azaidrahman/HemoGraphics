from aiogram import types
from bot import dp

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hello, World!")
