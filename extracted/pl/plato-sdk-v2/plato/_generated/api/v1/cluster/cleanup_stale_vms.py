"""Cleanup Stale Vms"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import CleanupStaleVMsRequest, CleanupStaleVMsResponse


def _build_request_args(
    body: CleanupStaleVMsRequest,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v1/cluster/cleanup/stale-vms"

    return {
        "method": "POST",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
    }


def sync(
    client: httpx.Client,
    body: CleanupStaleVMsRequest,
) -> CleanupStaleVMsResponse:
    """Clean up stale VMs that haven't sent heartbeats recently.

    Requires internal service authentication.

    A VM is considered stale if its selected heartbeat is older than
    the specified threshold (default: 10 minutes), excluding
    WAITING_FOR_START_REQUEST prewarmed VMs.

    This endpoint will:
    1. Scan all VM records in Redis
    2. Identify VMs with stale heartbeats
    3. Send forced shutdown requests to each stale VM
    4. Delete the VM records from Redis

    Args:
        cleanup_request: Cleanup parameters (threshold)

    Returns:
        CleanupStaleVMsResponse with cleanup results"""

    request_args = _build_request_args(
        body=body,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return CleanupStaleVMsResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    body: CleanupStaleVMsRequest,
) -> CleanupStaleVMsResponse:
    """Clean up stale VMs that haven't sent heartbeats recently.

    Requires internal service authentication.

    A VM is considered stale if its selected heartbeat is older than
    the specified threshold (default: 10 minutes), excluding
    WAITING_FOR_START_REQUEST prewarmed VMs.

    This endpoint will:
    1. Scan all VM records in Redis
    2. Identify VMs with stale heartbeats
    3. Send forced shutdown requests to each stale VM
    4. Delete the VM records from Redis

    Args:
        cleanup_request: Cleanup parameters (threshold)

    Returns:
        CleanupStaleVMsResponse with cleanup results"""

    request_args = _build_request_args(
        body=body,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return CleanupStaleVMsResponse.model_validate(response.json())
