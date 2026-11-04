"""Get Node Vms"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import NodeVMsResponse


def _build_request_args(
    instance_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/cluster/nodes/{instance_id}/vms"

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
    instance_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> NodeVMsResponse:
    """List VM records for one instance via a targeted scan.

    Unlike the dispatcher detail endpoint, this enumerates VM records directly
    (``vm:worker-{instance_id}-*:*``) so VMs whose owning dispatcher has gone
    offline or whose dispatcher record is gone entirely (orphaned) are still
    surfaced. The scan is scoped to a single instance, so it avoids a
    fleet-wide keyspace scan."""

    request_args = _build_request_args(
        instance_id=instance_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return NodeVMsResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    instance_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> NodeVMsResponse:
    """List VM records for one instance via a targeted scan.

    Unlike the dispatcher detail endpoint, this enumerates VM records directly
    (``vm:worker-{instance_id}-*:*``) so VMs whose owning dispatcher has gone
    offline or whose dispatcher record is gone entirely (orphaned) are still
    surfaced. The scan is scoped to a single instance, so it avoids a
    fleet-wide keyspace scan."""

    request_args = _build_request_args(
        instance_id=instance_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return NodeVMsResponse.model_validate(response.json())
