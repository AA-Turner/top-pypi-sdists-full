"""Complete Session"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import CompleteSessionRequest, SessionResponse


def _build_request_args(
    public_id: str,
    body: CompleteSessionRequest,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/sessions/{public_id}/complete"

    headers: dict[str, str] = {}
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "POST",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    public_id: str,
    body: CompleteSessionRequest,
    x_api_key: str | None = None,
) -> SessionResponse:
    """Mark a session as completed or failed.

    Called by the bootstrap script when the world runner finishes.
    Uses API key auth (no org check) since it's called from the VM.
    Also closes the Plato session to release VM resources."""

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
    body: CompleteSessionRequest,
    x_api_key: str | None = None,
) -> SessionResponse:
    """Mark a session as completed or failed.

    Called by the bootstrap script when the world runner finishes.
    Uses API key auth (no org check) since it's called from the VM.
    Also closes the Plato session to release VM resources."""

    request_args = _build_request_args(
        public_id=public_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return SessionResponse.model_validate(response.json())
