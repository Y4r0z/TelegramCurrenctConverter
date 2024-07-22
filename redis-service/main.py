import xml.etree.ElementTree as ET
from src.models import ValCurs, Valute
import settings
import redis
import schedule
import requests
import time
import logging

href = settings.CBR_XML

def updateValutes():
    # Могу использовать синхронную библиотеку `requests`, так как вынес обновление кеша в отдельный сервис
    try:
        with requests.get(href) as r:
            xml = r.text
    except Exception as e:
        logging.error(f'Cannot fetch data from cbr: {e}')
        return
    try:
        Curs = ValCurs.from_xml(xml)
        # Подключаеюсь к Redis с помощью менеджера контекста
        with redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, password=settings.REDIS_PASSWORD) as client:
            # Устанвливаю все валюты 
            for valute in Curs.Valutes:
                client.set(valute.CharCode, value=valute.VunitRate)
    except Exception as e:
        logging.error(f'Redis service is not avaliable: {e}')
        return


def main():
    updateValutes()
    # Один раз в день выполнять `updateValues`. Время не определено, но библиотека schedule позволяет его указать
    schedule.every().day.do(updateValutes)
    # Проверять каждую минуту наступление события `следующий день`
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    main()