from __future__ import annotations

from typing import TypeAlias

from capsule_sdk._http import HttpClient
from capsule_sdk.models.snapshot import Snapshot, SnapshotListResponse

_SnapshotList: TypeAlias = list[Snapshot]


class Snapshots:
    """Snapshot listing."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> _SnapshotList:
        data = self._http.get("/api/v1/snapshots")
        return SnapshotListResponse.model_validate(data).snapshots
