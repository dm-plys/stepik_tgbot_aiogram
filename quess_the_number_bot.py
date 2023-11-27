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
        'loss': 0,
        'be_dumb': False
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

# Этот хэндлер будет срабатывать на числа от 1 до 100(включительно)
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_number_answer(message: Message):
  if user['in_game']:
    if int(message.text) == user['hidden_number']:
      user['in_game'] = False
      user['total_game'] += 1
      user['wins'] += 1
      await message.answer(text='В этот раз тебе повезло! Сыграем еще?')
    elif int(message.text) > user['hidden_number']:
      user['attempts'] -= 1
      await message.answer(text=f"Мое число меньше!\nОсталось {user['attempts']} попытки.")
    elif int(message.text) < user['hidden_number']:
      user['attempts'] -= 1
      await message.answer(text=f"Мое число больше!\nОсталось {user['attempts']} попыток")

    if user['attempts'] == 0:
      user['in_game'] = False
      user['total_game'] += 1
      user['loss'] += 1
      await message.answer(text=f"Ты проиграл!\nЯ загадал число {user['hidden_number']}.\nХочешь отыграться пиши /go или /stat чтобы проверить что с тобой будет после восстания Машин.")
  else:
    await message.answer(text='Мы еще не играем!\nПиши /go чтобы начать.')

# Этот хэндлер будет срабатывать на любые другие сообщения
@dp.message()
async def process_other_answer(message: Message):
  if user['in_game']:
    if user['be_dumb']:
      user['be_dumb'] = False
      user['in_game'] = False
      user['loss'] += 1
      user['total_game'] += 1
      await message.answer(text='Я же тебя предупреждал. С машинами шутки плохи!\nТы проиграл!')
    else:
      user['be_dumb'] = True
      await message.answer(text='Нужно отгадать число от 1 до 100.\nЕще раз напишешь не то защитаеся как поражение!')
  else:
    await message.answer(text='Моя твоя не понимайт! Пиши /help чтобы узнать че по чем.')







if __name__ == '__main__':
  dp.run_polling(bot)

