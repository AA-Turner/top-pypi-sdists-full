"""Create Workspace Branch"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import CreateBranchRequest, CreateBranchResponse


def _build_request_args(
    repo_public_id: str,
    body: CreateBranchRequest,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/workspace-repos/{repo_public_id}/create-branch"

    headers: dict[str, str] = {}
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "POST",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    repo_public_id: str,
    body: CreateBranchRequest,
    x_api_key: str | None = None,
) -> CreateBranchResponse:
    """Create a new branch (session) under a workspace repo.

    Optionally fork from an existing ref to copy its DVC files as the starting point."""

    request_args = _build_request_args(
        repo_public_id=repo_public_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return CreateBranchResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    repo_public_id: str,
    body: CreateBranchRequest,
    x_api_key: str | None = None,
) -> CreateBranchResponse:
    """Create a new branch (session) under a workspace repo.

    Optionally fork from an existing ref to copy its DVC files as the starting point."""

    request_args = _build_request_args(
        repo_public_id=repo_public_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return CreateBranchResponse.model_validate(response.json())
