"""Stream Preview Assignments Route"""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any

import httpx

from plato.chronos.errors import raise_for_status


def _build_request_args(
    session_public_id: str,
    artifact_id: str | None = None,
    assignment_type: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/sessions/{session_public_id}/assignments/preview-stream"

    params: dict[str, Any] = {}
    if artifact_id is not None:
        params["artifact_id"] = artifact_id
    if assignment_type is not None:
        params["assignment_type"] = assignment_type

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
    artifact_id: str | None = None,
    assignment_type: str | None = None,
    x_api_key: str | None = None,
) -> None:
    """Stream assignment preview items as NDJSON as they are discovered from S3.

    assignment_type: layout type for generated assignments (default: "browser").
    Valid values: "browser", "browser_with_screenshots"."""

    request_args = _build_request_args(
        session_public_id=session_public_id,
        artifact_id=artifact_id,
        assignment_type=assignment_type,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return None


async def asyncio(
    client: httpx.AsyncClient,
    session_public_id: str,
    artifact_id: str | None = None,
    assignment_type: str | None = None,
    x_api_key: str | None = None,
) -> None:
    """Stream assignment preview items as NDJSON as they are discovered from S3.

    assignment_type: layout type for generated assignments (default: "browser").
    Valid values: "browser", "browser_with_screenshots"."""

    request_args = _build_request_args(
        session_public_id=session_public_id,
        artifact_id=artifact_id,
        assignment_type=assignment_type,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return None


def sync_stream(
    client: httpx.Client,
    session_public_id: str,
    artifact_id: str | None = None,
    assignment_type: str | None = None,
    x_api_key: str | None = None,
) -> Iterator[dict[str, Any]]:
    """Stream Preview Assignments Route (streaming)"""
    import json

    request_args = _build_request_args(
        session_public_id=session_public_id,
        artifact_id=artifact_id,
        assignment_type=assignment_type,
        x_api_key=x_api_key,
    )

    with client.stream(**request_args) as response:
        raise_for_status(response)
        for line in response.iter_lines():
            if line.strip():
                yield json.loads(line)


async def asyncio_stream(
    client: httpx.AsyncClient,
    session_public_id: str,
    artifact_id: str | None = None,
    assignment_type: str | None = None,
    x_api_key: str | None = None,
) -> AsyncIterator[dict[str, Any]]:
    """Stream Preview Assignments Route (streaming)"""
    import json

    request_args = _build_request_args(
        session_public_id=session_public_id,
        artifact_id=artifact_id,
        assignment_type=assignment_type,
        x_api_key=x_api_key,
    )

    async with client.stream(**request_args) as response:
        raise_for_status(response)
        async for line in response.aiter_lines():
            if line.strip():
                yield json.loads(line)
