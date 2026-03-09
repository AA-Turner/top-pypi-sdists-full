"""Get Downstream Sessions"""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import DownstreamSessionsResponse


def _build_request_args(
    ref_public_id: str,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/workspace-repos/refs/{ref_public_id}/downstream"

    headers: dict[str, str] = {}
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "GET",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    ref_public_id: str,
    x_api_key: str | None = None,
) -> DownstreamSessionsResponse:
    """Find all sessions that consumed (forked/resumed from) a given workspace ref."""

    request_args = _build_request_args(
        ref_public_id=ref_public_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return DownstreamSessionsResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    ref_public_id: str,
    x_api_key: str | None = None,
) -> DownstreamSessionsResponse:
    """Find all sessions that consumed (forked/resumed from) a given workspace ref."""

    request_args = _build_request_args(
        ref_public_id=ref_public_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return DownstreamSessionsResponse.model_validate(response.json())


def sync_stream(
    client: httpx.Client,
    ref_public_id: str,
    x_api_key: str | None = None,
) -> Iterator[dict[str, Any]]:
    """Get Downstream Sessions (streaming)"""
    import json

    request_args = _build_request_args(
        ref_public_id=ref_public_id,
        x_api_key=x_api_key,
    )

    with client.stream(**request_args) as response:
        raise_for_status(response)
        for line in response.iter_lines():
            if line.strip():
                yield json.loads(line)


async def asyncio_stream(
    client: httpx.AsyncClient,
    ref_public_id: str,
    x_api_key: str | None = None,
) -> AsyncIterator[dict[str, Any]]:
    """Get Downstream Sessions (streaming)"""
    import json

    request_args = _build_request_args(
        ref_public_id=ref_public_id,
        x_api_key=x_api_key,
    )

    async with client.stream(**request_args) as response:
        raise_for_status(response)
        async for line in response.aiter_lines():
            if line.strip():
                yield json.loads(line)
