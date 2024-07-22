from dotenv import load_dotenv
import os


load_dotenv()

REDIS_DB = os.environ.get('REDIS_DB')
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
CBR_XML = os.environ.get('CBR_XML')

assert REDIS_DB, 'REDIS_DB enviroment variable is None'
assert REDIS_HOST, 'REDIS_HOST enviroment variable is None'
assert REDIS_PORT, 'REDIS_PORT enviroment variable is None'
assert REDIS_PASSWORD, 'REDIS_PASSWORD enviroment variable is None'
assert CBR_XML, 'CBR_XML enviroment variable is None'