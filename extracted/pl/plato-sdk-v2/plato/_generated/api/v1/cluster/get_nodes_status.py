"""Get Nodes Status"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import NodeStatusResponse


def _build_request_args() -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v1/cluster/nodes/status"

    return {
        "method": "GET",
        "url": url,
    }


def sync(
    client: httpx.Client,
) -> NodeStatusResponse:
    """Get node/VM status across all Firecracker worker instances.

    Returns detailed information about:
    - Total instances with VMs
    - Total active VMs across all instances
    - Total capacity across all instances
    - Per-instance VM counts by state

    Returns:
        NodeStatusResponse with comprehensive node/VM status"""

    request_args = _build_request_args()

    response = client.request(**request_args)
    raise_for_status(response)
    return NodeStatusResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
) -> NodeStatusResponse:
    """Get node/VM status across all Firecracker worker instances.

    Returns detailed information about:
    - Total instances with VMs
    - Total active VMs across all instances
    - Total capacity across all instances
    - Per-instance VM counts by state

    Returns:
        NodeStatusResponse with comprehensive node/VM status"""

    request_args = _build_request_args()

    response = await client.request(**request_args)
    raise_for_status(response)
    return NodeStatusResponse.model_validate(response.json())
