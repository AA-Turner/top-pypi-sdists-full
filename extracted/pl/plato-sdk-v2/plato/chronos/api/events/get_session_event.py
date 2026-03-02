"""Get Event"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import OTelSpan


def _build_request_args(
    span_id: str,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/events/{span_id}"

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
    span_id: str,
    x_api_key: str | None = None,
) -> OTelSpan:
    """Get a span by ID.

    Note: This requires scanning all batches, so it's not efficient.
    Consider caching or indexing spans if this is used frequently."""

    request_args = _build_request_args(
        span_id=span_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return OTelSpan.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    span_id: str,
    x_api_key: str | None = None,
) -> OTelSpan:
    """Get a span by ID.

    Note: This requires scanning all batches, so it's not efficient.
    Consider caching or indexing spans if this is used frequently."""

    request_args = _build_request_args(
        span_id=span_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return OTelSpan.model_validate(response.json())
