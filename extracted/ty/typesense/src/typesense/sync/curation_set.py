"""
This module provides async functionality for managing individual curation sets in Typesense.

It contains the CurationSet class, which allows for retrieving, updating, deleting,
and managing items within a curation set asynchronously.

Classes:
    CurationSet: Manages async operations on a single curation set in the Typesense API.

Dependencies:
    - typesense.async_api_call: Provides the ApiCall class for making async API requests.
    - typesense.types.curation_set: Provides various curation set schema types.

Note: This module uses conditional imports to support both Python 3.11+ and earlier versions.
"""

import sys

if sys.version_info >= (3, 11):
    import typing
else:
    import typing_extensions as typing

from .api_call import ApiCall
from typesense.types.curation_set import (
    CurationItemDeleteSchema,
    CurationItemSchema,
    CurationSetDeleteSchema,
    CurationSetListItemResponseSchema,
    CurationSetSchema,
    CurationSetUpsertSchema,
)


class CurationSet:
    """
    Manages async operations on a single curation set in the Typesense API.

    This class provides async methods to retrieve, update, and delete a curation set,
    as well as manage items within the curation set.

    Attributes:
        api_call (ApiCall): The ApiCall instance for making async API requests.
        name (str): The name of the curation set.
    """

    def __init__(self, api_call: ApiCall, name: str) -> None:
        """
        Initialize the CurationSet instance.

        Args:
            api_call (ApiCall): The ApiCall instance for making async API requests.
            name (str): The name of the curation set.
        """
        self.api_call = api_call
        self.name = name

    @property
    def _endpoint_path(self) -> str:
        """
        Get the API endpoint path for this curation set.

        Returns:
            str: The full endpoint path for the curation set.
        """
        from .curation_sets import CurationSets

        return "/".join([CurationSets.resource_path, self.name])

    def retrieve(self) -> CurationSetSchema:
        """
        Retrieve this specific curation set.

        Returns:
            CurationSetSchema: The schema containing the curation set details.
        """
        response: CurationSetSchema = self.api_call.get(
            self._endpoint_path,
            as_json=True,
            entity_type=CurationSetSchema,
        )
        return response

    def delete(self) -> CurationSetDeleteSchema:
        """
        Delete this specific curation set.

        Returns:
            CurationSetDeleteSchema: The schema containing the deletion response.
        """
        response: CurationSetDeleteSchema = self.api_call.delete(
            self._endpoint_path,
            entity_type=CurationSetDeleteSchema,
        )
        return response

    def upsert(
        self,
        payload: CurationSetUpsertSchema,
    ) -> CurationSetSchema:
        """
        Create or update this curation set.

        Args:
            payload (CurationSetUpsertSchema): The schema for creating or updating the curation set.

        Returns:
            CurationSetSchema: The created or updated curation set.
        """
        response: CurationSetSchema = self.api_call.put(
            "/".join([self._endpoint_path]),
            body=payload,
            entity_type=CurationSetSchema,
        )
        return response

    # Items sub-resource
    @property
    def _items_path(self) -> str:
        """
        Get the API endpoint path for items in this curation set.

        Returns:
            str: The full endpoint path for items (e.g., /curation_sets/{name}/items).
        """
        return "/".join([self._endpoint_path, "items"])

    def list_items(
        self,
        *,
        limit: typing.Union[int, None] = None,
        offset: typing.Union[int, None] = None,
    ) -> CurationSetListItemResponseSchema:
        """
        List items in this curation set.

        Args:
            limit (Union[int, None], optional): Maximum number of items to return. Defaults to None.
            offset (Union[int, None], optional): Number of items to skip. Defaults to None.

        Returns:
            CurationSetListItemResponseSchema: The list of items in the curation set.
        """
        params: typing.Dict[str, typing.Union[int, None]] = {
            "limit": limit,
            "offset": offset,
        }
        # Filter out None values to avoid sending them
        clean_params: typing.Dict[str, int] = {
            k: v for k, v in params.items() if v is not None
        }
        response: CurationSetListItemResponseSchema = self.api_call.get(
            self._items_path,
            as_json=True,
            entity_type=CurationSetListItemResponseSchema,
            params=clean_params or None,
        )
        return response

    def get_item(self, item_id: str) -> CurationItemSchema:
        """
        Get a specific item from this curation set.

        Args:
            item_id (str): The ID of the item to retrieve.

        Returns:
            CurationItemSchema: The item schema.
        """
        response: CurationItemSchema = self.api_call.get(
            "/".join([self._items_path, item_id]),
            as_json=True,
            entity_type=CurationItemSchema,
        )
        return response

    def upsert_item(
        self, item_id: str, item: CurationItemSchema
    ) -> CurationItemSchema:
        """
        Create or update an item in this curation set.

        Args:
            item_id (str): The ID of the item.
            item (CurationItemSchema): The item schema.

        Returns:
            CurationItemSchema: The created or updated item.
        """
        response: CurationItemSchema = self.api_call.put(
            "/".join([self._items_path, item_id]),
            body=item,
            entity_type=CurationItemSchema,
        )
        return response

    def delete_item(self, item_id: str) -> CurationItemDeleteSchema:
        """
        Delete an item from this curation set.

        Args:
            item_id (str): The ID of the item to delete.

        Returns:
            CurationItemDeleteSchema: The deletion response.
        """
        response: CurationItemDeleteSchema = self.api_call.delete(
            "/".join([self._items_path, item_id]),
            entity_type=CurationItemDeleteSchema,
        )
        return response
