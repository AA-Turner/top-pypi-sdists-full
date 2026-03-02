"""Archive Work Order Item"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import WorkOrderItemResponse


def _build_request_args(
    item_public_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/work-orders/items/{item_public_id}/archive"

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "POST",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    item_public_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> WorkOrderItemResponse:
    """Archive a work order item and all its testcase statuses.

    For each testcase that would become orphaned (no other active statuses
    and not in Plato General), creates a copy in Plato General.

    Users can only archive items belonging to their organization's work orders.
    Admins can archive any item."""

    request_args = _build_request_args(
        item_public_id=item_public_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return WorkOrderItemResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    item_public_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> WorkOrderItemResponse:
    """Archive a work order item and all its testcase statuses.

    For each testcase that would become orphaned (no other active statuses
    and not in Plato General), creates a copy in Plato General.

    Users can only archive items belonging to their organization's work orders.
    Admins can archive any item."""

    request_args = _build_request_args(
        item_public_id=item_public_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return WorkOrderItemResponse.model_validate(response.json())
