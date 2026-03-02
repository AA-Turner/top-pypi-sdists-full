"""Get Session Plato Config"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import PlatoConfig


def _build_request_args(
    session_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/sessions/{session_id}/plato_config"

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "GET",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    session_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, PlatoConfig | None]:
    """Get parsed plato-config for all jobs in a session.

    Returns the plato_config YAML content parsed into typed PlatoConfig objects
    with discriminated union types for services and listeners.

    Args:
        session_id: The session ID.

    Returns:
        Dict mapping job_id to PlatoConfig (or None on error).

    Raises:
        404: If session not found."""

    request_args = _build_request_args(
        session_id=session_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    session_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, PlatoConfig | None]:
    """Get parsed plato-config for all jobs in a session.

    Returns the plato_config YAML content parsed into typed PlatoConfig objects
    with discriminated union types for services and listeners.

    Args:
        session_id: The session ID.

    Returns:
        Dict mapping job_id to PlatoConfig (or None on error).

    Raises:
        404: If session not found."""

    request_args = _build_request_args(
        session_id=session_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
