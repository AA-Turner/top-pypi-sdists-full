"""Delete Session"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status


def _build_request_args() -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/auth/session"

    return {
        "method": "DELETE",
        "url": url,
    }


def sync(
    client: httpx.Client,
) -> dict[str, Any]:
    """Clear the session cookie (logout)."""

    request_args = _build_request_args()

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
) -> dict[str, Any]:
    """Clear the session cookie (logout)."""

    request_args = _build_request_args()

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
