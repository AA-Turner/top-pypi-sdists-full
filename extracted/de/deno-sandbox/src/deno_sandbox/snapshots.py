from __future__ import annotations

from typing import Any, TypedDict, cast
from typing_extensions import Optional

from .bridge import AsyncBridge
from .console import (
    AsyncConsoleClient,
    AsyncPaginatedList,
    PaginatedList,
)

from .utils import convert_to_snake_case


class BaseSnapshot(TypedDict):
    id: str
    """The unique identifier for the snapshot."""

    slug: str
    """Human readable identifier for the snapshot."""


class Snapshot(TypedDict):
    id: str
    """The unique identifier for the snapshot."""

    slug: str
    """The human readable identifier for the snapshot."""

    region: str
    """The region the snapshot is located in."""

    allocated_size: int
    """
  The number of bytes currently allocated specifically for the snapshot.

  Snapshots created from other snapshots only store data that is different
  from their base snapshot, so this size may be smaller than the actual size
  of the file system on the snapshot.
  This is not the total size of the snapshot.
  """

    flattened_size: int
    """
  The total size of the file system on the snapshot, in bytes. This is the size the snapshot would take up if it were fully "flattened" (i.e., if all data from any snapshots it was created from were fully stored in this snapshot).

  Snapshots created from other snapshots only store data that is different from their base snapshot, so this size may be larger than the amount of data actually allocated for the snapshot.
  """

    is_bootable: bool
    """Whether the snapshot is bootable."""

    base_snapshot: BaseSnapshot
    """The snapshot the volume was created from."""


class AsyncSnapshots:
    def __init__(self, client: AsyncConsoleClient):
        self._client = client

    async def get(self, id_or_slug: str) -> Snapshot | None:
        """Get a snapshot by ID or slug."""
        result = await self._client.get_or_none(f"/api/v2/snapshots/{id_or_slug}")
        if result is None:
            return None
        raw_result = convert_to_snake_case(result)
        return cast(Snapshot, raw_result)

    async def list(
        self,
        *,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        search: Optional[str] = None,
    ) -> AsyncPaginatedList[Snapshot]:
        """List snapshots.

        Args:
            cursor: The cursor for pagination.
            limit: Limit the number of snapshots to return.
            search: The search query to filter snapshots by.
        """
        options: dict[str, Any] = {}
        if cursor is not None:
            options["cursor"] = cursor
        if limit is not None:
            options["limit"] = limit
        if search is not None:
            options["search"] = search
        return await self._client.get_paginated(
            "/api/v2/snapshots", cursor=None, params=options if options else None
        )

    async def delete(self, id_or_slug: str) -> None:
        """Delete snapshot by ID or slug."""
        await self._client.delete(f"/api/v2/snapshots/{id_or_slug}")


class Snapshots:
    def __init__(self, client: AsyncConsoleClient, bridge: AsyncBridge):
        self._client = client
        self._bridge = bridge
        self._async = AsyncSnapshots(client)

    def get(self, id_or_slug: str) -> Snapshot | None:
        """Get a snapshot by ID or slug."""
        return self._bridge.run(self._async.get(id_or_slug))

    def list(
        self,
        *,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        search: Optional[str] = None,
    ) -> PaginatedList[Snapshot]:
        """List snapshots.

        Args:
            cursor: The cursor for pagination.
            limit: Limit the number of snapshots to return.
            search: The search query to filter snapshots by.
        """
        paginated = self._bridge.run(
            self._async.list(cursor=cursor, limit=limit, search=search)
        )
        return PaginatedList(self._bridge, paginated)

    def delete(self, id_or_slug: str) -> None:
        """Delete snapshot by ID or slug."""
        self._bridge.run(self._async.delete(id_or_slug))
