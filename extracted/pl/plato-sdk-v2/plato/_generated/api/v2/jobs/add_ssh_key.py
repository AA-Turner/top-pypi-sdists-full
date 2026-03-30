"""Add Ssh Key"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import AddSSHKeyRequest, AddSSHKeyResult


def _build_request_args(
    job_id: str,
    body: AddSSHKeyRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/jobs/{job_id}/add_ssh_key"

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
    body: AddSSHKeyRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> AddSSHKeyResult:
    """Add an SSH public key to a specific job's VM.

    Adds the key to the specified user's authorized_keys file.
    This is the per-job equivalent of the session-level add_ssh_key endpoint."""

    request_args = _build_request_args(
        job_id=job_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return AddSSHKeyResult.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    job_id: str,
    body: AddSSHKeyRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> AddSSHKeyResult:
    """Add an SSH public key to a specific job's VM.

    Adds the key to the specified user's authorized_keys file.
    This is the per-job equivalent of the session-level add_ssh_key endpoint."""

    request_args = _build_request_args(
        job_id=job_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return AddSSHKeyResult.model_validate(response.json())
