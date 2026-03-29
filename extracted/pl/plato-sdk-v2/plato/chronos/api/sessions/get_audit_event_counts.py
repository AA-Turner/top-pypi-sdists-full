"""Get Audit Event Counts"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import AuditEventCountsResponse


def _build_request_args(
    public_id: str,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/sessions/{public_id}/audit-events/counts"

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
    public_id: str,
    x_api_key: str | None = None,
) -> AuditEventCountsResponse:
    """Return per-span audit event counts for a session.

    Lightweight query using the ``ix_audit_ref_trace_span`` composite index
    for an efficient GROUP BY without touching the main table rows."""

    request_args = _build_request_args(
        public_id=public_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return AuditEventCountsResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    public_id: str,
    x_api_key: str | None = None,
) -> AuditEventCountsResponse:
    """Return per-span audit event counts for a session.

    Lightweight query using the ``ix_audit_ref_trace_span`` composite index
    for an efficient GROUP BY without touching the main table rows."""

    request_args = _build_request_args(
        public_id=public_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return AuditEventCountsResponse.model_validate(response.json())
