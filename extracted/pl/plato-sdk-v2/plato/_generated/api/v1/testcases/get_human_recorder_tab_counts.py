"""Get Human Recorder Tab Counts"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status


def _build_request_args(
    admin_view: bool | None = False,
    is_sample: bool | None = False,
    organization_id: int | None = None,
    simulator_id: int | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v1/testcases/human-recorder/tab-counts"

    params: dict[str, Any] = {}
    if admin_view is not None:
        params["admin_view"] = admin_view
    if is_sample is not None:
        params["is_sample"] = is_sample
    if organization_id is not None:
        params["organization_id"] = organization_id
    if simulator_id is not None:
        params["simulator_id"] = simulator_id

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
    admin_view: bool | None = False,
    is_sample: bool | None = False,
    organization_id: int | None = None,
    simulator_id: int | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Get Human Recorder Tab Counts"""

    request_args = _build_request_args(
        admin_view=admin_view,
        is_sample=is_sample,
        organization_id=organization_id,
        simulator_id=simulator_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    admin_view: bool | None = False,
    is_sample: bool | None = False,
    organization_id: int | None = None,
    simulator_id: int | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Get Human Recorder Tab Counts"""

    request_args = _build_request_args(
        admin_view=admin_view,
        is_sample=is_sample,
        organization_id=organization_id,
        simulator_id=simulator_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
