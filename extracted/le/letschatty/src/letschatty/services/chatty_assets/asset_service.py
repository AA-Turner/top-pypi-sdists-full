from __future__ import annotations
from typing import TypeVar, Generic, Type, Callable, Protocol, Optional
from .base_container_with_collection import ChattyAssetCollectionInterface, ChattyAssetContainerWithCollection, CacheConfig
from ...models.base_models import ChattyAssetModel
from ...models.base_models.chatty_asset_model import ChattyAssetPreview
from ...models.data_base.mongo_connection import MongoConnection
import logging
import os
logger = logging.getLogger("AssetService")

# Protocol for assets that specify their preview type
class AssetWithPreview(Protocol):
    preview_class: Type[ChattyAssetPreview]

T = TypeVar('T', bound=ChattyAssetModel)
P = TypeVar('P', bound=ChattyAssetPreview)  # Preview type

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
            database=db_name, #type: ignore
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
    """Generic service for handling CRUD operations for any Chatty asset"""

    def __init__(self,
                 collection_name: str,
                 asset_type: Type[T],
                 connection: MongoConnection,
                 create_instance_method: Callable[[dict], T],
                 preview_type: Optional[Type[P]] = None,
                 cache_config: CacheConfig = CacheConfig.default()):
        logger.debug(f"AssetService {self.__class__.__name__} initializing for {collection_name}")
        asset_collection = AssetCollection(
            collection=collection_name,
            asset_type=asset_type,
            connection=connection,
            create_instance_method=create_instance_method,
            preview_type=preview_type
        )
        super().__init__(
            item_type=asset_type,
            preview_type=preview_type,
            collection=asset_collection,
            cache_config=cache_config,
        )
        logger.debug(f"AssetService {self.__class__.__name__} initialized for {collection_name}")

    def get_preview_type(self) -> Type[P]:
        """Get the preview type from the asset class if it has one"""
        if hasattr(self.item_type, 'preview_class') and self.item_type.preview_class is not None:
            return self.item_type.preview_class  # type: ignore
        return ChattyAssetPreview  # type: ignore

    def get_preview_by_id(self, id: str, company_id: str) -> P:
        """Get a preview by ID using the preview type from the asset class"""
        preview_type = self.get_preview_type()
        return super().get_preview_by_id(id, company_id, preview_type)

