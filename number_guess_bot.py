import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from send_random_picture import BOT_TOKEN


bot = Bot(BOT_TOKEN)
dp = Dispatcher()

ATTEMPTS = 5

users = {}


def get_random_number() -> int:
    return random.randint(1, 20)


@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        'Добро пожаловать в игру "Угадай число"!\n'
        'Чтобы прочитать правила игры или посмотреть список доступных\n'
        'команд - отправьте /help\n\n'
        'Правила игры: \n'
        'Для старта введите "играть".\n'
        'Я загадываю число от 1 до 20, а Вам нужно его угадать.\n'
        f'У Вас есть {ATTEMPTS} попыток.\n\n'
    )

    if message.from_user.id not in users.keys():
        users[message.from_user.id] = {
            'in_game': False,
            'secret_number': None,
            'attempts': None,
            'total_games': 0,
            'wins': 0
        }


@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(
        'Доступные команды: \n'
        '/help - правила игры и список команд,\n'
        '/cancel - выйти из игры, \n'
        '/stat - посмотреть статистику. \n\n'
       ' Давай поиграем?'
    )


@dp.message(Command(commands='stat'))
async def process_stat_command(message: Message):
    await message.answer(
        f'Всего игр сыграно: {users[message.from_user.id]["total_games"]}.\n'
        f'Игр выиграно: {users[message.from_user.id]["wins"]}'
    )


@dp.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    if users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = False
        await message.answer(
            'Вы вышли из игры. Если хотите сыграть снова - напишите об этом.'
        )
    else:
        await message.answer(
            'Вы не в процессе игры.\n'
            'Чтобы начать играть - введите "играть".'
        )


@dp.message(F.text.lower().in_(['играть', 'да', 'давай', 'хочу']))
async def process_agree_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_number()
        users[message.from_user.id]['attempts'] = ATTEMPTS
        await message.answer(
            'Я загадал число от 1 до 20, попробуйте отгадать его!'
        )
    else:
        await message.answer(
            'Пока мы играем в игру, я могу принимать только числа от 1 до 20, и команды /cancel и /stat. '
        )


@dp.message(F.text.lower().in_(["нет", "не хочу", "не буду"]))
async def process_refusal_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer(
            'Если захотите поиграть, отправьте слово "играть" мне в чат.'
        )
    else:
        await message.answer(
            'Пока вы в игре, вам доступна отправка чисел от 1 до 20.'
        )


@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 20)
async def process_number_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
            await message.answer(
                f'Вы отгадали! Я загадывал число {users[message.from_user.id]["secret_number"]}!\n'
                'Будем играть еще?'
            )
        elif int(message.text) > users[message.from_user.id]["secret_number"]:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer('Moe число меньше.')
        elif int(message.text) < users[message.from_user.id]["secret_number"]:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer('Мое число больше.')

        if users[message.from_user.id]['attempts'] == 0:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            await message.answer(
                'К сожалению, у Вас больше не осталось попыток. Вы проиграли.\n'
                f'Я загадал число {users[message.from_user.id]["secret_number"]}. \n'
                'Давайте сыграем еще раз?'
            )
    else:
        await message.answer('Мы еще не начинали игру. Хотите сыграть?')


@dp.message()
async def process_other_answers(message: Message):
    if message.from_user.id in users.keys():
        if users[message.from_user.id]['in_game']:
            await message.answer(
                'Пока мы с Вами играем, присылайте, ' 
                'пожалуйста, числа в пределах от 1 до 20.'
            )
    else:
        await message.answer(
            'Я умею только загадывать числа. '
            'Давайте сыграем в эту игру?\n'
            'Введите /start, чтобы начать работу с ботом.\n'
            'Для помощи в работе бота введите /help'
        )


if __name__ == '__main__':
    dp.run_polling(bot)