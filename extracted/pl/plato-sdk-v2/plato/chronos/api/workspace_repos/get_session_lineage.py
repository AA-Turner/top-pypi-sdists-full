"""Get Session Lineage"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import SessionLineageResponse


def _build_request_args(
    session_public_id: str,
    workspace: str,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/workspace-repos/sessions/{session_public_id}/lineage"

    params: dict[str, Any] = {}
    if workspace is not None:
        params["workspace"] = workspace

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
    workspace: str,
    x_api_key: str | None = None,
) -> SessionLineageResponse:
    """Walk backward through source_ref links to build session lineage for a workspace."""

    request_args = _build_request_args(
        session_public_id=session_public_id,
        workspace=workspace,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return SessionLineageResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_public_id: str,
    workspace: str,
    x_api_key: str | None = None,
) -> SessionLineageResponse:
    """Walk backward through source_ref links to build session lineage for a workspace."""

    request_args = _build_request_args(
        session_public_id=session_public_id,
        workspace=workspace,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return SessionLineageResponse.model_validate(response.json())
