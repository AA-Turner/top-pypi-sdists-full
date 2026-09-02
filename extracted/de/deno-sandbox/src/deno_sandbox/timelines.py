from __future__ import annotations

from typing import Any, TypedDict
from typing_extensions import Optional


from .bridge import AsyncBridge
from .console import (
    AsyncConsoleClient,
    AsyncPaginatedList,
    PaginatedList,
)


class TimelineApp(TypedDict):
    id: str
    """The unique identifier for the app."""

    slug: str
    """The human readable identifier for the app."""


class TimelineContext(TypedDict):
    slug: str


class Domain(TypedDict):
    domain: str
    """The domain name."""


class Timeline(TypedDict):
    slug: str
    """The unique identifier for the timeline."""

    partition: dict[str, str]
    """The partition of the timeline."""

    app: TimelineApp
    context: TimelineContext
    """The context of the timeline."""

    domains: list[Domain]
    """The domains associated with the timeline."""


class AsyncTimelines:
    def __init__(self, client: AsyncConsoleClient):
        self._client = client

    async def list(
        self,
        app: str,
        *,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> AsyncPaginatedList[Timeline]:
        """List timelines for a specific app.

        Args:
            app: The app ID or slug.
            cursor: The cursor for pagination.
            limit: Limit the number of items to return.
        """
        options: dict[str, Any] = {}
        if cursor is not None:
            options["cursor"] = cursor
        if limit is not None:
            options["limit"] = limit
        return await self._client.get_paginated(
            f"/api/v2/apps/{app}/timelines",
            cursor=None,
            params=options if options else None,
        )


class Timelines:
    def __init__(self, client: AsyncConsoleClient, bridge: AsyncBridge):
        self._client = client
        self._bridge = bridge
        self._async = AsyncTimelines(client)

    def list(
        self,
        app: str,
        *,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> PaginatedList[Timeline]:
        """List timelines for a specific app.

        Args:
            app: The app ID or slug.
            cursor: The cursor for pagination.
            limit: Limit the number of items to return.
        """
        paginated = self._bridge.run(self._async.list(app, cursor=cursor, limit=limit))
        return PaginatedList(self._bridge, paginated)
