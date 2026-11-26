"""Snapshot operations for sandbox data-plane client."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from azure.core.paging import ItemPaged
from azure.core.polling import LROPoller
from azure.core.tracing.decorator import distributed_trace

from azure.containerapps.sandbox._helpers import (
    _ERROR_MAP,
    _validate_segment,
)
from azure.containerapps.sandbox._models import Snapshot
from azure.containerapps.sandbox._response_helpers import _normalize_page
from azure.containerapps.sandbox._polling import DeletionPoller

if TYPE_CHECKING:
    pass

logger = logging.getLogger("azure.containerapps.sandbox")


class SnapshotOperationsMixin:
    """Snapshot operations (list, get, delete)."""

    @distributed_trace
    def list_snapshots(self, **kwargs: Any) -> ItemPaged[Snapshot]:
        """List snapshots in a sandbox group."""
        return self._generated.snapshots.list(
            **{
                "error_map": _ERROR_MAP,
                "_continuation_endpoint": self._endpoint,
                "cls": _normalize_page,
                **kwargs,
            },
        )

    @distributed_trace
    def get_snapshot(self, snapshot_id: str, **kwargs: Any) -> Snapshot:
        """Get a snapshot by ID."""
        _validate_segment(snapshot_id, "snapshot_id")
        return self._generated.snapshots.get(snapshot_id, **{"error_map": _ERROR_MAP, **kwargs})

    @distributed_trace
    def delete_snapshot(self, snapshot_id: str, **kwargs: Any) -> None:
        """Delete a snapshot (returns immediately; does not wait for tombstone)."""
        _validate_segment(snapshot_id, "snapshot_id")
        self._generated.snapshots.delete(snapshot_id, **{"error_map": _ERROR_MAP, **kwargs})

    @distributed_trace
    def begin_delete_snapshot(
        self,
        snapshot_id: str,
        *,
        polling_timeout: int = 300,
        polling_interval: int = 3,
        **kwargs: Any,
    ) -> LROPoller:
        """Begin deleting a snapshot; poll until GET returns 404."""
        self.delete_snapshot(snapshot_id, **kwargs)
        polling_method = DeletionPoller(
            getter=lambda: self.get_snapshot(snapshot_id),
            timeout=polling_timeout,
            poll_interval=polling_interval,
            resource_id=f"Snapshot {snapshot_id}",
        )
        return LROPoller(self, None, lambda _: None, polling_method)
