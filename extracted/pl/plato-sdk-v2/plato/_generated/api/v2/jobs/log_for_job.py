"""Log For Job"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import LogResponse, SystemLogInput


def _build_request_args(
    job_id: str,
    body: SystemLogInput,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/jobs/{job_id}/log"

    return {
        "method": "POST",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
    }


def sync(
    client: httpx.Client,
    job_id: str,
    body: SystemLogInput,
) -> LogResponse:
    """Log a state mutation or batch of mutations for a specific job.

    This v2 endpoint stores logs with job_id association, enabling per-job log queries.
    The job's session_id is looked up automatically.

    No auth required - this is called by the VM as a callback.

    Args:
        job_id: The job public ID.
        log: Single log entry or batch of mutations.

    Returns:
        LogResponse with status."""

    request_args = _build_request_args(
        job_id=job_id,
        body=body,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return LogResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    job_id: str,
    body: SystemLogInput,
) -> LogResponse:
    """Log a state mutation or batch of mutations for a specific job.

    This v2 endpoint stores logs with job_id association, enabling per-job log queries.
    The job's session_id is looked up automatically.

    No auth required - this is called by the VM as a callback.

    Args:
        job_id: The job public ID.
        log: Single log entry or batch of mutations.

    Returns:
        LogResponse with status."""

    request_args = _build_request_args(
        job_id=job_id,
        body=body,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LogResponse.model_validate(response.json())
