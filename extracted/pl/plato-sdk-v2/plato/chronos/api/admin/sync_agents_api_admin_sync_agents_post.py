"""Sync Agents"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import SyncResult


def _build_request_args(
    source_url: str,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/admin/sync/agents"

    params: dict[str, Any] = {}
    if source_url is not None:
        params["source_url"] = source_url

    headers: dict[str, str] = {}
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "POST",
        "url": url,
        "params": params,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    source_url: str,
    x_api_key: str | None = None,
) -> SyncResult:
    """Sync agents from source Chronos to local database."""

    request_args = _build_request_args(
        source_url=source_url,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return SyncResult.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    source_url: str,
    x_api_key: str | None = None,
) -> SyncResult:
    """Sync agents from source Chronos to local database."""

    request_args = _build_request_args(
        source_url=source_url,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return SyncResult.model_validate(response.json())
