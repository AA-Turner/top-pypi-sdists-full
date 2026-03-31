"""Preview Assignments"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import AssignmentPreviewResponse


def _build_request_args(
    session_public_id: str,
    scope_type: str,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/sessions/{session_public_id}/assignments/preview"

    params: dict[str, Any] = {}
    if scope_type is not None:
        params["scope_type"] = scope_type

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
    scope_type: str,
    x_api_key: str | None = None,
) -> AssignmentPreviewResponse:
    """Preview assignments that would be created for a session without persisting them.

    scope_type: "route" | "page" """

    request_args = _build_request_args(
        session_public_id=session_public_id,
        scope_type=scope_type,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return AssignmentPreviewResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_public_id: str,
    scope_type: str,
    x_api_key: str | None = None,
) -> AssignmentPreviewResponse:
    """Preview assignments that would be created for a session without persisting them.

    scope_type: "route" | "page" """

    request_args = _build_request_args(
        session_public_id=session_public_id,
        scope_type=scope_type,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return AssignmentPreviewResponse.model_validate(response.json())
