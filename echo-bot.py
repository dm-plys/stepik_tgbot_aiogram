from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from bot_token import bot_token

BOT_TOKEN = bot_token

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Этот хэндлер будет срабатывать на команду /start
async def process_start_command(message: Message):
  await message.answer(text='Привет!\nМеня зовут Повторяшка\nЕсли хочешь узнать что я могу напиши "/info"')

# Этот хэндлер будет срабатывать на команду /info
async def process_info_command(message: Message):
  await message.answer(text='Я отвечаю тебе твоими сообщениями. Вот такое я абышто!')

# Этот хэндлер будет срабатывать на любые сообщения кроме /start и /info
async def send_echo(message: Message):
  await message.reply(text=message.text)

# Регистрируем хэндлеры
dp.message.register(process_start_command, Command(commands=['start']))
dp.message.register(process_info_command, Command(commands=['info']))
dp.message.register(send_echo)

if __name__ == '__main__':
  dp.run_polling(bot)