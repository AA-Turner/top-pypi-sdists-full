"""Volume operations for sandbox data-plane client."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Literal

from azure.core.paging import ItemPaged
from azure.core.polling import LROPoller
from azure.core.tracing.decorator import distributed_trace

from azure.containerapps.sandbox._helpers import (
    _ERROR_MAP,
    _validate_segment,
)
from azure.containerapps.sandbox._models import (
    AzureBlobByoManagedIdentityAuth,
    Volume,
)
from azure.containerapps.sandbox._polling import DeletionPoller
from azure.containerapps.sandbox._volume_helpers import _validate_byo_blob_auth
from azure.containerapps.sandbox._response_helpers import _normalize_page
from azure.containerapps.sandbox.models import AzureBlobByoVolume, AzureBlobVolume, DataDiskVolume

if TYPE_CHECKING:
    pass

logger = logging.getLogger("azure.containerapps.sandbox")


class VolumeOperationsMixin:
    """Volume operations (list, get, create, delete)."""

    @distributed_trace
    def list_volumes(self, **kwargs: Any) -> ItemPaged[Volume]:
        """List volumes in a sandbox group."""
        return self._generated.volumes.list(
            **{
                "error_map": _ERROR_MAP,
                "_continuation_endpoint": self._endpoint,
                "cls": _normalize_page,
                **kwargs,
            },
        )

    @distributed_trace
    def get_volume(self, volume_name: str, **kwargs: Any) -> Volume:
        """Get a volume by name."""
        _validate_segment(volume_name, "volume_name")
        return self._generated.volumes.get(volume_name, **{"error_map": _ERROR_MAP, **kwargs})

    @distributed_trace
    def create_volume(self, name: str, *, size: str | None = None,
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
            _validate_byo_blob_auth(auth)
            body["storageContainerResourceId"] = storage_container_resource_id
            body["auth"] = auth
        _validate_segment(name, "name")
        content = {"AzureBlob": AzureBlobVolume, "AzureBlobByo": AzureBlobByoVolume, "DataDisk": DataDiskVolume}[type](
            body
        )
        return self._generated.volumes.create(name, content, **{"error_map": _ERROR_MAP, **kwargs})

    @distributed_trace
    def delete_volume(self, volume_name: str, **kwargs: Any) -> None:
        """Delete a volume (returns immediately; does not wait for tombstone)."""
        _validate_segment(volume_name, "volume_name")
        self._generated.volumes.delete(volume_name, **{"error_map": _ERROR_MAP, **kwargs})

    @distributed_trace
    def begin_delete_volume(
        self,
        volume_name: str,
        *,
        polling_timeout: int = 300,
        polling_interval: int = 3,
        **kwargs: Any,
    ) -> LROPoller:
        """Begin deleting a volume; poll until GET returns 404."""
        self.delete_volume(volume_name, **kwargs)
        polling_method = DeletionPoller(
            getter=lambda: self.get_volume(volume_name),
            timeout=polling_timeout,
            poll_interval=polling_interval,
            resource_id=f"Volume {volume_name}",
        )
        return LROPoller(self, None, lambda _: None, polling_method)
