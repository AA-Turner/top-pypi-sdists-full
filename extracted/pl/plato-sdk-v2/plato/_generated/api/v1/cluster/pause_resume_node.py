"""Pause Resume Node"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import DispatcherPauseResponse, NodePauseRequest


def _build_request_args(
    body: NodePauseRequest,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v1/cluster/nodes/pause"

    return {
        "method": "POST",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
    }


def sync(
    client: httpx.Client,
    body: NodePauseRequest,
) -> DispatcherPauseResponse:
    """Pause or resume demand processing on every dispatcher for one instance."""

    request_args = _build_request_args(
        body=body,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return DispatcherPauseResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    body: NodePauseRequest,
) -> DispatcherPauseResponse:
    """Pause or resume demand processing on every dispatcher for one instance."""

    request_args = _build_request_args(
        body=body,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return DispatcherPauseResponse.model_validate(response.json())
