"""Checkpoint Vm"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import (
    AppApiV1PublicBuildRoutesCreateSnapshotRequest,
    AppApiV1PublicBuildRoutesCreateSnapshotResponse,
)


def _build_request_args(
    public_id: str,
    body: AppApiV1PublicBuildRoutesCreateSnapshotRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/sandbox/public-build/vm/{public_id}/checkpoint"

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
    public_id: str,
    body: AppApiV1PublicBuildRoutesCreateSnapshotRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> AppApiV1PublicBuildRoutesCreateSnapshotResponse:
    """Create a checkpoint snapshot of a VM.

    This creates a blockdiff_checkpoint artifact type instead of a regular blockdiff.
    Optional parameters allow overriding artifact labels:
    - service: Simulator name (defaults to job's service)
    - git_hash: Git hash/version (defaults to job's version or "unknown")
    - dataset: Dataset name (defaults to job's dataset)"""

    request_args = _build_request_args(
        public_id=public_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return AppApiV1PublicBuildRoutesCreateSnapshotResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    public_id: str,
    body: AppApiV1PublicBuildRoutesCreateSnapshotRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> AppApiV1PublicBuildRoutesCreateSnapshotResponse:
    """Create a checkpoint snapshot of a VM.

    This creates a blockdiff_checkpoint artifact type instead of a regular blockdiff.
    Optional parameters allow overriding artifact labels:
    - service: Simulator name (defaults to job's service)
    - git_hash: Git hash/version (defaults to job's version or "unknown")
    - dataset: Dataset name (defaults to job's dataset)"""

    request_args = _build_request_args(
        public_id=public_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return AppApiV1PublicBuildRoutesCreateSnapshotResponse.model_validate(response.json())
