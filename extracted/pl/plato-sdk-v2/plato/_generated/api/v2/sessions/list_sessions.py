"""List Sessions"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status


def _build_request_args(
    page: int | None = 1,
    page_size: int | None = 50,
    include_public: bool | None = False,
    exclude_unknown_agents: bool | None = False,
    organization_ids: str | None = None,
    agent_artifact_ids: str | None = None,
    simulator_ids: str | None = None,
    simulator_match_mode: str | None = "any",
    statuses: str | None = None,
    test_case_names: str | None = None,
    test_case_ids: str | None = None,
    test_case_public_id: str | None = None,
    score_filter: str | None = "all",
    human_score_filter: str | None = "all",
    days: float | None = None,
    date: str | None = None,
    include_total: bool | None = True,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v2/sessions"

    params: dict[str, Any] = {}
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["page_size"] = page_size
    if include_public is not None:
        params["include_public"] = include_public
    if exclude_unknown_agents is not None:
        params["exclude_unknown_agents"] = exclude_unknown_agents
    if organization_ids is not None:
        params["organization_ids"] = organization_ids
    if agent_artifact_ids is not None:
        params["agent_artifact_ids"] = agent_artifact_ids
    if simulator_ids is not None:
        params["simulator_ids"] = simulator_ids
    if simulator_match_mode is not None:
        params["simulator_match_mode"] = simulator_match_mode
    if statuses is not None:
        params["statuses"] = statuses
    if test_case_names is not None:
        params["test_case_names"] = test_case_names
    if test_case_ids is not None:
        params["test_case_ids"] = test_case_ids
    if test_case_public_id is not None:
        params["test_case_public_id"] = test_case_public_id
    if score_filter is not None:
        params["score_filter"] = score_filter
    if human_score_filter is not None:
        params["human_score_filter"] = human_score_filter
    if days is not None:
        params["days"] = days
    if date is not None:
        params["date"] = date
    if include_total is not None:
        params["include_total"] = include_total

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
    page: int | None = 1,
    page_size: int | None = 50,
    include_public: bool | None = False,
    exclude_unknown_agents: bool | None = False,
    organization_ids: str | None = None,
    agent_artifact_ids: str | None = None,
    simulator_ids: str | None = None,
    simulator_match_mode: str | None = "any",
    statuses: str | None = None,
    test_case_names: str | None = None,
    test_case_ids: str | None = None,
    test_case_public_id: str | None = None,
    score_filter: str | None = "all",
    human_score_filter: str | None = "all",
    days: float | None = None,
    date: str | None = None,
    include_total: bool | None = True,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """List sessions with two-phase query: lean filter for COUNT + paginated IDs,
    then eager-load full objects for the page only.

    When include_total is False, the expensive COUNT query is skipped; ``total`` is
    null, ``total_known`` is False, and ``has_next`` indicates another page exists
    (fetched via limit+1). When include_total is True, ``total`` is a non-negative
    integer and ``total_known`` is True."""

    request_args = _build_request_args(
        page=page,
        page_size=page_size,
        include_public=include_public,
        exclude_unknown_agents=exclude_unknown_agents,
        organization_ids=organization_ids,
        agent_artifact_ids=agent_artifact_ids,
        simulator_ids=simulator_ids,
        simulator_match_mode=simulator_match_mode,
        statuses=statuses,
        test_case_names=test_case_names,
        test_case_ids=test_case_ids,
        test_case_public_id=test_case_public_id,
        score_filter=score_filter,
        human_score_filter=human_score_filter,
        days=days,
        date=date,
        include_total=include_total,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    page: int | None = 1,
    page_size: int | None = 50,
    include_public: bool | None = False,
    exclude_unknown_agents: bool | None = False,
    organization_ids: str | None = None,
    agent_artifact_ids: str | None = None,
    simulator_ids: str | None = None,
    simulator_match_mode: str | None = "any",
    statuses: str | None = None,
    test_case_names: str | None = None,
    test_case_ids: str | None = None,
    test_case_public_id: str | None = None,
    score_filter: str | None = "all",
    human_score_filter: str | None = "all",
    days: float | None = None,
    date: str | None = None,
    include_total: bool | None = True,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """List sessions with two-phase query: lean filter for COUNT + paginated IDs,
    then eager-load full objects for the page only.

    When include_total is False, the expensive COUNT query is skipped; ``total`` is
    null, ``total_known`` is False, and ``has_next`` indicates another page exists
    (fetched via limit+1). When include_total is True, ``total`` is a non-negative
    integer and ``total_known`` is True."""

    request_args = _build_request_args(
        page=page,
        page_size=page_size,
        include_public=include_public,
        exclude_unknown_agents=exclude_unknown_agents,
        organization_ids=organization_ids,
        agent_artifact_ids=agent_artifact_ids,
        simulator_ids=simulator_ids,
        simulator_match_mode=simulator_match_mode,
        statuses=statuses,
        test_case_names=test_case_names,
        test_case_ids=test_case_ids,
        test_case_public_id=test_case_public_id,
        score_filter=score_filter,
        human_score_filter=human_score_filter,
        days=days,
        date=date,
        include_total=include_total,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
