"""List Testcases"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import ListTestcasesResponse


def _build_request_args(
    simulator_ids: str | None = None,
    name: str | None = None,
    prompt: str | None = None,
    tags: str | None = None,
    has_scoring_config: bool | None = None,
    scoring_config_type: str | None = None,
    testcase_statuses: str | None = None,
    work_order_item_id: str | None = None,
    status: str | None = None,
    page: int | None = 1,
    page_size: int | None = 250,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v2/testcases"

    params: dict[str, Any] = {}
    if simulator_ids is not None:
        params["simulator_ids"] = simulator_ids
    if name is not None:
        params["name"] = name
    if prompt is not None:
        params["prompt"] = prompt
    if tags is not None:
        params["tags"] = tags
    if has_scoring_config is not None:
        params["has_scoring_config"] = has_scoring_config
    if scoring_config_type is not None:
        params["scoring_config_type"] = scoring_config_type
    if testcase_statuses is not None:
        params["testcase_statuses"] = testcase_statuses
    if work_order_item_id is not None:
        params["work_order_item_id"] = work_order_item_id
    if status is not None:
        params["status"] = status
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["page_size"] = page_size

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
    simulator_ids: str | None = None,
    name: str | None = None,
    prompt: str | None = None,
    tags: str | None = None,
    has_scoring_config: bool | None = None,
    scoring_config_type: str | None = None,
    testcase_statuses: str | None = None,
    work_order_item_id: str | None = None,
    status: str | None = None,
    page: int | None = 1,
    page_size: int | None = 250,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ListTestcasesResponse:
    """List test cases with filtering and pagination."""

    request_args = _build_request_args(
        simulator_ids=simulator_ids,
        name=name,
        prompt=prompt,
        tags=tags,
        has_scoring_config=has_scoring_config,
        scoring_config_type=scoring_config_type,
        testcase_statuses=testcase_statuses,
        work_order_item_id=work_order_item_id,
        status=status,
        page=page,
        page_size=page_size,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ListTestcasesResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    simulator_ids: str | None = None,
    name: str | None = None,
    prompt: str | None = None,
    tags: str | None = None,
    has_scoring_config: bool | None = None,
    scoring_config_type: str | None = None,
    testcase_statuses: str | None = None,
    work_order_item_id: str | None = None,
    status: str | None = None,
    page: int | None = 1,
    page_size: int | None = 250,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ListTestcasesResponse:
    """List test cases with filtering and pagination."""

    request_args = _build_request_args(
        simulator_ids=simulator_ids,
        name=name,
        prompt=prompt,
        tags=tags,
        has_scoring_config=has_scoring_config,
        scoring_config_type=scoring_config_type,
        testcase_statuses=testcase_statuses,
        work_order_item_id=work_order_item_id,
        status=status,
        page=page,
        page_size=page_size,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ListTestcasesResponse.model_validate(response.json())
