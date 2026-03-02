"""Get Connect Url"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import ConnectUrlResponse


def _build_request_args(
    session_id: str,
    port: int | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/sessions/{session_id}/connect_url"

    params: dict[str, Any] = {}
    if port is not None:
        params["port"] = port

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
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
    session_id: str,
    port: int | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ConnectUrlResponse:
    """Get connect URLs for all jobs in a session.

    Returns direct connect URLs with embedded token in format: {token}.connect.plato.so
    Requires jobs to be running with worker IP available.

    Args:
        session_id: The session ID.
        port: Port number for the URLs (default: 8080).

    Returns:
        ConnectUrlResponse with connect URL for each job."""

    request_args = _build_request_args(
        session_id=session_id,
        port=port,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ConnectUrlResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_id: str,
    port: int | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ConnectUrlResponse:
    """Get connect URLs for all jobs in a session.

    Returns direct connect URLs with embedded token in format: {token}.connect.plato.so
    Requires jobs to be running with worker IP available.

    Args:
        session_id: The session ID.
        port: Port number for the URLs (default: 8080).

    Returns:
        ConnectUrlResponse with connect URL for each job."""

    request_args = _build_request_args(
        session_id=session_id,
        port=port,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ConnectUrlResponse.model_validate(response.json())
