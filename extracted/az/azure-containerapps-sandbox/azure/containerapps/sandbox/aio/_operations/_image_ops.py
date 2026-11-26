"""Async disk image operations for sandbox data-plane client."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from azure.core.async_paging import AsyncItemPaged
from azure.core.polling import AsyncLROPoller
from azure.core.tracing.decorator import distributed_trace
from azure.core.tracing.decorator_async import distributed_trace_async

from azure.containerapps.sandbox._helpers import (
    _disk_image_create_body,
    _ERROR_MAP,
    _validate_segment,
)
from azure.containerapps.sandbox._models import DiskImage, PublicDiskImage
from azure.containerapps.sandbox._response_helpers import _normalize_page
from azure.containerapps.sandbox.aio._polling import (
    AsyncDeletionPoller,
    AsyncResourceStatePoller,
)

if TYPE_CHECKING:
    from azure.containerapps.sandbox._models import RegistryCredentials

logger = logging.getLogger("azure.containerapps.sandbox")


class AsyncImageOperationsMixin:
    """Async disk image operations (list, get, create, delete; public images)."""

    @distributed_trace
    def list_disk_images(self, **kwargs: Any) -> AsyncItemPaged[DiskImage]:
        """List private disk images in a sandbox group."""
        return self._generated.disk_images.list(
            **{
                "error_map": _ERROR_MAP,
                "_continuation_endpoint": self._endpoint,
                "cls": _normalize_page,
                **kwargs,
            },
        )

    @distributed_trace
    def list_public_disk_images(self, **kwargs: Any) -> AsyncItemPaged[PublicDiskImage]:
        """List public disk images available within a sandbox group's scope."""
        return self._generated.public_disk_images.list(
            **{
                "error_map": _ERROR_MAP,
                "_continuation_endpoint": self._endpoint,
                "cls": _normalize_page,
                **kwargs,
            },
        )

    @distributed_trace_async
    async def get_disk_image(self, image_id: str, **kwargs: Any) -> DiskImage:
        """Get a disk image by ID."""
        _validate_segment(image_id, "image_id")
        return await self._generated.disk_images.get(image_id, **{"error_map": _ERROR_MAP, **kwargs})

    @distributed_trace_async
    async def create_disk_image(self, base_image: str, *, name: str | None = None,
                                registry_credentials: "RegistryCredentials | None" = None,
                                managed_identity_client_id: str | None = None,
                                **kwargs: Any) -> DiskImage:
        """Create a disk image from a container image (returns immediately).

        Prefer :meth:`begin_create_disk_image` to wait for build completion.

        ``managed_identity_client_id`` accepts case-insensitive ``system`` or
        a user-assigned identity's canonical UUID client ID. Registry credentials
        and managed identity are mutually exclusive. No identity lookup is performed.
        """
        body = _disk_image_create_body(
            base_image, name, registry_credentials, managed_identity_client_id, kwargs,
        )
        return await self._generated.disk_images.create(body, **{"error_map": _ERROR_MAP, **kwargs})

    @distributed_trace_async
    async def begin_create_disk_image(
        self,
        base_image: str,
        *,
        name: str | None = None,
        registry_credentials: "RegistryCredentials | None" = None,
        managed_identity_client_id: str | None = None,
        polling_timeout: int = 600,
        polling_interval: int = 5,
        **kwargs: Any,
    ) -> AsyncLROPoller:
        """Begin building a disk image; poll until ``status.state == "Ready"``."""
        initial = await self.create_disk_image(
            base_image, name=name,
            registry_credentials=registry_credentials,
            managed_identity_client_id=managed_identity_client_id, **kwargs,
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
        await self._generated.disk_images.delete(image_id, **{"error_map": _ERROR_MAP, **kwargs})

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
        await self.delete_disk_image(image_id, **kwargs)
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
        return await self._generated.public_disk_images.get(image_name, **{"error_map": _ERROR_MAP, **kwargs})
