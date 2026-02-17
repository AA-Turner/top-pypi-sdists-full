"""
This module provides async functionality for managing individual collections in the Typesense API.

It contains the AsyncCollection class, which allows for retrieving, updating, and deleting
collections asynchronously.

Classes:
    AsyncCollection: Manages async operations on a single collection in the Typesense API.

Dependencies:
    - typesense.async_api_call: Provides the AsyncApiCall class for making async API requests.
    - typesense.types.collection: Provides CollectionSchema and CollectionUpdateSchema types.
    - typesense.types.document: Provides DocumentSchema type.

Note: This module uses conditional imports to support both Python 3.11+ and earlier versions.
"""

import sys

from typing_extensions import deprecated

from typesense.types.collection import CollectionSchema, CollectionUpdateSchema

if sys.version_info >= (3, 11):
    import typing
else:
    import typing_extensions as typing

from .api_call import AsyncApiCall
from .documents import AsyncDocuments
from .overrides import AsyncOverrides
from .synonyms import AsyncSynonyms
from typesense.types.document import DocumentSchema

TDoc = typing.TypeVar("TDoc", bound=DocumentSchema, covariant=True)


class AsyncCollection(typing.Generic[TDoc]):
    """
    Manages async operations on a single collection in the Typesense API.

    This class provides async methods to retrieve, update, and delete a collection.
    It is generic over the document type TDoc, which should be a subtype of DocumentSchema.

    Attributes:
        name (str): The name of the collection.
        api_call (AsyncApiCall): The AsyncApiCall instance for making async API requests.
    """

    def __init__(self, api_call: AsyncApiCall, name: str):
        """
        Initialize the AsyncCollection instance.

        Args:
            api_call (AsyncApiCall): The AsyncApiCall instance for making async API requests.
            name (str): The name of the collection.
        """
        self.name = name
        self.api_call = api_call

        self.documents: AsyncDocuments[TDoc] = AsyncDocuments(api_call, name)
        self._overrides = AsyncOverrides(api_call, name)
        self._synonyms = AsyncSynonyms(api_call, name)

    async def retrieve(self) -> CollectionSchema:
        """
        Retrieve the schema of this collection from Typesense.

        Returns:
            CollectionSchema: The schema of the collection.
        """
        response: CollectionSchema = await self.api_call.get(
            endpoint=self._endpoint_path,
            entity_type=CollectionSchema,
            as_json=True,
        )
        return response

    async def update(
        self, schema_change: CollectionUpdateSchema
    ) -> CollectionUpdateSchema:
        """
        Update the schema of this collection in Typesense.

        Args:
            schema_change (CollectionUpdateSchema):
                The changes to apply to the collection schema.

        Returns:
            CollectionUpdateSchema: The updated schema of the collection.
        """
        response: CollectionUpdateSchema = await self.api_call.patch(
            endpoint=self._endpoint_path,
            body=schema_change,
            entity_type=CollectionUpdateSchema,
        )
        return response

    async def delete(
        self,
        delete_parameters: typing.Union[
            typing.Dict[str, typing.Union[str, bool]],
            None,
        ] = None,
    ) -> CollectionSchema:
        """
        Delete this collection from Typesense.

        Args:
            delete_parameters (Union[Dict[str, Union[str, bool]], None], optional):
                Additional parameters for the delete operation. Defaults to None.

        Returns:
            CollectionSchema: The schema of the deleted collection.
        """
        response: CollectionSchema = await self.api_call.delete(
            self._endpoint_path,
            entity_type=CollectionSchema,
            params=delete_parameters,
        )
        return response

    @property
    @deprecated(
        "Overrides is deprecated on v30+. Use client.curation_sets instead.",
        category=None,
    )
    def overrides(self) -> AsyncOverrides:
        """Return the AsyncOverrides instance for this collection.

        Returns:
            AsyncOverrides: The AsyncOverrides instance for this collection.
        """
        return self._overrides

    @property
    @deprecated(
        "Synonyms is deprecated on v30+. Use client.synonym_sets instead.",
        category=None,
    )
    def synonyms(self) -> AsyncSynonyms:
        """Return the AsyncSynonyms instance for this collection.

        Returns:
            AsyncSynonyms: The AsyncSynonyms instance for this collection.
        """
        """Return the AsyncSynonyms instance for this collection."""
        return self._synonyms

    @property
    def _endpoint_path(self) -> str:
        """
        Get the API endpoint path for this collection.

        Returns:
            str: The full endpoint path for the collection.
        """
        from .collections import AsyncCollections

        return "/".join([AsyncCollections.resource_path, self.name])
