"""Get Testcases"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status


def _build_request_args(
    start_path: str | None = None,
    test_case_set_ids: str | None = None,
    name: str | None = None,
    prompt: str | None = None,
    mode: str | None = None,
    page: int | None = None,
    page_size: int | None = 30,
    simulator_id: int | None = None,
    simulator_name: str | None = None,
    test_case_public_id: str | None = None,
    scoring_config_type: str | None = None,
    is_assigned: bool | None = None,
    is_sample: bool | None = None,
    rejected: bool | None = None,
    exclude_assigned_to_annotators: bool | None = None,
    workorder: str | None = None,
    infeasible: bool | None = None,
    testcase_statuses: str | None = None,
    work_order_item_id: str | None = None,
    status: str | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v1/testcases"

    params: dict[str, Any] = {}
    if start_path is not None:
        params["start_path"] = start_path
    if test_case_set_ids is not None:
        params["test_case_set_ids"] = test_case_set_ids
    if name is not None:
        params["name"] = name
    if prompt is not None:
        params["prompt"] = prompt
    if mode is not None:
        params["mode"] = mode
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["page_size"] = page_size
    if simulator_id is not None:
        params["simulator_id"] = simulator_id
    if simulator_name is not None:
        params["simulator_name"] = simulator_name
    if test_case_public_id is not None:
        params["test_case_public_id"] = test_case_public_id
    if scoring_config_type is not None:
        params["scoring_config_type"] = scoring_config_type
    if is_assigned is not None:
        params["is_assigned"] = is_assigned
    if is_sample is not None:
        params["is_sample"] = is_sample
    if rejected is not None:
        params["rejected"] = rejected
    if exclude_assigned_to_annotators is not None:
        params["exclude_assigned_to_annotators"] = exclude_assigned_to_annotators
    if workorder is not None:
        params["workorder"] = workorder
    if infeasible is not None:
        params["infeasible"] = infeasible
    if testcase_statuses is not None:
        params["testcase_statuses"] = testcase_statuses
    if work_order_item_id is not None:
        params["work_order_item_id"] = work_order_item_id
    if status is not None:
        params["status"] = status

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
    start_path: str | None = None,
    test_case_set_ids: str | None = None,
    name: str | None = None,
    prompt: str | None = None,
    mode: str | None = None,
    page: int | None = None,
    page_size: int | None = 30,
    simulator_id: int | None = None,
    simulator_name: str | None = None,
    test_case_public_id: str | None = None,
    scoring_config_type: str | None = None,
    is_assigned: bool | None = None,
    is_sample: bool | None = None,
    rejected: bool | None = None,
    exclude_assigned_to_annotators: bool | None = None,
    workorder: str | None = None,
    infeasible: bool | None = None,
    testcase_statuses: str | None = None,
    work_order_item_id: str | None = None,
    status: str | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Get Testcases"""

    request_args = _build_request_args(
        start_path=start_path,
        test_case_set_ids=test_case_set_ids,
        name=name,
        prompt=prompt,
        mode=mode,
        page=page,
        page_size=page_size,
        simulator_id=simulator_id,
        simulator_name=simulator_name,
        test_case_public_id=test_case_public_id,
        scoring_config_type=scoring_config_type,
        is_assigned=is_assigned,
        is_sample=is_sample,
        rejected=rejected,
        exclude_assigned_to_annotators=exclude_assigned_to_annotators,
        workorder=workorder,
        infeasible=infeasible,
        testcase_statuses=testcase_statuses,
        work_order_item_id=work_order_item_id,
        status=status,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    start_path: str | None = None,
    test_case_set_ids: str | None = None,
    name: str | None = None,
    prompt: str | None = None,
    mode: str | None = None,
    page: int | None = None,
    page_size: int | None = 30,
    simulator_id: int | None = None,
    simulator_name: str | None = None,
    test_case_public_id: str | None = None,
    scoring_config_type: str | None = None,
    is_assigned: bool | None = None,
    is_sample: bool | None = None,
    rejected: bool | None = None,
    exclude_assigned_to_annotators: bool | None = None,
    workorder: str | None = None,
    infeasible: bool | None = None,
    testcase_statuses: str | None = None,
    work_order_item_id: str | None = None,
    status: str | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Get Testcases"""

    request_args = _build_request_args(
        start_path=start_path,
        test_case_set_ids=test_case_set_ids,
        name=name,
        prompt=prompt,
        mode=mode,
        page=page,
        page_size=page_size,
        simulator_id=simulator_id,
        simulator_name=simulator_name,
        test_case_public_id=test_case_public_id,
        scoring_config_type=scoring_config_type,
        is_assigned=is_assigned,
        is_sample=is_sample,
        rejected=rejected,
        exclude_assigned_to_annotators=exclude_assigned_to_annotators,
        workorder=workorder,
        infeasible=infeasible,
        testcase_statuses=testcase_statuses,
        work_order_item_id=work_order_item_id,
        status=status,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
