"""Stream Session Logs"""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from datetime import datetime
from typing import Any

import httpx

from plato.chronos.errors import raise_for_status


def _build_request_args(
    public_id: str,
    limit: int | None = 2000,
    cursor: str | None = None,
    search: str | None = None,
    errors_only: bool | None = False,
    atif_only: bool | None = False,
    checkpoint_only: bool | None = False,
    plato_type: str | None = None,
    include_debug: bool | None = False,
    include_ancestors: bool | None = True,
    max_spans: int | None = None,
    name: list[str] | None = None,
    kind: list[str] | None = None,
    status: str | None = None,
    started_after: datetime | None = None,
    started_before: datetime | None = None,
    attr: list[str] | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/sessions/{public_id}/logs-stream"

    params: dict[str, Any] = {}
    if limit is not None:
        params["limit"] = limit
    if cursor is not None:
        params["cursor"] = cursor
    if search is not None:
        params["search"] = search
    if errors_only is not None:
        params["errors_only"] = errors_only
    if atif_only is not None:
        params["atif_only"] = atif_only
    if checkpoint_only is not None:
        params["checkpoint_only"] = checkpoint_only
    if plato_type is not None:
        params["plato_type"] = plato_type
    if include_debug is not None:
        params["include_debug"] = include_debug
    if include_ancestors is not None:
        params["include_ancestors"] = include_ancestors
    if max_spans is not None:
        params["max_spans"] = max_spans
    if name is not None:
        params["name"] = name
    if kind is not None:
        params["kind"] = kind
    if status is not None:
        params["status"] = status
    if started_after is not None:
        params["started_after"] = started_after
    if started_before is not None:
        params["started_before"] = started_before
    if attr is not None:
        params["attr"] = attr

    headers: dict[str, str] = {}
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "GET",
        "url": url,
        "params": params,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    public_id: str,
    limit: int | None = 2000,
    cursor: str | None = None,
    search: str | None = None,
    errors_only: bool | None = False,
    atif_only: bool | None = False,
    checkpoint_only: bool | None = False,
    plato_type: str | None = None,
    include_debug: bool | None = False,
    include_ancestors: bool | None = True,
    max_spans: int | None = None,
    name: list[str] | None = None,
    kind: list[str] | None = None,
    status: str | None = None,
    started_after: datetime | None = None,
    started_before: datetime | None = None,
    attr: list[str] | None = None,
    x_api_key: str | None = None,
) -> None:
    """Stream logs/events for a session as NDJSON chunks.

    ``limit`` is the page size the server loads per round-trip and is clamped
    to ``LOGS_STREAM_PAGE_LIMIT``; the stream runs to ``complete``, so a
    larger request only changes chunking, not the span set delivered.

    Filters (``name``, ``kind``, ``status``, ``started_after``/``started_before``,
    ``attr`` and the boolean ones) are applied in ClickHouse, so a client
    pulling a slice of a 200k-span session only receives that slice.
    ``max_spans`` ends the stream early: its ``complete`` event carries
    ``has_more=true`` and the cursor to pass back for the next slice."""

    request_args = _build_request_args(
        public_id=public_id,
        limit=limit,
        cursor=cursor,
        search=search,
        errors_only=errors_only,
        atif_only=atif_only,
        checkpoint_only=checkpoint_only,
        plato_type=plato_type,
        include_debug=include_debug,
        include_ancestors=include_ancestors,
        max_spans=max_spans,
        name=name,
        kind=kind,
        status=status,
        started_after=started_after,
        started_before=started_before,
        attr=attr,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return None


async def asyncio(
    client: httpx.AsyncClient,
    public_id: str,
    limit: int | None = 2000,
    cursor: str | None = None,
    search: str | None = None,
    errors_only: bool | None = False,
    atif_only: bool | None = False,
    checkpoint_only: bool | None = False,
    plato_type: str | None = None,
    include_debug: bool | None = False,
    include_ancestors: bool | None = True,
    max_spans: int | None = None,
    name: list[str] | None = None,
    kind: list[str] | None = None,
    status: str | None = None,
    started_after: datetime | None = None,
    started_before: datetime | None = None,
    attr: list[str] | None = None,
    x_api_key: str | None = None,
) -> None:
    """Stream logs/events for a session as NDJSON chunks.

    ``limit`` is the page size the server loads per round-trip and is clamped
    to ``LOGS_STREAM_PAGE_LIMIT``; the stream runs to ``complete``, so a
    larger request only changes chunking, not the span set delivered.

    Filters (``name``, ``kind``, ``status``, ``started_after``/``started_before``,
    ``attr`` and the boolean ones) are applied in ClickHouse, so a client
    pulling a slice of a 200k-span session only receives that slice.
    ``max_spans`` ends the stream early: its ``complete`` event carries
    ``has_more=true`` and the cursor to pass back for the next slice."""

    request_args = _build_request_args(
        public_id=public_id,
        limit=limit,
        cursor=cursor,
        search=search,
        errors_only=errors_only,
        atif_only=atif_only,
        checkpoint_only=checkpoint_only,
        plato_type=plato_type,
        include_debug=include_debug,
        include_ancestors=include_ancestors,
        max_spans=max_spans,
        name=name,
        kind=kind,
        status=status,
        started_after=started_after,
        started_before=started_before,
        attr=attr,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return None


def sync_stream(
    client: httpx.Client,
    public_id: str,
    limit: int | None = 2000,
    cursor: str | None = None,
    search: str | None = None,
    errors_only: bool | None = False,
    atif_only: bool | None = False,
    checkpoint_only: bool | None = False,
    plato_type: str | None = None,
    include_debug: bool | None = False,
    include_ancestors: bool | None = True,
    max_spans: int | None = None,
    name: list[str] | None = None,
    kind: list[str] | None = None,
    status: str | None = None,
    started_after: datetime | None = None,
    started_before: datetime | None = None,
    attr: list[str] | None = None,
    x_api_key: str | None = None,
) -> Iterator[dict[str, Any]]:
    """Stream Session Logs (streaming)"""
    import json

    request_args = _build_request_args(
        public_id=public_id,
        limit=limit,
        cursor=cursor,
        search=search,
        errors_only=errors_only,
        atif_only=atif_only,
        checkpoint_only=checkpoint_only,
        plato_type=plato_type,
        include_debug=include_debug,
        include_ancestors=include_ancestors,
        max_spans=max_spans,
        name=name,
        kind=kind,
        status=status,
        started_after=started_after,
        started_before=started_before,
        attr=attr,
        x_api_key=x_api_key,
    )

    with client.stream(**request_args) as response:
        raise_for_status(response)
        for line in response.iter_lines():
            if line.strip():
                yield json.loads(line)


async def asyncio_stream(
    client: httpx.AsyncClient,
    public_id: str,
    limit: int | None = 2000,
    cursor: str | None = None,
    search: str | None = None,
    errors_only: bool | None = False,
    atif_only: bool | None = False,
    checkpoint_only: bool | None = False,
    plato_type: str | None = None,
    include_debug: bool | None = False,
    include_ancestors: bool | None = True,
    max_spans: int | None = None,
    name: list[str] | None = None,
    kind: list[str] | None = None,
    status: str | None = None,
    started_after: datetime | None = None,
    started_before: datetime | None = None,
    attr: list[str] | None = None,
    x_api_key: str | None = None,
) -> AsyncIterator[dict[str, Any]]:
    """Stream Session Logs (streaming)"""
    import json

    request_args = _build_request_args(
        public_id=public_id,
        limit=limit,
        cursor=cursor,
        search=search,
        errors_only=errors_only,
        atif_only=atif_only,
        checkpoint_only=checkpoint_only,
        plato_type=plato_type,
        include_debug=include_debug,
        include_ancestors=include_ancestors,
        max_spans=max_spans,
        name=name,
        kind=kind,
        status=status,
        started_after=started_after,
        started_before=started_before,
        attr=attr,
        x_api_key=x_api_key,
    )

    async with client.stream(**request_args) as response:
        raise_for_status(response)
        async for line in response.aiter_lines():
            if line.strip():
                yield json.loads(line)
