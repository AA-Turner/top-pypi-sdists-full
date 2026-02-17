"""
This module provides async functionality for retrieving metrics from the Typesense API.

It contains the AsyncMetrics class, which handles async API operations for retrieving
system and Typesense metrics such as CPU, memory, disk, and network usage.

Classes:
    MetricsResponse: Type definition for metrics response (imported from typesense.types.metrics).
    AsyncMetrics: Manages async retrieval of metrics from the Typesense API.

Dependencies:
    - typesense.async_api_call: Provides the AsyncApiCall class for making async API requests.
    - typesense.metrics: Provides MetricsResponse type definitions.

Note: This module uses conditional imports to support both Python 3.11+ and earlier versions.
"""

import sys

if sys.version_info >= (3, 11):
    import typing
else:
    import typing_extensions as typing

from .api_call import AsyncApiCall
from typesense.types.metrics import MetricsResponse


class AsyncMetrics:
    """
    Manages async metrics retrieval from the Typesense API.

    This class provides async methods to retrieve system and Typesense metrics
    such as CPU, memory, disk, and network usage.

    Attributes:
        resource_path (str): The base path for metrics endpoint.
        api_call (AsyncApiCall): The AsyncApiCall instance for making async API requests.
    """

    resource_path: typing.Final[str] = "/metrics.json"

    def __init__(self, api_call: AsyncApiCall):
        """
        Initialize the AsyncMetrics instance.

        Args:
            api_call (AsyncApiCall): The AsyncApiCall instance for making async API requests.
        """
        self.api_call = api_call

    async def retrieve(self) -> MetricsResponse:
        """
        Retrieve metrics from the Typesense API.

        Returns:
            MetricsResponse: A dictionary containing system and Typesense metrics.

        Example:
            >>> metrics = AsyncMetrics(async_api_call)
            >>> response = await metrics.retrieve()
            >>> print(response["system_cpu_active_percentage"])
        """
        response: MetricsResponse = await self.api_call.get(
            AsyncMetrics.resource_path,
            as_json=True,
            entity_type=MetricsResponse,
        )
        return response
