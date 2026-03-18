"""List Audit Events"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import AuditEventsListResponse


def _build_request_args(
    session_public_id: str,
    step_name: str | None = None,
    repo_name: str | None = None,
    ref_public_id: str | None = None,
    path: str | None = None,
    trace_id: str | None = None,
    span_id: str | None = None,
    agent_id: str | None = None,
    agent_name: str | None = None,
    tool_name: str | None = None,
    pid: int | None = None,
    attribution_kind: str | None = None,
    operation: str | None = None,
    limit: int | None = 500,
    offset: int | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/workspace-repos/sessions/{session_public_id}/audit-events"

    params: dict[str, Any] = {}
    if step_name is not None:
        params["step_name"] = step_name
    if repo_name is not None:
        params["repo_name"] = repo_name
    if ref_public_id is not None:
        params["ref_public_id"] = ref_public_id
    if path is not None:
        params["path"] = path
    if trace_id is not None:
        params["trace_id"] = trace_id
    if span_id is not None:
        params["span_id"] = span_id
    if agent_id is not None:
        params["agent_id"] = agent_id
    if agent_name is not None:
        params["agent_name"] = agent_name
    if tool_name is not None:
        params["tool_name"] = tool_name
    if pid is not None:
        params["pid"] = pid
    if attribution_kind is not None:
        params["attribution_kind"] = attribution_kind
    if operation is not None:
        params["operation"] = operation
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset

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
    step_name: str | None = None,
    repo_name: str | None = None,
    ref_public_id: str | None = None,
    path: str | None = None,
    trace_id: str | None = None,
    span_id: str | None = None,
    agent_id: str | None = None,
    agent_name: str | None = None,
    tool_name: str | None = None,
    pid: int | None = None,
    attribution_kind: str | None = None,
    operation: str | None = None,
    limit: int | None = 500,
    offset: int | None = None,
    x_api_key: str | None = None,
) -> AuditEventsListResponse:
    """Query audit events for a session with optional filters."""

    request_args = _build_request_args(
        session_public_id=session_public_id,
        step_name=step_name,
        repo_name=repo_name,
        ref_public_id=ref_public_id,
        path=path,
        trace_id=trace_id,
        span_id=span_id,
        agent_id=agent_id,
        agent_name=agent_name,
        tool_name=tool_name,
        pid=pid,
        attribution_kind=attribution_kind,
        operation=operation,
        limit=limit,
        offset=offset,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return AuditEventsListResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_public_id: str,
    step_name: str | None = None,
    repo_name: str | None = None,
    ref_public_id: str | None = None,
    path: str | None = None,
    trace_id: str | None = None,
    span_id: str | None = None,
    agent_id: str | None = None,
    agent_name: str | None = None,
    tool_name: str | None = None,
    pid: int | None = None,
    attribution_kind: str | None = None,
    operation: str | None = None,
    limit: int | None = 500,
    offset: int | None = None,
    x_api_key: str | None = None,
) -> AuditEventsListResponse:
    """Query audit events for a session with optional filters."""

    request_args = _build_request_args(
        session_public_id=session_public_id,
        step_name=step_name,
        repo_name=repo_name,
        ref_public_id=ref_public_id,
        path=path,
        trace_id=trace_id,
        span_id=span_id,
        agent_id=agent_id,
        agent_name=agent_name,
        tool_name=tool_name,
        pid=pid,
        attribution_kind=attribution_kind,
        operation=operation,
        limit=limit,
        offset=offset,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return AuditEventsListResponse.model_validate(response.json())
