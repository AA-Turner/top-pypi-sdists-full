"""Connect Routing Info"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import ConnectRoutingInfoResult


def _build_request_args(
    job_id: str,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/jobs/{job_id}/connect_routing_info"

    return {
        "method": "GET",
        "url": url,
    }


def sync(
    client: httpx.Client,
    job_id: str,
) -> ConnectRoutingInfoResult:
    """Get routing information for connect subdomain routing.

    Used by the nginx Lua script to route requests from {job_id}.connect.plato.so
    directly to the VM. Tries job_id as direct job lookup first, then as job group.

    No auth required - internal endpoint called by nginx only.

    Args:
        job_id: The job public ID or job group ID.

    Returns:
        ConnectRoutingInfoResult with routing info."""

    request_args = _build_request_args(
        job_id=job_id,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ConnectRoutingInfoResult.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    job_id: str,
) -> ConnectRoutingInfoResult:
    """Get routing information for connect subdomain routing.

    Used by the nginx Lua script to route requests from {job_id}.connect.plato.so
    directly to the VM. Tries job_id as direct job lookup first, then as job group.

    No auth required - internal endpoint called by nginx only.

    Args:
        job_id: The job public ID or job group ID.

    Returns:
        ConnectRoutingInfoResult with routing info."""

    request_args = _build_request_args(
        job_id=job_id,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ConnectRoutingInfoResult.model_validate(response.json())
