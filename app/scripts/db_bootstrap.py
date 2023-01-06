from pymongo import MongoClient

from ..config import settings


def run():
    client = MongoClient(settings.mongo_db_conn_str)
    client.comic_store.layaways.create_index("user_id", unique=True)
