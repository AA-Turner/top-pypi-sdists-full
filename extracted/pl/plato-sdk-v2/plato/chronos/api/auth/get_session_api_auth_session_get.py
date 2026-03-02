"""Get Session"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import AuthSessionResponse


def _build_request_args() -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/auth/session"

    return {
        "method": "GET",
        "url": url,
    }


def sync(
    client: httpx.Client,
) -> AuthSessionResponse:
    """Get the current session from cookie."""

    request_args = _build_request_args()

    response = client.request(**request_args)
    raise_for_status(response)
    return AuthSessionResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
) -> AuthSessionResponse:
    """Get the current session from cookie."""

    request_args = _build_request_args()

    response = await client.request(**request_args)
    raise_for_status(response)
    return AuthSessionResponse.model_validate(response.json())
