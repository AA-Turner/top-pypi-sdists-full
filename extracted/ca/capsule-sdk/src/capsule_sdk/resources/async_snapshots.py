from __future__ import annotations

from typing import TypeAlias

from capsule_sdk._http_async import AsyncHttpClient
from capsule_sdk.models.snapshot import Snapshot, SnapshotListResponse

_SnapshotList: TypeAlias = list[Snapshot]


class AsyncSnapshots:
    """Snapshot listing."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list(self) -> _SnapshotList:
        data = await self._http.get("/api/v1/snapshots")
        return SnapshotListResponse.model_validate(data).snapshots
