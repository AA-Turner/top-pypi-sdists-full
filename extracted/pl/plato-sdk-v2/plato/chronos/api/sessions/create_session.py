"""Create Session"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import CreateSessionRequest, CreateSessionResponse


def _build_request_args(
    body: CreateSessionRequest,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/sessions"

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
    body: CreateSessionRequest,
    x_api_key: str | None = None,
) -> CreateSessionResponse:
    """Create a new session for dev/testing.

    This creates a chronos session record that can receive OTel traces.
    Used by plato-world-runner dev mode to get a real session in chronos."""

    request_args = _build_request_args(
        body=body,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return CreateSessionResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    body: CreateSessionRequest,
    x_api_key: str | None = None,
) -> CreateSessionResponse:
    """Create a new session for dev/testing.

    This creates a chronos session record that can receive OTel traces.
    Used by plato-world-runner dev mode to get a real session in chronos."""

    request_args = _build_request_args(
        body=body,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return CreateSessionResponse.model_validate(response.json())
