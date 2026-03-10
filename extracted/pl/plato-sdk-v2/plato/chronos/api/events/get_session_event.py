"""Get Event"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import OTelSpan


def _build_request_args(
    span_id: str,
    session_public_id: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/events/{span_id}"

    params: dict[str, Any] = {}
    if session_public_id is not None:
        params["session_public_id"] = session_public_id

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
    span_id: str,
    session_public_id: str | None = None,
    x_api_key: str | None = None,
) -> OTelSpan:
    """Get a span by ID.

    Optionally pass session_public_id to narrow the search and verify org access.
    Uses ClickHouse when available, falls back to scanning Postgres batches."""

    request_args = _build_request_args(
        span_id=span_id,
        session_public_id=session_public_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return OTelSpan.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    span_id: str,
    session_public_id: str | None = None,
    x_api_key: str | None = None,
) -> OTelSpan:
    """Get a span by ID.

    Optionally pass session_public_id to narrow the search and verify org access.
    Uses ClickHouse when available, falls back to scanning Postgres batches."""

    request_args = _build_request_args(
        span_id=span_id,
        session_public_id=session_public_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return OTelSpan.model_validate(response.json())
