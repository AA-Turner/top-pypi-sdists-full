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
    user_slug_path: str,
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
    user_slug_query: Union[Unset, str] = UNSET,
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

    params["user_slug"] = user_slug_query

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/anonymous-chat-interactions/by-user/{user_slug_path}/",
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
    user_slug_path: str,
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
    user_slug_query: Union[Unset, str] = UNSET,
) -> Response[list["AnonymousChatInteraction"]]:
    """All sessions for one pseudonymous user

     Returns interactions sharing a ``user_slug`` (Scrypt of originating IP) — across however many
    sessions that anon user opened, ordered chronologically.

    Args:
        user_slug_path (str):
        created_from (Union[Unset, datetime.date]):
        created_to (Union[Unset, datetime.date]):
        has_negative_feedback (Union[Unset, bool]):
        is_flagged (Union[Unset, bool]):
        o (Union[Unset, list[AnonymousChatInteractionOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        session_id (Union[Unset, str]):
        severity (Union[Unset, InjectionSeverityEnum]):
        user_slug_query (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AnonymousChatInteraction']]
    """

    kwargs = _get_kwargs(
        user_slug_path=user_slug_path,
        created_from=created_from,
        created_to=created_to,
        has_negative_feedback=has_negative_feedback,
        is_flagged=is_flagged,
        o=o,
        page=page,
        page_size=page_size,
        session_id=session_id,
        severity=severity,
        user_slug_query=user_slug_query,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_slug_path: str,
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
    user_slug_query: Union[Unset, str] = UNSET,
) -> list["AnonymousChatInteraction"]:
    """All sessions for one pseudonymous user

     Returns interactions sharing a ``user_slug`` (Scrypt of originating IP) — across however many
    sessions that anon user opened, ordered chronologically.

    Args:
        user_slug_path (str):
        created_from (Union[Unset, datetime.date]):
        created_to (Union[Unset, datetime.date]):
        has_negative_feedback (Union[Unset, bool]):
        is_flagged (Union[Unset, bool]):
        o (Union[Unset, list[AnonymousChatInteractionOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        session_id (Union[Unset, str]):
        severity (Union[Unset, InjectionSeverityEnum]):
        user_slug_query (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AnonymousChatInteraction']
    """

    return sync_detailed(
        user_slug_path=user_slug_path,
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
        user_slug_query=user_slug_query,
    ).parsed


async def asyncio_detailed(
    user_slug_path: str,
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
    user_slug_query: Union[Unset, str] = UNSET,
) -> Response[list["AnonymousChatInteraction"]]:
    """All sessions for one pseudonymous user

     Returns interactions sharing a ``user_slug`` (Scrypt of originating IP) — across however many
    sessions that anon user opened, ordered chronologically.

    Args:
        user_slug_path (str):
        created_from (Union[Unset, datetime.date]):
        created_to (Union[Unset, datetime.date]):
        has_negative_feedback (Union[Unset, bool]):
        is_flagged (Union[Unset, bool]):
        o (Union[Unset, list[AnonymousChatInteractionOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        session_id (Union[Unset, str]):
        severity (Union[Unset, InjectionSeverityEnum]):
        user_slug_query (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AnonymousChatInteraction']]
    """

    kwargs = _get_kwargs(
        user_slug_path=user_slug_path,
        created_from=created_from,
        created_to=created_to,
        has_negative_feedback=has_negative_feedback,
        is_flagged=is_flagged,
        o=o,
        page=page,
        page_size=page_size,
        session_id=session_id,
        severity=severity,
        user_slug_query=user_slug_query,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_slug_path: str,
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
    user_slug_query: Union[Unset, str] = UNSET,
) -> list["AnonymousChatInteraction"]:
    """All sessions for one pseudonymous user

     Returns interactions sharing a ``user_slug`` (Scrypt of originating IP) — across however many
    sessions that anon user opened, ordered chronologically.

    Args:
        user_slug_path (str):
        created_from (Union[Unset, datetime.date]):
        created_to (Union[Unset, datetime.date]):
        has_negative_feedback (Union[Unset, bool]):
        is_flagged (Union[Unset, bool]):
        o (Union[Unset, list[AnonymousChatInteractionOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        session_id (Union[Unset, str]):
        severity (Union[Unset, InjectionSeverityEnum]):
        user_slug_query (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AnonymousChatInteraction']
    """

    return (
        await asyncio_detailed(
            user_slug_path=user_slug_path,
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
            user_slug_query=user_slug_query,
        )
    ).parsed


def sync_all(
    user_slug_path: str,
    *,
    client: AuthenticatedClient,
    created_from: Union[Unset, datetime.date] = UNSET,
    created_to: Union[Unset, datetime.date] = UNSET,
    has_negative_feedback: Union[Unset, bool] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[AnonymousChatInteractionOEnum]] = UNSET,
    session_id: Union[Unset, str] = UNSET,
    severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    user_slug_query: Union[Unset, str] = UNSET,
) -> list["AnonymousChatInteraction"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        user_slug_path (str):
        created_from (Union[Unset, datetime.date]):
        created_to (Union[Unset, datetime.date]):
        has_negative_feedback (Union[Unset, bool]):
        is_flagged (Union[Unset, bool]):
        o (Union[Unset, list[AnonymousChatInteractionOEnum]]):
        session_id (Union[Unset, str]):
        severity (Union[Unset, InjectionSeverityEnum]):
        user_slug_query (Union[Unset, str]):

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
        user_slug_path=user_slug_path,
        created_from=created_from,
        created_to=created_to,
        has_negative_feedback=has_negative_feedback,
        is_flagged=is_flagged,
        o=o,
        session_id=session_id,
        severity=severity,
        user_slug_query=user_slug_query,
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
    user_slug_path: str,
    *,
    client: AuthenticatedClient,
    created_from: Union[Unset, datetime.date] = UNSET,
    created_to: Union[Unset, datetime.date] = UNSET,
    has_negative_feedback: Union[Unset, bool] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[AnonymousChatInteractionOEnum]] = UNSET,
    session_id: Union[Unset, str] = UNSET,
    severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    user_slug_query: Union[Unset, str] = UNSET,
) -> list["AnonymousChatInteraction"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        user_slug_path (str):
        created_from (Union[Unset, datetime.date]):
        created_to (Union[Unset, datetime.date]):
        has_negative_feedback (Union[Unset, bool]):
        is_flagged (Union[Unset, bool]):
        o (Union[Unset, list[AnonymousChatInteractionOEnum]]):
        session_id (Union[Unset, str]):
        severity (Union[Unset, InjectionSeverityEnum]):
        user_slug_query (Union[Unset, str]):

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
        user_slug_path=user_slug_path,
        created_from=created_from,
        created_to=created_to,
        has_negative_feedback=has_negative_feedback,
        is_flagged=is_flagged,
        o=o,
        session_id=session_id,
        severity=severity,
        user_slug_query=user_slug_query,
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
