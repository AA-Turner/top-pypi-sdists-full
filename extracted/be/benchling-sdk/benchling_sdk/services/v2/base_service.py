from abc import ABC
from typing import Optional, Type, TYPE_CHECKING

from benchling_api_client.v2.stable.client import Client
from benchling_api_client.v2.types import Response

from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.retry_helpers import RetryStrategy

if TYPE_CHECKING:
    from benchling_sdk.helpers.task_helpers import TaskHelper


class BaseService(ABC):
    """Abstract class for Benchling functional namespaces."""

    _client: Client
    _retry_strategy: RetryStrategy

    def __init__(self, client: Client, retry_strategy: Optional[RetryStrategy] = None):
        """
        Initialize a service.

        :param client: Underlying generated Client.
        :param retry_strategy: Retry strategy for failed HTTP calls
        """
        self._client = client
        self._retry_strategy = retry_strategy or RetryStrategy()

    @property
    def client(self) -> Client:
        """Provide access to the underlying generated Benchling Client."""
        return self._client

    @property
    def retry_strategy(self) -> RetryStrategy:
        """Provide access to the underlying user-specified RetryStrategy."""
        return self._retry_strategy

    def _create_service(self, cls):
        """
        Instantiate a service that derives from BaseService, with the same properties as this service.

        Override this in alpha and beta services that use a client other than self._client.
        """
        return cls(self._client, self._retry_strategy)

    def _task_helper_from_response(self, response: Response, result_type: Type) -> "TaskHelper":
        from benchling_sdk.helpers.task_helpers import TaskHelper

        return TaskHelper(model_from_detailed(response), self.client, result_type)
