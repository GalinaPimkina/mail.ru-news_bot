from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ContentType


BOT_TOKEN = "7784160373:AAEg1e0XjdN7adXRT7Xdp8AfNukLaoEQcAk"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer("Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь")


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое сообщение'
    )


@dp.message(F.photo)
async def send_photo_echo(message: Message):
    print(message)
    await message.reply_photo(message.photo[0].file_id)


@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)


if __name__ == '__main__':
    dp.run_polling(bot)