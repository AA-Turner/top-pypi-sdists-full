"""Get Snapshots Status"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import SnapshotStatusResponse


def _build_request_args() -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v1/cluster/snapshots/status"

    return {
        "method": "GET",
        "url": url,
    }


def sync(
    client: httpx.Client,
) -> SnapshotStatusResponse:
    """Get snapshot status across all Firecracker worker instances.

    Returns detailed information about:
    - Total instances with snapshots
    - Total snapshots across all instances
    - Breakdown by status (available, downloading, failed, not_downloaded)
    - Per-instance snapshot details

    Returns:
        SnapshotStatusResponse with comprehensive snapshot status"""

    request_args = _build_request_args()

    response = client.request(**request_args)
    raise_for_status(response)
    return SnapshotStatusResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
) -> SnapshotStatusResponse:
    """Get snapshot status across all Firecracker worker instances.

    Returns detailed information about:
    - Total instances with snapshots
    - Total snapshots across all instances
    - Breakdown by status (available, downloading, failed, not_downloaded)
    - Per-instance snapshot details

    Returns:
        SnapshotStatusResponse with comprehensive snapshot status"""

    request_args = _build_request_args()

    response = await client.request(**request_args)
    raise_for_status(response)
    return SnapshotStatusResponse.model_validate(response.json())
