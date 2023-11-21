from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from bot_token import bot_token

BOT_TOKEN = bot_token
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
  await message.answer(text='Привет!\nМеня зовут Повторяшка\nЕсли хочешь узнать что я могу напиши "/info"')

@dp.message(Command(commands=['info']))
async def process_info_command(message: Message):
  await message.answer(text='Я отвечаю тебе твоими сообщениями. Вот такое я абышто!')

@dp.message()
async def send_echo(message: Message):
  await message.reply(text=message.text)

if __name__ == '__main__':
  dp.run_polling(bot)