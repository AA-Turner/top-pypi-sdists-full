"""Get Queue Status"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import QueueStatusResponse


def _build_request_args() -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v1/queue/status"

    return {
        "method": "GET",
        "url": url,
    }


def sync(
    client: httpx.Client,
) -> QueueStatusResponse:
    """Get simplified queue status showing VMs by state, VMs by state per worker,
    total workers, and resource matcher statistics with breakdown by service/version/dataset.

    Returns:
        Simplified status with VM breakdowns and detailed matcher stats including:
        - Total pending demands and available supplies
        - Per-resource breakdown showing pending demands and available supplies for each service/version/dataset combination"""

    request_args = _build_request_args()

    response = client.request(**request_args)
    raise_for_status(response)
    return QueueStatusResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
) -> QueueStatusResponse:
    """Get simplified queue status showing VMs by state, VMs by state per worker,
    total workers, and resource matcher statistics with breakdown by service/version/dataset.

    Returns:
        Simplified status with VM breakdowns and detailed matcher stats including:
        - Total pending demands and available supplies
        - Per-resource breakdown showing pending demands and available supplies for each service/version/dataset combination"""

    request_args = _build_request_args()

    response = await client.request(**request_args)
    raise_for_status(response)
    return QueueStatusResponse.model_validate(response.json())
