"""Get Vm Detail"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import VMStatus


def _build_request_args(
    worker_id: str,
    vm_id: int,
    stale_threshold_seconds: int | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/queue/vm/{worker_id}/{vm_id}"

    params: dict[str, Any] = {}
    if stale_threshold_seconds is not None:
        params["stale_threshold_seconds"] = stale_threshold_seconds

    return {
        "method": "GET",
        "url": url,
        "params": params,
    }


def sync(
    client: httpx.Client,
    worker_id: str,
    vm_id: int,
    stale_threshold_seconds: int | None = None,
) -> VMStatus:
    """Get detailed status for a specific VM.

    Args:
        worker_id: Worker ID
        vm_id: VM ID
        stale_threshold_seconds: Threshold for considering a heartbeat stale (defaults to worker_heartbeat_timeout from settings)

    Returns:
        Detailed VM status"""

    request_args = _build_request_args(
        worker_id=worker_id,
        vm_id=vm_id,
        stale_threshold_seconds=stale_threshold_seconds,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return VMStatus.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    worker_id: str,
    vm_id: int,
    stale_threshold_seconds: int | None = None,
) -> VMStatus:
    """Get detailed status for a specific VM.

    Args:
        worker_id: Worker ID
        vm_id: VM ID
        stale_threshold_seconds: Threshold for considering a heartbeat stale (defaults to worker_heartbeat_timeout from settings)

    Returns:
        Detailed VM status"""

    request_args = _build_request_args(
        worker_id=worker_id,
        vm_id=vm_id,
        stale_threshold_seconds=stale_threshold_seconds,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return VMStatus.model_validate(response.json())
