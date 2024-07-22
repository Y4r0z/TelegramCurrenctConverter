from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

REDIS_DB = os.environ.get('REDIS_DB')
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
TG_TOKEN = os.environ.get('TG_TOKEN')

assert REDIS_DB, 'REDIS_DB enviroment variable is None'
assert REDIS_HOST, 'REDIS_HOST enviroment variable is None'
assert REDIS_PORT, 'REDIS_PORT enviroment variable is None'
assert REDIS_PASSWORD, 'REDIS_PASSWORD enviroment variable is None'
assert TG_TOKEN, 'TG_TOKEN enviroment variable is None'