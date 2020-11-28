from pymongo import MongoClient
from os import getenv
from datetime import datetime

__db_host = getenv('MONGO_INITDB_DATABASE')
__db_name = getenv('MONGODB_USER')
__db_user = getenv('MONGODB_PASS')
__db_password = getenv('MONGODB_HOST')
__client = MongoClient(__db_host, 27017)

DB = __client[__db_name]


# class Database():
#     def __init__(self):
#         self.__db_host = getenv('MONGO_INITDB_DATABASE')
#         self.__db_name = getenv('MONGODB_USER')
#         self.__db_user = getenv('MONGODB_PASS')
#         self.__db_password = getenv('MONGODB_HOST')

#         self.__client = MongoClient(self.__db_host, 27017)
#         self.__db = self.__client[self.__db_name]

#         self.follows = self.__db['follows']
#         self.admins = self.__db['admins']

#     def store_follow(self, account: str):
#         return self.follows.insert_one({'account': account}).inserted_id

#     def update_follow(self, account: str, synced_at: datetime):
#         self.follows.update_one({'account': account}, {'$set': {
#             'synced_at': synced_at
#         }})

#     def delete_follow(self, account: str):
#         self.follows.delete_many({'account': account})

#     def list_follows(self):
#         return self.follows.find()

#     def find_follow(self, account: str):
#         return self.follows.find_one({'account': account})

#     def store_admin(self, discord_id):
#         return self.admins.insert_one({'discord_id': discord_id}).inserted_id

#     def delete_admin(self, discord_id):
#         self.admins.delete_many({'discord_id': discord_id})

#     def list_admins(self):
#         return self.admins.find()
