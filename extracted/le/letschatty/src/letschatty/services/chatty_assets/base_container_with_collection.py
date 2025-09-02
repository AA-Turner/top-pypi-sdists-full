from typing import TypeVar, Type, List, Optional, Dict, Any
from pydantic import BaseModel, Field
from abc import ABC
from ...models.base_models.chatty_asset_model import ChattyAssetModel, CompanyAssetModel, ChattyAssetPreview
from .base_container import ChattyAssetBaseContainer
from ...models.execution.execution import ExecutionContext
from ...models.analytics.events.event_types import EventType
from ...models.data_base.collection_interface import ChattyAssetCollectionInterface
from ...models.utils.custom_exceptions.custom_exceptions import NotFoundError
from ...models.utils.types.deletion_type import DeletionType
from ...models.utils.types import StrObjectId
from bson import ObjectId
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import logging
import threading
import json
logger = logging.getLogger("ChattyAssetContainerWithCollection")

T = TypeVar('T', bound=ChattyAssetModel)
P = TypeVar('P', bound=ChattyAssetPreview)

class CacheConfig(BaseModel):
    keep_items_always_in_memory: bool = Field(default=False, description="If true, the items will be kept in memory instead of using a cache mechanism")
    cache_expiration_time: int = Field(default=60*5, description="The time in seconds that the cache will be kept")
    keep_previews_always_in_memory: bool = Field(default=False, description="If true, the previews will be kept in memory")
    cache_expiration_time_previews: int = Field(default=60*5, description="The time in seconds that the cache will be kept")
    keep_deleted_previews_in_memory: bool = Field(default=False, description="If true, the deleted previews will be kept in memory")

    @classmethod
    def default(cls) -> 'CacheConfig':
        return cls(
            keep_items_always_in_memory=False,
            cache_expiration_time=60*5,
            keep_previews_always_in_memory=False,
            cache_expiration_time_previews=60*5
        )

