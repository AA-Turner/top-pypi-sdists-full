"""Get Mutation Groups For Testcase"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status


def _build_request_args(
    public_id: str,
    session_ids: str | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/testcases/{public_id}/mutation-groups"

    params: dict[str, Any] = {}
    if session_ids is not None:
        params["session_ids"] = session_ids

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
    public_id: str,
    session_ids: str | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Get mutation groups for a test case using generated scoring configs.

    This uses AI-based config generation to group sessions by their mutation patterns,
    properly handling things like random IDs (mutation_variables) that differ between
    sessions but represent the same logical mutation.

    Returns groups of session IDs where sessions in each group have equivalent mutations.

    Args:
        session_ids: Optional comma-separated list of session IDs to process.
                    If not provided, will process up to 50 most recent sessions."""

    request_args = _build_request_args(
        public_id=public_id,
        session_ids=session_ids,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    public_id: str,
    session_ids: str | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Get mutation groups for a test case using generated scoring configs.

    This uses AI-based config generation to group sessions by their mutation patterns,
    properly handling things like random IDs (mutation_variables) that differ between
    sessions but represent the same logical mutation.

    Returns groups of session IDs where sessions in each group have equivalent mutations.

    Args:
        session_ids: Optional comma-separated list of session IDs to process.
                    If not provided, will process up to 50 most recent sessions."""

    request_args = _build_request_args(
        public_id=public_id,
        session_ids=session_ids,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
