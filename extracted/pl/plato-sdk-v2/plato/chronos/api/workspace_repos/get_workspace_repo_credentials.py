"""Get Workspace Repo Credentials"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import WorkspaceRepoCredentialsResponse


def _build_request_args(
    repo_public_id: str,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/workspace-repos/{repo_public_id}/credentials"

    headers: dict[str, str] = {}
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "POST",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    repo_public_id: str,
    x_api_key: str | None = None,
) -> WorkspaceRepoCredentialsResponse:
    """Get STS credentials scoped to a repo's S3 prefix."""

    request_args = _build_request_args(
        repo_public_id=repo_public_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return WorkspaceRepoCredentialsResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    repo_public_id: str,
    x_api_key: str | None = None,
) -> WorkspaceRepoCredentialsResponse:
    """Get STS credentials scoped to a repo's S3 prefix."""

    request_args = _build_request_args(
        repo_public_id=repo_public_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return WorkspaceRepoCredentialsResponse.model_validate(response.json())
