"""Get Session Logs"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import SessionLogsResponse


def _build_request_args(
    public_id: str,
    limit: int | None = 10000,
    cursor: str | None = None,
    offset: int | None = None,
    search: str | None = None,
    errors_only: bool | None = False,
    atif_only: bool | None = False,
    checkpoint_only: bool | None = False,
    plato_type: str | None = None,
    include_audit_events: bool | None = False,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/sessions/{public_id}/logs"

    params: dict[str, Any] = {}
    if limit is not None:
        params["limit"] = limit
    if cursor is not None:
        params["cursor"] = cursor
    if offset is not None:
        params["offset"] = offset
    if search is not None:
        params["search"] = search
    if errors_only is not None:
        params["errors_only"] = errors_only
    if atif_only is not None:
        params["atif_only"] = atif_only
    if checkpoint_only is not None:
        params["checkpoint_only"] = checkpoint_only
    if plato_type is not None:
        params["plato_type"] = plato_type
    if include_audit_events is not None:
        params["include_audit_events"] = include_audit_events

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
    public_id: str,
    limit: int | None = 10000,
    cursor: str | None = None,
    offset: int | None = None,
    search: str | None = None,
    errors_only: bool | None = False,
    atif_only: bool | None = False,
    checkpoint_only: bool | None = False,
    plato_type: str | None = None,
    include_audit_events: bool | None = False,
    x_api_key: str | None = None,
) -> SessionLogsResponse:
    """Get logs/events for a session with cursor-based pagination.

    Pass the cursor from the previous response to load the next page.
    On the first call, omit cursor to load from the beginning."""

    request_args = _build_request_args(
        public_id=public_id,
        limit=limit,
        cursor=cursor,
        offset=offset,
        search=search,
        errors_only=errors_only,
        atif_only=atif_only,
        checkpoint_only=checkpoint_only,
        plato_type=plato_type,
        include_audit_events=include_audit_events,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return SessionLogsResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    public_id: str,
    limit: int | None = 10000,
    cursor: str | None = None,
    offset: int | None = None,
    search: str | None = None,
    errors_only: bool | None = False,
    atif_only: bool | None = False,
    checkpoint_only: bool | None = False,
    plato_type: str | None = None,
    include_audit_events: bool | None = False,
    x_api_key: str | None = None,
) -> SessionLogsResponse:
    """Get logs/events for a session with cursor-based pagination.

    Pass the cursor from the previous response to load the next page.
    On the first call, omit cursor to load from the beginning."""

    request_args = _build_request_args(
        public_id=public_id,
        limit=limit,
        cursor=cursor,
        offset=offset,
        search=search,
        errors_only=errors_only,
        atif_only=atif_only,
        checkpoint_only=checkpoint_only,
        plato_type=plato_type,
        include_audit_events=include_audit_events,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return SessionLogsResponse.model_validate(response.json())
