import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.accessor_type_enum import AccessorTypeEnum
from ...models.global_user_data_access_log import GlobalUserDataAccessLog
from ...models.global_user_data_access_log_o_enum import GlobalUserDataAccessLogOEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    accessor_type: Union[Unset, AccessorTypeEnum] = UNSET,
    accessor_uuid: Union[Unset, UUID] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[GlobalUserDataAccessLogOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_accessor_type: Union[Unset, str] = UNSET
    if not isinstance(accessor_type, Unset):
        json_accessor_type = accessor_type.value

    params["accessor_type"] = json_accessor_type

    json_accessor_uuid: Union[Unset, str] = UNSET
    if not isinstance(accessor_uuid, Unset):
        json_accessor_uuid = str(accessor_uuid)
    params["accessor_uuid"] = json_accessor_uuid

    json_end_date: Union[Unset, str] = UNSET
    if not isinstance(end_date, Unset):
        json_end_date = end_date.isoformat()
    params["end_date"] = json_end_date

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

    json_start_date: Union[Unset, str] = UNSET
    if not isinstance(start_date, Unset):
        json_start_date = start_date.isoformat()
    params["start_date"] = json_start_date

    json_user_uuid: Union[Unset, str] = UNSET
    if not isinstance(user_uuid, Unset):
        json_user_uuid = str(user_uuid)
    params["user_uuid"] = json_user_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/data-access-logs/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["GlobalUserDataAccessLog"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = GlobalUserDataAccessLog.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["GlobalUserDataAccessLog"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    accessor_type: Union[Unset, AccessorTypeEnum] = UNSET,
    accessor_uuid: Union[Unset, UUID] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[GlobalUserDataAccessLogOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["GlobalUserDataAccessLog"]]:
    """
    Args:
        accessor_type (Union[Unset, AccessorTypeEnum]):
        accessor_uuid (Union[Unset, UUID]):
        end_date (Union[Unset, datetime.date]):
        o (Union[Unset, list[GlobalUserDataAccessLogOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        start_date (Union[Unset, datetime.date]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['GlobalUserDataAccessLog']]
    """

    kwargs = _get_kwargs(
        accessor_type=accessor_type,
        accessor_uuid=accessor_uuid,
        end_date=end_date,
        o=o,
        page=page,
        page_size=page_size,
        query=query,
        start_date=start_date,
        user_uuid=user_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    accessor_type: Union[Unset, AccessorTypeEnum] = UNSET,
    accessor_uuid: Union[Unset, UUID] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[GlobalUserDataAccessLogOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> list["GlobalUserDataAccessLog"]:
    """
    Args:
        accessor_type (Union[Unset, AccessorTypeEnum]):
        accessor_uuid (Union[Unset, UUID]):
        end_date (Union[Unset, datetime.date]):
        o (Union[Unset, list[GlobalUserDataAccessLogOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        start_date (Union[Unset, datetime.date]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['GlobalUserDataAccessLog']
    """

    return sync_detailed(
        client=client,
        accessor_type=accessor_type,
        accessor_uuid=accessor_uuid,
        end_date=end_date,
        o=o,
        page=page,
        page_size=page_size,
        query=query,
        start_date=start_date,
        user_uuid=user_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    accessor_type: Union[Unset, AccessorTypeEnum] = UNSET,
    accessor_uuid: Union[Unset, UUID] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[GlobalUserDataAccessLogOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["GlobalUserDataAccessLog"]]:
    """
    Args:
        accessor_type (Union[Unset, AccessorTypeEnum]):
        accessor_uuid (Union[Unset, UUID]):
        end_date (Union[Unset, datetime.date]):
        o (Union[Unset, list[GlobalUserDataAccessLogOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        start_date (Union[Unset, datetime.date]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['GlobalUserDataAccessLog']]
    """

    kwargs = _get_kwargs(
        accessor_type=accessor_type,
        accessor_uuid=accessor_uuid,
        end_date=end_date,
        o=o,
        page=page,
        page_size=page_size,
        query=query,
        start_date=start_date,
        user_uuid=user_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    accessor_type: Union[Unset, AccessorTypeEnum] = UNSET,
    accessor_uuid: Union[Unset, UUID] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[GlobalUserDataAccessLogOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> list["GlobalUserDataAccessLog"]:
    """
    Args:
        accessor_type (Union[Unset, AccessorTypeEnum]):
        accessor_uuid (Union[Unset, UUID]):
        end_date (Union[Unset, datetime.date]):
        o (Union[Unset, list[GlobalUserDataAccessLogOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        start_date (Union[Unset, datetime.date]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['GlobalUserDataAccessLog']
    """

    return (
        await asyncio_detailed(
            client=client,
            accessor_type=accessor_type,
            accessor_uuid=accessor_uuid,
            end_date=end_date,
            o=o,
            page=page,
            page_size=page_size,
            query=query,
            start_date=start_date,
            user_uuid=user_uuid,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    accessor_type: Union[Unset, AccessorTypeEnum] = UNSET,
    accessor_uuid: Union[Unset, UUID] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[GlobalUserDataAccessLogOEnum]] = UNSET,
    query: Union[Unset, str] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> list["GlobalUserDataAccessLog"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        accessor_type (Union[Unset, AccessorTypeEnum]):
        accessor_uuid (Union[Unset, UUID]):
        end_date (Union[Unset, datetime.date]):
        o (Union[Unset, list[GlobalUserDataAccessLogOEnum]]):
        query (Union[Unset, str]):
        start_date (Union[Unset, datetime.date]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['GlobalUserDataAccessLog']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[GlobalUserDataAccessLog] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        accessor_type=accessor_type,
        accessor_uuid=accessor_uuid,
        end_date=end_date,
        o=o,
        query=query,
        start_date=start_date,
        user_uuid=user_uuid,
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
    accessor_type: Union[Unset, AccessorTypeEnum] = UNSET,
    accessor_uuid: Union[Unset, UUID] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[GlobalUserDataAccessLogOEnum]] = UNSET,
    query: Union[Unset, str] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> list["GlobalUserDataAccessLog"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        accessor_type (Union[Unset, AccessorTypeEnum]):
        accessor_uuid (Union[Unset, UUID]):
        end_date (Union[Unset, datetime.date]):
        o (Union[Unset, list[GlobalUserDataAccessLogOEnum]]):
        query (Union[Unset, str]):
        start_date (Union[Unset, datetime.date]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['GlobalUserDataAccessLog']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[GlobalUserDataAccessLog] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        accessor_type=accessor_type,
        accessor_uuid=accessor_uuid,
        end_date=end_date,
        o=o,
        query=query,
        start_date=start_date,
        user_uuid=user_uuid,
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
