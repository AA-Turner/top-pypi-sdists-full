import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.assignment_batch_list import AssignmentBatchList
from ...models.assignment_batch_list_o_enum import AssignmentBatchListOEnum
from ...models.assignment_batch_status import AssignmentBatchStatus
from ...models.assignment_source import AssignmentSource
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    call_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[AssignmentBatchListOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    reviewer_pool_entry_uuid: Union[Unset, UUID] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    sent_after: Union[Unset, datetime.datetime] = UNSET,
    sent_before: Union[Unset, datetime.datetime] = UNSET,
    source: Union[Unset, list[AssignmentSource]] = UNSET,
    status: Union[Unset, list[AssignmentBatchStatus]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_call_uuid: Union[Unset, str] = UNSET
    if not isinstance(call_uuid, Unset):
        json_call_uuid = str(call_uuid)
    params["call_uuid"] = json_call_uuid

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["page"] = page

    params["page_size"] = page_size

    json_reviewer_pool_entry_uuid: Union[Unset, str] = UNSET
    if not isinstance(reviewer_pool_entry_uuid, Unset):
        json_reviewer_pool_entry_uuid = str(reviewer_pool_entry_uuid)
    params["reviewer_pool_entry_uuid"] = json_reviewer_pool_entry_uuid

    json_reviewer_uuid: Union[Unset, str] = UNSET
    if not isinstance(reviewer_uuid, Unset):
        json_reviewer_uuid = str(reviewer_uuid)
    params["reviewer_uuid"] = json_reviewer_uuid

    json_sent_after: Union[Unset, str] = UNSET
    if not isinstance(sent_after, Unset):
        json_sent_after = sent_after.isoformat()
    params["sent_after"] = json_sent_after

    json_sent_before: Union[Unset, str] = UNSET
    if not isinstance(sent_before, Unset):
        json_sent_before = sent_before.isoformat()
    params["sent_before"] = json_sent_before

    json_source: Union[Unset, list[str]] = UNSET
    if not isinstance(source, Unset):
        json_source = []
        for source_item_data in source:
            source_item = source_item_data.value
            json_source.append(source_item)

    params["source"] = json_source

    json_status: Union[Unset, list[str]] = UNSET
    if not isinstance(status, Unset):
        json_status = []
        for status_item_data in status:
            status_item = status_item_data.value
            json_status.append(status_item)

    params["status"] = json_status

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/assignment-batches/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["AssignmentBatchList"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = AssignmentBatchList.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["AssignmentBatchList"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[AssignmentBatchListOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    reviewer_pool_entry_uuid: Union[Unset, UUID] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    sent_after: Union[Unset, datetime.datetime] = UNSET,
    sent_before: Union[Unset, datetime.datetime] = UNSET,
    source: Union[Unset, list[AssignmentSource]] = UNSET,
    status: Union[Unset, list[AssignmentBatchStatus]] = UNSET,
) -> Response[list["AssignmentBatchList"]]:
    """
    Args:
        call_uuid (Union[Unset, UUID]):
        o (Union[Unset, list[AssignmentBatchListOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        reviewer_pool_entry_uuid (Union[Unset, UUID]):
        reviewer_uuid (Union[Unset, UUID]):
        sent_after (Union[Unset, datetime.datetime]):
        sent_before (Union[Unset, datetime.datetime]):
        source (Union[Unset, list[AssignmentSource]]):
        status (Union[Unset, list[AssignmentBatchStatus]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AssignmentBatchList']]
    """

    kwargs = _get_kwargs(
        call_uuid=call_uuid,
        o=o,
        page=page,
        page_size=page_size,
        reviewer_pool_entry_uuid=reviewer_pool_entry_uuid,
        reviewer_uuid=reviewer_uuid,
        sent_after=sent_after,
        sent_before=sent_before,
        source=source,
        status=status,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[AssignmentBatchListOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    reviewer_pool_entry_uuid: Union[Unset, UUID] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    sent_after: Union[Unset, datetime.datetime] = UNSET,
    sent_before: Union[Unset, datetime.datetime] = UNSET,
    source: Union[Unset, list[AssignmentSource]] = UNSET,
    status: Union[Unset, list[AssignmentBatchStatus]] = UNSET,
) -> list["AssignmentBatchList"]:
    """
    Args:
        call_uuid (Union[Unset, UUID]):
        o (Union[Unset, list[AssignmentBatchListOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        reviewer_pool_entry_uuid (Union[Unset, UUID]):
        reviewer_uuid (Union[Unset, UUID]):
        sent_after (Union[Unset, datetime.datetime]):
        sent_before (Union[Unset, datetime.datetime]):
        source (Union[Unset, list[AssignmentSource]]):
        status (Union[Unset, list[AssignmentBatchStatus]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AssignmentBatchList']
    """

    return sync_detailed(
        client=client,
        call_uuid=call_uuid,
        o=o,
        page=page,
        page_size=page_size,
        reviewer_pool_entry_uuid=reviewer_pool_entry_uuid,
        reviewer_uuid=reviewer_uuid,
        sent_after=sent_after,
        sent_before=sent_before,
        source=source,
        status=status,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[AssignmentBatchListOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    reviewer_pool_entry_uuid: Union[Unset, UUID] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    sent_after: Union[Unset, datetime.datetime] = UNSET,
    sent_before: Union[Unset, datetime.datetime] = UNSET,
    source: Union[Unset, list[AssignmentSource]] = UNSET,
    status: Union[Unset, list[AssignmentBatchStatus]] = UNSET,
) -> Response[list["AssignmentBatchList"]]:
    """
    Args:
        call_uuid (Union[Unset, UUID]):
        o (Union[Unset, list[AssignmentBatchListOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        reviewer_pool_entry_uuid (Union[Unset, UUID]):
        reviewer_uuid (Union[Unset, UUID]):
        sent_after (Union[Unset, datetime.datetime]):
        sent_before (Union[Unset, datetime.datetime]):
        source (Union[Unset, list[AssignmentSource]]):
        status (Union[Unset, list[AssignmentBatchStatus]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AssignmentBatchList']]
    """

    kwargs = _get_kwargs(
        call_uuid=call_uuid,
        o=o,
        page=page,
        page_size=page_size,
        reviewer_pool_entry_uuid=reviewer_pool_entry_uuid,
        reviewer_uuid=reviewer_uuid,
        sent_after=sent_after,
        sent_before=sent_before,
        source=source,
        status=status,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[AssignmentBatchListOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    reviewer_pool_entry_uuid: Union[Unset, UUID] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    sent_after: Union[Unset, datetime.datetime] = UNSET,
    sent_before: Union[Unset, datetime.datetime] = UNSET,
    source: Union[Unset, list[AssignmentSource]] = UNSET,
    status: Union[Unset, list[AssignmentBatchStatus]] = UNSET,
) -> list["AssignmentBatchList"]:
    """
    Args:
        call_uuid (Union[Unset, UUID]):
        o (Union[Unset, list[AssignmentBatchListOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        reviewer_pool_entry_uuid (Union[Unset, UUID]):
        reviewer_uuid (Union[Unset, UUID]):
        sent_after (Union[Unset, datetime.datetime]):
        sent_before (Union[Unset, datetime.datetime]):
        source (Union[Unset, list[AssignmentSource]]):
        status (Union[Unset, list[AssignmentBatchStatus]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AssignmentBatchList']
    """

    return (
        await asyncio_detailed(
            client=client,
            call_uuid=call_uuid,
            o=o,
            page=page,
            page_size=page_size,
            reviewer_pool_entry_uuid=reviewer_pool_entry_uuid,
            reviewer_uuid=reviewer_uuid,
            sent_after=sent_after,
            sent_before=sent_before,
            source=source,
            status=status,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[AssignmentBatchListOEnum]] = UNSET,
    reviewer_pool_entry_uuid: Union[Unset, UUID] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    sent_after: Union[Unset, datetime.datetime] = UNSET,
    sent_before: Union[Unset, datetime.datetime] = UNSET,
    source: Union[Unset, list[AssignmentSource]] = UNSET,
    status: Union[Unset, list[AssignmentBatchStatus]] = UNSET,
) -> list["AssignmentBatchList"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        call_uuid (Union[Unset, UUID]):
        o (Union[Unset, list[AssignmentBatchListOEnum]]):
        reviewer_pool_entry_uuid (Union[Unset, UUID]):
        reviewer_uuid (Union[Unset, UUID]):
        sent_after (Union[Unset, datetime.datetime]):
        sent_before (Union[Unset, datetime.datetime]):
        source (Union[Unset, list[AssignmentSource]]):
        status (Union[Unset, list[AssignmentBatchStatus]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AssignmentBatchList']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[AssignmentBatchList] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        call_uuid=call_uuid,
        o=o,
        reviewer_pool_entry_uuid=reviewer_pool_entry_uuid,
        reviewer_uuid=reviewer_uuid,
        sent_after=sent_after,
        sent_before=sent_before,
        source=source,
        status=status,
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
    call_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[AssignmentBatchListOEnum]] = UNSET,
    reviewer_pool_entry_uuid: Union[Unset, UUID] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    sent_after: Union[Unset, datetime.datetime] = UNSET,
    sent_before: Union[Unset, datetime.datetime] = UNSET,
    source: Union[Unset, list[AssignmentSource]] = UNSET,
    status: Union[Unset, list[AssignmentBatchStatus]] = UNSET,
) -> list["AssignmentBatchList"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        call_uuid (Union[Unset, UUID]):
        o (Union[Unset, list[AssignmentBatchListOEnum]]):
        reviewer_pool_entry_uuid (Union[Unset, UUID]):
        reviewer_uuid (Union[Unset, UUID]):
        sent_after (Union[Unset, datetime.datetime]):
        sent_before (Union[Unset, datetime.datetime]):
        source (Union[Unset, list[AssignmentSource]]):
        status (Union[Unset, list[AssignmentBatchStatus]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AssignmentBatchList']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[AssignmentBatchList] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        call_uuid=call_uuid,
        o=o,
        reviewer_pool_entry_uuid=reviewer_pool_entry_uuid,
        reviewer_uuid=reviewer_uuid,
        sent_after=sent_after,
        sent_before=sent_before,
        source=source,
        status=status,
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
