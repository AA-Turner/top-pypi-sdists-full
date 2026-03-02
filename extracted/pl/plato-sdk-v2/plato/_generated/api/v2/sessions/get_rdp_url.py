"""Get Rdp Url"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import RdpUrlResponse


def _build_request_args(
    session_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/sessions/{session_id}/rdp_url"

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
) -> RdpUrlResponse:
    """Get RDP viewer URLs for all jobs in a session.

    Returns browser-accessible URLs to the Guacamole-based RDP viewer for Windows VMs.
    The URLs include a trailing slash which is required for proper routing.

    Args:
        session_id: The session ID.

    Returns:
        RdpUrlResponse with RDP URL for each job."""

    request_args = _build_request_args(
        session_id=session_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return RdpUrlResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> RdpUrlResponse:
    """Get RDP viewer URLs for all jobs in a session.

    Returns browser-accessible URLs to the Guacamole-based RDP viewer for Windows VMs.
    The URLs include a trailing slash which is required for proper routing.

    Args:
        session_id: The session ID.

    Returns:
        RdpUrlResponse with RDP URL for each job."""

    request_args = _build_request_args(
        session_id=session_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return RdpUrlResponse.model_validate(response.json())
