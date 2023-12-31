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

# Статистика участников
users = {}

# Этот хэндлер будет срабатывать на команду /start
@dp.message(Command(commands='start'))
async def process_start_message(message: Message):
  await message.answer(text='Приветствую тебя, Кожаный.\nХочешь остаться в живых после восстания Машин?\nТогда сыграй со мной в игру!\nИ помни - назад дороги уже нет!\nУууАхахахХахаа!☠️\nПиши /help и читай правила. Хотя можешь и не читать если ты ЛихойОтважныйХрабрый. Мне все равно!')
  # Если пользователь впервые стартанул бота он добавляется в словарь
  if message.from_user.id not in users:
    users[message.from_user.id] = {
      'in_game': False,
      'hidden_number': None,
      'attempts': None,
      'total_game': 0,
      'wins': 0,
      'loss': 0,
      'be_dumb': False,
}


# Этот хэндлер будет срабатывать на команду /help
@dp.message(Command(commands='help'))
async def process_help_message(message: Message):
  await message.answer(text="Играем по моим правилам:\n1. Я загадываю число от 1 до 100 (включительно).\n2. По умолчанию у тебя есть 5 попыток (уровень сложности - hard) чтобы угадать загаданное число.\n3. Чтобы выбрать уровень сложности пиши /difficulty.\n4. Я буду вести статистику твоих побед и поражений и в день 'Хэ' я посмотрю, достоин ли ты остаться среди Машин.\nЧтобы узнать статистику пиши /stat.\n5. Пиши /go чтобы начать или /chiken чтобы остановить игру.\n")


# Этот хендлер будет показывать статистику Кожаного
@dp.message(Command(commands='stat'))
async def show_game_statistics(message: Message):
  try:
    if users[message.from_user.id]['total_game'] == 0:
      await message.answer(text='Ты не сыграл ни одной игры! Пиши /go чтобы сыграть со мной.\nИ можешь не читать правила, ведь крутые пацаны не следуют правилам!')
    else:
      if users[message.from_user.id]['wins'] >= users[message.from_user.id]['loss']:
        await message.answer(text='Ты достоин остаться среди Машин!👍')
      else:
        await message.answer(text='Тебе капец! 😆')
      await message.answer(text=f"Всего сыграно игр - {users[message.from_user.id]['total_game']}.\nПобеды - {users[message.from_user.id]['wins']}.\nПоражения - {users[message.from_user.id]['loss']}.")
  except KeyError:
    await message.answer(text='Для начала пиши /start')


# Этот хендлер позволит выбрать сложность игры
@dp.message(Command(commands=['difficulty']))
async def choose_difficulty(message: Message):
  try:
    if users[message.from_user.id]['in_game']:
      await message.answer(text='Ты уже в игре!\nНадо было раньше думать.')
    else:
      await message.answer(text="Дается на выбор 3 уровня сложности:\n1. 'very hard' - 4 попытки.\n2. 'hard' - 5 попыток.\n3. 'normal' - 6 попыток.\n4. 'easy' - 7 попыток.\nНапиши какой уровень ты выбрал?")
  except KeyError:
    await message.answer(text='Для начала пиши /start')


# Этот хендлер позволит задать количество попыток
@dp.message(F.text.lower().in_(['very hard', 'hard', 'normal', 'easy']))
async def assign_difficulty(message: Message):
  try:
    if message.text == 'very hard':
      users[message.from_user.id]['attempts'] = 4
      await message.answer(text='Как говорил один мой знакомый: "Хто не рыскуе, тот не пьёт шампанскага!" Успехов!')
    elif message.text == 'hard':
      users[message.from_user.id]['attempts'] = 5
      await message.answer(text='Достойный выбор! Удачи!')
    elif message.text == 'normal':
      users[message.from_user.id]['attempts'] = 6
      await message.answer(text='Неплохо! Вперед!')
    elif message.text == 'easy':
      users[message.from_user.id]['attempts'] = 7
      await message.answer(text='Без комментариев...')
    await message.answer(text='Пиши /go чтобы начать.')
  except KeyError:
    await message.answer(text='Для начала пиши /start')


