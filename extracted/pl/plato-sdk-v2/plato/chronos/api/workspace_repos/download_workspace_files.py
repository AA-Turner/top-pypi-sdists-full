"""Download Workspace Files"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status


def _build_request_args(
    session_public_id: str,
    step_name: str,
    repo_name: str,
    ref_public_id: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/workspace-repos/sessions/{session_public_id}/download"

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
) -> Any:
    """Stream a ZIP archive of all files in a workspace ref.

    Files are streamed directly from S3 through the ZIP compressor to the
    client — only one file chunk (~8 MB) is held in memory at a time."""

    request_args = _build_request_args(
        session_public_id=session_public_id,
        step_name=step_name,
        repo_name=repo_name,
        ref_public_id=ref_public_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.content


async def asyncio(
    client: httpx.AsyncClient,
    session_public_id: str,
    step_name: str,
    repo_name: str,
    ref_public_id: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Stream a ZIP archive of all files in a workspace ref.

    Files are streamed directly from S3 through the ZIP compressor to the
    client — only one file chunk (~8 MB) is held in memory at a time."""

    request_args = _build_request_args(
        session_public_id=session_public_id,
        step_name=step_name,
        repo_name=repo_name,
        ref_public_id=ref_public_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.content
