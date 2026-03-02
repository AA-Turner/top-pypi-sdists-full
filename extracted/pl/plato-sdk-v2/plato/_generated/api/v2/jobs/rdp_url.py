"""Rdp Url"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import RdpUrlResult


def _build_request_args(
    job_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/jobs/{job_id}/rdp_url"

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
    job_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> RdpUrlResult:
    """Get RDP viewer URL for browser-based remote desktop access.

    Returns URL to the Guacamole-based RDP viewer for Windows VMs.
    The URL includes a trailing slash which is required for proper routing.

    Args:
        job_id: The job public ID.

    Returns:
        RdpUrlResult with RDP viewer URL.

    Raises:
        404: If job not found."""

    request_args = _build_request_args(
        job_id=job_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return RdpUrlResult.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    job_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> RdpUrlResult:
    """Get RDP viewer URL for browser-based remote desktop access.

    Returns URL to the Guacamole-based RDP viewer for Windows VMs.
    The URL includes a trailing slash which is required for proper routing.

    Args:
        job_id: The job public ID.

    Returns:
        RdpUrlResult with RDP viewer URL.

    Raises:
        404: If job not found."""

    request_args = _build_request_args(
        job_id=job_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return RdpUrlResult.model_validate(response.json())
