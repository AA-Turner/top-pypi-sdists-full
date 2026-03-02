"""Get Dispatchers"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import DispatchersResponse


def _build_request_args() -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v1/cluster/dispatchers"

    return {
        "method": "GET",
        "url": url,
    }


def sync(
    client: httpx.Client,
) -> DispatchersResponse:
    """Get all Firecracker dispatchers with their status and VM counts.

    Returns:
        DispatchersResponse with all dispatcher information"""

    request_args = _build_request_args()

    response = client.request(**request_args)
    raise_for_status(response)
    return DispatchersResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
) -> DispatchersResponse:
    """Get all Firecracker dispatchers with their status and VM counts.

    Returns:
        DispatchersResponse with all dispatcher information"""

    request_args = _build_request_args()

    response = await client.request(**request_args)
    raise_for_status(response)
    return DispatchersResponse.model_validate(response.json())
