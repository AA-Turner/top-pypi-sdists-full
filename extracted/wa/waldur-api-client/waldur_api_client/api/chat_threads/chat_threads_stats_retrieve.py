import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.chat_thread_stats_response import ChatThreadStatsResponse
from ...models.injection_severity_enum import InjectionSeverityEnum
from ...models.thread_session_o_enum import ThreadSessionOEnum
from ...models.thread_session_scope_enum import ThreadSessionScopeEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    created_after: Union[Unset, datetime.date] = UNSET,
    created_before: Union[Unset, datetime.date] = UNSET,
    has_feedback: Union[Unset, bool] = UNSET,
    input_tokens_max: Union[Unset, float] = UNSET,
    input_tokens_min: Union[Unset, float] = UNSET,
    is_archived: Union[Unset, bool] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    max_severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    modified_after: Union[Unset, datetime.date] = UNSET,
    modified_before: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[ThreadSessionOEnum]] = UNSET,
    output_tokens_max: Union[Unset, float] = UNSET,
    output_tokens_min: Union[Unset, float] = UNSET,
    query: Union[Unset, str] = UNSET,
    scope: Union[Unset, ThreadSessionScopeEnum] = UNSET,
    total_tokens_max: Union[Unset, float] = UNSET,
    total_tokens_min: Union[Unset, float] = UNSET,
    user: Union[Unset, UUID] = UNSET,
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

    params["is_archived"] = is_archived

    params["is_flagged"] = is_flagged

    json_max_severity: Union[Unset, str] = UNSET
    if not isinstance(max_severity, Unset):
        json_max_severity = max_severity.value

    params["max_severity"] = json_max_severity

    json_modified_after: Union[Unset, str] = UNSET
    if not isinstance(modified_after, Unset):
        json_modified_after = modified_after.isoformat()
    params["modified_after"] = json_modified_after

    json_modified_before: Union[Unset, str] = UNSET
    if not isinstance(modified_before, Unset):
        json_modified_before = modified_before.isoformat()
    params["modified_before"] = json_modified_before

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

    json_scope: Union[Unset, str] = UNSET
    if not isinstance(scope, Unset):
        json_scope = scope.value

    params["scope"] = json_scope

    params["total_tokens_max"] = total_tokens_max

    params["total_tokens_min"] = total_tokens_min

    json_user: Union[Unset, str] = UNSET
    if not isinstance(user, Unset):
        json_user = str(user)
    params["user"] = json_user

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/chat-threads/stats/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ChatThreadStatsResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ChatThreadStatsResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ChatThreadStatsResponse]:
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
    is_archived: Union[Unset, bool] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    max_severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    modified_after: Union[Unset, datetime.date] = UNSET,
    modified_before: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[ThreadSessionOEnum]] = UNSET,
    output_tokens_max: Union[Unset, float] = UNSET,
    output_tokens_min: Union[Unset, float] = UNSET,
    query: Union[Unset, str] = UNSET,
    scope: Union[Unset, ThreadSessionScopeEnum] = UNSET,
    total_tokens_max: Union[Unset, float] = UNSET,
    total_tokens_min: Union[Unset, float] = UNSET,
    user: Union[Unset, UUID] = UNSET,
) -> Response[ChatThreadStatsResponse]:
    """Get statistics for visible chat threads

     Summary statistics for the visible chat threads.

    Filters run against the annotated list queryset, then the matched
    threads are re-read as a plain queryset. Both halves are load-bearing:
    ``has_feedback`` and the token ranges resolve against annotations that
    exist only on ``get_queryset``, while the per-row annotations there
    would collide with the aggregates below. Visibility comes from
    ``get_queryset`` — staff/support see all, other users only their own.

    Args:
        created_after (Union[Unset, datetime.date]):
        created_before (Union[Unset, datetime.date]):
        has_feedback (Union[Unset, bool]):
        input_tokens_max (Union[Unset, float]):
        input_tokens_min (Union[Unset, float]):
        is_archived (Union[Unset, bool]):
        is_flagged (Union[Unset, bool]):
        max_severity (Union[Unset, InjectionSeverityEnum]):
        modified_after (Union[Unset, datetime.date]):
        modified_before (Union[Unset, datetime.date]):
        o (Union[Unset, list[ThreadSessionOEnum]]):
        output_tokens_max (Union[Unset, float]):
        output_tokens_min (Union[Unset, float]):
        query (Union[Unset, str]):
        scope (Union[Unset, ThreadSessionScopeEnum]):
        total_tokens_max (Union[Unset, float]):
        total_tokens_min (Union[Unset, float]):
        user (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ChatThreadStatsResponse]
    """

    kwargs = _get_kwargs(
        created_after=created_after,
        created_before=created_before,
        has_feedback=has_feedback,
        input_tokens_max=input_tokens_max,
        input_tokens_min=input_tokens_min,
        is_archived=is_archived,
        is_flagged=is_flagged,
        max_severity=max_severity,
        modified_after=modified_after,
        modified_before=modified_before,
        o=o,
        output_tokens_max=output_tokens_max,
        output_tokens_min=output_tokens_min,
        query=query,
        scope=scope,
        total_tokens_max=total_tokens_max,
        total_tokens_min=total_tokens_min,
        user=user,
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
    is_archived: Union[Unset, bool] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    max_severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    modified_after: Union[Unset, datetime.date] = UNSET,
    modified_before: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[ThreadSessionOEnum]] = UNSET,
    output_tokens_max: Union[Unset, float] = UNSET,
    output_tokens_min: Union[Unset, float] = UNSET,
    query: Union[Unset, str] = UNSET,
    scope: Union[Unset, ThreadSessionScopeEnum] = UNSET,
    total_tokens_max: Union[Unset, float] = UNSET,
    total_tokens_min: Union[Unset, float] = UNSET,
    user: Union[Unset, UUID] = UNSET,
) -> ChatThreadStatsResponse:
    """Get statistics for visible chat threads

     Summary statistics for the visible chat threads.

    Filters run against the annotated list queryset, then the matched
    threads are re-read as a plain queryset. Both halves are load-bearing:
    ``has_feedback`` and the token ranges resolve against annotations that
    exist only on ``get_queryset``, while the per-row annotations there
    would collide with the aggregates below. Visibility comes from
    ``get_queryset`` — staff/support see all, other users only their own.

    Args:
        created_after (Union[Unset, datetime.date]):
        created_before (Union[Unset, datetime.date]):
        has_feedback (Union[Unset, bool]):
        input_tokens_max (Union[Unset, float]):
        input_tokens_min (Union[Unset, float]):
        is_archived (Union[Unset, bool]):
        is_flagged (Union[Unset, bool]):
        max_severity (Union[Unset, InjectionSeverityEnum]):
        modified_after (Union[Unset, datetime.date]):
        modified_before (Union[Unset, datetime.date]):
        o (Union[Unset, list[ThreadSessionOEnum]]):
        output_tokens_max (Union[Unset, float]):
        output_tokens_min (Union[Unset, float]):
        query (Union[Unset, str]):
        scope (Union[Unset, ThreadSessionScopeEnum]):
        total_tokens_max (Union[Unset, float]):
        total_tokens_min (Union[Unset, float]):
        user (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ChatThreadStatsResponse
    """

    return sync_detailed(
        client=client,
        created_after=created_after,
        created_before=created_before,
        has_feedback=has_feedback,
        input_tokens_max=input_tokens_max,
        input_tokens_min=input_tokens_min,
        is_archived=is_archived,
        is_flagged=is_flagged,
        max_severity=max_severity,
        modified_after=modified_after,
        modified_before=modified_before,
        o=o,
        output_tokens_max=output_tokens_max,
        output_tokens_min=output_tokens_min,
        query=query,
        scope=scope,
        total_tokens_max=total_tokens_max,
        total_tokens_min=total_tokens_min,
        user=user,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    created_after: Union[Unset, datetime.date] = UNSET,
    created_before: Union[Unset, datetime.date] = UNSET,
    has_feedback: Union[Unset, bool] = UNSET,
    input_tokens_max: Union[Unset, float] = UNSET,
    input_tokens_min: Union[Unset, float] = UNSET,
    is_archived: Union[Unset, bool] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    max_severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    modified_after: Union[Unset, datetime.date] = UNSET,
    modified_before: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[ThreadSessionOEnum]] = UNSET,
    output_tokens_max: Union[Unset, float] = UNSET,
    output_tokens_min: Union[Unset, float] = UNSET,
    query: Union[Unset, str] = UNSET,
    scope: Union[Unset, ThreadSessionScopeEnum] = UNSET,
    total_tokens_max: Union[Unset, float] = UNSET,
    total_tokens_min: Union[Unset, float] = UNSET,
    user: Union[Unset, UUID] = UNSET,
) -> Response[ChatThreadStatsResponse]:
    """Get statistics for visible chat threads

     Summary statistics for the visible chat threads.

    Filters run against the annotated list queryset, then the matched
    threads are re-read as a plain queryset. Both halves are load-bearing:
    ``has_feedback`` and the token ranges resolve against annotations that
    exist only on ``get_queryset``, while the per-row annotations there
    would collide with the aggregates below. Visibility comes from
    ``get_queryset`` — staff/support see all, other users only their own.

    Args:
        created_after (Union[Unset, datetime.date]):
        created_before (Union[Unset, datetime.date]):
        has_feedback (Union[Unset, bool]):
        input_tokens_max (Union[Unset, float]):
        input_tokens_min (Union[Unset, float]):
        is_archived (Union[Unset, bool]):
        is_flagged (Union[Unset, bool]):
        max_severity (Union[Unset, InjectionSeverityEnum]):
        modified_after (Union[Unset, datetime.date]):
        modified_before (Union[Unset, datetime.date]):
        o (Union[Unset, list[ThreadSessionOEnum]]):
        output_tokens_max (Union[Unset, float]):
        output_tokens_min (Union[Unset, float]):
        query (Union[Unset, str]):
        scope (Union[Unset, ThreadSessionScopeEnum]):
        total_tokens_max (Union[Unset, float]):
        total_tokens_min (Union[Unset, float]):
        user (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ChatThreadStatsResponse]
    """

    kwargs = _get_kwargs(
        created_after=created_after,
        created_before=created_before,
        has_feedback=has_feedback,
        input_tokens_max=input_tokens_max,
        input_tokens_min=input_tokens_min,
        is_archived=is_archived,
        is_flagged=is_flagged,
        max_severity=max_severity,
        modified_after=modified_after,
        modified_before=modified_before,
        o=o,
        output_tokens_max=output_tokens_max,
        output_tokens_min=output_tokens_min,
        query=query,
        scope=scope,
        total_tokens_max=total_tokens_max,
        total_tokens_min=total_tokens_min,
        user=user,
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
    is_archived: Union[Unset, bool] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    max_severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    modified_after: Union[Unset, datetime.date] = UNSET,
    modified_before: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[ThreadSessionOEnum]] = UNSET,
    output_tokens_max: Union[Unset, float] = UNSET,
    output_tokens_min: Union[Unset, float] = UNSET,
    query: Union[Unset, str] = UNSET,
    scope: Union[Unset, ThreadSessionScopeEnum] = UNSET,
    total_tokens_max: Union[Unset, float] = UNSET,
    total_tokens_min: Union[Unset, float] = UNSET,
    user: Union[Unset, UUID] = UNSET,
) -> ChatThreadStatsResponse:
    """Get statistics for visible chat threads

     Summary statistics for the visible chat threads.

    Filters run against the annotated list queryset, then the matched
    threads are re-read as a plain queryset. Both halves are load-bearing:
    ``has_feedback`` and the token ranges resolve against annotations that
    exist only on ``get_queryset``, while the per-row annotations there
    would collide with the aggregates below. Visibility comes from
    ``get_queryset`` — staff/support see all, other users only their own.

    Args:
        created_after (Union[Unset, datetime.date]):
        created_before (Union[Unset, datetime.date]):
        has_feedback (Union[Unset, bool]):
        input_tokens_max (Union[Unset, float]):
        input_tokens_min (Union[Unset, float]):
        is_archived (Union[Unset, bool]):
        is_flagged (Union[Unset, bool]):
        max_severity (Union[Unset, InjectionSeverityEnum]):
        modified_after (Union[Unset, datetime.date]):
        modified_before (Union[Unset, datetime.date]):
        o (Union[Unset, list[ThreadSessionOEnum]]):
        output_tokens_max (Union[Unset, float]):
        output_tokens_min (Union[Unset, float]):
        query (Union[Unset, str]):
        scope (Union[Unset, ThreadSessionScopeEnum]):
        total_tokens_max (Union[Unset, float]):
        total_tokens_min (Union[Unset, float]):
        user (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ChatThreadStatsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            created_after=created_after,
            created_before=created_before,
            has_feedback=has_feedback,
            input_tokens_max=input_tokens_max,
            input_tokens_min=input_tokens_min,
            is_archived=is_archived,
            is_flagged=is_flagged,
            max_severity=max_severity,
            modified_after=modified_after,
            modified_before=modified_before,
            o=o,
            output_tokens_max=output_tokens_max,
            output_tokens_min=output_tokens_min,
            query=query,
            scope=scope,
            total_tokens_max=total_tokens_max,
            total_tokens_min=total_tokens_min,
            user=user,
        )
    ).parsed
