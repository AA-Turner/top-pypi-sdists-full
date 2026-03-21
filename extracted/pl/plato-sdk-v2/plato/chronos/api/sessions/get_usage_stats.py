"""Get Usage Stats"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import UsageStatsResponse


def _build_request_args(
    days: int | None = 30,
    exclude_tags: list[str] | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/sessions/usage-stats"

    params: dict[str, Any] = {}
    if days is not None:
        params["days"] = days
    if exclude_tags is not None:
        params["exclude_tags"] = exclude_tags

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
    days: int | None = 30,
    exclude_tags: list[str] | None = None,
    x_api_key: str | None = None,
) -> UsageStatsResponse:
    """Get org-wide usage stats for the leaderboard dashboard."""

    request_args = _build_request_args(
        days=days,
        exclude_tags=exclude_tags,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return UsageStatsResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    days: int | None = 30,
    exclude_tags: list[str] | None = None,
    x_api_key: str | None = None,
) -> UsageStatsResponse:
    """Get org-wide usage stats for the leaderboard dashboard."""

    request_args = _build_request_args(
        days=days,
        exclude_tags=exclude_tags,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return UsageStatsResponse.model_validate(response.json())
