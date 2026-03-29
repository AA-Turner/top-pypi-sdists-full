"""List Sessions"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import SessionListResponse


def _build_request_args(
    tag: str | None = None,
    tags: list[str] | None = None,
    tags_mode: str | None = "or",
    exclude_tags: list[str] | None = None,
    created_by: str | None = None,
    limit: int | None = 50,
    offset: int | None = None,
    status: str | None = None,
    top_level_only: bool | None = True,
    world_package: str | None = None,
    world_version: str | None = None,
    archived_only: bool | None = False,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/sessions"

    params: dict[str, Any] = {}
    if tag is not None:
        params["tag"] = tag
    if tags is not None:
        params["tags"] = tags
    if tags_mode is not None:
        params["tags_mode"] = tags_mode
    if exclude_tags is not None:
        params["exclude_tags"] = exclude_tags
    if created_by is not None:
        params["created_by"] = created_by
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    if status is not None:
        params["status"] = status
    if top_level_only is not None:
        params["top_level_only"] = top_level_only
    if world_package is not None:
        params["world_package"] = world_package
    if world_version is not None:
        params["world_version"] = world_version
    if archived_only is not None:
        params["archived_only"] = archived_only

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
    tag: str | None = None,
    tags: list[str] | None = None,
    tags_mode: str | None = "or",
    exclude_tags: list[str] | None = None,
    created_by: str | None = None,
    limit: int | None = 50,
    offset: int | None = None,
    status: str | None = None,
    top_level_only: bool | None = True,
    world_package: str | None = None,
    world_version: str | None = None,
    archived_only: bool | None = False,
    x_api_key: str | None = None,
) -> SessionListResponse:
    """List sessions for the org with pagination and filtering.

    Tag filtering uses ltree for hierarchical matching:
    - 'project' matches 'project', 'project.foo', 'project.foo.bar'
    - 'project.foo' matches 'project.foo', 'project.foo.bar'"""

    request_args = _build_request_args(
        tag=tag,
        tags=tags,
        tags_mode=tags_mode,
        exclude_tags=exclude_tags,
        created_by=created_by,
        limit=limit,
        offset=offset,
        status=status,
        top_level_only=top_level_only,
        world_package=world_package,
        world_version=world_version,
        archived_only=archived_only,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return SessionListResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    tag: str | None = None,
    tags: list[str] | None = None,
    tags_mode: str | None = "or",
    exclude_tags: list[str] | None = None,
    created_by: str | None = None,
    limit: int | None = 50,
    offset: int | None = None,
    status: str | None = None,
    top_level_only: bool | None = True,
    world_package: str | None = None,
    world_version: str | None = None,
    archived_only: bool | None = False,
    x_api_key: str | None = None,
) -> SessionListResponse:
    """List sessions for the org with pagination and filtering.

    Tag filtering uses ltree for hierarchical matching:
    - 'project' matches 'project', 'project.foo', 'project.foo.bar'
    - 'project.foo' matches 'project.foo', 'project.foo.bar'"""

    request_args = _build_request_args(
        tag=tag,
        tags=tags,
        tags_mode=tags_mode,
        exclude_tags=exclude_tags,
        created_by=created_by,
        limit=limit,
        offset=offset,
        status=status,
        top_level_only=top_level_only,
        world_package=world_package,
        world_version=world_version,
        archived_only=archived_only,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return SessionListResponse.model_validate(response.json())