class ChattyAssetContainerWithCollection(ChattyAssetBaseContainer[T, P], ABC):
    """
    Base class for containers that store ChattyAssetModel items.

    Type Parameters:
        T: The type of items stored in the container. Must be a ChattyAssetModel.
    """
    def __init__(self, item_type: Type[T], preview_type: Optional[Type[P]], collection: ChattyAssetCollectionInterface[T, P], cache_config: CacheConfig):
        """
        Initialize the container with a specific item type.

        Args:
            item_type: The class type of items to be stored
            collection: The collection interface to use for database operations
        """
        if not isinstance(collection, ChattyAssetCollectionInterface):
            raise TypeError(
                f"Expected collection of type ChattyAssetCollectionInterface, "
                f"got {type(collection).__name__}"
            )
        super().__init__(item_type, preview_type)
        self.collection = collection
        self.item_last_accessed_at_cache: Dict[StrObjectId, datetime] = {}
        self.preview_last_accessed_at_cache: datetime = datetime.now(ZoneInfo("UTC"))
        self.cache_config = cache_config
        self.update_previews_thread()
        self.load_from_db_thread(company_id=None)

    def insert(self, item: T, execution_context: ExecutionContext) -> T:
        """
        Add an item to the container and insert it into the database collection.

        Args:
            item: The item to add. Must be of type T.

        Raises:
            TypeError: If the item is not of the correct type
            Exception: If insertion into database collection fails
        """
        logger.debug(f"{self.__class__.__name__} inserting item {item}")
        inserted_item = super().insert(item)
        self.collection.insert(inserted_item)
        execution_context.set_event_time(inserted_item.created_at)
        self.update_previews_thread()
        return inserted_item

    def update(self, id: str, new_item: T, execution_context: ExecutionContext) -> T:
        """
        Update an item in the container and in the database collection.

        Args:
            item_id: The ID of the item to update
            new_item: The new item data

        Raises:
            NotFoundError: If the item_id doesn't exist in both container and collection
            TypeError: If the new_item is not of the correct type

        Note:
            If the item exists in the collection but not in the container,
            it will be updated in both places. If it exists in neither,
            a NotFoundError will be raised.
        """
        try:
            logger.debug(f"{self.__class__.__name__} updating item {new_item}")
            updated_item = super().update(id, new_item)
            if id != updated_item.id:
                logger.error(f"Item id {id} does not match updated item id {updated_item.id}")
                raise ValueError(f"Item id {id} does not match updated item id {updated_item.id}")
            self.collection.update(updated_item)
            execution_context.set_event_time(updated_item.updated_at)
            self.update_preview(updated_item)
            self.update_previews_thread()
            return updated_item

        except NotFoundError as e:
            outdated_item = self.collection.get_by_id(id)
            if outdated_item:
                updated_item = outdated_item.update(new_item)
                self.items[id] = updated_item
                self.collection.update(updated_item)
                execution_context.set_event_time(updated_item.updated_at)
                self.update_previews_thread()
                return updated_item
            else:
                raise NotFoundError(
                f"Item with id {id} not found in {self.__class__.__name__} nor in collection DB"
            )

    def delete(self, id: str, execution_context: ExecutionContext,deletion_type : DeletionType = DeletionType.LOGICAL) -> T:
        """
        Delete an item from the container and the collection.

        Args:
            item_id: The ID of the item to delete
            deletion_type: The type of deletion to perform (logical or physical)

        Raises:
            NotFoundError: If the item_id doesn't exist in both container and collection
            ValueError: If an invalid deletion type is provided
        """
        try:
            logger.debug(f"{self.__class__.__name__} deleting item {id}")
            deleted_item = super().delete(id)
            execution_context.set_event_time(datetime.now(ZoneInfo("UTC")))
            self.collection.delete(id, deletion_type)
            return deleted_item
        except NotFoundError as e:
            self.collection.delete(id, deletion_type)
            self.delete_preview(id)
            self.update_previews_thread()
            execution_context.set_event_time(datetime.now(ZoneInfo("UTC")))
            return self.collection.get_by_id(id)

    def get_by_id(self, id: str) -> T:
        """
        Get an item from the container.

        Args:
            item_id: The ID of the item to retrieve

        Returns:
            The requested item

        Raises:
            NotFoundError: If the item_id doesn't exist
        """
        try:
            logger.debug(f"{self.__class__.__name__} getting item {id}")
            item = super().get_by_id(id)
            self.item_last_accessed_at_cache[id] = datetime.now(ZoneInfo("UTC"))
            return item
        except NotFoundError as e:
            # if self.cache_config.keep_items_always_in_memory:
            #     #if they are supposed to be in memory, we raise an error since it shouldn't be in the collection DB
            #     raise NotFoundError(f"Item with id {id} not found in {self.__class__.__name__} nor in collection DB")
            logger.debug(f"{self.__class__.__name__} getting item {id} not found in container, trying to get from collection")
            item = self.collection.get_by_id(id)
            if item:
                self.item_last_accessed_at_cache[id] = datetime.now(ZoneInfo("UTC"))
                return self.add_to_memory(item)
            else:
                raise NotFoundError(f"Item with id {id} not found in {self.__class__.__name__} nor in collection DB")

    def delete_preview(self, id: str):
        """We delete a preview from the container"""
        self.preview_items = [item for item in self.preview_items if item.id != id]

    def get_preview_by_id(self, id: str, company_id: StrObjectId, preview_type: Type[P]) -> P:
        """We get the preview for one item and update the last_accessed_at cache"""
        if not self.cache_config.keep_previews_always_in_memory and (self.preview_last_accessed_at_cache < datetime.now(ZoneInfo("UTC")) - timedelta(seconds=self.cache_config.cache_expiration_time_previews) or not self.preview_items):
            logger.debug(f"Clearing previews cache of {self.__class__.__name__}")
            self.update_previews_cache()
        return super().get_preview_by_id(id, company_id=company_id)

    def get_all_previews(self, company_id: Optional[StrObjectId]) -> List[Dict[str, Any]]:
        """We get the previews for one company and update the last_accessed_at cache"""
        logger.info(f"Getting all previews for {self.__class__.__name__}")
        if not self.cache_config.keep_previews_always_in_memory and (self.preview_last_accessed_at_cache < datetime.now(ZoneInfo("UTC")) - timedelta(seconds=self.cache_config.cache_expiration_time_previews) or not self.preview_items):
            logger.debug(f"Clearing previews cache of {self.__class__.__name__}")
            self.update_previews_cache()
        previews = super().get_all_previews(company_id=company_id)
        self.preview_last_accessed_at_cache = datetime.now(ZoneInfo("UTC"))
        previews= [json.loads(preview.model_dump_json()) for preview in previews if preview.deleted_at is None]
        logger.debug(f"Previews: {previews}")
        return previews

    def add_to_memory(self, item: T) -> T:
        if not isinstance(item, self.item_type):
            raise TypeError(f"Expected item of type {self.item_type.__name__}, got {type(item).__name__}")
        self.items[item.id] = item
        return item

    def clear_cache(self):
        """Clear the cache of all items that have not been accessed in the last 5 minutes"""
        if not self.cache_config.keep_items_always_in_memory:
            self.clear_cache_items()
        if not self.cache_config.keep_previews_always_in_memory:
            self.clear_previews_cache()

    def clear_cache_items(self):
        """Clear the cache of all items that have not been accessed in the cache_expiration_time"""
        ids_to_remove = []
        for id, last_accessed_at in self.item_last_accessed_at_cache.items():
            if last_accessed_at < datetime.now(ZoneInfo("UTC")) - timedelta(seconds=self.cache_config.cache_expiration_time):
                ids_to_remove.append(id)
        logger.debug(f"Clearing cache of {len(ids_to_remove)} {self.item_type.__name__}")
        for id in ids_to_remove:
            del self.items[id]
            del self.item_last_accessed_at_cache[id]

    def clear_previews_cache(self):
        """Clear the cache of all previews that have not been accessed in the cache_expiration_time_previews"""
        if self.preview_last_accessed_at_cache < datetime.now(ZoneInfo("UTC")) - timedelta(seconds=self.cache_config.cache_expiration_time_previews):
            logger.debug(f"Clearing previews cache of {self.__class__.__name__}")
            self.set_preview_items([])

    def get_all(self, company_id: Optional[StrObjectId]) -> List[T]:
        # Get items from memory
        logger.debug(f"{self.__class__.__name__} getting all items from memory and collection")
        memory_items = super().get_all(company_id=company_id)
        # Get items from collection that are not in memory
        memory_ids = [ObjectId(item.id) for item in memory_items]
        # Build the query for collection items
        query = {"deleted_at": None, "_id": {"$nin": memory_ids}}
        collection_items = self.collection.get_docs(query=query, company_id=company_id)
        all_items = memory_items + collection_items
        return sorted(all_items, key=lambda x: x.created_at, reverse=True)

    def update_preview(self, item: T):
        """We update the preview for an item"""
        if not self.preview_type:
            return
        preview = self.preview_type.from_asset(item)
        self.preview_items = [preview if item.id == preview.id else item for item in self.preview_items]

    def update_previews_thread(self):
        """We start a thread to update the previews cache so it doesn't block the main thread"""
        # self.update_previews_cache()
        thread = threading.Thread(target=self.update_previews_cache)
        thread.start()

    def update_previews_cache(self):
        """We update the previews cache of all the documents in the collection for all companies"""
        # if not self.cache_config.keep_previews_always_in_memory:
        #     return
        if not self.preview_type or self.preview_type is None:
            return
        projection = self.preview_type.get_projection()
        collection_items = self.collection.get_preview_docs(projection=projection, all=self.cache_config.keep_deleted_previews_in_memory)
        self.set_preview_items(collection_items)
        return collection_items

    def get_by_query(self, query: dict, company_id: Optional[StrObjectId]) -> List[T]:
        logger.debug(f"{self.__class__.__name__} getting items by query {query} from collection")
        return self.collection.get_docs(query=query, company_id=company_id)

    def get_deleted(self, company_id: Optional[StrObjectId]) -> List[T]:
        logger.debug(f"{self.__class__.__name__} getting deleted items from collection")
        return self.collection.get_docs(query={"deleted_at": {"$ne": None}}, company_id=company_id)

    def load_from_db_thread(self, company_id: Optional[StrObjectId]):
        """We start a thread to load the items from the database so it doesn't block the main thread"""
        if not self.cache_config.keep_items_always_in_memory:
            return
        # self.load_from_db(company_id=company_id)
        thread = threading.Thread(target=self.load_from_db, args=(company_id,))
        thread.start()

    def load_from_db(self, company_id: Optional[StrObjectId]):
        """Pass company_id=None to load all items from the database."""
        logger.debug(f"{self.__class__.__name__} loading items from collection")
        # self.items = {item.id: item for item in self.collection.get_docs(query={}, company_id=company_id)}
        self.items = {item.id: item for item in self.collection.get_docs(query={"deleted_at": None}, company_id=company_id)}

    def restore(self, id: str, execution_context: ExecutionContext) -> T:
        logger.debug(f"{self.__class__.__name__} restoring item {id} with execution context {execution_context}")
        if id in self.items:
            raise ValueError(f"Item with id {id} already exists in {self.__class__.__name__}")
        restored_item = self.collection.get_by_id(id)
        if restored_item is None:
            raise NotFoundError(f"Item with id {id} not found in collection DB")
        restored_item.deleted_at = None
        restored_item.update_now()
        execution_context.set_event_time(restored_item.updated_at)
        self.items[id] = restored_item
        self.collection.update(restored_item)
        return restored_item
