"""Search Session Spans"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import SpanSearchRequest, SpanSearchResponse


def _build_request_args(
    body: SpanSearchRequest,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/otel/spans/search"

    headers: dict[str, str] = {}
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "POST",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    body: SpanSearchRequest,
    x_api_key: str | None = None,
) -> SpanSearchResponse:
    """Search span text across a set of sessions.

    The sessions come from the request's filters within the caller's org (a Plato-org admin may name
    other orgs in ``org_ids``, e.g. to search two orgs' benchmark runs at once), capped per request. Terms match message, reasoning, tool input
    (``tool_calls``) and tool output (``observation``) as case-insensitive substrings; hits carry a
    snippet around the first match, with inlined base64 elided."""

    request_args = _build_request_args(
        body=body,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return SpanSearchResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    body: SpanSearchRequest,
    x_api_key: str | None = None,
) -> SpanSearchResponse:
    """Search span text across a set of sessions.

    The sessions come from the request's filters within the caller's org (a Plato-org admin may name
    other orgs in ``org_ids``, e.g. to search two orgs' benchmark runs at once), capped per request. Terms match message, reasoning, tool input
    (``tool_calls``) and tool output (``observation``) as case-insensitive substrings; hits carry a
    snippet around the first match, with inlined base64 elided."""

    request_args = _build_request_args(
        body=body,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return SpanSearchResponse.model_validate(response.json())
