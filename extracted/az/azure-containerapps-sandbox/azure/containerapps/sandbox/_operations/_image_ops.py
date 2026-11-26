"""Disk image operations for sandbox data-plane client."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from azure.core.paging import ItemPaged
from azure.core.polling import LROPoller
from azure.core.tracing.decorator import distributed_trace

from azure.containerapps.sandbox._helpers import (
    _disk_image_create_body,
    _ERROR_MAP,
    _validate_segment,
)
from azure.containerapps.sandbox._models import DiskImage, PublicDiskImage
from azure.containerapps.sandbox._response_helpers import _normalize_page
from azure.containerapps.sandbox._polling import (
    DeletionPoller,
    ResourceStatePoller,
)

if TYPE_CHECKING:
    from azure.containerapps.sandbox._models import RegistryCredentials

logger = logging.getLogger("azure.containerapps.sandbox")


def _image_state(img: DiskImage) -> str | None:
    return img.status.state if (img and img.status) else None


class ImageOperationsMixin:
    """Disk image operations (list, get, create, delete; public images)."""

    @distributed_trace
    def list_disk_images(self, **kwargs: Any) -> ItemPaged[DiskImage]:
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
    def list_public_disk_images(self, **kwargs: Any) -> ItemPaged[PublicDiskImage]:
        """List public disk images available within a sandbox group's scope."""
        return self._generated.public_disk_images.list(
            **{
                "error_map": _ERROR_MAP,
                "_continuation_endpoint": self._endpoint,
                "cls": _normalize_page,
                **kwargs,
            },
        )

    @distributed_trace
    def get_disk_image(self, image_id: str, **kwargs: Any) -> DiskImage:
        """Get a disk image by ID."""
        _validate_segment(image_id, "image_id")
        return self._generated.disk_images.get(image_id, **{"error_map": _ERROR_MAP, **kwargs})

    @distributed_trace
    def create_disk_image(self, base_image: str, *, name: str | None = None,
                          registry_credentials: "RegistryCredentials | None" = None,
                          managed_identity_client_id: str | None = None,
                          **kwargs: Any) -> DiskImage:
        """Create a disk image from a container image (returns immediately).

        For build completion, prefer :meth:`begin_create_disk_image` which
        returns an :class:`~azure.core.polling.LROPoller` and can poll until
        ``status.state == "Ready"``.

        ``managed_identity_client_id`` accepts case-insensitive ``system`` or
        a user-assigned identity's canonical UUID client ID. Registry credentials
        and managed identity are mutually exclusive. No identity lookup is performed.
        """
        body = _disk_image_create_body(
            base_image, name, registry_credentials, managed_identity_client_id, kwargs,
        )
        return self._generated.disk_images.create(body, **{"error_map": _ERROR_MAP, **kwargs})

    @distributed_trace
    def begin_create_disk_image(
        self,
        base_image: str,
        *,
        name: str | None = None,
        registry_credentials: "RegistryCredentials | None" = None,
        managed_identity_client_id: str | None = None,
        polling_timeout: int = 600,
        polling_interval: int = 5,
        **kwargs: Any,
    ) -> LROPoller:
        """Begin building a disk image; poll until ``status.state == "Ready"``."""
        initial = self.create_disk_image(
            base_image,
            name=name,
            registry_credentials=registry_credentials,
            managed_identity_client_id=managed_identity_client_id,
            **kwargs,
        )
        polling_method = ResourceStatePoller(
            getter=lambda: self.get_disk_image(initial.id),
            state_fn=_image_state,
            target_states=("Ready", "Succeeded"),
            failed_states=("Failed",),
            timeout=polling_timeout,
            poll_interval=polling_interval,
            resource_id=f"DiskImage {initial.id}",
            initial_resource=initial,
        )
        return LROPoller(self, initial, lambda _: polling_method.resource(), polling_method)

    @distributed_trace
    def delete_disk_image(self, image_id: str, **kwargs: Any) -> None:
        """Delete a disk image (returns immediately; does not wait for tombstone)."""
        _validate_segment(image_id, "image_id")
        self._generated.disk_images.delete(image_id, **{"error_map": _ERROR_MAP, **kwargs})

    @distributed_trace
    def begin_delete_disk_image(
        self,
        image_id: str,
        *,
        polling_timeout: int = 300,
        polling_interval: int = 3,
        **kwargs: Any,
    ) -> LROPoller:
        """Begin deleting a disk image; poll until GET returns 404."""
        self.delete_disk_image(image_id, **kwargs)
        polling_method = DeletionPoller(
            getter=lambda: self.get_disk_image(image_id),
            timeout=polling_timeout,
            poll_interval=polling_interval,
            resource_id=f"DiskImage {image_id}",
        )
        return LROPoller(self, None, lambda _: None, polling_method)

    @distributed_trace
    def get_public_disk_image(self, image_name: str, **kwargs: Any) -> PublicDiskImage:
        """Get a public disk image by name."""
        _validate_segment(image_name, "image_name")
        return self._generated.public_disk_images.get(image_name, **{"error_map": _ERROR_MAP, **kwargs})
