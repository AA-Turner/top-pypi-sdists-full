from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, List, Generic, TypeVar, Type, Optional, Any
from bson.objectid import ObjectId
from pymongo.collection import Collection
from pymongo.database import Database

from letschatty.models.chat.chat import Chat
from ...models.base_models.chatty_asset_model import ChattyAssetModel, CompanyAssetModel, ChattyAssetPreview
from ...models.utils.types import StrObjectId
from ...models.utils.types.serializer_type import SerializerType
from ...models.utils.types.deletion_type import DeletionType
from datetime import datetime
from zoneinfo import ZoneInfo
from ...models.utils.custom_exceptions.custom_exceptions import NotFoundError
import logging

logger = logging.getLogger("CollectionInterface")

if TYPE_CHECKING:
    from .mongo_connection import MongoConnection

T = TypeVar('T', bound=ChattyAssetModel | CompanyAssetModel)
P = TypeVar('P', bound=ChattyAssetPreview)

class ChattyAssetCollectionInterface(Generic[T, P], ABC):
    def __init__(self, database: str, collection: str, connection: MongoConnection, type: Type[T], preview_type: Optional[Type[P]] = None):
        logger.info(f"Initializing collection {collection} in database {database}")
        self.db: Database = connection.client[database]
        self.collection: Collection = connection.client[database][collection]
        self.type = type
        self.preview_type = preview_type
    @abstractmethod
    def create_instance(self, data: dict) -> T:
        """Factory method to create instance from data"""
        pass

    def insert(self, asset: T) -> StrObjectId:
        if not isinstance(asset, self.type):
            raise ValueError(f"Asset must be of type {self.type.__name__}")
        document = asset.model_dump_json(serializer=SerializerType.DATABASE)
        logger.debug(f"Inserting document: {document}")
        result = self.collection.insert_one(document)
        if not result.inserted_id:
            raise Exception("Failed to insert document")
        logger.debug(f"Inserted document with id {result.inserted_id}")
        return result.inserted_id

    def update(self, asset: T) -> StrObjectId:
        logger.debug(f"Updating document with id {asset.id}")
        if not isinstance(asset, self.type):
            raise ValueError(f"Asset must be of type {self.type.__name__}")
        asset.update_now()
        document = asset.model_dump_json(serializer=SerializerType.DATABASE)
        document.pop('_id', None)  # Still needed
        result = self.collection.update_one({"_id": ObjectId(asset.id)}, {"$set": document})
        if result.matched_count == 0:
            raise NotFoundError(f"No document found with id {asset.id}")
        if result.modified_count == 0:
            logger.debug(f"No changes were made to the document with id {asset.id} probably because the values were the same")
        return asset.id

    def get_by_id(self, doc_id: str) -> T:
        logger.debug(f"Getting document with id {doc_id} from collection {self.collection.name} and db {self.db.name}")
        doc = self.collection.find_one({"_id": ObjectId(doc_id)})

        if doc:
            return self.create_instance(doc)
        else:
            raise NotFoundError(f"No document found with id {doc_id} in db collection {self.collection.name} and db {self.db.name}")

    def get_docs(self, company_id:Optional[StrObjectId], query = {}, limit = 0) -> List[T]:
        logger.debug(f"Getting documents from collection {self.collection.name} with company_id {company_id} and query {query}")
        if company_id:
            query = query.copy()  # Create a copy to avoid modifying the original
            query["company_id"] = company_id
        docs = list(self.collection.find(filter=query).limit(limit))
        logger.debug(f"Found {len(docs)} documents in collection {self.collection.name}")
        return [self.create_instance(doc) for doc in docs]

    def get_preview_docs(self, projection = {}, all=True) -> List[P]:
        """We get the previews of all the documents in the collection for all companies"""
        if not self.preview_type:
            raise ValueError(f"{self.__class__.__name__} has no preview class")
        logger.debug(f"Getting preview documents from collection {self.collection.name}")
        if all:
            docs = list(self.collection.find(projection=projection))
        else:
            docs = list(self.collection.find(filter={"deleted_at": None}, projection=projection))
        logger.debug(f"Found {len(docs)} preview documents in collection {self.collection.name}")
        return [self.preview_type.from_dict(doc) for doc in docs]

    def get_by_query(self, query = {}) -> List[T]:
        docs = self.collection.find(query)
        return [self.create_instance(doc) for doc in docs]

    def delete(self, doc_id: str, deletion_type : DeletionType = DeletionType.LOGICAL) -> StrObjectId:
        logger.debug(f"Deleting document with id {doc_id} - deletion type: {deletion_type}")
        if deletion_type == DeletionType.LOGICAL:
            result = self.collection.update_one({"_id": ObjectId(doc_id)}, {"$set": {"deleted_at": datetime.now(ZoneInfo("UTC")), "updated_at": datetime.now(ZoneInfo("UTC"))}})
            if result.modified_count == 0:
                raise NotFoundError(f"No document found with id {doc_id}")
            return doc_id
        elif deletion_type == DeletionType.PHYSICAL:
            result = self.collection.delete_one({"_id": ObjectId(doc_id)})
            if result.deleted_count == 0:
                raise NotFoundError(f"No document found with id {doc_id}")
            return doc_id
        else:
            raise ValueError(f"Invalid deletion type: {deletion_type}")

