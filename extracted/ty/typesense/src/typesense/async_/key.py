"""
This module provides async functionality for managing individual API keys in Typesense.

It contains the AsyncKey class, which allows for retrieving and deleting
API keys asynchronously.

Classes:
    AsyncKey: Manages async operations on a single API key in the Typesense API.

Dependencies:
    - typesense.async_api_call: Provides the AsyncApiCall class for making async API requests.
    - typesense.types.key: Provides ApiKeyDeleteSchema and ApiKeySchema types.

Note: This module uses conditional imports to support both Python 3.11+ and earlier versions.
"""

from .api_call import AsyncApiCall
from typesense.types.key import ApiKeyDeleteSchema, ApiKeySchema


class AsyncKey:
    """
    Manages async operations on a single API key in the Typesense API.

    This class provides async methods to retrieve and delete an API key.

    Attributes:
        key_id (int): The ID of the API key.
        api_call (AsyncApiCall): The AsyncApiCall instance for making async API requests.
    """

    def __init__(self, api_call: AsyncApiCall, key_id: int) -> None:
        """
        Initialize the AsyncKey instance.

        Args:
            api_call (AsyncApiCall): The AsyncApiCall instance for making async API requests.
            key_id (int): The ID of the API key.
        """
        self.key_id = key_id
        self.api_call = api_call

    async def retrieve(self) -> ApiKeySchema:
        """
        Retrieve this specific API key.

        Returns:
            ApiKeySchema: The schema containing the API key details.
        """
        response: ApiKeySchema = await self.api_call.get(
            self._endpoint_path,
            as_json=True,
            entity_type=ApiKeySchema,
        )
        return response

    async def delete(self) -> ApiKeyDeleteSchema:
        """
        Delete this specific API key.

        Returns:
            ApiKeyDeleteSchema: The schema containing the deletion response.
        """
        response: ApiKeyDeleteSchema = await self.api_call.delete(
            self._endpoint_path,
            entity_type=ApiKeyDeleteSchema,
        )
        return response

    @property
    def _endpoint_path(self) -> str:
        """
        Construct the API endpoint path for this specific API key.

        Returns:
            str: The constructed endpoint path.
        """
        from .keys import AsyncKeys

        return "/".join([AsyncKeys.resource_path, str(self.key_id)])
