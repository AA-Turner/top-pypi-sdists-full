"""Update Workspace File"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import UpdateFileRequest, UpdateFileResponse


def _build_request_args(
    session_public_id: str,
    body: UpdateFileRequest,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/workspace-repos/sessions/{session_public_id}/update-file"

    headers: dict[str, str] = {}
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "PUT",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    session_public_id: str,
    body: UpdateFileRequest,
    x_api_key: str | None = None,
) -> UpdateFileResponse:
    """Update a single file in a workspace ref's DVC-tracked directory.

    This is an S3-only operation — no VM is needed. It:
    1. Resolves the workspace ref and reads the existing DVC manifest
    2. Uploads the new file content to DVC cache (keyed by MD5)
    3. Updates the manifest entry for the target file
    4. Uploads the new manifest to DVC cache
    5. Creates a new SessionWorkspaceRef with the updated dvc_files pointer"""

    request_args = _build_request_args(
        session_public_id=session_public_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return UpdateFileResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_public_id: str,
    body: UpdateFileRequest,
    x_api_key: str | None = None,
) -> UpdateFileResponse:
    """Update a single file in a workspace ref's DVC-tracked directory.

    This is an S3-only operation — no VM is needed. It:
    1. Resolves the workspace ref and reads the existing DVC manifest
    2. Uploads the new file content to DVC cache (keyed by MD5)
    3. Updates the manifest entry for the target file
    4. Uploads the new manifest to DVC cache
    5. Creates a new SessionWorkspaceRef with the updated dvc_files pointer"""

    request_args = _build_request_args(
        session_public_id=session_public_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return UpdateFileResponse.model_validate(response.json())
