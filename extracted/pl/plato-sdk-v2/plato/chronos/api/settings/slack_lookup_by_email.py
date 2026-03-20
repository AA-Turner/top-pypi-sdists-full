"""Slack Lookup By Email"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import SlackLookupResponse


def _build_request_args(
    email: str,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/settings/slack/lookup"

    params: dict[str, Any] = {}
    if email is not None:
        params["email"] = email

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
    email: str,
    x_api_key: str | None = None,
) -> SlackLookupResponse:
    """Look up a Slack user ID by email address."""

    request_args = _build_request_args(
        email=email,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return SlackLookupResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    email: str,
    x_api_key: str | None = None,
) -> SlackLookupResponse:
    """Look up a Slack user ID by email address."""

    request_args = _build_request_args(
        email=email,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return SlackLookupResponse.model_validate(response.json())
