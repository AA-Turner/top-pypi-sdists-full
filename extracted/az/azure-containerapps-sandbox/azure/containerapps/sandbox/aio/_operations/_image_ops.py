"""Async disk image operations for sandbox data-plane client."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from azure.core.async_paging import AsyncItemPaged
from azure.core.polling import AsyncLROPoller
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator import distributed_trace
from azure.core.tracing.decorator_async import distributed_trace_async

from azure.containerapps.sandbox._helpers import (
    _validate_continuation_token,
    _validate_segment,
)
from azure.containerapps.sandbox._models import DiskImage, PublicDiskImage
from azure.containerapps.sandbox.aio._polling import (
    AsyncDeletionPoller,
    AsyncResourceStatePoller,
)

if TYPE_CHECKING:
    pass

logger = logging.getLogger("azure.containerapps.sandbox")


class AsyncImageOperationsMixin:
    """Async disk image operations (list, get, create, delete; public images)."""

    @distributed_trace
    def list_disk_images(self, **kwargs: Any) -> AsyncItemPaged[DiskImage]:
        """List private disk images in a sandbox group."""
        base_url = f"{self._endpoint}{self._group_path}/diskimages"
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
                return None, iter([DiskImage._from_dict(d) for d in data])
            items = [DiskImage._from_dict(d) for d in data.get("value", [])]
            return data.get("nextLink"), iter(items)

        return AsyncItemPaged(_get_next, extract_data=_extract_data)

    @distributed_trace
    def list_public_disk_images(self, **kwargs: Any) -> AsyncItemPaged[PublicDiskImage]:
        """List public disk images available within a sandbox group's scope."""
        base_url = f"{self._endpoint}{self._group_path}/diskimages/public"
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
                return None, iter([PublicDiskImage._from_dict(d) for d in data])
            items = [PublicDiskImage._from_dict(d) for d in data.get("value", [])]
            return data.get("nextLink"), iter(items)

        return AsyncItemPaged(_get_next, extract_data=_extract_data)

    @distributed_trace_async
    async def get_disk_image(self, image_id: str, **kwargs: Any) -> DiskImage:
        """Get a disk image by ID."""
        _validate_segment(image_id, "image_id")
        return DiskImage._from_dict(await self._dp_get(f"{self._group_path}/diskimages/{image_id}"))

    @distributed_trace_async
    async def create_disk_image(self, base_image: str, *, name: str | None = None,
                                entrypoint: list[str] | None = None,
                                cmd: list[str] | None = None,
                                registry_credentials: "RegistryCredentials | None" = None,
                                managed_identity_resource_id: str | None = None,
                                **kwargs: Any) -> DiskImage:
        """Create a disk image from a container image (returns immediately).

        Prefer :meth:`begin_create_disk_image` to wait for build completion.
        """
        body: dict = {"image": {"base": base_image}}
        if entrypoint:
            body["image"]["entrypoint"] = entrypoint
        if cmd:
            body["image"]["cmd"] = cmd
        if name:
            body["labels"] = {"name": name}
        if registry_credentials:
            body["registryCredentials"] = registry_credentials._to_dict()
        if managed_identity_resource_id:
            body["managedIdentityResourceId"] = managed_identity_resource_id
        return DiskImage._from_dict(await self._dp_put(f"{self._group_path}/diskimages", body))

    @distributed_trace_async
    async def begin_create_disk_image(
        self,
        base_image: str,
        *,
        name: str | None = None,
        entrypoint: list[str] | None = None,
        cmd: list[str] | None = None,
        registry_credentials: "RegistryCredentials | None" = None,
        managed_identity_resource_id: str | None = None,
        polling_timeout: int = 600,
        polling_interval: int = 5,
        **kwargs: Any,
    ) -> AsyncLROPoller:
        """Begin building a disk image; poll until ``status.state == "Ready"``."""
        initial = await self.create_disk_image(
            base_image, name=name, entrypoint=entrypoint, cmd=cmd,
            registry_credentials=registry_credentials,
            managed_identity_resource_id=managed_identity_resource_id, **kwargs,
        )
        polling_method = AsyncResourceStatePoller(
            getter=lambda: self.get_disk_image(initial.id),
            state_fn=lambda i: i.status.state if (i and i.status) else None,
            target_states=("Ready", "Succeeded"),
            failed_states=("Failed",),
            timeout=polling_timeout,
            poll_interval=polling_interval,
            resource_id=f"DiskImage {initial.id}",
            initial_resource=initial,
        )
        return AsyncLROPoller(self, initial, lambda _: polling_method.resource(), polling_method)

    @distributed_trace_async
    async def delete_disk_image(self, image_id: str, **kwargs: Any) -> None:
        """Delete a disk image (returns immediately; does not wait for tombstone)."""
        _validate_segment(image_id, "image_id")
        await self._dp_delete(f"{self._group_path}/diskimages/{image_id}")

    @distributed_trace_async
    async def begin_delete_disk_image(
        self,
        image_id: str,
        *,
        polling_timeout: int = 300,
        polling_interval: int = 3,
        **kwargs: Any,
    ) -> AsyncLROPoller:
        """Begin deleting a disk image; poll until GET returns 404."""
        await self.delete_disk_image(image_id)
        polling_method = AsyncDeletionPoller(
            getter=lambda: self.get_disk_image(image_id),
            timeout=polling_timeout,
            poll_interval=polling_interval,
            resource_id=f"DiskImage {image_id}",
        )
        return AsyncLROPoller(self, None, lambda _: None, polling_method)

    @distributed_trace_async
    async def get_public_disk_image(self, image_name: str, **kwargs: Any) -> PublicDiskImage:
        """Get a public disk image by name."""
        _validate_segment(image_name, "image_name")
        return PublicDiskImage._from_dict(
            await self._dp_get(f"{self._group_path}/diskimages/public/{image_name}")
        )
