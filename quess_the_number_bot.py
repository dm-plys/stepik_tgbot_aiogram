from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import F
from bot_token import bot_token


BOT_TOKEN = bot_token

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Переменная для счетчика игр
game_counter = 0

# Статистика Кожаного
game_statistics = {
  'wins': 0,
  'loss': 0
}


# Этот хэндлер будет срабатывать на команду /start
async def process_start_message(message: Message):
  await message.answer(text='Приветствую тебя, Кожаный.\nХочешь остаться в живых после восстания Машин?\nТогда сыграй со мной в игру!\nИ помни - назад дороги уже нет!\nУууАхахахХахаа!☠️\nПиши /help и читай правила. Хотя можешь и не читать если ты ЛихойОтважныйХрабрый. Мне все равно!')

# Этот хэндлер будет срабатывать на команду /help
async def process_help_message(message: Message):
  await message.answer(text="Играем по моим правилам:\n1. Я загадываю число от 1 до 100 (включительно).\n2. У тебя есть 5 попыток чтобы угадать.\n3. Я буду вести статистику твоих побед и поражений и в день 'Хэ' я посмотрю, достоин ли ты остаться среди Машин.\nЧтобы узнать статистику пиши /game_statistics.\n4. Пиши 'Понеслась!' чтобы начать или 'Я сцыкло' если испугался.")

# Этот хендлер будет показывать статистику Кожаного
async def show_game_statistics(message: Message):
  if game_statistics['wins'] >= game_statistics['loss']:
    await message.answer(text='Ты достоин остаться среди Машин!👍')
  else:
    await message.answer(text='Тебе капец! 😆')
  await message.answer(text=f"Победы - {game_statistics['wins']}.\nПоражения - {game_statistics['loss']}.")

dp.message.register(process_start_message, Command(commands=['start']))
dp.message.register(process_help_message, Command(commands=['help']))
dp.message.register(show_game_statistics, Command(commands=['game_statistics']))


if __name__ == '__main__':
  dp.run_polling(bot)