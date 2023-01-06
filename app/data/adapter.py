from pymongo import MongoClient

from ..config import settings


class MongoDbClient:
    def __init__(self) -> None:
        self.client = MongoClient(settings.mongo_db_conn_str)

    def __get_comic_store_db(self):
        return self.client.comic_store

    def __get_layaways_collection(self):
        db = self.__get_comic_store_db()
        return db.layaways

    def find_and_push_by_user_id(self, user_id, comics):
        collection = self.__get_layaways_collection()
        return collection.find_one_and_update(
            {"user_id": user_id},
            {"$push": {"comics": {"$each": comics}}},
        )

    def find_and_overwrite_by_user_id(self, user_id, comics):
        collection = self.__get_layaways_collection()
        return collection.find_one_and_update(
            {"user_id": user_id}, {"$set": {"comics": comics}}
        )

    def find_one_by_id_user(self, user_id):
        collection = self.__get_layaways_collection()
        return collection.find_one({"user_id": user_id})

    def insert_layaway(self, layaway):
        collection = self.__get_layaways_collection()
        return collection.insert_one(layaway).inserted_id
