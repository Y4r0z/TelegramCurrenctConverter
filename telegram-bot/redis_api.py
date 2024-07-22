import redis.asyncio as redis
import settings
from dataclasses import dataclass

"""

В зависимости от загрузки бота можно убрать клиент Redis из контекстного менеджера и держать постоянно открытым.
В данном же случае, не имеет смысла постоянно быть соединенным с сервером. 

"""
# Простой класс для хранения валюты
@dataclass
class Valute():
    name: str
    value: float

class RedisValueException(Exception):
    """
    Специальное исключение, текст которго возвращается пользователю.
    """
    pass

async def getValutes() -> list[Valute]:
    """
    Запрашивает из Redis все ключи (названия валют) и их значения (курсы).
    """
    # Можно сразу выдавать список, не создавая генераторную функцию, так как колчиество валют слишком мало
    result = []
    # Открываем и закрываем соединение через контекстный менеджер по необходимости
    async with redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, password=settings.REDIS_PASSWORD,
                           decode_responses=True) as client:
        # Итерируемся по всем ключам в БД
        async for key in client.scan_iter():
            result.append(Valute(name=str(key), value=float(await client.get(key))))
    return result

async def getPair(key1: str, key2: str) -> tuple[Valute, Valute]:
    """
    Запрашивает из Redis два значения по ключам (аргументам функции).

    """
    async with redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, password=settings.REDIS_PASSWORD,
                           decode_responses=True) as client:
        if key1.lower() == 'rub': val1 = 1
        else:
            val1 = await client.get(key1)
            if val1 is None: raise RedisValueException(f'Валюта с кодом {key1} не найдена!')
        if key2.lower() == 'rub': val2 = 1
        else:
            val2 = await client.get(key2)
            if val2 is None: raise RedisValueException(f'Валюта с кодом {key2} не найдена!')
    return (Valute(name=key1,value=float(val1)), Valute(name=key2,value=float(val2)))