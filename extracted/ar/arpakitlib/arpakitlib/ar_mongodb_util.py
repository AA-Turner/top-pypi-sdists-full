# arpakit

import asyncio
import logging
from abc import abstractmethod
from random import randint
from typing import Optional
from urllib.parse import quote

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def generate_mongo_uri(
        *,
        mongo_user: Optional[str] = None,
        mongo_password: Optional[str] = None,
        mongo_hostname: str = "localhost",
        mongo_port: int = 27017,
        mongo_auth_db: Optional[str] = None
) -> str:
    res: str = f'mongodb://'
    if mongo_user:
        res += f"{mongo_user}"
        if mongo_password:
            res += f":{quote(mongo_password)}"
        res += "@"
    res += f"{mongo_hostname}:{mongo_port}"
    if mongo_auth_db is not None:
        res += f"/?authSource={mongo_auth_db}"

    return res


class EasyMongoDb:
    def __init__(
            self,
            *,
            db_name: str,
            username: str | None = None,
            password: str | None = None,
            hostname: str = "127.0.0.1",
            port: int = 27017,
            auth_source: str | None = None,
    ):
        self._logger = logging.getLogger(self.__class__.__name__)
        self.hostname = hostname
        self.username = username
        self.password = password
        self.auth_source = auth_source
        self.port = port
        self.db_name = db_name
        self.used_collections: list[Collection] = []

    def init(self):
        self.ensure_indexes()

    def reinit(self):
        self.drop_all_collections()
        self.init()

    def get_pymongo_client(self) -> MongoClient:
        kwargs = {
            "host": self.hostname,
            "port": self.port,
            "tz_aware": True
        }
        if self.username is not None:
            kwargs["username"] = self.username
        if self.password is not None:
            kwargs["password"] = self.password
        if self.auth_source is not None:
            kwargs["authSource"] = self.auth_source
        kwargs["timeoutMS"] = 5000
        kwargs["connectTimeoutMS"] = 5000
        kwargs["socketTimeoutMS"] = 5000
        kwargs["serverSelectionTimeoutMS"] = 5000
        return MongoClient(**kwargs)

    def check_conn(self):
        self.get_pymongo_client().server_info()

    def is_db_conn_good(self) -> bool:
        try:
            self.get_pymongo_client().server_info()
        except Exception as e:
            self._logger.error(e)
            return False
        return True

    def get_pymongo_db(self) -> Database:
        return self.get_pymongo_client().get_database(self.db_name)

    def drop_all_collections(self):
        for collection in self.get_pymongo_db().list_collections():
            self.get_pymongo_db().get_collection(collection["name"]).drop()

    def drop_used_collections(self):
        for collection in self.used_collections:
            collection.drop()

    def generate_collection_int_id(self, collection: Collection) -> int:
        existing_ids = set(
            doc["id"] for doc in collection.find({}, {"id": True}) if "id" in doc.keys()
        )
        if existing_ids:
            res = max(existing_ids) + 1
        else:
            res = 1
        while res in existing_ids:
            res += 1
        return res

    def generate_collection_rand_int_id(self, collection: Collection, max_rand_int: int = 30) -> int:
        existing_ids = set(
            doc["id"] for doc in collection.find({}, {"id": True}) if "id" in doc.keys()
        )

        id_ = self.generate_collection_int_id(collection=collection)
        res = id_ + randint(1, max_rand_int)
        while res in existing_ids:
            id_ += 1
            res = id_ + randint(1, max_rand_int)

        return res

    @abstractmethod
    def ensure_indexes(self):
        raise NotImplemented()


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
