"""Disk image operations for sandbox data-plane client."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from azure.core.paging import ItemPaged
from azure.core.polling import LROPoller
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator import distributed_trace

from azure.containerapps.sandbox._helpers import (
    _validate_continuation_token,
    _validate_segment,
)
from azure.containerapps.sandbox._models import DiskImage, PublicDiskImage
from azure.containerapps.sandbox._polling import (
    DeletionPoller,
    ResourceStatePoller,
)

if TYPE_CHECKING:
    pass

logger = logging.getLogger("azure.containerapps.sandbox")


def _image_state(img: DiskImage) -> str | None:
    return img.status.state if (img and img.status) else None


class ImageOperationsMixin:
    """Disk image operations (list, get, create, delete; public images)."""

    @distributed_trace
    def list_disk_images(self, **kwargs: Any) -> ItemPaged[DiskImage]:
        """List private disk images in a sandbox group."""
        base_url = f"{self._endpoint}{self._group_path}/diskimages"
        params = {"api-version": self._api_version}

        def _get_next(continuation_token=None):
            if continuation_token:
                _validate_continuation_token(continuation_token, self._endpoint)
                request = HttpRequest("GET", continuation_token)
            else:
                request = HttpRequest("GET", base_url, params=params)
            return self._send_request(request)

        def _extract_data(response):
            data = response.json()
            if isinstance(data, list):
                return None, iter([DiskImage._from_dict(d) for d in data])
            items = [DiskImage._from_dict(d) for d in data.get("value", [])]
            return data.get("nextLink"), iter(items)

        return ItemPaged(_get_next, extract_data=_extract_data)

    @distributed_trace
    def list_public_disk_images(self, **kwargs: Any) -> ItemPaged[PublicDiskImage]:
        """List public disk images available within a sandbox group's scope."""
        base_url = f"{self._endpoint}{self._group_path}/diskimages/public"
        params = {"api-version": self._api_version}

        def _get_next(continuation_token=None):
            if continuation_token:
                _validate_continuation_token(continuation_token, self._endpoint)
                request = HttpRequest("GET", continuation_token)
            else:
                request = HttpRequest("GET", base_url, params=params)
            return self._send_request(request)

        def _extract_data(response):
            data = response.json()
            if isinstance(data, list):
                return None, iter([PublicDiskImage._from_dict(d) for d in data])
            items = [PublicDiskImage._from_dict(d) for d in data.get("value", [])]
            return data.get("nextLink"), iter(items)

        return ItemPaged(_get_next, extract_data=_extract_data)

    @distributed_trace
    def get_disk_image(self, image_id: str, **kwargs: Any) -> DiskImage:
        """Get a disk image by ID."""
        _validate_segment(image_id, "image_id")
        return DiskImage._from_dict(self._dp_get(f"{self._group_path}/diskimages/{image_id}"))

    @distributed_trace
    def create_disk_image(self, base_image: str, *, name: str | None = None,
                          entrypoint: list[str] | None = None,
                          cmd: list[str] | None = None,
                          registry_credentials: "RegistryCredentials | None" = None,
                          managed_identity_resource_id: str | None = None,
                          **kwargs: Any) -> DiskImage:
        """Create a disk image from a container image (returns immediately).

        For build completion, prefer :meth:`begin_create_disk_image` which
        returns an :class:`~azure.core.polling.LROPoller` and can poll until
        ``status.state == "Ready"``.
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
        return DiskImage._from_dict(self._dp_put(f"{self._group_path}/diskimages", body))

    @distributed_trace
    def begin_create_disk_image(
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
    ) -> LROPoller:
        """Begin building a disk image; poll until ``status.state == "Ready"``."""
        initial = self.create_disk_image(
            base_image,
            name=name,
            entrypoint=entrypoint,
            cmd=cmd,
            registry_credentials=registry_credentials,
            managed_identity_resource_id=managed_identity_resource_id,
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
        self._dp_delete(f"{self._group_path}/diskimages/{image_id}")

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
        self.delete_disk_image(image_id)
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
        return PublicDiskImage._from_dict(
            self._dp_get(f"{self._group_path}/diskimages/public/{image_name}")
        )
