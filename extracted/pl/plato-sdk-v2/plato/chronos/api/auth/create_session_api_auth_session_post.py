"""Create Session"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import AuthSessionResponse, SSOLoginRequest


def _build_request_args(
    body: SSOLoginRequest,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/auth/session"

    return {
        "method": "POST",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
    }


def sync(
    client: httpx.Client,
    body: SSOLoginRequest,
) -> AuthSessionResponse:
    """Exchange an SSO JWT for an HTTP-only session cookie."""

    request_args = _build_request_args(
        body=body,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return AuthSessionResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    body: SSOLoginRequest,
) -> AuthSessionResponse:
    """Exchange an SSO JWT for an HTTP-only session cookie."""

    request_args = _build_request_args(
        body=body,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return AuthSessionResponse.model_validate(response.json())
