"""Update Review Node"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import NodeTreeOutput, UpdateNodeRequest


def _build_request_args(
    review_public_id: str,
    node_id: str,
    body: UpdateNodeRequest,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/reviews/{review_public_id}/nodes/{node_id}"

    headers: dict[str, str] = {}
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "PATCH",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    review_public_id: str,
    node_id: str,
    body: UpdateNodeRequest,
    x_api_key: str | None = None,
) -> NodeTreeOutput:
    """Update runtime values on a node tree node."""

    request_args = _build_request_args(
        review_public_id=review_public_id,
        node_id=node_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return NodeTreeOutput.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    review_public_id: str,
    node_id: str,
    body: UpdateNodeRequest,
    x_api_key: str | None = None,
) -> NodeTreeOutput:
    """Update runtime values on a node tree node."""

    request_args = _build_request_args(
        review_public_id=review_public_id,
        node_id=node_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return NodeTreeOutput.model_validate(response.json())
