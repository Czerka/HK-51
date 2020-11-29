from pymongo import MongoClient
from os import getenv

__db_connection_string = getenv('MONGODB_CONNECTION_STRING')
__client = MongoClient(__db_connection_string)

DB = __client['db']
