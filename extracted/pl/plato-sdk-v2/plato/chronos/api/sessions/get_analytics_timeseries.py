"""Get Analytics Timeseries Endpoint"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import AnalyticsTimeseriesResponse


def _build_request_args(
    days: int | None = 30,
    bucket: str | None = "day",
    group_by: str | None = "user",
    tags: list[str] | None = None,
    exclude_tags: list[str] | None = None,
    worlds: list[str] | None = None,
    statuses: list[str] | None = None,
    users: list[str] | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/sessions/analytics-timeseries"

    params: dict[str, Any] = {}
    if days is not None:
        params["days"] = days
    if bucket is not None:
        params["bucket"] = bucket
    if group_by is not None:
        params["group_by"] = group_by
    if tags is not None:
        params["tags"] = tags
    if exclude_tags is not None:
        params["exclude_tags"] = exclude_tags
    if worlds is not None:
        params["worlds"] = worlds
    if statuses is not None:
        params["statuses"] = statuses
    if users is not None:
        params["users"] = users

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
    bucket: str | None = "day",
    group_by: str | None = "user",
    tags: list[str] | None = None,
    exclude_tags: list[str] | None = None,
    worlds: list[str] | None = None,
    statuses: list[str] | None = None,
    users: list[str] | None = None,
    x_api_key: str | None = None,
) -> AnalyticsTimeseriesResponse:
    """Get analytics timeseries data for charting. Combines PG session data with ClickHouse token metrics."""

    request_args = _build_request_args(
        days=days,
        bucket=bucket,
        group_by=group_by,
        tags=tags,
        exclude_tags=exclude_tags,
        worlds=worlds,
        statuses=statuses,
        users=users,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return AnalyticsTimeseriesResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    days: int | None = 30,
    bucket: str | None = "day",
    group_by: str | None = "user",
    tags: list[str] | None = None,
    exclude_tags: list[str] | None = None,
    worlds: list[str] | None = None,
    statuses: list[str] | None = None,
    users: list[str] | None = None,
    x_api_key: str | None = None,
) -> AnalyticsTimeseriesResponse:
    """Get analytics timeseries data for charting. Combines PG session data with ClickHouse token metrics."""

    request_args = _build_request_args(
        days=days,
        bucket=bucket,
        group_by=group_by,
        tags=tags,
        exclude_tags=exclude_tags,
        worlds=worlds,
        statuses=statuses,
        users=users,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return AnalyticsTimeseriesResponse.model_validate(response.json())
