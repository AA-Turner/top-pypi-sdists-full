"""
This module provides async functionality for managing individual documents in Typesense collections.

It contains the Document class, which allows for retrieving, updating, and deleting
documents asynchronously.

Classes:
    Document: Manages async operations on a single document in the Typesense API.

Dependencies:
    - typesense.async_api_call: Provides the ApiCall class for making async API requests.
    - typesense.types.document: Provides various document schema types.

Note: This module uses conditional imports to support both Python 3.11+ and earlier versions.
"""

import sys

from .api_call import ApiCall
from typesense.types.document import (
    DeleteSingleDocumentParameters,
    DirtyValuesParameters,
    DocumentSchema,
    RetrieveParameters,
)

if sys.version_info >= (3, 11):
    import typing
else:
    import typing_extensions as typing

TDoc = typing.TypeVar("TDoc", bound=DocumentSchema)


class Document(typing.Generic[TDoc]):
    """
    Manages async operations on a single document in the Typesense API.

    This class provides async methods to retrieve, update, and delete a document.

    Attributes:
        api_call (ApiCall): The ApiCall instance for making async API requests.
        collection_name (str): The name of the collection.
        document_id (str): The ID of the document.
    """

    def __init__(
        self,
        api_call: ApiCall,
        collection_name: str,
        document_id: str,
    ) -> None:
        """
        Initialize the Document instance.

        Args:
            api_call (ApiCall): The ApiCall instance for making async API requests.
            collection_name (str): The name of the collection.
            document_id (str): The ID of the document.
        """
        self.api_call = api_call
        self.collection_name = collection_name
        self.document_id = document_id

    def retrieve(
        self,
        retrieve_parameters: typing.Union[RetrieveParameters, None] = None,
    ) -> TDoc:
        """
        Retrieve this specific document.

        Args:
            retrieve_parameters (Union[RetrieveParameters, None], optional):
                Parameters for retrieving the document.

        Returns:
            TDoc: The retrieved document.
        """
        response = self.api_call.get(
            endpoint=self._endpoint_path,
            entity_type=typing.Dict[str, str],
            as_json=True,
            params=retrieve_parameters,
        )
        return typing.cast(TDoc, response)

    def update(
        self,
        document: TDoc,
        dirty_values_parameters: typing.Union[DirtyValuesParameters, None] = None,
    ) -> TDoc:
        """
        Update this specific document.

        Args:
            document (TDoc): The updated document data.
            dirty_values_parameters (Union[DirtyValuesParameters, None], optional):
                Parameters for handling dirty values.

        Returns:
            TDoc: The updated document.
        """
        response = self.api_call.patch(
            self._endpoint_path,
            body=document,
            params=dirty_values_parameters,
            entity_type=typing.Dict[str, str],
        )
        return typing.cast(TDoc, response)

    def delete(
        self,
        delete_parameters: typing.Union[DeleteSingleDocumentParameters, None] = None,
    ) -> TDoc:
        """
        Delete this specific document.

        Args:
            delete_parameters (Union[DeleteSingleDocumentParameters, None], optional):
                Parameters for deletion.

        Returns:
            TDoc: The deleted document.
        """
        response = self.api_call.delete(
            self._endpoint_path,
            entity_type=typing.Dict[str, str],
            params=delete_parameters,
        )
        return typing.cast(TDoc, response)

    @property
    def _endpoint_path(self) -> str:
        """
        Construct the API endpoint path for this specific document.

        Returns:
            str: The constructed endpoint path.
        """
        from .collections import Collections
        from .documents import Documents

        return "/".join(
            [
                Collections.resource_path,
                self.collection_name,
                Documents.resource_path,
                self.document_id,
            ],
        )
