import datetime
from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.managed_project_audit_entry import ManagedProjectAuditEntry
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    event_type: Union[Unset, str] = UNSET,
    managed_project_destination: Union[Unset, str] = UNSET,
    managed_project_identifier: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    q: Union[Unset, str] = UNSET,
    timestamp_after: Union[Unset, datetime.datetime] = UNSET,
    timestamp_before: Union[Unset, datetime.datetime] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["event_type"] = event_type

    params["managed_project_destination"] = managed_project_destination

    params["managed_project_identifier"] = managed_project_identifier

    params["o"] = o

    params["page"] = page

    params["page_size"] = page_size

    params["q"] = q

    json_timestamp_after: Union[Unset, str] = UNSET
    if not isinstance(timestamp_after, Unset):
        json_timestamp_after = timestamp_after.isoformat()
    params["timestamp_after"] = json_timestamp_after

    json_timestamp_before: Union[Unset, str] = UNSET
    if not isinstance(timestamp_before, Unset):
        json_timestamp_before = timestamp_before.isoformat()
    params["timestamp_before"] = json_timestamp_before

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/openportal-managed-project-audit/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["ManagedProjectAuditEntry"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ManagedProjectAuditEntry.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["ManagedProjectAuditEntry"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    event_type: Union[Unset, str] = UNSET,
    managed_project_destination: Union[Unset, str] = UNSET,
    managed_project_identifier: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    q: Union[Unset, str] = UNSET,
    timestamp_after: Union[Unset, datetime.datetime] = UNSET,
    timestamp_before: Union[Unset, datetime.datetime] = UNSET,
) -> Response[list["ManagedProjectAuditEntry"]]:
    """
    Args:
        event_type (Union[Unset, str]):
        managed_project_destination (Union[Unset, str]):
        managed_project_identifier (Union[Unset, str]):
        o (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        q (Union[Unset, str]):
        timestamp_after (Union[Unset, datetime.datetime]):
        timestamp_before (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ManagedProjectAuditEntry']]
    """

    kwargs = _get_kwargs(
        event_type=event_type,
        managed_project_destination=managed_project_destination,
        managed_project_identifier=managed_project_identifier,
        o=o,
        page=page,
        page_size=page_size,
        q=q,
        timestamp_after=timestamp_after,
        timestamp_before=timestamp_before,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    event_type: Union[Unset, str] = UNSET,
    managed_project_destination: Union[Unset, str] = UNSET,
    managed_project_identifier: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    q: Union[Unset, str] = UNSET,
    timestamp_after: Union[Unset, datetime.datetime] = UNSET,
    timestamp_before: Union[Unset, datetime.datetime] = UNSET,
) -> list["ManagedProjectAuditEntry"]:
    """
    Args:
        event_type (Union[Unset, str]):
        managed_project_destination (Union[Unset, str]):
        managed_project_identifier (Union[Unset, str]):
        o (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        q (Union[Unset, str]):
        timestamp_after (Union[Unset, datetime.datetime]):
        timestamp_before (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ManagedProjectAuditEntry']
    """

    return sync_detailed(
        client=client,
        event_type=event_type,
        managed_project_destination=managed_project_destination,
        managed_project_identifier=managed_project_identifier,
        o=o,
        page=page,
        page_size=page_size,
        q=q,
        timestamp_after=timestamp_after,
        timestamp_before=timestamp_before,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    event_type: Union[Unset, str] = UNSET,
    managed_project_destination: Union[Unset, str] = UNSET,
    managed_project_identifier: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    q: Union[Unset, str] = UNSET,
    timestamp_after: Union[Unset, datetime.datetime] = UNSET,
    timestamp_before: Union[Unset, datetime.datetime] = UNSET,
) -> Response[list["ManagedProjectAuditEntry"]]:
    """
    Args:
        event_type (Union[Unset, str]):
        managed_project_destination (Union[Unset, str]):
        managed_project_identifier (Union[Unset, str]):
        o (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        q (Union[Unset, str]):
        timestamp_after (Union[Unset, datetime.datetime]):
        timestamp_before (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ManagedProjectAuditEntry']]
    """

    kwargs = _get_kwargs(
        event_type=event_type,
        managed_project_destination=managed_project_destination,
        managed_project_identifier=managed_project_identifier,
        o=o,
        page=page,
        page_size=page_size,
        q=q,
        timestamp_after=timestamp_after,
        timestamp_before=timestamp_before,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    event_type: Union[Unset, str] = UNSET,
    managed_project_destination: Union[Unset, str] = UNSET,
    managed_project_identifier: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    q: Union[Unset, str] = UNSET,
    timestamp_after: Union[Unset, datetime.datetime] = UNSET,
    timestamp_before: Union[Unset, datetime.datetime] = UNSET,
) -> list["ManagedProjectAuditEntry"]:
    """
    Args:
        event_type (Union[Unset, str]):
        managed_project_destination (Union[Unset, str]):
        managed_project_identifier (Union[Unset, str]):
        o (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        q (Union[Unset, str]):
        timestamp_after (Union[Unset, datetime.datetime]):
        timestamp_before (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ManagedProjectAuditEntry']
    """

    return (
        await asyncio_detailed(
            client=client,
            event_type=event_type,
            managed_project_destination=managed_project_destination,
            managed_project_identifier=managed_project_identifier,
            o=o,
            page=page,
            page_size=page_size,
            q=q,
            timestamp_after=timestamp_after,
            timestamp_before=timestamp_before,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    event_type: Union[Unset, str] = UNSET,
    managed_project_destination: Union[Unset, str] = UNSET,
    managed_project_identifier: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    q: Union[Unset, str] = UNSET,
    timestamp_after: Union[Unset, datetime.datetime] = UNSET,
    timestamp_before: Union[Unset, datetime.datetime] = UNSET,
) -> list["ManagedProjectAuditEntry"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        event_type (Union[Unset, str]):
        managed_project_destination (Union[Unset, str]):
        managed_project_identifier (Union[Unset, str]):
        o (Union[Unset, str]):
        q (Union[Unset, str]):
        timestamp_after (Union[Unset, datetime.datetime]):
        timestamp_before (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ManagedProjectAuditEntry']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[ManagedProjectAuditEntry] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        event_type=event_type,
        managed_project_destination=managed_project_destination,
        managed_project_identifier=managed_project_identifier,
        o=o,
        q=q,
        timestamp_after=timestamp_after,
        timestamp_before=timestamp_before,
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
    event_type: Union[Unset, str] = UNSET,
    managed_project_destination: Union[Unset, str] = UNSET,
    managed_project_identifier: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    q: Union[Unset, str] = UNSET,
    timestamp_after: Union[Unset, datetime.datetime] = UNSET,
    timestamp_before: Union[Unset, datetime.datetime] = UNSET,
) -> list["ManagedProjectAuditEntry"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        event_type (Union[Unset, str]):
        managed_project_destination (Union[Unset, str]):
        managed_project_identifier (Union[Unset, str]):
        o (Union[Unset, str]):
        q (Union[Unset, str]):
        timestamp_after (Union[Unset, datetime.datetime]):
        timestamp_before (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ManagedProjectAuditEntry']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[ManagedProjectAuditEntry] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        event_type=event_type,
        managed_project_destination=managed_project_destination,
        managed_project_identifier=managed_project_identifier,
        o=o,
        q=q,
        timestamp_after=timestamp_after,
        timestamp_before=timestamp_before,
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
