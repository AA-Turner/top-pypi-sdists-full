from typing import Dict, Generic, TypeVar, Type, List, Optional
from abc import ABC
from ...models.base_models.chatty_asset_model import ChattyAssetModel, CompanyAssetModel, ChattyAssetPreview
from ...models.utils.custom_exceptions.custom_exceptions import NotFoundError
from ...models.company.empresa import EmpresaModel
from ...models.utils.types import StrObjectId
from bson import ObjectId
from datetime import datetime
from zoneinfo import ZoneInfo
import logging
logger = logging.getLogger("ChattyAssetBaseContainer")

T = TypeVar('T', bound=ChattyAssetModel | CompanyAssetModel)
P = TypeVar('P', bound=ChattyAssetPreview)

class ChattyAssetBaseContainer(Generic[T, P], ABC):
    """
    Base class for containers that store ChattyAssetModel items.

    Type Parameters:
        T: The type of items stored in the container. Must be a ChattyAssetModel.
    """
    def __init__(self, item_type: Type[T], preview_type: Optional[Type[P]] = None):
        """
        Initialize the container with a specific item type.

        Args:
            item_type: The class type of items to be stored
        """
        self.items: Dict[str, T] = {}
        self.item_type = item_type
        self.preview_type : Optional[Type[P]] = preview_type
        self.preview_items: List[P] = []

    def insert(self, item: T) -> T:
        """
        Add an item to the container.

        Args:
            item: The item to add. Must be of type T.

        Raises:
            TypeError: If the item is not of the correct type
        """
        if not isinstance(item, self.item_type):
            raise TypeError(
                f"Expected item of type {self.item_type.__name__}, "
                f"got {type(item).__name__}"
            )

        self.items[item.id] = item
        return item
    def update(self, item_id: str, new_item: T) -> T:
        """
        Update an item in the container.

        Args:
            item_id: The ID of the item to update
            new_item: The new item data

        Raises:
            NotFoundError: If the item_id doesn't exist
            TypeError: If the new_item is not of the correct type
        """
        if item_id not in self.items:
            raise NotFoundError(
                f"Item with id {item_id} not found in {self.__class__.__name__}."
            )

        if not isinstance(new_item, self.item_type):
            raise TypeError(
                f"Expected item of type {self.item_type.__name__}, "
                f"got {type(new_item).__name__}"
            )

        original_item = self.items[item_id]
        updated_item = original_item.update(new_item) # type: ignore
        self.items[item_id] = updated_item
        return updated_item

    def delete(self, item_id: str) -> T:
        """
        Delete an item from the container.

        Args:
            item_id: The ID of the item to delete

        Raises:
            NotFoundError: If the item_id doesn't exist
        """
        if item_id not in self.items:
            raise NotFoundError(
                f"Item with id {item_id} not found in {self.__class__.__name__}."
            )
        item = self.items.pop(item_id)
        item.deleted_at = datetime.now(ZoneInfo("UTC"))
        return item

    def get_by_id(self, item_id: str) -> T:
        """
        Get an item from the container.

        Args:
            item_id: The ID of the item to retrieve

        Returns:
            The requested item

        Raises:
            NotFoundError: If the item_id doesn't exist
        """
        if item_id not in self.items:
            raise NotFoundError(
                f"Item with id {item_id} not found in {self.__class__.__name__}."
            )
        return self.items[item_id]

    def get_all(self, company_id:Optional[StrObjectId]) -> List[T]:
        if issubclass(self.item_type, CompanyAssetModel) and not company_id:
            raise ValueError(f"company_id is required for asset_type {self.item_type}")
        elif issubclass(self.item_type, CompanyAssetModel) and company_id:
            return [item for item in self.items.values() if item.company_id == company_id] # type: ignore
        else:
            return list(self.items.values())

    def get_all_dict_id_item(self, company_id:Optional[StrObjectId]) -> Dict[StrObjectId, T]:
        return {item.id: item for item in self.get_all(company_id)}

    def get_all_previews(self, company_id:Optional[StrObjectId]) -> List[P]:
        logger.info(f"Getting all previews for {self.__class__.__name__}")
        if issubclass(self.item_type, CompanyAssetModel) and not company_id:
            raise ValueError(f"company_id is required for asset_type {self.item_type}")
        elif issubclass(self.item_type, CompanyAssetModel) and company_id:
            return [item for item in self.preview_items if item.company_id == company_id]
        else:
            return self.preview_items

    def set_preview_items(self, items: List[P]):
        self.preview_items = sorted(items, key=lambda x: x.created_at, reverse=True)

    def get_preview_by_id(self, id: str, company_id: StrObjectId) -> P:
        """We get the preview for one item and update the last_accessed_at cache"""
        if not self.preview_type:
            raise ValueError(f"Preview type is not set for {self.__class__.__name__}")
        preview = next((item for item in self.preview_items if item.id == id), None)
        if preview:
            return preview
        else:
            if not ObjectId.is_valid(id):
                logger.warning(f"Preview with id {id} for {self.preview_type.__name__} is not a valid object id, returning not found preview")
                id = "000000000000000000000000"
            return self.preview_type.not_found(id, company_id)
