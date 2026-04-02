import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.injection_severity_enum import InjectionSeverityEnum
from ...models.thread_session import ThreadSession
from ...models.thread_session_field_enum import ThreadSessionFieldEnum
from ...models.thread_session_o_enum import ThreadSessionOEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    created: Union[Unset, datetime.date] = UNSET,
    field: Union[Unset, list[ThreadSessionFieldEnum]] = UNSET,
    is_archived: Union[Unset, bool] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    max_severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    modified: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[ThreadSessionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    user: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_created: Union[Unset, str] = UNSET
    if not isinstance(created, Unset):
        json_created = created.isoformat()
    params["created"] = json_created

    json_field: Union[Unset, list[str]] = UNSET
    if not isinstance(field, Unset):
        json_field = []
        for field_item_data in field:
            field_item = field_item_data.value
            json_field.append(field_item)

    params["field"] = json_field

    params["is_archived"] = is_archived

    params["is_flagged"] = is_flagged

    json_max_severity: Union[Unset, str] = UNSET
    if not isinstance(max_severity, Unset):
        json_max_severity = max_severity.value

    params["max_severity"] = json_max_severity

    json_modified: Union[Unset, str] = UNSET
    if not isinstance(modified, Unset):
        json_modified = modified.isoformat()
    params["modified"] = json_modified

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

    json_user: Union[Unset, str] = UNSET
    if not isinstance(user, Unset):
        json_user = str(user)
    params["user"] = json_user

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/chat-threads/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["ThreadSession"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ThreadSession.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["ThreadSession"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.date] = UNSET,
    field: Union[Unset, list[ThreadSessionFieldEnum]] = UNSET,
    is_archived: Union[Unset, bool] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    max_severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    modified: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[ThreadSessionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    user: Union[Unset, UUID] = UNSET,
) -> Response[list["ThreadSession"]]:
    """
    Args:
        created (Union[Unset, datetime.date]):
        field (Union[Unset, list[ThreadSessionFieldEnum]]):
        is_archived (Union[Unset, bool]):
        is_flagged (Union[Unset, bool]):
        max_severity (Union[Unset, InjectionSeverityEnum]):
        modified (Union[Unset, datetime.date]):
        o (Union[Unset, list[ThreadSessionOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        user (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ThreadSession']]
    """

    kwargs = _get_kwargs(
        created=created,
        field=field,
        is_archived=is_archived,
        is_flagged=is_flagged,
        max_severity=max_severity,
        modified=modified,
        o=o,
        page=page,
        page_size=page_size,
        query=query,
        user=user,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.date] = UNSET,
    field: Union[Unset, list[ThreadSessionFieldEnum]] = UNSET,
    is_archived: Union[Unset, bool] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    max_severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    modified: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[ThreadSessionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    user: Union[Unset, UUID] = UNSET,
) -> list["ThreadSession"]:
    """
    Args:
        created (Union[Unset, datetime.date]):
        field (Union[Unset, list[ThreadSessionFieldEnum]]):
        is_archived (Union[Unset, bool]):
        is_flagged (Union[Unset, bool]):
        max_severity (Union[Unset, InjectionSeverityEnum]):
        modified (Union[Unset, datetime.date]):
        o (Union[Unset, list[ThreadSessionOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        user (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ThreadSession']
    """

    return sync_detailed(
        client=client,
        created=created,
        field=field,
        is_archived=is_archived,
        is_flagged=is_flagged,
        max_severity=max_severity,
        modified=modified,
        o=o,
        page=page,
        page_size=page_size,
        query=query,
        user=user,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.date] = UNSET,
    field: Union[Unset, list[ThreadSessionFieldEnum]] = UNSET,
    is_archived: Union[Unset, bool] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    max_severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    modified: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[ThreadSessionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    user: Union[Unset, UUID] = UNSET,
) -> Response[list["ThreadSession"]]:
    """
    Args:
        created (Union[Unset, datetime.date]):
        field (Union[Unset, list[ThreadSessionFieldEnum]]):
        is_archived (Union[Unset, bool]):
        is_flagged (Union[Unset, bool]):
        max_severity (Union[Unset, InjectionSeverityEnum]):
        modified (Union[Unset, datetime.date]):
        o (Union[Unset, list[ThreadSessionOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        user (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ThreadSession']]
    """

    kwargs = _get_kwargs(
        created=created,
        field=field,
        is_archived=is_archived,
        is_flagged=is_flagged,
        max_severity=max_severity,
        modified=modified,
        o=o,
        page=page,
        page_size=page_size,
        query=query,
        user=user,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.date] = UNSET,
    field: Union[Unset, list[ThreadSessionFieldEnum]] = UNSET,
    is_archived: Union[Unset, bool] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    max_severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    modified: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[ThreadSessionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    user: Union[Unset, UUID] = UNSET,
) -> list["ThreadSession"]:
    """
    Args:
        created (Union[Unset, datetime.date]):
        field (Union[Unset, list[ThreadSessionFieldEnum]]):
        is_archived (Union[Unset, bool]):
        is_flagged (Union[Unset, bool]):
        max_severity (Union[Unset, InjectionSeverityEnum]):
        modified (Union[Unset, datetime.date]):
        o (Union[Unset, list[ThreadSessionOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        user (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ThreadSession']
    """

    return (
        await asyncio_detailed(
            client=client,
            created=created,
            field=field,
            is_archived=is_archived,
            is_flagged=is_flagged,
            max_severity=max_severity,
            modified=modified,
            o=o,
            page=page,
            page_size=page_size,
            query=query,
            user=user,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.date] = UNSET,
    field: Union[Unset, list[ThreadSessionFieldEnum]] = UNSET,
    is_archived: Union[Unset, bool] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    max_severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    modified: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[ThreadSessionOEnum]] = UNSET,
    query: Union[Unset, str] = UNSET,
    user: Union[Unset, UUID] = UNSET,
) -> list["ThreadSession"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        created (Union[Unset, datetime.date]):
        field (Union[Unset, list[ThreadSessionFieldEnum]]):
        is_archived (Union[Unset, bool]):
        is_flagged (Union[Unset, bool]):
        max_severity (Union[Unset, InjectionSeverityEnum]):
        modified (Union[Unset, datetime.date]):
        o (Union[Unset, list[ThreadSessionOEnum]]):
        query (Union[Unset, str]):
        user (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ThreadSession']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[ThreadSession] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        created=created,
        field=field,
        is_archived=is_archived,
        is_flagged=is_flagged,
        max_severity=max_severity,
        modified=modified,
        o=o,
        query=query,
        user=user,
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
    created: Union[Unset, datetime.date] = UNSET,
    field: Union[Unset, list[ThreadSessionFieldEnum]] = UNSET,
    is_archived: Union[Unset, bool] = UNSET,
    is_flagged: Union[Unset, bool] = UNSET,
    max_severity: Union[Unset, InjectionSeverityEnum] = UNSET,
    modified: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[ThreadSessionOEnum]] = UNSET,
    query: Union[Unset, str] = UNSET,
    user: Union[Unset, UUID] = UNSET,
) -> list["ThreadSession"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        created (Union[Unset, datetime.date]):
        field (Union[Unset, list[ThreadSessionFieldEnum]]):
        is_archived (Union[Unset, bool]):
        is_flagged (Union[Unset, bool]):
        max_severity (Union[Unset, InjectionSeverityEnum]):
        modified (Union[Unset, datetime.date]):
        o (Union[Unset, list[ThreadSessionOEnum]]):
        query (Union[Unset, str]):
        user (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ThreadSession']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[ThreadSession] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        created=created,
        field=field,
        is_archived=is_archived,
        is_flagged=is_flagged,
        max_severity=max_severity,
        modified=modified,
        o=o,
        query=query,
        user=user,
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
