import settings
from redis_api import getValutes, getPair, Valute, RedisValueException
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message, BotCommand
from aiogram.filters import Command, CommandObject
import asyncio
from decimal import Decimal

def calculate_rate(vfrom: Valute, vto: Valute, cnt: float) -> Decimal:
    return Decimal(cnt) * (Decimal(vfrom.value) / Decimal(vto.value))


commands = [
    BotCommand(command='/exchange', description='Конвертирует валюты. /exchange USD RUB 10 - отображает стоимость 10 долларов в рублях.'),
    BotCommand(command='/rates', description='Отправляет актуальные курсы валют.')
]


dp = Dispatcher()

@dp.message(Command('exchange'))
async def exchange_command(message: Message, command: CommandObject):
    argsstr = command.args
    if argsstr is None or len(argsstr.split(' ')) == 0 or len(argsstr.split(' ')) != 3:
        await message.answer('Команда требует следующих аргументов:\nВалюта из которой переводить;\nВалюта, в которую переводить;\nКоличество.\
                             \nПример: /exchange USD RUB 10')
        return
    args = argsstr.split(' ')
    try:
        vfrom = str(args[0])
        vto = str(args[1])
        cnt = float(args[2].replace(',', '.'))
    except:
        await message.answer('Введены неверные аргументы команды!')
        return
    try:
        result = calculate_rate(*(await getPair(vfrom, vto)), cnt)
    except RedisValueException as e:
        await message.answer(str(e))
        return
    except Exception:
        await message.answer('Не удалось перевести валюты, повторите попытку позже')
        return
    await message.answer(f'{round(result, 4)}')
    

@dp.message(Command('rates'))
async def rates_command(message: Message, command: CommandObject):
    v = await getValutes()
    mes = f'Актуальные курсы валют по ЦБ РФ:\n{'\n'.join([f'{i.name}: {i.value}' for i in v])}'
    await message.answer(mes)

async def main():
    bot = Bot(token=settings.TG_TOKEN)
    await bot.set_my_commands(commands)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())