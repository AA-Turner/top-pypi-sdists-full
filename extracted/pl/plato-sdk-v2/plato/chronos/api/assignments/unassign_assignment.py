"""Unassign Assignment"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import AssignmentResponse


def _build_request_args(
    assignment_id: str,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/assignments/{assignment_id}/unassign"

    headers: dict[str, str] = {}
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "POST",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    assignment_id: str,
    x_api_key: str | None = None,
) -> AssignmentResponse:
    """Unassign an in_progress claim back to the pool (claiming reviewer, or annotator admin for someone else's claim). Discards the claimed review and its annotations."""

    request_args = _build_request_args(
        assignment_id=assignment_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return AssignmentResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    assignment_id: str,
    x_api_key: str | None = None,
) -> AssignmentResponse:
    """Unassign an in_progress claim back to the pool (claiming reviewer, or annotator admin for someone else's claim). Discards the claimed review and its annotations."""

    request_args = _build_request_args(
        assignment_id=assignment_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return AssignmentResponse.model_validate(response.json())
