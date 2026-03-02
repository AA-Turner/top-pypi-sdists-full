"""Log State Mutation"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import BaseStructuredRunLog, LogResponse


def _build_request_args(
    session_id: str,
    body: BaseStructuredRunLog,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/env/{session_id}/log"

    return {
        "method": "POST",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
    }


def sync(
    client: httpx.Client,
    session_id: str,
    body: BaseStructuredRunLog,
) -> LogResponse:
    """Log a state mutation or batch of mutations.

    TODO: Deprecate in favor of v2 log endpoint in app/api/v2/session_routes.py.
    This endpoint uses BaseStructuredRunLog which doesn't generate proper OpenAPI schemas."""

    request_args = _build_request_args(
        session_id=session_id,
        body=body,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return LogResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_id: str,
    body: BaseStructuredRunLog,
) -> LogResponse:
    """Log a state mutation or batch of mutations.

    TODO: Deprecate in favor of v2 log endpoint in app/api/v2/session_routes.py.
    This endpoint uses BaseStructuredRunLog which doesn't generate proper OpenAPI schemas."""

    request_args = _build_request_args(
        session_id=session_id,
        body=body,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LogResponse.model_validate(response.json())
