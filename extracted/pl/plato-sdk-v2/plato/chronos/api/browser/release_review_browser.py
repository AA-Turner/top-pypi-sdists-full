"""Release Review Browser"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status


def _build_request_args(
    anchor_session_id: str,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/browser/{anchor_session_id}"

    headers: dict[str, str] = {}
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "DELETE",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    anchor_session_id: str,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Release an Anchor Browser session."""

    request_args = _build_request_args(
        anchor_session_id=anchor_session_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    anchor_session_id: str,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Release an Anchor Browser session."""

    request_args = _build_request_args(
        anchor_session_id=anchor_session_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
