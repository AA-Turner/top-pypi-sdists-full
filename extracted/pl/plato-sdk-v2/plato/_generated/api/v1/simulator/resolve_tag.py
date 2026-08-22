"""Resolve Tag"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import ResolveTagResponse


def _build_request_args(
    tag_name: str,
    dataset: str | None = None,
    category: list[str] | None = None,
    cursor: str | None = None,
    limit: int | None = 100,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/simulator/resolve-tag/{tag_name}"

    params: dict[str, Any] = {}
    if dataset is not None:
        params["dataset"] = dataset
    if category is not None:
        params["category"] = category
    if cursor is not None:
        params["cursor"] = cursor
    if limit is not None:
        params["limit"] = limit

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
    tag_name: str,
    dataset: str | None = None,
    category: list[str] | None = None,
    cursor: str | None = None,
    limit: int | None = 100,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ResolveTagResponse:
    """Resolve a tag to every artifact it points at, across all simulators.

    Returns one entry per (simulator, dataset) the tag exists for, each with
    the artifact public id and the full simulator details. Simulators the
    principal cannot view are omitted; `category` narrows to simulators in
    any of the named categories.

    Cursor-paginated: pass `next_cursor` back as `cursor` until `has_more` is
    false. `total` counts the entries visible to the caller, so every page but
    the last is exactly `limit` long. Only the simulators on the requested page
    are loaded in full."""

    request_args = _build_request_args(
        tag_name=tag_name,
        dataset=dataset,
        category=category,
        cursor=cursor,
        limit=limit,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ResolveTagResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    tag_name: str,
    dataset: str | None = None,
    category: list[str] | None = None,
    cursor: str | None = None,
    limit: int | None = 100,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ResolveTagResponse:
    """Resolve a tag to every artifact it points at, across all simulators.

    Returns one entry per (simulator, dataset) the tag exists for, each with
    the artifact public id and the full simulator details. Simulators the
    principal cannot view are omitted; `category` narrows to simulators in
    any of the named categories.

    Cursor-paginated: pass `next_cursor` back as `cursor` until `has_more` is
    false. `total` counts the entries visible to the caller, so every page but
    the last is exactly `limit` long. Only the simulators on the requested page
    are loaded in full."""

    request_args = _build_request_args(
        tag_name=tag_name,
        dataset=dataset,
        category=category,
        cursor=cursor,
        limit=limit,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ResolveTagResponse.model_validate(response.json())
