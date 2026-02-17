"""
This module provides async functionality for managing collections in the Typesense API.

It contains the AsyncCollections class, which allows for creating, retrieving, and
accessing individual collections asynchronously.

Classes:
    AsyncCollections: Manages collections in the Typesense API (async).

Dependencies:
    - typesense.async_api_call: Provides the AsyncApiCall class for making async API requests.
    - typesense.async_collection: Provides the AsyncCollection class for individual collection operations.
    - typesense.types.collection: Provides CollectionCreateSchema and CollectionSchema types.
    - typesense.types.document: Provides DocumentSchema type.

Note: This module uses conditional imports to support both Python 3.11+ and earlier versions.
"""

import sys

if sys.version_info >= (3, 11):
    import typing
else:
    import typing_extensions as typing

from .api_call import AsyncApiCall
from .collection import AsyncCollection
from typesense.types.collection import CollectionCreateSchema, CollectionSchema
from typesense.types.document import DocumentSchema

TDoc = typing.TypeVar("TDoc", bound=DocumentSchema, covariant=True)


class AsyncCollections(typing.Generic[TDoc]):
    """
    Manages collections in the Typesense API (async).

    This class provides async methods to create, retrieve, and access individual collections.
    It is generic over the document type TDoc, which should be a subtype of DocumentSchema.

    Attributes:
        resource_path (str): The API endpoint path for collections operations.
        api_call (AsyncApiCall): The AsyncApiCall instance for making async API requests.
        collections (Dict[str, AsyncCollection[TDoc]]):
           A dictionary of AsyncCollection instances, keyed by collection name.
    """

    resource_path: typing.Final[str] = "/collections"

    def __init__(self, api_call: AsyncApiCall):
        """
        Initialize the AsyncCollections instance.

        Args:
            api_call (AsyncApiCall): The AsyncApiCall instance for making async API requests.
        """
        self.api_call = api_call
        self.collections: typing.Dict[str, AsyncCollection[TDoc]] = {}

    async def __contains__(self, collection_name: str) -> bool:
        """
        Check if a collection exists in Typesense.

        This method tries to retrieve the specified collection to check for its existence,
        utilizing the AsyncCollection.retrieve() method but without caching non-existent collections.

        Args:
            collection_name (str): The name of the collection to check.

        Returns:
            bool: True if the collection exists, False otherwise.
        """
        if collection_name in self.collections:
            try:
                await self.collections[collection_name].retrieve()
                return True
            except Exception:
                self.collections.pop(collection_name, None)
                return False

        try:
            await AsyncCollection(self.api_call, collection_name).retrieve()
            return True
        except Exception:
            return False

    def __getitem__(self, collection_name: str) -> AsyncCollection[TDoc]:
        """
        Get or create an AsyncCollection instance for a given collection name.

        This method allows accessing collections using dictionary-like syntax.
        If the AsyncCollection instance doesn't exist, it creates a new one.

        Args:
            collection_name (str): The name of the collection to access.

        Returns:
            AsyncCollection[TDoc]: The AsyncCollection instance for the specified collection name.

        Example:
            >>> collections = AsyncCollections(async_api_call)
            >>> fruits_collection = collections["fruits"]
        """
        if not self.collections.get(collection_name):
            self.collections[collection_name] = AsyncCollection(
                self.api_call,
                collection_name,
            )
        return self.collections[collection_name]

    async def create(self, schema: CollectionCreateSchema) -> CollectionSchema:
        """
        Create a new collection in Typesense.

        Args:
            schema (CollectionCreateSchema):
               The schema defining the structure of the new collection.

        Returns:
            CollectionSchema:
                The schema of the created collection, as returned by the API.

        Example:
            >>> collections = AsyncCollections(async_api_call)
            >>> schema = {
            ...     "name": "companies",
            ...     "fields": [
            ...         {"name": "company_name", "type": "string"},
            ...         {"name": "num_employees", "type": "int32"},
            ...         {"name": "country", "type": "string", "facet": True},
            ...     ],
            ...     "default_sorting_field": "num_employees",
            ... }
            >>> created_schema = await collections.create(schema)
        """
        call: CollectionSchema = await self.api_call.post(
            endpoint=AsyncCollections.resource_path,
            entity_type=CollectionSchema,
            as_json=True,
            body=schema,
        )
        return call

    async def retrieve(self) -> typing.List[CollectionSchema]:
        """
        Retrieve all collections from Typesense.

        Returns:
            List[CollectionSchema]:
               A list of schemas for all collections in the Typesense instance.

        Example:
            >>> collections = AsyncCollections(async_api_call)
            >>> all_collections = await collections.retrieve()
            >>> for collection in all_collections:
            ...     print(collection["name"])
        """
        call: typing.List[CollectionSchema] = await self.api_call.get(
            endpoint=AsyncCollections.resource_path,
            as_json=True,
            entity_type=typing.List[CollectionSchema],
        )
        return call
