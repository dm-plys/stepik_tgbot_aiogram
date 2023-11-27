from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from bot_token import bot_token
from random import randint


BOT_TOKEN = bot_token

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Переменная счетчик попыток
ATTEMPTS = 5

# Статистика Кожаного
user = {'in_game': False,
        'hidden_number': None,
        'attempts': None,
        'total_game': 0,
        'wins': 0,
        'loss': 0
}

# Этот хэндлер будет срабатывать на команду /start
@dp.message(Command(commands='start'))
async def process_start_message(message: Message):
  await message.answer(text='Приветствую тебя, Кожаный.\nХочешь остаться в живых после восстания Машин?\nТогда сыграй со мной в игру!\nИ помни - назад дороги уже нет!\nУууАхахахХахаа!☠️\nПиши /help и читай правила. Хотя можешь и не читать если ты ЛихойОтважныйХрабрый. Мне все равно!')

# Этот хэндлер будет срабатывать на команду /help
@dp.message(Command(commands='help'))
async def process_help_message(message: Message):
  await message.answer(text="Играем по моим правилам:\n1. Я загадываю число от 1 до 100 (включительно).\n2. У тебя есть 5 попыток чтобы угадать.\n3. Я буду вести статистику твоих побед и поражений и в день 'Хэ' я посмотрю, достоин ли ты остаться среди Машин.\nЧтобы узнать статистику пиши /stat.\n4. Пиши /go чтобы начать или /chiken чтобы остановить игру.")

# Этот хендлер будет показывать статистику Кожаного
@dp.message(Command(commands='stat'))
async def show_game_statistics(message: Message):
  if user['wins'] >= user['loss']:
    await message.answer(text='Ты достоин остаться среди Машин!👍')
  else:
    await message.answer(text='Тебе капец! 😆')
  await message.answer(text=f"Победы - {user['wins']}.\nПоражения - {user['loss']}.")

# Эта функция будет генерировать случайное число
def random_num() -> int:
  return randint(1, 101)

#Этот хэндлер будет срабатывать на команду /chiken
@dp.message(Command(commands=['chiken']))
async def stop_the_game(message: Message):
  if user['in_game']:
    user['in_game'] = False
    user['loss'] += 1
    await message.answer(text='Ты остановил игру? Тебе это не поможет! Отказ записан в поражения.')
  else:
    await message.answer(text='Ты и так не играешь. Хватит тискать что попало!')

# Этот хэндлер будет срабатывать на команду /go
@dp.message(Command(commands=['go']))
async def start_the_game(message: Message):
  if not user['in_game']:
    user['in_game'] = True
    user['hidden_number'] = random_num()
    user['attempts'] = ATTEMPTS
    await message.answer(text='Игра началась! Я загадал число. Угадывай.')
  else:
    await message.answer(text='Начать игру сначала не получится! Думай лучше!')








if __name__ == '__main__':
  dp.run_polling(bot)

