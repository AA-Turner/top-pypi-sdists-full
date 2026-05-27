"""Pause"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import ReleaseResponse


def _build_request_args(
    public_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/releases/{public_id}/pause"

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
    public_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ReleaseResponse:
    """Pause an in-progress deployment. In-flight items finish; no new items start.
    Resume by calling deploy again (already-deployed items are skipped by destinations).
    Admin only."""

    request_args = _build_request_args(
        public_id=public_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ReleaseResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    public_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ReleaseResponse:
    """Pause an in-progress deployment. In-flight items finish; no new items start.
    Resume by calling deploy again (already-deployed items are skipped by destinations).
    Admin only."""

    request_args = _build_request_args(
        public_id=public_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ReleaseResponse.model_validate(response.json())
