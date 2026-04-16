"""Authz Check"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import AuthzCheckResponse


def _build_request_args(
    role: str,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/auth/authz/check"

    params: dict[str, Any] = {}
    if role is not None:
        params["role"] = role

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
    role: str,
    x_api_key: str | None = None,
) -> AuthzCheckResponse:
    """Proxy an authz check to Plato using the current principal's SSO auth.

    Checks whether the current principal has the given role on their org."""

    request_args = _build_request_args(
        role=role,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return AuthzCheckResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    role: str,
    x_api_key: str | None = None,
) -> AuthzCheckResponse:
    """Proxy an authz check to Plato using the current principal's SSO auth.

    Checks whether the current principal has the given role on their org."""

    request_args = _build_request_args(
        role=role,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return AuthzCheckResponse.model_validate(response.json())
