"""
This module provides async functionality for managing curation sets in Typesense.

It contains the AsyncCurationSets class, which allows for retrieving and
accessing individual curation sets asynchronously.

Classes:
    AsyncCurationSets: Manages curation sets in the Typesense API (async).

Dependencies:
    - typesense.async_api_call: Provides the AsyncApiCall class for making async API requests.
    - typesense.async_curation_set: Provides the AsyncCurationSet class for individual curation set operations.
    - typesense.types.curation_set: Provides CurationSetsListResponseSchema type.

Note: This module uses conditional imports to support both Python 3.11+ and earlier versions.
"""

import sys

if sys.version_info >= (3, 11):
    import typing
else:
    import typing_extensions as typing

from .api_call import AsyncApiCall
from .curation_set import AsyncCurationSet
from typesense.types.curation_set import CurationSetsListResponseSchema


class AsyncCurationSets:
    """
    Manages curation sets in the Typesense API (async).

    This class provides async methods to retrieve and access individual curation sets.

    Attributes:
        resource_path (str): The API endpoint path for curation sets operations.
        api_call (AsyncApiCall): The AsyncApiCall instance for making async API requests.
    """

    resource_path: typing.Final[str] = "/curation_sets"

    def __init__(self, api_call: AsyncApiCall) -> None:
        """
        Initialize the AsyncCurationSets instance.

        Args:
            api_call (AsyncApiCall): The AsyncApiCall instance for making async API requests.
        """
        self.api_call = api_call

    async def retrieve(self) -> CurationSetsListResponseSchema:
        """
        Retrieve all curation sets.

        Returns:
            CurationSetsListResponseSchema: The list of all curation sets.

        Example:
            >>> curation_sets = AsyncCurationSets(async_api_call)
            >>> all_sets = await curation_sets.retrieve()
            >>> for set in all_sets:
            ...     print(set["name"])
        """
        response: CurationSetsListResponseSchema = await self.api_call.get(
            AsyncCurationSets.resource_path,
            as_json=True,
            entity_type=CurationSetsListResponseSchema,
        )
        return response

    def __getitem__(self, curation_set_name: str) -> AsyncCurationSet:
        """
        Get or create an AsyncCurationSet instance for a given curation set name.

        This method allows accessing curation sets using dictionary-like syntax.
        If the AsyncCurationSet instance doesn't exist, it creates a new one.

        Args:
            curation_set_name (str): The name of the curation set.

        Returns:
            AsyncCurationSet: The AsyncCurationSet instance for the specified name.

        Example:
            >>> curation_sets = AsyncCurationSets(async_api_call)
            >>> products_set = curation_sets["products"]
        """
        from .curation_set import AsyncCurationSet as PerSet

        return PerSet(self.api_call, curation_set_name)
