"""Update Starred Checkpoint"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import StarredCheckpointResponse, StarredCheckpointUpdate


def _build_request_args(
    checkpoint_id: int,
    body: StarredCheckpointUpdate,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/starred-checkpoints/{checkpoint_id}"

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
    checkpoint_id: int,
    body: StarredCheckpointUpdate,
    x_api_key: str | None = None,
) -> StarredCheckpointResponse:
    """Update a starred checkpoint's note."""

    request_args = _build_request_args(
        checkpoint_id=checkpoint_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return StarredCheckpointResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    checkpoint_id: int,
    body: StarredCheckpointUpdate,
    x_api_key: str | None = None,
) -> StarredCheckpointResponse:
    """Update a starred checkpoint's note."""

    request_args = _build_request_args(
        checkpoint_id=checkpoint_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return StarredCheckpointResponse.model_validate(response.json())
