"""Update Session Tags"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import SessionResponse, UpdateTagsRequest


def _build_request_args(
    public_id: str,
    body: UpdateTagsRequest,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/sessions/{public_id}/tags"

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
    public_id: str,
    body: UpdateTagsRequest,
    x_api_key: str | None = None,
) -> SessionResponse:
    """Update tags for a session."""

    request_args = _build_request_args(
        public_id=public_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return SessionResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    public_id: str,
    body: UpdateTagsRequest,
    x_api_key: str | None = None,
) -> SessionResponse:
    """Update tags for a session."""

    request_args = _build_request_args(
        public_id=public_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return SessionResponse.model_validate(response.json())
