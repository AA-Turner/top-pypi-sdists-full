"""Pause Resume Dispatchers"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import DispatcherPauseRequest, DispatcherPauseResponse


def _build_request_args(
    body: DispatcherPauseRequest,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v1/cluster/dispatchers/pause"

    return {
        "method": "POST",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
    }


def sync(
    client: httpx.Client,
    body: DispatcherPauseRequest,
) -> DispatcherPauseResponse:
    """Pause or resume demand processing on a specific Firecracker dispatcher.

    Requires internal service authentication.

    When paused, the dispatcher will:
    - Stop consuming new demand events (run/resume requests)
    - Continue processing worker ops events (ssh/scp/snapshot/shutdown)
    - Continue running existing VMs

    This is useful for:
    - Maintenance windows
    - Controlled draining before deployment
    - Targeting specific workers for updates

    NOTE: dispatcher_id is REQUIRED to prevent accidentally pausing all workers.

    Args:
        pause_request: Pause/resume parameters with required dispatcher_id

    Returns:
        DispatcherPauseResponse with result"""

    request_args = _build_request_args(
        body=body,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return DispatcherPauseResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    body: DispatcherPauseRequest,
) -> DispatcherPauseResponse:
    """Pause or resume demand processing on a specific Firecracker dispatcher.

    Requires internal service authentication.

    When paused, the dispatcher will:
    - Stop consuming new demand events (run/resume requests)
    - Continue processing worker ops events (ssh/scp/snapshot/shutdown)
    - Continue running existing VMs

    This is useful for:
    - Maintenance windows
    - Controlled draining before deployment
    - Targeting specific workers for updates

    NOTE: dispatcher_id is REQUIRED to prevent accidentally pausing all workers.

    Args:
        pause_request: Pause/resume parameters with required dispatcher_id

    Returns:
        DispatcherPauseResponse with result"""

    request_args = _build_request_args(
        body=body,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return DispatcherPauseResponse.model_validate(response.json())
