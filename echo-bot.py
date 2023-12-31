from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import ContentType
from aiogram import F
from bot_token import bot_token

BOT_TOKEN = bot_token

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Этот хэндлер(обработчик) будет срабатывать на команду /start
async def process_start_command(message: Message):
  await message.answer(text='Привет!\nМеня зовут Повторяшка\nЕсли хочешь узнать что я могу напиши "/info"')

# Этот хэндлер(обработчик) будет срабатывать на команду /info
async def process_info_command(message: Message):
  await message.answer(text='Я отвечаю тебе твоими сообщениями. Вот такое я абышто!')


# Этот хэндлер(обработчик) будет срабатывать на отправку фото
# async def send_photo_echo(message: Message):
#   await message.reply_photo(message.photo[0].file_id)

# Этот хэндлер(обработчик) будет срабатывать на стикеры
# async def send_sticker_echo(message: Message):
#   await message.reply_sticker(message.sticker.file_id)

# Этот хэндлер(обработчик) срабатывает на голосовые сообщения
# async def send_voice_echo(message: Message):
#   await message.reply_voice(message.voice.file_id)

# Этот хэндлер срабатывает на видео
# async def send_video_echo(message: Message):
#   await message.reply_video(message.video.file_id)

# Этот хэндлер будет срабатывать на отправку документа
# async def send_document_echo(message: Message):
#   await message.answer(text='Держи назад свой документ')
#   await message.reply_document(message.document.file_id)

# Этот хэндлер(обработчик) будет срабатывать на любые сообщения кроме /start и /info
# async def send_echo(message: Message):
#   await message.reply(text=message.text)

# Этот хендлер будет срабатывать почти на все сообщения
async def send_echo(message: Message):
  try:
    # await message.answer(text=f'Зачем ты мне прислал эту гадость??')
    await message.send_copy(chat_id=message.chat.id)
  except TypeError:
    await message.reply(text="Данный тип апдейтов (сообщений) не поддерживает метод 'send_copy'")

# Регистрируем хэндлеры(обработчики)
dp.message.register(process_start_command, Command(commands=['start']))
dp.message.register(process_info_command, Command(commands=['info']))
# dp.message.register(send_photo_echo, F.content_type == ContentType.PHOTO)  #можно заменить на F.photo
# dp.message.register(send_sticker_echo, F.sticker)
# dp.message.register(send_voice_echo, F.voice)
# dp.message.register(send_video_echo, F.video)
# dp.message.register(send_document_echo, F.document)
dp.message.register(send_echo)

if __name__ == '__main__':
  dp.run_polling(bot)