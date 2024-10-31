from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message


API_URL = "https://api.telegram.org/bot"
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


@dp.message()
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(
            text='''Данный тип апдейтов не поддерживается\nметодом send_copy'''
        )

    print(message.model_dump_json(indent=4, exclude_none=True))




if __name__ == '__main__':
    dp.run_polling(bot)