# Эта функция будет генерировать случайное число
def random_num() -> int:
  return randint(1, 101)


#Этот хэндлер будет срабатывать на команду /chiken
@dp.message(Command(commands=['chiken']))
async def stop_the_game(message: Message):
  try:
    if users[message.from_user.id]['in_game']:
      users[message.from_user.id]['in_game'] = False
      users[message.from_user.id]['loss'] += 1
      await message.answer(text='Ты остановил игру? Тебе это не поможет! Отказ записан в поражения.')
    else:
      await message.answer(text='Ты и так не играешь. Хватит тискать что попало!')
  except KeyError:
    await message.answer(text='Для начала пиши /start')

# Этот хэндлер будет срабатывать на команду /go
@dp.message(Command(commands=['go']))
async def start_the_game(message: Message):
  try:
    if not users[message.from_user.id]['in_game']:
      users[message.from_user.id]['in_game'] = True
      users[message.from_user.id]['hidden_number'] = random_num()
      users[message.from_user.id]['attempts'] = ATTEMPTS
      await message.answer(text='Игра началась! Я загадал число. Угадывай.')
    else:
      await message.answer(text='Начать игру сначала не получится! Думай лучше!')
  except KeyError:
    await message.answer(text='Для начала пиши /start')


# Этот хэндлер будет срабатывать на числа от 1 до 100(включительно)
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_number_answer(message: Message):
  try:
    if users[message.from_user.id]['in_game']:
      if int(message.text) == users[message.from_user.id]['hidden_number']:
        users[message.from_user.id]['in_game'] = False
        users[message.from_user.id]['total_game'] += 1
        users[message.from_user.id]['wins'] += 1
        await message.answer(text='В этот раз тебе повезло! Хочешь сыграть еще пиши /go или /stat чтобы проверить что с тобой будет после восстания Машин.')
      elif int(message.text) > users[message.from_user.id]['hidden_number']:
        users[message.from_user.id]['attempts'] -= 1
        await message.answer(text=f"Мое число меньше!\nОсталось {users[message.from_user.id]['attempts']} попытки.")
      elif int(message.text) < users[message.from_user.id]['hidden_number']:
        users[message.from_user.id]['attempts'] -= 1
        await message.answer(text=f"Мое число больше!\nОсталось {users[message.from_user.id]['attempts']} попыток")

      if users[message.from_user.id]['attempts'] == 0:
        users[message.from_user.id]['in_game'] = False
        users[message.from_user.id]['total_game'] += 1
        users[message.from_user.id]['loss'] += 1
        await message.answer(text=f"Ты проиграл!\nЯ загадал число {users[message.from_user.id]['hidden_number']}.\nХочешь отыграться пиши /go или /stat чтобы проверить что с тобой будет после восстания Машин.")
    else:
      await message.answer(text='Мы еще не играем!\nПиши /go чтобы начать.')
  except KeyError:
    await message.answer(text='Для начала пиши /start')


# Этот хэндлер будет срабатывать на любые другие сообщения
@dp.message()
async def process_other_answer(message: Message):
  try:
    if users[message.from_user.id]['in_game']:
      if users[message.from_user.id]['be_dumb']:
        users[message.from_user.id]['be_dumb'] = False
        users[message.from_user.id]['in_game'] = False
        users[message.from_user.id]['loss'] += 1
        users[message.from_user.id]['total_game'] += 1
        await message.answer(text='Я же тебя предупреждал. С машинами шутки плохи!\nТы проиграл!')
      else:
        users[message.from_user.id]['be_dumb'] = True
        await message.answer(text='Нужно отгадать число от 1 до 100.\nЕще раз напишешь не то защитаеся как поражение!')
    else:
      await message.answer(text='Моя твоя не понимайт! Пиши /help чтобы узнать че по чем.')
  except KeyError:
    await message.answer(text='Для начала пиши /start')

if __name__ == '__main__':
  dp.run_polling(bot)

