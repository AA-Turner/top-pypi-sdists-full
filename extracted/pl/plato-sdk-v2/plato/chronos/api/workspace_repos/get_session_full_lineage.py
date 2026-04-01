"""Get Session Full Lineage"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import FullLineageResponse


def _build_request_args(
    session_public_id: str,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/workspace-repos/sessions/{session_public_id}/full-lineage"

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
    session_public_id: str,
    x_api_key: str | None = None,
) -> FullLineageResponse:
    """Build a full lineage tree across all workspaces for a session, including costs."""

    request_args = _build_request_args(
        session_public_id=session_public_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return FullLineageResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_public_id: str,
    x_api_key: str | None = None,
) -> FullLineageResponse:
    """Build a full lineage tree across all workspaces for a session, including costs."""

    request_args = _build_request_args(
        session_public_id=session_public_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return FullLineageResponse.model_validate(response.json())
