"""
This module provides async functionality for managing individual aliases in Typesense.

It contains the AsyncAlias class, which allows for retrieving and deleting
aliases asynchronously.

Classes:
    AsyncAlias: Manages async operations on a single alias in the Typesense API.

Dependencies:
    - typesense.async_api_call: Provides the AsyncApiCall class for making async API requests.
    - typesense.types.alias: Provides AliasSchema type.

Note: This module uses conditional imports to support both Python 3.11+ and earlier versions.
"""

from .api_call import AsyncApiCall
from typesense.types.alias import AliasSchema


class AsyncAlias:
    """
    Manages async operations on a single alias in the Typesense API.

    This class provides async methods to retrieve and delete an alias.

    Attributes:
        api_call (AsyncApiCall): The AsyncApiCall instance for making async API requests.
        name (str): The name of the alias.
    """

    def __init__(self, api_call: AsyncApiCall, name: str):
        """
        Initialize the AsyncAlias instance.

        Args:
            api_call (AsyncApiCall): The AsyncApiCall instance for making async API requests.
            name (str): The name of the alias.
        """
        self.api_call = api_call
        self.name = name

    async def retrieve(self) -> AliasSchema:
        """
        Retrieve this specific alias.

        Returns:
            AliasSchema: The schema containing the alias details.
        """
        response: AliasSchema = await self.api_call.get(
            self._endpoint_path,
            entity_type=AliasSchema,
            as_json=True,
        )
        return response

    async def delete(self) -> AliasSchema:
        """
        Delete this specific alias.

        Returns:
            AliasSchema: The schema containing the deletion response.
        """
        response: AliasSchema = await self.api_call.delete(
            self._endpoint_path,
            entity_type=AliasSchema,
        )
        return response

    @property
    def _endpoint_path(self) -> str:
        """
        Construct the API endpoint path for this specific alias.

        Returns:
            str: The constructed endpoint path.
        """
        from .aliases import AsyncAliases

        return "/".join([AsyncAliases.resource_path, self.name])
