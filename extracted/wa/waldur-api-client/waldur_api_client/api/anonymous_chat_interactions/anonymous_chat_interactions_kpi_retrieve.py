import datetime
from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.anonymous_chat_interaction_o_enum import AnonymousChatInteractionOEnum
from ...models.anonymous_chat_kpi_response import AnonymousChatKpiResponse
from ...models.injection_severity_enum import InjectionSeverityEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    created_after: Union[Unset, datetime.date] = UNSET,
    created_before: Union[Unset, datetime.date] = UNSET,
    has_feedback: Union[Unset, bool] = UNSET,
    input_tokens_max: Union[Unset, float] = UNSET,
    input_tokens_min: Union[Unset, float] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    is_reviewed: Union[Unset, bool] = UNSET,
    last_active_after: Union[Unset, datetime.date] = UNSET,
    last_active_before: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[AnonymousChatInteractionOEnum]] = UNSET,
    output_tokens_max: Union[Unset, float] = UNSET,
    output_tokens_min: Union[Unset, float] = UNSET,
    query: Union[Unset, str] = UNSET,
    session_id: Union[Unset, str] = UNSET,
    severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    total_tokens_max: Union[Unset, float] = UNSET,
    total_tokens_min: Union[Unset, float] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_created_after: Union[Unset, str] = UNSET
    if not isinstance(created_after, Unset):
        json_created_after = created_after.isoformat()
    params["created_after"] = json_created_after

    json_created_before: Union[Unset, str] = UNSET
    if not isinstance(created_before, Unset):
        json_created_before = created_before.isoformat()
    params["created_before"] = json_created_before

    params["has_feedback"] = has_feedback

    params["input_tokens_max"] = input_tokens_max

    params["input_tokens_min"] = input_tokens_min

    params["is_flagged"] = is_flagged

    params["is_reviewed"] = is_reviewed

    json_last_active_after: Union[Unset, str] = UNSET
    if not isinstance(last_active_after, Unset):
        json_last_active_after = last_active_after.isoformat()
    params["last_active_after"] = json_last_active_after

    json_last_active_before: Union[Unset, str] = UNSET
    if not isinstance(last_active_before, Unset):
        json_last_active_before = last_active_before.isoformat()
    params["last_active_before"] = json_last_active_before

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["output_tokens_max"] = output_tokens_max

    params["output_tokens_min"] = output_tokens_min

    params["query"] = query

    params["session_id"] = session_id

    json_severity: Union[Unset, str] = UNSET
    if not isinstance(severity, Unset):
        json_severity = severity.value

    params["severity"] = json_severity

    params["total_tokens_max"] = total_tokens_max

    params["total_tokens_min"] = total_tokens_min

    params["user_slug"] = user_slug

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/anonymous-chat-interactions/kpi/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> AnonymousChatKpiResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = AnonymousChatKpiResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[AnonymousChatKpiResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    created_after: Union[Unset, datetime.date] = UNSET,
    created_before: Union[Unset, datetime.date] = UNSET,
    has_feedback: Union[Unset, bool] = UNSET,
    input_tokens_max: Union[Unset, float] = UNSET,
    input_tokens_min: Union[Unset, float] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    is_reviewed: Union[Unset, bool] = UNSET,
    last_active_after: Union[Unset, datetime.date] = UNSET,
    last_active_before: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[AnonymousChatInteractionOEnum]] = UNSET,
    output_tokens_max: Union[Unset, float] = UNSET,
    output_tokens_min: Union[Unset, float] = UNSET,
    query: Union[Unset, str] = UNSET,
    session_id: Union[Unset, str] = UNSET,
    severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    total_tokens_max: Union[Unset, float] = UNSET,
    total_tokens_min: Union[Unset, float] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
) -> Response[AnonymousChatKpiResponse]:
    """Aggregate KPI roll-up

     Returns aggregate counters and rates for the anonymous chat flow. Filters are honoured (date range
    etc.) so the same parameters work as on the list endpoint.

    Args:
        created_after (Union[Unset, datetime.date]):
        created_before (Union[Unset, datetime.date]):
        has_feedback (Union[Unset, bool]):
        input_tokens_max (Union[Unset, float]):
        input_tokens_min (Union[Unset, float]):
        is_flagged (Union[Unset, bool]):
        is_reviewed (Union[Unset, bool]):
        last_active_after (Union[Unset, datetime.date]):
        last_active_before (Union[Unset, datetime.date]):
        o (Union[Unset, list[AnonymousChatInteractionOEnum]]):
        output_tokens_max (Union[Unset, float]):
        output_tokens_min (Union[Unset, float]):
        query (Union[Unset, str]):
        session_id (Union[Unset, str]):
        severity (Union[Unset, InjectionSeverityEnum]):
        total_tokens_max (Union[Unset, float]):
        total_tokens_min (Union[Unset, float]):
        user_slug (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AnonymousChatKpiResponse]
    """

    kwargs = _get_kwargs(
        created_after=created_after,
        created_before=created_before,
        has_feedback=has_feedback,
        input_tokens_max=input_tokens_max,
        input_tokens_min=input_tokens_min,
        is_flagged=is_flagged,
        is_reviewed=is_reviewed,
        last_active_after=last_active_after,
        last_active_before=last_active_before,
        o=o,
        output_tokens_max=output_tokens_max,
        output_tokens_min=output_tokens_min,
        query=query,
        session_id=session_id,
        severity=severity,
        total_tokens_max=total_tokens_max,
        total_tokens_min=total_tokens_min,
        user_slug=user_slug,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    created_after: Union[Unset, datetime.date] = UNSET,
    created_before: Union[Unset, datetime.date] = UNSET,
    has_feedback: Union[Unset, bool] = UNSET,
    input_tokens_max: Union[Unset, float] = UNSET,
    input_tokens_min: Union[Unset, float] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    is_reviewed: Union[Unset, bool] = UNSET,
    last_active_after: Union[Unset, datetime.date] = UNSET,
    last_active_before: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[AnonymousChatInteractionOEnum]] = UNSET,
    output_tokens_max: Union[Unset, float] = UNSET,
    output_tokens_min: Union[Unset, float] = UNSET,
    query: Union[Unset, str] = UNSET,
    session_id: Union[Unset, str] = UNSET,
    severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    total_tokens_max: Union[Unset, float] = UNSET,
    total_tokens_min: Union[Unset, float] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
) -> AnonymousChatKpiResponse:
    """Aggregate KPI roll-up

     Returns aggregate counters and rates for the anonymous chat flow. Filters are honoured (date range
    etc.) so the same parameters work as on the list endpoint.

    Args:
        created_after (Union[Unset, datetime.date]):
        created_before (Union[Unset, datetime.date]):
        has_feedback (Union[Unset, bool]):
        input_tokens_max (Union[Unset, float]):
        input_tokens_min (Union[Unset, float]):
        is_flagged (Union[Unset, bool]):
        is_reviewed (Union[Unset, bool]):
        last_active_after (Union[Unset, datetime.date]):
        last_active_before (Union[Unset, datetime.date]):
        o (Union[Unset, list[AnonymousChatInteractionOEnum]]):
        output_tokens_max (Union[Unset, float]):
        output_tokens_min (Union[Unset, float]):
        query (Union[Unset, str]):
        session_id (Union[Unset, str]):
        severity (Union[Unset, InjectionSeverityEnum]):
        total_tokens_max (Union[Unset, float]):
        total_tokens_min (Union[Unset, float]):
        user_slug (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AnonymousChatKpiResponse
    """

    return sync_detailed(
        client=client,
        created_after=created_after,
        created_before=created_before,
        has_feedback=has_feedback,
        input_tokens_max=input_tokens_max,
        input_tokens_min=input_tokens_min,
        is_flagged=is_flagged,
        is_reviewed=is_reviewed,
        last_active_after=last_active_after,
        last_active_before=last_active_before,
        o=o,
        output_tokens_max=output_tokens_max,
        output_tokens_min=output_tokens_min,
        query=query,
        session_id=session_id,
        severity=severity,
        total_tokens_max=total_tokens_max,
        total_tokens_min=total_tokens_min,
        user_slug=user_slug,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    created_after: Union[Unset, datetime.date] = UNSET,
    created_before: Union[Unset, datetime.date] = UNSET,
    has_feedback: Union[Unset, bool] = UNSET,
    input_tokens_max: Union[Unset, float] = UNSET,
    input_tokens_min: Union[Unset, float] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    is_reviewed: Union[Unset, bool] = UNSET,
    last_active_after: Union[Unset, datetime.date] = UNSET,
    last_active_before: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[AnonymousChatInteractionOEnum]] = UNSET,
    output_tokens_max: Union[Unset, float] = UNSET,
    output_tokens_min: Union[Unset, float] = UNSET,
    query: Union[Unset, str] = UNSET,
    session_id: Union[Unset, str] = UNSET,
    severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    total_tokens_max: Union[Unset, float] = UNSET,
    total_tokens_min: Union[Unset, float] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
) -> Response[AnonymousChatKpiResponse]:
    """Aggregate KPI roll-up

     Returns aggregate counters and rates for the anonymous chat flow. Filters are honoured (date range
    etc.) so the same parameters work as on the list endpoint.

    Args:
        created_after (Union[Unset, datetime.date]):
        created_before (Union[Unset, datetime.date]):
        has_feedback (Union[Unset, bool]):
        input_tokens_max (Union[Unset, float]):
        input_tokens_min (Union[Unset, float]):
        is_flagged (Union[Unset, bool]):
        is_reviewed (Union[Unset, bool]):
        last_active_after (Union[Unset, datetime.date]):
        last_active_before (Union[Unset, datetime.date]):
        o (Union[Unset, list[AnonymousChatInteractionOEnum]]):
        output_tokens_max (Union[Unset, float]):
        output_tokens_min (Union[Unset, float]):
        query (Union[Unset, str]):
        session_id (Union[Unset, str]):
        severity (Union[Unset, InjectionSeverityEnum]):
        total_tokens_max (Union[Unset, float]):
        total_tokens_min (Union[Unset, float]):
        user_slug (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AnonymousChatKpiResponse]
    """

    kwargs = _get_kwargs(
        created_after=created_after,
        created_before=created_before,
        has_feedback=has_feedback,
        input_tokens_max=input_tokens_max,
        input_tokens_min=input_tokens_min,
        is_flagged=is_flagged,
        is_reviewed=is_reviewed,
        last_active_after=last_active_after,
        last_active_before=last_active_before,
        o=o,
        output_tokens_max=output_tokens_max,
        output_tokens_min=output_tokens_min,
        query=query,
        session_id=session_id,
        severity=severity,
        total_tokens_max=total_tokens_max,
        total_tokens_min=total_tokens_min,
        user_slug=user_slug,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    created_after: Union[Unset, datetime.date] = UNSET,
    created_before: Union[Unset, datetime.date] = UNSET,
    has_feedback: Union[Unset, bool] = UNSET,
    input_tokens_max: Union[Unset, float] = UNSET,
    input_tokens_min: Union[Unset, float] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    is_reviewed: Union[Unset, bool] = UNSET,
    last_active_after: Union[Unset, datetime.date] = UNSET,
    last_active_before: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[AnonymousChatInteractionOEnum]] = UNSET,
    output_tokens_max: Union[Unset, float] = UNSET,
    output_tokens_min: Union[Unset, float] = UNSET,
    query: Union[Unset, str] = UNSET,
    session_id: Union[Unset, str] = UNSET,
    severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    total_tokens_max: Union[Unset, float] = UNSET,
    total_tokens_min: Union[Unset, float] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
) -> AnonymousChatKpiResponse:
    """Aggregate KPI roll-up

     Returns aggregate counters and rates for the anonymous chat flow. Filters are honoured (date range
    etc.) so the same parameters work as on the list endpoint.

    Args:
        created_after (Union[Unset, datetime.date]):
        created_before (Union[Unset, datetime.date]):
        has_feedback (Union[Unset, bool]):
        input_tokens_max (Union[Unset, float]):
        input_tokens_min (Union[Unset, float]):
        is_flagged (Union[Unset, bool]):
        is_reviewed (Union[Unset, bool]):
        last_active_after (Union[Unset, datetime.date]):
        last_active_before (Union[Unset, datetime.date]):
        o (Union[Unset, list[AnonymousChatInteractionOEnum]]):
        output_tokens_max (Union[Unset, float]):
        output_tokens_min (Union[Unset, float]):
        query (Union[Unset, str]):
        session_id (Union[Unset, str]):
        severity (Union[Unset, InjectionSeverityEnum]):
        total_tokens_max (Union[Unset, float]):
        total_tokens_min (Union[Unset, float]):
        user_slug (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AnonymousChatKpiResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            created_after=created_after,
            created_before=created_before,
            has_feedback=has_feedback,
            input_tokens_max=input_tokens_max,
            input_tokens_min=input_tokens_min,
            is_flagged=is_flagged,
            is_reviewed=is_reviewed,
            last_active_after=last_active_after,
            last_active_before=last_active_before,
            o=o,
            output_tokens_max=output_tokens_max,
            output_tokens_min=output_tokens_min,
            query=query,
            session_id=session_id,
            severity=severity,
            total_tokens_max=total_tokens_max,
            total_tokens_min=total_tokens_min,
            user_slug=user_slug,
        )
    ).parsed
