import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from send_random_picture import BOT_TOKEN


bot = Bot(BOT_TOKEN)
dp = Dispatcher()

ATTEMPTS = 5

user = {
    'in_game': False,
    'secret_number': None,
    'attempts': None,
    'total_games': 0,
    'wins': 0
}


def get_random_number():
    return random.randint(1, 20)


@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer('''
        Добро пожаловать в игру "Угадай число"!\n
        Чтобы прочитать правила игры или посмотреть список доступных\n
        команд - отправьте /help
    ''')


@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(f'''
        Правила игры: \n
        Я загадываю число от 1 до 20, а Вам нужно его угадать.\n
        У Вас есть {ATTEMPTS} попыток.\n\n
        Доступные команды: \n
        /help - правила игры и список команд,\n
        /cancel - выйти из игры, \n
        /stat - посмотреть статистику. \n\n
        Давай поиграем?
    ''')


@dp.message(Command(commands='stat'))
async def process_stat_command(message: Message):
    await message.answer(f'''
        Всего игры сыграно: {user['total_games']}.\n
        Игр выиграно: {user['wins']}
    ''')


@dp.message(Command(commands='cancel'))
async def proccess_cancel_command(message: Message):
    if user['in_game']:
        user['in_game'] = False
        await message.answer('''
            Вы вышли из игры. Если хотите сыграть снова - напишите об этом.
        ''')
    else:
        await message.answer('''
            Вы не в процессе игры.\n
            Чтобы начать играть - введите "играть".
        ''')

