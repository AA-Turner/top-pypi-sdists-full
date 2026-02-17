"""
This module provides async functionality for accessing debug information in Typesense.

It contains the AsyncDebug class, which allows for retrieving debug information
asynchronously.

Classes:
    AsyncDebug: Manages async operations for accessing debug information in the Typesense API.

Dependencies:
    - typesense.async_api_call: Provides the AsyncApiCall class for making async API requests.
    - typesense.types.debug: Provides DebugResponseSchema type.

Note: This module uses conditional imports to support both Python 3.11+ and earlier versions.
"""

import sys

if sys.version_info >= (3, 11):
    import typing
else:
    import typing_extensions as typing

from .api_call import AsyncApiCall
from typesense.types.debug import DebugResponseSchema


class AsyncDebug:
    """
    Manages async operations for accessing debug information in the Typesense API.

    This class provides async methods to retrieve debug information from the Typesense server,
    which can be useful for system diagnostics and troubleshooting.

    Attributes:
        resource_path (str): The API resource path for debug operations.
        api_call (AsyncApiCall): The AsyncApiCall instance for making async API requests.
    """

    resource_path: typing.Final[str] = "/debug"

    def __init__(self, api_call: AsyncApiCall) -> None:
        """
        Initialize the AsyncDebug instance.

        Args:
            api_call (AsyncApiCall): The AsyncApiCall instance for making async API requests.
        """
        self.api_call = api_call

    async def retrieve(self) -> DebugResponseSchema:
        """
        Retrieve debug information from the Typesense server.

        This method sends an async GET request to the debug endpoint and returns
        the server's debug information.

        Returns:
            DebugResponseSchema: A schema containing the debug information.

        Example:
            >>> debug = AsyncDebug(async_api_call)
            >>> info = await debug.retrieve()
            >>> print(info["version"])
        """
        response: DebugResponseSchema = await self.api_call.get(
            AsyncDebug.resource_path,
            as_json=True,
            entity_type=DebugResponseSchema,
        )
        return response
