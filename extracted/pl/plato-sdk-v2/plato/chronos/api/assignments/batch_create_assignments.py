"""Batch Create Assignments"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import AssignmentListResponse, BatchCreateAssignmentsBody


def _build_request_args(
    body: BatchCreateAssignmentsBody,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/assignments/batch"

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
    body: BatchCreateAssignmentsBody,
    x_api_key: str | None = None,
) -> AssignmentListResponse:
    """Create multiple assignments at once in the caller's org."""

    request_args = _build_request_args(
        body=body,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return AssignmentListResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    body: BatchCreateAssignmentsBody,
    x_api_key: str | None = None,
) -> AssignmentListResponse:
    """Create multiple assignments at once in the caller's org."""

    request_args = _build_request_args(
        body=body,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return AssignmentListResponse.model_validate(response.json())
