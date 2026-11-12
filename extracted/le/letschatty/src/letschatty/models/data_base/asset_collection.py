"""`AssetCollection`: la base de las `*Collection` de letschatty (antes en `services/chatty_assets/asset_service.py`).

Se conservan dos cosas del módulo viejo, porque eran comportamiento observable: el `ValueError` al importar sin
`MONGO_DB_NAME` (el arranque falla igual) y el logger `AssetService` en sus líneas de log.
"""
from __future__ import annotations
from typing import TypeVar, Generic, Type, Callable, Optional
from ..base_models import ChattyAssetModel
from ..base_models.chatty_asset_model import ChattyAssetPreview
from .mongo_connection import MongoConnection
from .collection_interface import ChattyAssetCollectionInterface
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
