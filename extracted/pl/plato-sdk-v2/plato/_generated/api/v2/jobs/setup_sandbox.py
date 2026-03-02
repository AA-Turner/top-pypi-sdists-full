"""Setup Sandbox"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import AppApiV2SchemasSessionSetupSandboxRequest, SetupSandboxResult


def _build_request_args(
    job_id: str,
    body: AppApiV2SchemasSessionSetupSandboxRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/jobs/{job_id}/setup_sandbox"

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
    body: AppApiV2SchemasSessionSetupSandboxRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> SetupSandboxResult:
    """Setup sandbox environment with Docker overlay on a specific job.

    This configures the VM for Docker usage with overlay2 storage driver,
    which is significantly faster than the default vfs driver. Should be called
    after job creation and before pulling Docker images.

    Args:
        job_id: The job public ID.
        request: Optional SetupSandboxRequest with timeout.

    Returns:
        SetupSandboxResult with success status and command output."""

    request_args = _build_request_args(
        job_id=job_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return SetupSandboxResult.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    job_id: str,
    body: AppApiV2SchemasSessionSetupSandboxRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> SetupSandboxResult:
    """Setup sandbox environment with Docker overlay on a specific job.

    This configures the VM for Docker usage with overlay2 storage driver,
    which is significantly faster than the default vfs driver. Should be called
    after job creation and before pulling Docker images.

    Args:
        job_id: The job public ID.
        request: Optional SetupSandboxRequest with timeout.

    Returns:
        SetupSandboxResult with success status and command output."""

    request_args = _build_request_args(
        job_id=job_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return SetupSandboxResult.model_validate(response.json())
