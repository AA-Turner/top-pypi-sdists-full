"""Snapshot operations for sandbox data-plane client."""
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
from azure.containerapps.sandbox._models import Snapshot
from azure.containerapps.sandbox._polling import DeletionPoller

if TYPE_CHECKING:
    pass

logger = logging.getLogger("azure.containerapps.sandbox")


class SnapshotOperationsMixin:
    """Snapshot operations (list, get, delete)."""

    @distributed_trace
    def list_snapshots(self, **kwargs: Any) -> ItemPaged[Snapshot]:
        """List snapshots in a sandbox group."""
        base_url = f"{self._endpoint}{self._group_path}/snapshots"
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
                return None, iter([Snapshot._from_dict(s) for s in data])
            items = [Snapshot._from_dict(s) for s in data.get("value", [])]
            return data.get("nextLink"), iter(items)

        return ItemPaged(_get_next, extract_data=_extract_data)

    @distributed_trace
    def get_snapshot(self, snapshot_id: str, **kwargs: Any) -> Snapshot:
        """Get a snapshot by ID."""
        _validate_segment(snapshot_id, "snapshot_id")
        return Snapshot._from_dict(self._dp_get(f"{self._group_path}/snapshots/{snapshot_id}"))

    @distributed_trace
    def delete_snapshot(self, snapshot_id: str, **kwargs: Any) -> None:
        """Delete a snapshot (returns immediately; does not wait for tombstone)."""
        _validate_segment(snapshot_id, "snapshot_id")
        self._dp_delete(f"{self._group_path}/snapshots/{snapshot_id}")

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
        self.delete_snapshot(snapshot_id)
        polling_method = DeletionPoller(
            getter=lambda: self.get_snapshot(snapshot_id),
            timeout=polling_timeout,
            poll_interval=polling_interval,
            resource_id=f"Snapshot {snapshot_id}",
        )
        return LROPoller(self, None, lambda _: None, polling_method)
