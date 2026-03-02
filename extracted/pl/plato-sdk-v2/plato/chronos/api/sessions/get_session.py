"""Get Session"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import SessionResponse


def _build_request_args(
    public_id: str,
    reveal_secrets: bool | None = False,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/sessions/{public_id}"

    params: dict[str, Any] = {}
    if reveal_secrets is not None:
        params["reveal_secrets"] = reveal_secrets

    headers: dict[str, str] = {}
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "GET",
        "url": url,
        "params": params,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    public_id: str,
    reveal_secrets: bool | None = False,
    x_api_key: str | None = None,
) -> SessionResponse:
    """Get a session by public ID.

    Args:
        public_id: Session public ID
        reveal_secrets: If true, decrypt and return actual secret values"""

    request_args = _build_request_args(
        public_id=public_id,
        reveal_secrets=reveal_secrets,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return SessionResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    public_id: str,
    reveal_secrets: bool | None = False,
    x_api_key: str | None = None,
) -> SessionResponse:
    """Get a session by public ID.

    Args:
        public_id: Session public ID
        reveal_secrets: If true, decrypt and return actual secret values"""

    request_args = _build_request_args(
        public_id=public_id,
        reveal_secrets=reveal_secrets,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return SessionResponse.model_validate(response.json())
