"""Get Workspace File Content"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status


def _build_request_args(
    session_public_id: str,
    repo_name: str,
    file_hash: str,
    file_path: str,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/workspace-repos/sessions/{session_public_id}/file-content"

    params: dict[str, Any] = {}
    if repo_name is not None:
        params["repo_name"] = repo_name
    if file_hash is not None:
        params["file_hash"] = file_hash
    if file_path is not None:
        params["file_path"] = file_path

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
    repo_name: str,
    file_hash: str,
    file_path: str,
    x_api_key: str | None = None,
) -> Any:
    """Proxy a DVC-cached file from S3 to the browser (avoids CORS issues)."""

    request_args = _build_request_args(
        session_public_id=session_public_id,
        repo_name=repo_name,
        file_hash=file_hash,
        file_path=file_path,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    session_public_id: str,
    repo_name: str,
    file_hash: str,
    file_path: str,
    x_api_key: str | None = None,
) -> Any:
    """Proxy a DVC-cached file from S3 to the browser (avoids CORS issues)."""

    request_args = _build_request_args(
        session_public_id=session_public_id,
        repo_name=repo_name,
        file_hash=file_hash,
        file_path=file_path,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
