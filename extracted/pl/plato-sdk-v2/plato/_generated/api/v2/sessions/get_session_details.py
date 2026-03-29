"""Get Session Details"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import SessionDetailsResponse


def _build_request_args(
    session_id: str,
    include_mutations: bool | None = False,
    merge_mutations: bool | None = False,
    session_detail: bool | None = False,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/sessions/{session_id}"

    params: dict[str, Any] = {}
    if include_mutations is not None:
        params["include_mutations"] = include_mutations
    if merge_mutations is not None:
        params["merge_mutations"] = merge_mutations
    if session_detail is not None:
        params["session_detail"] = session_detail

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
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
    session_id: str,
    include_mutations: bool | None = False,
    merge_mutations: bool | None = False,
    session_detail: bool | None = False,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> SessionDetailsResponse:
    """Get detailed information about a session.

    Args:
        session_id: The session ID.
        include_mutations: If true, include state mutations grouped by environment alias.
            Ignore rules from the test case config are always applied when available.
        merge_mutations: If true (and include_mutations=true), also merge consecutive
            mutations (e.g. INSERT+UPDATE → INSERT).
        session_detail: If true, include session_detail (SessionPage / v1-shaped payload with
            flat state_mutations and org-scoped session row). Does not change other fields."""

    request_args = _build_request_args(
        session_id=session_id,
        include_mutations=include_mutations,
        merge_mutations=merge_mutations,
        session_detail=session_detail,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return SessionDetailsResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_id: str,
    include_mutations: bool | None = False,
    merge_mutations: bool | None = False,
    session_detail: bool | None = False,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> SessionDetailsResponse:
    """Get detailed information about a session.

    Args:
        session_id: The session ID.
        include_mutations: If true, include state mutations grouped by environment alias.
            Ignore rules from the test case config are always applied when available.
        merge_mutations: If true (and include_mutations=true), also merge consecutive
            mutations (e.g. INSERT+UPDATE → INSERT).
        session_detail: If true, include session_detail (SessionPage / v1-shaped payload with
            flat state_mutations and org-scoped session row). Does not change other fields."""

    request_args = _build_request_args(
        session_id=session_id,
        include_mutations=include_mutations,
        merge_mutations=merge_mutations,
        session_detail=session_detail,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return SessionDetailsResponse.model_validate(response.json())
