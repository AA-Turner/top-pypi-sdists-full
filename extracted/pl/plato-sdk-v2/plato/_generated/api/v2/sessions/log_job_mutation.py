"""Log Job Mutation"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import LogResponse, SystemLogInput


def _build_request_args(
    session_id: str,
    job_id: str,
    body: SystemLogInput,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/sessions/{session_id}/jobs/{job_id}/log"

    return {
        "method": "POST",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
    }


def sync(
    client: httpx.Client,
    session_id: str,
    job_id: str,
    body: SystemLogInput,
) -> LogResponse:
    """Log agent mutations/events for a specific job in a session.

    This endpoint receives logs from agents running in jobs and stores them
    associated with the session for later retrieval and analysis.

    Supports both single log entries and batch log requests."""

    request_args = _build_request_args(
        session_id=session_id,
        job_id=job_id,
        body=body,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return LogResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_id: str,
    job_id: str,
    body: SystemLogInput,
) -> LogResponse:
    """Log agent mutations/events for a specific job in a session.

    This endpoint receives logs from agents running in jobs and stores them
    associated with the session for later retrieval and analysis.

    Supports both single log entries and batch log requests."""

    request_args = _build_request_args(
        session_id=session_id,
        job_id=job_id,
        body=body,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LogResponse.model_validate(response.json())
