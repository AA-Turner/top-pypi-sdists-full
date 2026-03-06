"""List Workspace Files"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import WorkspaceFilesResponse


def _build_request_args(
    session_public_id: str,
    step_name: str,
    repo_name: str,
    ref_public_id: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/workspace-repos/sessions/{session_public_id}/files"

    params: dict[str, Any] = {}
    if step_name is not None:
        params["step_name"] = step_name
    if repo_name is not None:
        params["repo_name"] = repo_name
    if ref_public_id is not None:
        params["ref_public_id"] = ref_public_id

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
    session_public_id: str,
    step_name: str,
    repo_name: str,
    ref_public_id: str | None = None,
    x_api_key: str | None = None,
) -> WorkspaceFilesResponse:
    """List files in a workspace ref by parsing DVC .dir manifests from S3.

    This is lightweight — only fetches the small directory manifest JSON,
    not the actual data files.

    When ref_public_id is provided, looks up that specific ref instead of
    the latest ref matching step_name."""

    request_args = _build_request_args(
        session_public_id=session_public_id,
        step_name=step_name,
        repo_name=repo_name,
        ref_public_id=ref_public_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return WorkspaceFilesResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_public_id: str,
    step_name: str,
    repo_name: str,
    ref_public_id: str | None = None,
    x_api_key: str | None = None,
) -> WorkspaceFilesResponse:
    """List files in a workspace ref by parsing DVC .dir manifests from S3.

    This is lightweight — only fetches the small directory manifest JSON,
    not the actual data files.

    When ref_public_id is provided, looks up that specific ref instead of
    the latest ref matching step_name."""

    request_args = _build_request_args(
        session_public_id=session_public_id,
        step_name=step_name,
        repo_name=repo_name,
        ref_public_id=ref_public_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return WorkspaceFilesResponse.model_validate(response.json())
