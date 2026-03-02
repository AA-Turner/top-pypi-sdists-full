"""Get Annotator Assignments"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import AnnotatorAssignmentListItem


def _build_request_args(
    assignment_type: str | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v1/organization/annotator-assignments"

    params: dict[str, Any] = {}
    if assignment_type is not None:
        params["assignment_type"] = assignment_type

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
    assignment_type: str | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> list[AnnotatorAssignmentListItem]:
    """Get annotator assignments for the user's organization"""

    request_args = _build_request_args(
        assignment_type=assignment_type,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    assignment_type: str | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> list[AnnotatorAssignmentListItem]:
    """Get annotator assignments for the user's organization"""

    request_args = _build_request_args(
        assignment_type=assignment_type,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
