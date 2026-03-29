"""Stream Session Logs"""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
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
    x_api_key: str | None = None,
) -> None:
    """Stream logs/events for a session as NDJSON chunks.

    Audit events are not included in the stream. Use the per-span
    ``/{public_id}/spans/{span_id}/audit-events`` endpoint to load
    them lazily."""

    request_args = _build_request_args(
        public_id=public_id,
        limit=limit,
        cursor=cursor,
        search=search,
        errors_only=errors_only,
        atif_only=atif_only,
        checkpoint_only=checkpoint_only,
        plato_type=plato_type,
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
    x_api_key: str | None = None,
) -> None:
    """Stream logs/events for a session as NDJSON chunks.

    Audit events are not included in the stream. Use the per-span
    ``/{public_id}/spans/{span_id}/audit-events`` endpoint to load
    them lazily."""

    request_args = _build_request_args(
        public_id=public_id,
        limit=limit,
        cursor=cursor,
        search=search,
        errors_only=errors_only,
        atif_only=atif_only,
        checkpoint_only=checkpoint_only,
        plato_type=plato_type,
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
        x_api_key=x_api_key,
    )

    async with client.stream(**request_args) as response:
        raise_for_status(response)
        async for line in response.aiter_lines():
            if line.strip():
                yield json.loads(line)
