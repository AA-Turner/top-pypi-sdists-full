"""
This module provides async functionality for managing individual collections in the Typesense API.

It contains the Collection class, which allows for retrieving, updating, and deleting
collections asynchronously.

Classes:
    Collection: Manages async operations on a single collection in the Typesense API.

Dependencies:
    - typesense.async_api_call: Provides the ApiCall class for making async API requests.
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

from .api_call import ApiCall
from .documents import Documents
from .overrides import Overrides
from .synonyms import Synonyms
from typesense.types.document import DocumentSchema

TDoc = typing.TypeVar("TDoc", bound=DocumentSchema, covariant=True)


class Collection(typing.Generic[TDoc]):
    """
    Manages async operations on a single collection in the Typesense API.

    This class provides async methods to retrieve, update, and delete a collection.
    It is generic over the document type TDoc, which should be a subtype of DocumentSchema.

    Attributes:
        name (str): The name of the collection.
        api_call (ApiCall): The ApiCall instance for making async API requests.
    """

    def __init__(self, api_call: ApiCall, name: str):
        """
        Initialize the Collection instance.

        Args:
            api_call (ApiCall): The ApiCall instance for making async API requests.
            name (str): The name of the collection.
        """
        self.name = name
        self.api_call = api_call

        self.documents: Documents[TDoc] = Documents(api_call, name)
        self._overrides = Overrides(api_call, name)
        self._synonyms = Synonyms(api_call, name)

    def retrieve(self) -> CollectionSchema:
        """
        Retrieve the schema of this collection from Typesense.

        Returns:
            CollectionSchema: The schema of the collection.
        """
        response: CollectionSchema = self.api_call.get(
            endpoint=self._endpoint_path,
            entity_type=CollectionSchema,
            as_json=True,
        )
        return response

    def update(
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
        response: CollectionUpdateSchema = self.api_call.patch(
            endpoint=self._endpoint_path,
            body=schema_change,
            entity_type=CollectionUpdateSchema,
        )
        return response

    def delete(
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
        response: CollectionSchema = self.api_call.delete(
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
    def overrides(self) -> Overrides:
        """Return the Overrides instance for this collection.

        Returns:
            Overrides: The Overrides instance for this collection.
        """
        return self._overrides

    @property
    @deprecated(
        "Synonyms is deprecated on v30+. Use client.synonym_sets instead.",
        category=None,
    )
    def synonyms(self) -> Synonyms:
        """Return the Synonyms instance for this collection.

        Returns:
            Synonyms: The Synonyms instance for this collection.
        """
        """Return the Synonyms instance for this collection."""
        return self._synonyms

    @property
    def _endpoint_path(self) -> str:
        """
        Get the API endpoint path for this collection.

        Returns:
            str: The full endpoint path for the collection.
        """
        from .collections import Collections

        return "/".join([Collections.resource_path, self.name])
