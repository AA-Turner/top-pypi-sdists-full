"""Get Scores By User"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status


def _build_request_args(
    user_id: int,
    page: int | None = 1,
    page_size: int | None = None,
    days: float | None = None,
    include_human_results: bool | None = False,
    date: str | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v1/evals/scores"

    params: dict[str, Any] = {}
    if user_id is not None:
        params["user_id"] = user_id
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["pageSize"] = page_size
    if days is not None:
        params["days"] = days
    if include_human_results is not None:
        params["include_human_results"] = include_human_results
    if date is not None:
        params["date"] = date

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
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
    user_id: int,
    page: int | None = 1,
    page_size: int | None = None,
    days: float | None = None,
    include_human_results: bool | None = False,
    date: str | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Get Scores By User"""

    request_args = _build_request_args(
        user_id=user_id,
        page=page,
        page_size=page_size,
        days=days,
        include_human_results=include_human_results,
        date=date,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    user_id: int,
    page: int | None = 1,
    page_size: int | None = None,
    days: float | None = None,
    include_human_results: bool | None = False,
    date: str | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Get Scores By User"""

    request_args = _build_request_args(
        user_id=user_id,
        page=page,
        page_size=page_size,
        days=days,
        include_human_results=include_human_results,
        date=date,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
