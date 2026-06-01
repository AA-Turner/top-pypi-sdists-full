"""
The compute client module contains the main classes to interact with the Arraylake compute service.
For asynchronous operations, the `AsyncComputeClient` class is recommended,
while the `ComputeClient` class should be used for synchronous operations.

**Example usage:**

```python
from arraylake import Client
services = Client().get_services("my-org")
services.list_enabled()
```
"""

import functools
import re
from collections.abc import AsyncGenerator
from datetime import datetime
from typing import Any

from arraylake.asyn import sync
from arraylake.compute.http_client import ComputeHttpClient, HttpComputeConfig
from arraylake.compute.types import DeploymentInfo

_VALID_NAME = r"(\w[\w\.\-_]+)"


def _validate_org(org_name: str):
    if not re.fullmatch(_VALID_NAME, org_name):
        raise ValueError(f"Invalid org name: `{org_name}`.")


class AsyncComputeClient:
    """
    Asyncio Client for interacting with the Arraylake Compute API
    for a specific organization.
    """

    def __init__(self, service_uri: str, token: str | None, org: str):
        """
        Initializes the AsyncComputeClient with the service URI, API token, and organization.

        Args:
            service_uri:
                The service URI to target.
            token:
                API token for service account authentication.
            org:
                The organization to target.
        """
        self.service_uri = service_uri
        self.token = token
        _validate_org(org)
        self.org = org
        self.http_client = self._http_client_for_org()

    def to_sync_client(self) -> "ComputeClient":
        return ComputeClient(self)

    def _http_client_for_org(self) -> ComputeHttpClient:
        """Get a new HTTP client for the organization."""
        return ComputeHttpClient(HttpComputeConfig(self.service_uri, self.org, self.token))

    async def enable(self, protocol: str, is_public: bool = False, **kwargs) -> dict[str, Any]:
        """Enables a new Arraylake compute service."""
        return await self.http_client.create_compute_service(protocol, is_public, **kwargs)

    async def list_enabled(self) -> list[DeploymentInfo]:
        """Lists all of the Arraylake compute services for the organization."""
        return await self.http_client.list_compute_services()

    async def get_status(self, service_id: str) -> dict[str, Any]:
        """Gets the status of an Arraylake compute service."""
        return await self.http_client.get_compute_service_status(service_id)

    async def stream_logs(
        self,
        service_id: str,
        *,
        tail: int | None = None,
        follow: bool = False,
        since: datetime | None = None,
        until: datetime | None = None,
        follow_timeout: int = 30,
    ) -> AsyncGenerator[str, None]:
        """Streams the logs of an Arraylake compute service."""
        return self.http_client.get_compute_service_logs(
            service_id, tail=tail, follow=follow, since=since, until=until, follow_timeout=follow_timeout
        )

    async def get_logs(
        self, service_id: str, *, tail: int | None = None, since: datetime | None = None, until: datetime | None = None
    ) -> str:
        """Gets a snapshot of the logs of an Arraylake compute service."""
        log_stream = await self.stream_logs(service_id, tail=tail, since=since, until=until)
        return "\n".join([s async for s in log_stream])

    async def disable(self, service_id: str) -> dict[str, Any]:
        """Disables an Arraylake compute service."""
        # TODO: output types?
        return await self.http_client.delete_compute_service(service_id)


class ComputeClient:
    """Synchronous interface for interacting with the Arraylake Compute API."""

    _aclient: AsyncComputeClient

    def __init__(self, aclient: AsyncComputeClient):
        """Initializes the ComputeClient with an existing AsyncComputeClient instance.

        Args:
            aclient: An existing AsyncComputeClient instance.
        """
        self._aclient = aclient

    def _synchronize(self, method, *args, **kwargs):
        @functools.wraps(method)
        def wrap(*args, **kwargs):
            return sync(method, *args, **kwargs)

        return wrap(*args, **kwargs)

    def enable(self, protocol: str, is_public: bool = False, **kwargs) -> dict[str, Any]:
        """Enables a new Arraylake compute service.

        Args:
            protocol: The protocol to use. Must be one of dap2, edr, wms, or zarr.
            is_public: Whether the service should be public or not. Defaults to False.
            **kwargs: Additional arguments to pass to the service.

        Returns:
            Confirmation of the service being enabled.
        """
        return self._synchronize(self._aclient.enable, protocol, is_public, **kwargs)

    def list_enabled(self) -> list[DeploymentInfo]:
        """Lists all of the Arraylake compute services for the organization.

        Returns:
            The list of services in the organization.
        """
        return self._synchronize(self._aclient.list_enabled)

    def get_status(self, service_id: str) -> dict[str, Any]:
        """Gets the status of an Arraylake compute service.

        Args:
            org: The organization where the service is located.
            service_id: The ID of the service to get status for.

        Returns:
            Dictionary containing the status of the service.
        """
        return self._synchronize(self._aclient.get_status, service_id)

    def get_logs(self, service_id: str, *, tail: int | None = None, since: datetime | None = None, until: datetime | None = None) -> str:
        """Gets a snapshot of the logs of an Arraylake compute service.

        Args:
            service_id: The ID of the service to get logs for.
            tail: The number of lines to fetch from the end of the log.
            since: The start time of the log window.
            until: The end time of the log window.

        Returns:
            The kubernetes logs for the service.
        """
        return self._synchronize(self._aclient.get_logs, service_id, tail=tail, since=since, until=until)

    def disable(self, service_id: str) -> dict[str, Any]:
        """Disables an Arraylake compute service..

        Args:
            service_id: The ID of the service to disable.

        Returns:
            Confirmation of the service being disabled.
        """
        return self._synchronize(self._aclient.disable, service_id)
