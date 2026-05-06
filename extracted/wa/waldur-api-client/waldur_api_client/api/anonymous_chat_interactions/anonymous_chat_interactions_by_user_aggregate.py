import datetime
from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.anonymous_chat_interaction_o_enum import AnonymousChatInteractionOEnum
from ...models.anonymous_chat_user_aggregate import AnonymousChatUserAggregate
from ...models.injection_severity_enum import InjectionSeverityEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    created_from: Union[Unset, datetime.date] = UNSET,
    created_to: Union[Unset, datetime.date] = UNSET,
    has_negative_feedback: Union[Unset, bool] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[AnonymousChatInteractionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    session_id: Union[Unset, str] = UNSET,
    severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_created_from: Union[Unset, str] = UNSET
    if not isinstance(created_from, Unset):
        json_created_from = created_from.isoformat()
    params["created_from"] = json_created_from

    json_created_to: Union[Unset, str] = UNSET
    if not isinstance(created_to, Unset):
        json_created_to = created_to.isoformat()
    params["created_to"] = json_created_to

    params["has_negative_feedback"] = has_negative_feedback

    params["is_flagged"] = is_flagged

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["page"] = page

    params["page_size"] = page_size

    params["session_id"] = session_id

    json_severity: Union[Unset, str] = UNSET
    if not isinstance(severity, Unset):
        json_severity = severity.value

    params["severity"] = json_severity

    params["user_slug"] = user_slug

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/anonymous-chat-interactions/by-user/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["AnonymousChatUserAggregate"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = AnonymousChatUserAggregate.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["AnonymousChatUserAggregate"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    created_from: Union[Unset, datetime.date] = UNSET,
    created_to: Union[Unset, datetime.date] = UNSET,
    has_negative_feedback: Union[Unset, bool] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[AnonymousChatInteractionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    session_id: Union[Unset, str] = UNSET,
    severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
) -> Response[list["AnonymousChatUserAggregate"]]:
    """Aggregate user list (no slug)

     Returns one row per user_slug with aggregate counters. Powers the staff Users page in the admin
    analytics.

    Args:
        created_from (Union[Unset, datetime.date]):
        created_to (Union[Unset, datetime.date]):
        has_negative_feedback (Union[Unset, bool]):
        is_flagged (Union[Unset, bool]):
        o (Union[Unset, list[AnonymousChatInteractionOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        session_id (Union[Unset, str]):
        severity (Union[Unset, InjectionSeverityEnum]):
        user_slug (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AnonymousChatUserAggregate']]
    """

    kwargs = _get_kwargs(
        created_from=created_from,
        created_to=created_to,
        has_negative_feedback=has_negative_feedback,
        is_flagged=is_flagged,
        o=o,
        page=page,
        page_size=page_size,
        session_id=session_id,
        severity=severity,
        user_slug=user_slug,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    created_from: Union[Unset, datetime.date] = UNSET,
    created_to: Union[Unset, datetime.date] = UNSET,
    has_negative_feedback: Union[Unset, bool] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[AnonymousChatInteractionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    session_id: Union[Unset, str] = UNSET,
    severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
) -> list["AnonymousChatUserAggregate"]:
    """Aggregate user list (no slug)

     Returns one row per user_slug with aggregate counters. Powers the staff Users page in the admin
    analytics.

    Args:
        created_from (Union[Unset, datetime.date]):
        created_to (Union[Unset, datetime.date]):
        has_negative_feedback (Union[Unset, bool]):
        is_flagged (Union[Unset, bool]):
        o (Union[Unset, list[AnonymousChatInteractionOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        session_id (Union[Unset, str]):
        severity (Union[Unset, InjectionSeverityEnum]):
        user_slug (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AnonymousChatUserAggregate']
    """

    return sync_detailed(
        client=client,
        created_from=created_from,
        created_to=created_to,
        has_negative_feedback=has_negative_feedback,
        is_flagged=is_flagged,
        o=o,
        page=page,
        page_size=page_size,
        session_id=session_id,
        severity=severity,
        user_slug=user_slug,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    created_from: Union[Unset, datetime.date] = UNSET,
    created_to: Union[Unset, datetime.date] = UNSET,
    has_negative_feedback: Union[Unset, bool] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[AnonymousChatInteractionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    session_id: Union[Unset, str] = UNSET,
    severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
) -> Response[list["AnonymousChatUserAggregate"]]:
    """Aggregate user list (no slug)

     Returns one row per user_slug with aggregate counters. Powers the staff Users page in the admin
    analytics.

    Args:
        created_from (Union[Unset, datetime.date]):
        created_to (Union[Unset, datetime.date]):
        has_negative_feedback (Union[Unset, bool]):
        is_flagged (Union[Unset, bool]):
        o (Union[Unset, list[AnonymousChatInteractionOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        session_id (Union[Unset, str]):
        severity (Union[Unset, InjectionSeverityEnum]):
        user_slug (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AnonymousChatUserAggregate']]
    """

    kwargs = _get_kwargs(
        created_from=created_from,
        created_to=created_to,
        has_negative_feedback=has_negative_feedback,
        is_flagged=is_flagged,
        o=o,
        page=page,
        page_size=page_size,
        session_id=session_id,
        severity=severity,
        user_slug=user_slug,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    created_from: Union[Unset, datetime.date] = UNSET,
    created_to: Union[Unset, datetime.date] = UNSET,
    has_negative_feedback: Union[Unset, bool] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[AnonymousChatInteractionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    session_id: Union[Unset, str] = UNSET,
    severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
) -> list["AnonymousChatUserAggregate"]:
    """Aggregate user list (no slug)

     Returns one row per user_slug with aggregate counters. Powers the staff Users page in the admin
    analytics.

    Args:
        created_from (Union[Unset, datetime.date]):
        created_to (Union[Unset, datetime.date]):
        has_negative_feedback (Union[Unset, bool]):
        is_flagged (Union[Unset, bool]):
        o (Union[Unset, list[AnonymousChatInteractionOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        session_id (Union[Unset, str]):
        severity (Union[Unset, InjectionSeverityEnum]):
        user_slug (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AnonymousChatUserAggregate']
    """

    return (
        await asyncio_detailed(
            client=client,
            created_from=created_from,
            created_to=created_to,
            has_negative_feedback=has_negative_feedback,
            is_flagged=is_flagged,
            o=o,
            page=page,
            page_size=page_size,
            session_id=session_id,
            severity=severity,
            user_slug=user_slug,
        )
    ).parsed
