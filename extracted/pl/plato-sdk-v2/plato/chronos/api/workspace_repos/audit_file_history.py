"""Audit File History"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import AuditEventsListResponse


def _build_request_args(
    session_public_id: str,
    path: str,
    repo_name: str,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/workspace-repos/sessions/{session_public_id}/audit/file-history"

    params: dict[str, Any] = {}
    if path is not None:
        params["path"] = path
    if repo_name is not None:
        params["repo_name"] = repo_name

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
    path: str,
    repo_name: str,
    x_api_key: str | None = None,
) -> AuditEventsListResponse:
    """Get all audit events for a specific file across all steps."""

    request_args = _build_request_args(
        session_public_id=session_public_id,
        path=path,
        repo_name=repo_name,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return AuditEventsListResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_public_id: str,
    path: str,
    repo_name: str,
    x_api_key: str | None = None,
) -> AuditEventsListResponse:
    """Get all audit events for a specific file across all steps."""

    request_args = _build_request_args(
        session_public_id=session_public_id,
        path=path,
        repo_name=repo_name,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return AuditEventsListResponse.model_validate(response.json())
