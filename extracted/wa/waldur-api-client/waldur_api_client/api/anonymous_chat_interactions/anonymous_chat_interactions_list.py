import datetime
from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.anonymous_chat_interaction import AnonymousChatInteraction
from ...models.anonymous_chat_interaction_o_enum import AnonymousChatInteractionOEnum
from ...models.injection_severity_enum import InjectionSeverityEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    created_after: Union[Unset, datetime.date] = UNSET,
    created_before: Union[Unset, datetime.date] = UNSET,
    has_feedback: Union[Unset, bool] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[AnonymousChatInteractionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    session_id: Union[Unset, str] = UNSET,
    severity: Union[Unset, InjectionSeverityEnum] = UNSET,
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

    params["query"] = query

    params["session_id"] = session_id

    json_severity: Union[Unset, str] = UNSET
    if not isinstance(severity, Unset):
        json_severity = severity.value

    params["severity"] = json_severity

    params["user_slug"] = user_slug

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/anonymous-chat-interactions/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["AnonymousChatInteraction"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = AnonymousChatInteraction.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["AnonymousChatInteraction"]]:
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
    is_flagged: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[AnonymousChatInteractionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    session_id: Union[Unset, str] = UNSET,
    severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
) -> Response[list["AnonymousChatInteraction"]]:
    """
    Args:
        created_after (Union[Unset, datetime.date]):
        created_before (Union[Unset, datetime.date]):
        has_feedback (Union[Unset, bool]):
        is_flagged (Union[Unset, bool]):
        o (Union[Unset, list[AnonymousChatInteractionOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        session_id (Union[Unset, str]):
        severity (Union[Unset, InjectionSeverityEnum]):
        user_slug (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AnonymousChatInteraction']]
    """

    kwargs = _get_kwargs(
        created_after=created_after,
        created_before=created_before,
        has_feedback=has_feedback,
        is_flagged=is_flagged,
        o=o,
        page=page,
        page_size=page_size,
        query=query,
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
    created_after: Union[Unset, datetime.date] = UNSET,
    created_before: Union[Unset, datetime.date] = UNSET,
    has_feedback: Union[Unset, bool] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[AnonymousChatInteractionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    session_id: Union[Unset, str] = UNSET,
    severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
) -> list["AnonymousChatInteraction"]:
    """
    Args:
        created_after (Union[Unset, datetime.date]):
        created_before (Union[Unset, datetime.date]):
        has_feedback (Union[Unset, bool]):
        is_flagged (Union[Unset, bool]):
        o (Union[Unset, list[AnonymousChatInteractionOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        session_id (Union[Unset, str]):
        severity (Union[Unset, InjectionSeverityEnum]):
        user_slug (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AnonymousChatInteraction']
    """

    return sync_detailed(
        client=client,
        created_after=created_after,
        created_before=created_before,
        has_feedback=has_feedback,
        is_flagged=is_flagged,
        o=o,
        page=page,
        page_size=page_size,
        query=query,
        session_id=session_id,
        severity=severity,
        user_slug=user_slug,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    created_after: Union[Unset, datetime.date] = UNSET,
    created_before: Union[Unset, datetime.date] = UNSET,
    has_feedback: Union[Unset, bool] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[AnonymousChatInteractionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    session_id: Union[Unset, str] = UNSET,
    severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
) -> Response[list["AnonymousChatInteraction"]]:
    """
    Args:
        created_after (Union[Unset, datetime.date]):
        created_before (Union[Unset, datetime.date]):
        has_feedback (Union[Unset, bool]):
        is_flagged (Union[Unset, bool]):
        o (Union[Unset, list[AnonymousChatInteractionOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        session_id (Union[Unset, str]):
        severity (Union[Unset, InjectionSeverityEnum]):
        user_slug (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AnonymousChatInteraction']]
    """

    kwargs = _get_kwargs(
        created_after=created_after,
        created_before=created_before,
        has_feedback=has_feedback,
        is_flagged=is_flagged,
        o=o,
        page=page,
        page_size=page_size,
        query=query,
        session_id=session_id,
        severity=severity,
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
    is_flagged: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[AnonymousChatInteractionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    session_id: Union[Unset, str] = UNSET,
    severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
) -> list["AnonymousChatInteraction"]:
    """
    Args:
        created_after (Union[Unset, datetime.date]):
        created_before (Union[Unset, datetime.date]):
        has_feedback (Union[Unset, bool]):
        is_flagged (Union[Unset, bool]):
        o (Union[Unset, list[AnonymousChatInteractionOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        session_id (Union[Unset, str]):
        severity (Union[Unset, InjectionSeverityEnum]):
        user_slug (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AnonymousChatInteraction']
    """

    return (
        await asyncio_detailed(
            client=client,
            created_after=created_after,
            created_before=created_before,
            has_feedback=has_feedback,
            is_flagged=is_flagged,
            o=o,
            page=page,
            page_size=page_size,
            query=query,
            session_id=session_id,
            severity=severity,
            user_slug=user_slug,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    created_after: Union[Unset, datetime.date] = UNSET,
    created_before: Union[Unset, datetime.date] = UNSET,
    has_feedback: Union[Unset, bool] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[AnonymousChatInteractionOEnum]] = UNSET,
    query: Union[Unset, str] = UNSET,
    session_id: Union[Unset, str] = UNSET,
    severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
) -> list["AnonymousChatInteraction"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        created_after (Union[Unset, datetime.date]):
        created_before (Union[Unset, datetime.date]):
        has_feedback (Union[Unset, bool]):
        is_flagged (Union[Unset, bool]):
        o (Union[Unset, list[AnonymousChatInteractionOEnum]]):
        query (Union[Unset, str]):
        session_id (Union[Unset, str]):
        severity (Union[Unset, InjectionSeverityEnum]):
        user_slug (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AnonymousChatInteraction']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[AnonymousChatInteraction] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        created_after=created_after,
        created_before=created_before,
        has_feedback=has_feedback,
        is_flagged=is_flagged,
        o=o,
        query=query,
        session_id=session_id,
        severity=severity,
        user_slug=user_slug,
    )

    # Set page_size to maximum
    if "params" not in kwargs:
        kwargs["params"] = {}
    kwargs["params"]["page_size"] = 100

    # Make initial request
    response = client.get_httpx_client().request(**kwargs)
    parsed_response = _parse_response(client=client, response=response)

    if parsed_response:
        all_results.extend(parsed_response)

    # Follow pagination links
    while True:
        link_header = response.headers.get("Link", "")
        links = parse_link_header(link_header)

        if "next" not in links:
            break

        # Extract page number from next URL
        next_url = links["next"]
        parsed_url = urlparse(next_url)
        next_params = parse_qs(parsed_url.query)

        if "page" not in next_params:
            break

        # Update only the page parameter, keep all other params
        page_number = next_params["page"][0]
        kwargs["params"]["page"] = page_number

        # Fetch next page
        response = client.get_httpx_client().request(**kwargs)
        parsed_response = _parse_response(client=client, response=response)

        if parsed_response:
            all_results.extend(parsed_response)

    return all_results


async def asyncio_all(
    *,
    client: AuthenticatedClient,
    created_after: Union[Unset, datetime.date] = UNSET,
    created_before: Union[Unset, datetime.date] = UNSET,
    has_feedback: Union[Unset, bool] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[AnonymousChatInteractionOEnum]] = UNSET,
    query: Union[Unset, str] = UNSET,
    session_id: Union[Unset, str] = UNSET,
    severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
) -> list["AnonymousChatInteraction"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        created_after (Union[Unset, datetime.date]):
        created_before (Union[Unset, datetime.date]):
        has_feedback (Union[Unset, bool]):
        is_flagged (Union[Unset, bool]):
        o (Union[Unset, list[AnonymousChatInteractionOEnum]]):
        query (Union[Unset, str]):
        session_id (Union[Unset, str]):
        severity (Union[Unset, InjectionSeverityEnum]):
        user_slug (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AnonymousChatInteraction']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[AnonymousChatInteraction] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        created_after=created_after,
        created_before=created_before,
        has_feedback=has_feedback,
        is_flagged=is_flagged,
        o=o,
        query=query,
        session_id=session_id,
        severity=severity,
        user_slug=user_slug,
    )

    # Set page_size to maximum
    if "params" not in kwargs:
        kwargs["params"] = {}
    kwargs["params"]["page_size"] = 100

    # Make initial request
    response = await client.get_async_httpx_client().request(**kwargs)
    parsed_response = _parse_response(client=client, response=response)

    if parsed_response:
        all_results.extend(parsed_response)

    # Follow pagination links
    while True:
        link_header = response.headers.get("Link", "")
        links = parse_link_header(link_header)

        if "next" not in links:
            break

        # Extract page number from next URL
        next_url = links["next"]
        parsed_url = urlparse(next_url)
        next_params = parse_qs(parsed_url.query)

        if "page" not in next_params:
            break

        # Update only the page parameter, keep all other params
        page_number = next_params["page"][0]
        kwargs["params"]["page"] = page_number

        # Fetch next page
        response = await client.get_async_httpx_client().request(**kwargs)
        parsed_response = _parse_response(client=client, response=response)

        if parsed_response:
            all_results.extend(parsed_response)

    return all_results
