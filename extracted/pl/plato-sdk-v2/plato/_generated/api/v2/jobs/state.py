"""State"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import SessionStateResult


def _build_request_args(
    job_id: str,
    merge_mutations: bool | None = False,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/jobs/{job_id}/state"

    params: dict[str, Any] = {}
    if merge_mutations is not None:
        params["merge_mutations"] = merge_mutations

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
    job_id: str,
    merge_mutations: bool | None = False,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> SessionStateResult:
    """Get the current state of a specific job."""

    request_args = _build_request_args(
        job_id=job_id,
        merge_mutations=merge_mutations,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return SessionStateResult.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    job_id: str,
    merge_mutations: bool | None = False,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> SessionStateResult:
    """Get the current state of a specific job."""

    request_args = _build_request_args(
        job_id=job_id,
        merge_mutations=merge_mutations,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return SessionStateResult.model_validate(response.json())
