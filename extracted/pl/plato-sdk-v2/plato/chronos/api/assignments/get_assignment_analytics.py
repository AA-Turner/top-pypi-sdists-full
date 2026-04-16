"""Get Assignment Analytics"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import AssignmentAnalyticsResponse


def _build_request_args(
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/assignments/analytics"

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
    x_api_key: str | None = None,
) -> AssignmentAnalyticsResponse:
    """Per-reviewer stats for all assignments assigned to the caller's org.

    Returns, for each distinct reviewer (user who created reviews):
    - assignment_count: number of assignments this reviewer has reviewed
    - completed_count: assignments marked completed
    - review_count: total reviews created by this user
    - annotation_count: total annotations by this user

    Assignments with no reviews yet appear as a null-reviewer bucket."""

    request_args = _build_request_args(
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return AssignmentAnalyticsResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    x_api_key: str | None = None,
) -> AssignmentAnalyticsResponse:
    """Per-reviewer stats for all assignments assigned to the caller's org.

    Returns, for each distinct reviewer (user who created reviews):
    - assignment_count: number of assignments this reviewer has reviewed
    - completed_count: assignments marked completed
    - review_count: total reviews created by this user
    - annotation_count: total annotations by this user

    Assignments with no reviews yet appear as a null-reviewer bucket."""

    request_args = _build_request_args(
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return AssignmentAnalyticsResponse.model_validate(response.json())
