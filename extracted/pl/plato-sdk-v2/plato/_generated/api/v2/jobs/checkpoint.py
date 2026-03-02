"""Checkpoint"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import CreateCheckpointRequest, CreateCheckpointResult


def _build_request_args(
    job_id: str,
    body: CreateCheckpointRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/jobs/{job_id}/checkpoint"

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
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
    job_id: str,
    body: CreateCheckpointRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> CreateCheckpointResult:
    """Create a checkpoint of a specific job.

    Checkpoints are lightweight snapshots that can only be created from VMs
    that were started from an existing artifact. They store only the diff
    from the parent artifact.

    Optional request body allows overriding artifact metadata:
    - override_service: Override simulator/service name
    - override_version: Override version/git_hash
    - override_dataset: Override dataset name"""

    request_args = _build_request_args(
        job_id=job_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return CreateCheckpointResult.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    job_id: str,
    body: CreateCheckpointRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> CreateCheckpointResult:
    """Create a checkpoint of a specific job.

    Checkpoints are lightweight snapshots that can only be created from VMs
    that were started from an existing artifact. They store only the diff
    from the parent artifact.

    Optional request body allows overriding artifact metadata:
    - override_service: Override simulator/service name
    - override_version: Override version/git_hash
    - override_dataset: Override dataset name"""

    request_args = _build_request_args(
        job_id=job_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return CreateCheckpointResult.model_validate(response.json())
