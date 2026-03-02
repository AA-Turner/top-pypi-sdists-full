"""Filter Human Recorder Testcases"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status


def _build_request_args(
    stage: str,
    sim: str,
    page: int | None = 1,
    page_size: int | None = 50,
    is_sample: bool | None = False,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v1/testcases/human-recorder/filter"

    params: dict[str, Any] = {}
    if stage is not None:
        params["stage"] = stage
    if sim is not None:
        params["sim"] = sim
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["page_size"] = page_size
    if is_sample is not None:
        params["is_sample"] = is_sample

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
    stage: str,
    sim: str,
    page: int | None = 1,
    page_size: int | None = 50,
    is_sample: bool | None = False,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Filter Human Recorder Testcases"""

    request_args = _build_request_args(
        stage=stage,
        sim=sim,
        page=page,
        page_size=page_size,
        is_sample=is_sample,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    stage: str,
    sim: str,
    page: int | None = 1,
    page_size: int | None = 50,
    is_sample: bool | None = False,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Filter Human Recorder Testcases"""

    request_args = _build_request_args(
        stage=stage,
        sim=sim,
        page=page,
        page_size=page_size,
        is_sample=is_sample,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
