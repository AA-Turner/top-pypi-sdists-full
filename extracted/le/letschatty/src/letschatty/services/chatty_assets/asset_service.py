from __future__ import annotations
from typing import TypeVar, Generic, Type, Callable, Protocol, Optional
from .base_container_with_collection import ChattyAssetContainerWithCollection, CacheConfig
from ...models.base_models import ChattyAssetModel
from ...models.base_models.chatty_asset_model import ChattyAssetPreview
from ...models.cache import CacheProtocol, NoCache
from ...models.data_base.mongo_connection import MongoConnection
from ...models.data_base.collection_interface import ChattyAssetCollectionInterface
import logging
import os

logger = logging.getLogger("AssetService")

T = TypeVar('T', bound=ChattyAssetModel)
P = TypeVar('P', bound=ChattyAssetPreview)

db_name = os.getenv("MONGO_DB_NAME")
logger.info(f"🚨🚨🚨🚨🚨🚨 db_name: {db_name}")
if db_name is None:
    raise ValueError("MONGO_DB_NAME is not set in the environment variables")


class AssetCollection(Generic[T, P], ChattyAssetCollectionInterface[T, P]):
    def __init__(self,
                 collection: str,
                 asset_type: Type[T],
                 connection: MongoConnection,
                 create_instance_method: Callable[[dict], T],
                 preview_type: Optional[Type[P]] = None):
        logger.debug(f"AssetCollection {self.__class__.__name__} initializing for {collection}")
        super().__init__(
            database=db_name,  # type: ignore
            collection=collection,
            connection=connection,
            type=asset_type,
            preview_type=preview_type
        )
        self._create_instance_method = create_instance_method
        logger.debug(f"AssetCollection {self.__class__.__name__} initialized for {collection}")

    def create_instance(self, data: dict) -> T:
        if not isinstance(data, dict):
            raise ValueError(f"Data must be a dictionary, got {type(data)}: {data}")
        return self._create_instance_method(data)


class AssetService(Generic[T, P], ChattyAssetContainerWithCollection[T, P]):
    """Generic async service for any Chatty asset. Reads: cache → MongoDB. Writes: MongoDB → cache invalidation."""

    def __init__(self,
                 collection: AssetCollection[T, P],
                 cache_config: CacheConfig = None,
                 cache: CacheProtocol = None):
        logger.debug(f"AssetService {self.__class__.__name__} initializing")
        super().__init__(
            item_type=collection.type,
            preview_type=collection.preview_type,
            collection=collection,
            cache_config=cache_config,
            cache=cache or NoCache(),
        )
        logger.debug(f"AssetService {self.__class__.__name__} initialized")

    def get_preview_type(self) -> Type[P]:
        if hasattr(self.item_type, 'preview_class') and self.item_type.preview_class is not None:
            return self.item_type.preview_class  # type: ignore
        return ChattyAssetPreview  # type: ignore
