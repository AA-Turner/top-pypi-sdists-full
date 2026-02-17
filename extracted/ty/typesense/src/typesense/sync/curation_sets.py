"""
This module provides async functionality for managing curation sets in Typesense.

It contains the CurationSets class, which allows for retrieving and
accessing individual curation sets asynchronously.

Classes:
    CurationSets: Manages curation sets in the Typesense API (async).

Dependencies:
    - typesense.async_api_call: Provides the ApiCall class for making async API requests.
    - typesense.async_curation_set: Provides the CurationSet class for individual curation set operations.
    - typesense.types.curation_set: Provides CurationSetsListResponseSchema type.

Note: This module uses conditional imports to support both Python 3.11+ and earlier versions.
"""

import sys

if sys.version_info >= (3, 11):
    import typing
else:
    import typing_extensions as typing

from .api_call import ApiCall
from .curation_set import CurationSet
from typesense.types.curation_set import CurationSetsListResponseSchema


class CurationSets:
    """
    Manages curation sets in the Typesense API (async).

    This class provides async methods to retrieve and access individual curation sets.

    Attributes:
        resource_path (str): The API endpoint path for curation sets operations.
        api_call (ApiCall): The ApiCall instance for making async API requests.
    """

    resource_path: typing.Final[str] = "/curation_sets"

    def __init__(self, api_call: ApiCall) -> None:
        """
        Initialize the CurationSets instance.

        Args:
            api_call (ApiCall): The ApiCall instance for making async API requests.
        """
        self.api_call = api_call

    def retrieve(self) -> CurationSetsListResponseSchema:
        """
        Retrieve all curation sets.

        Returns:
            CurationSetsListResponseSchema: The list of all curation sets.

        Example:
            >>> curation_sets = CurationSets(async_api_call)
            >>> all_sets = await curation_sets.retrieve()
            >>> for set in all_sets:
            ...     print(set["name"])
        """
        response: CurationSetsListResponseSchema = self.api_call.get(
            CurationSets.resource_path,
            as_json=True,
            entity_type=CurationSetsListResponseSchema,
        )
        return response

    def __getitem__(self, curation_set_name: str) -> CurationSet:
        """
        Get or create an CurationSet instance for a given curation set name.

        This method allows accessing curation sets using dictionary-like syntax.
        If the CurationSet instance doesn't exist, it creates a new one.

        Args:
            curation_set_name (str): The name of the curation set.

        Returns:
            CurationSet: The CurationSet instance for the specified name.

        Example:
            >>> curation_sets = CurationSets(async_api_call)
            >>> products_set = curation_sets["products"]
        """
        from .curation_set import CurationSet as PerSet

        return PerSet(self.api_call, curation_set_name)
