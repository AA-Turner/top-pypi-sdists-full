"""List Workspace Repos"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import WorkspaceRepoListResponse


def _build_request_args(
    exclude_session_tag: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/workspace-repos"

    params: dict[str, Any] = {}
    if exclude_session_tag is not None:
        params["exclude_session_tag"] = exclude_session_tag

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
    exclude_session_tag: str | None = None,
    x_api_key: str | None = None,
) -> WorkspaceRepoListResponse:
    """List all workspace repos for the org."""

    request_args = _build_request_args(
        exclude_session_tag=exclude_session_tag,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return WorkspaceRepoListResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    exclude_session_tag: str | None = None,
    x_api_key: str | None = None,
) -> WorkspaceRepoListResponse:
    """List all workspace repos for the org."""

    request_args = _build_request_args(
        exclude_session_tag=exclude_session_tag,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return WorkspaceRepoListResponse.model_validate(response.json())
