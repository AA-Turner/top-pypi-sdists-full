"""Setup Sandbox"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import (
    AppApiV2SchemasSessionSetupSandboxRequest,
    AppApiV2SchemasSessionSetupSandboxResponse,
)


def _build_request_args(
    session_id: str,
    body: AppApiV2SchemasSessionSetupSandboxRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/sessions/{session_id}/setup_sandbox"

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
    session_id: str,
    body: AppApiV2SchemasSessionSetupSandboxRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> AppApiV2SchemasSessionSetupSandboxResponse:
    """Setup sandbox environment with Docker overlay on all jobs in the session.

    This configures the VM for Docker usage with overlay2 storage driver,
    which is significantly faster than the default vfs driver. Should be called
    after session creation and before pulling Docker images.

    The setup includes:
    - Mounting /dev/vdb to /mnt/docker for Docker storage
    - Configuring Docker with overlay2 storage driver
    - Setting up ECR and Docker Hub authentication
    - Adding plato user to docker group for shared Docker access"""

    request_args = _build_request_args(
        session_id=session_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return AppApiV2SchemasSessionSetupSandboxResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_id: str,
    body: AppApiV2SchemasSessionSetupSandboxRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> AppApiV2SchemasSessionSetupSandboxResponse:
    """Setup sandbox environment with Docker overlay on all jobs in the session.

    This configures the VM for Docker usage with overlay2 storage driver,
    which is significantly faster than the default vfs driver. Should be called
    after session creation and before pulling Docker images.

    The setup includes:
    - Mounting /dev/vdb to /mnt/docker for Docker storage
    - Configuring Docker with overlay2 storage driver
    - Setting up ECR and Docker Hub authentication
    - Adding plato user to docker group for shared Docker access"""

    request_args = _build_request_args(
        session_id=session_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return AppApiV2SchemasSessionSetupSandboxResponse.model_validate(response.json())
