"""Get Workspace Repo Size"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import WorkspaceRepoSizeResponse


def _build_request_args(
    repo_public_id: str,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/workspace-repos/{repo_public_id}/size"

    headers: dict[str, str] = {}
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "GET",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    repo_public_id: str,
    x_api_key: str | None = None,
) -> WorkspaceRepoSizeResponse:
    """Calculate the total S3 storage used by a workspace repo's DVC cache."""

    request_args = _build_request_args(
        repo_public_id=repo_public_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return WorkspaceRepoSizeResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    repo_public_id: str,
    x_api_key: str | None = None,
) -> WorkspaceRepoSizeResponse:
    """Calculate the total S3 storage used by a workspace repo's DVC cache."""

    request_args = _build_request_args(
        repo_public_id=repo_public_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return WorkspaceRepoSizeResponse.model_validate(response.json())
