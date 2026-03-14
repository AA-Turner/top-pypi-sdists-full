"""List Reviews"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import ReviewListResponse


def _build_request_args(
    session_id: str | None = None,
    tags: list[str] | None = None,
    tags_mode: str | None = "or",
    author_type: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/reviews"

    params: dict[str, Any] = {}
    if session_id is not None:
        params["session_id"] = session_id
    if tags is not None:
        params["tags"] = tags
    if tags_mode is not None:
        params["tags_mode"] = tags_mode
    if author_type is not None:
        params["author_type"] = author_type

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
    session_id: str | None = None,
    tags: list[str] | None = None,
    tags_mode: str | None = "or",
    author_type: str | None = None,
    x_api_key: str | None = None,
) -> ReviewListResponse:
    """List reviews, optionally filtered by session and/or tags."""

    request_args = _build_request_args(
        session_id=session_id,
        tags=tags,
        tags_mode=tags_mode,
        author_type=author_type,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ReviewListResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_id: str | None = None,
    tags: list[str] | None = None,
    tags_mode: str | None = "or",
    author_type: str | None = None,
    x_api_key: str | None = None,
) -> ReviewListResponse:
    """List reviews, optionally filtered by session and/or tags."""

    request_args = _build_request_args(
        session_id=session_id,
        tags=tags,
        tags_mode=tags_mode,
        author_type=author_type,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ReviewListResponse.model_validate(response.json())
