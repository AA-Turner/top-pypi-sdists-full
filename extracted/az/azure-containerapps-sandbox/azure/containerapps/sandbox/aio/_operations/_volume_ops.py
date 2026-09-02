"""Async volume operations for sandbox data-plane client."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Literal

from azure.core.async_paging import AsyncItemPaged
from azure.core.polling import AsyncLROPoller
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator import distributed_trace
from azure.core.tracing.decorator_async import distributed_trace_async

from azure.containerapps.sandbox._helpers import (
    _validate_continuation_token,
    _validate_segment,
)
from azure.containerapps.sandbox._models import (
    AzureBlobByoManagedIdentityAuth,
    Volume,
)
from azure.containerapps.sandbox.aio._polling import AsyncDeletionPoller

if TYPE_CHECKING:
    pass

logger = logging.getLogger("azure.containerapps.sandbox")


class AsyncVolumeOperationsMixin:
    """Async volume operations (list, get, create, delete)."""

    @distributed_trace
    def list_volumes(self, **kwargs: Any) -> AsyncItemPaged[Volume]:
        """List volumes in a sandbox group."""
        base_url = f"{self._endpoint}{self._group_path}/volumes"
        params = {"api-version": self._api_version}

        async def _get_next(continuation_token=None):
            if continuation_token:
                _validate_continuation_token(continuation_token, self._endpoint)
                request = HttpRequest("GET", continuation_token)
            else:
                request = HttpRequest("GET", base_url, params=params)
            return await self._send_request(request)

        async def _extract_data(response):
            data = response.json()
            if isinstance(data, list):
                return None, iter([Volume._from_dict(v) for v in data])
            items = [Volume._from_dict(v) for v in data.get("value", [])]
            return data.get("nextLink"), iter(items)

        return AsyncItemPaged(_get_next, extract_data=_extract_data)

    @distributed_trace_async
    async def get_volume(self, volume_name: str, **kwargs: Any) -> Volume:
        """Get a volume by name."""
        _validate_segment(volume_name, "volume_name")
        return Volume._from_dict(await self._dp_get(f"{self._group_path}/volumes/{volume_name}"))

    @distributed_trace_async
    async def create_volume(self, name: str, *, size: str | None = None,
                            type: Literal["AzureBlob", "DataDisk", "AzureBlobByo"] = "AzureBlob",
                            labels: dict[str, str] | None = None,
                            storage_container_resource_id: str | None = None,
                            auth: AzureBlobByoManagedIdentityAuth | None = None,
                            **kwargs: Any) -> Volume:
        """Create a volume.

        :param str type: Volume type — ``"AzureBlob"``, ``"DataDisk"``, or
            ``"AzureBlobByo"``.
        :param str size: Disk size (e.g. ``"1Gi"``). Required for DataDisk, ignored for AzureBlob.
        :param str storage_container_resource_id: ARM id of the customer-owned
            blob container. Required for ``"AzureBlobByo"``; ignored otherwise.
        :param auth: Authentication for the customer-owned container. Required
            for ``"AzureBlobByo"``; ignored otherwise.
        """
        _VALID_VOLUME_TYPES = ("AzureBlob", "DataDisk", "AzureBlobByo")
        if type not in _VALID_VOLUME_TYPES:
            raise ValueError(f"Invalid volume type {type!r}. Must be one of {_VALID_VOLUME_TYPES}")
        body: dict = {"type": type}
        if size:
            body["size"] = size
        if labels and len(labels) > 0:
            body["labels"] = labels
        if type == "AzureBlobByo":
            if not storage_container_resource_id:
                raise ValueError(
                    "storage_container_resource_id is required for AzureBlobByo volumes"
                )
            if auth is None:
                raise ValueError("auth is required for AzureBlobByo volumes")
            auth.validate()
            body["storageContainerResourceId"] = storage_container_resource_id
            body["auth"] = auth._to_dict()
        _validate_segment(name, "name")
        return Volume._from_dict(await self._dp_put(f"{self._group_path}/volumes/{name}", body))

    @distributed_trace_async
    async def delete_volume(self, volume_name: str, **kwargs: Any) -> None:
        """Delete a volume (returns immediately; does not wait for tombstone)."""
        _validate_segment(volume_name, "volume_name")
        await self._dp_delete(f"{self._group_path}/volumes/{volume_name}")

    @distributed_trace_async
    async def begin_delete_volume(
        self,
        volume_name: str,
        *,
        polling_timeout: int = 300,
        polling_interval: int = 3,
        **kwargs: Any,
    ) -> AsyncLROPoller:
        """Begin deleting a volume; poll until GET returns 404."""
        await self.delete_volume(volume_name)
        polling_method = AsyncDeletionPoller(
            getter=lambda: self.get_volume(volume_name),
            timeout=polling_timeout,
            poll_interval=polling_interval,
            resource_id=f"Volume {volume_name}",
        )
        return AsyncLROPoller(self, None, lambda _: None, polling_method)
