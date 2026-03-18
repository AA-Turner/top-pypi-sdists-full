"""Audit Events Summary"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import AuditSummaryResponse


def _build_request_args(
    session_public_id: str,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/workspace-repos/sessions/{session_public_id}/audit-events/summary"

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
) -> AuditSummaryResponse:
    """Get aggregated audit event summary grouped by step/repo/agent."""

    request_args = _build_request_args(
        session_public_id=session_public_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return AuditSummaryResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_public_id: str,
    x_api_key: str | None = None,
) -> AuditSummaryResponse:
    """Get aggregated audit event summary grouped by step/repo/agent."""

    request_args = _build_request_args(
        session_public_id=session_public_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return AuditSummaryResponse.model_validate(response.json())
