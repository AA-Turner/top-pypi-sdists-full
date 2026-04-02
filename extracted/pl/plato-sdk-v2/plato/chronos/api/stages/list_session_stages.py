"""List Session Stages"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import SessionStagesResponse


def _build_request_args(
    session_public_id: str,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/stages/{session_public_id}"

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
    session_public_id: str,
    x_api_key: str | None = None,
) -> SessionStagesResponse:
    """List all stages for a session, ordered by start time."""

    request_args = _build_request_args(
        session_public_id=session_public_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return SessionStagesResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_public_id: str,
    x_api_key: str | None = None,
) -> SessionStagesResponse:
    """List all stages for a session, ordered by start time."""

    request_args = _build_request_args(
        session_public_id=session_public_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return SessionStagesResponse.model_validate(response.json())
