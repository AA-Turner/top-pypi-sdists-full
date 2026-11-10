from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.hpc_software import HpcSoftware
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    uuid: UUID,
    *,
    partition: Union[Unset, str] = "",
    query: Union[Unset, str] = "",
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["partition"] = partition

    params["query"] = query

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/hpc-workspaces/{uuid}/software/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["HpcSoftware"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = HpcSoftware.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["HpcSoftware"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    partition: Union[Unset, str] = "",
    query: Union[Unset, str] = "",
) -> Response[list["HpcSoftware"]]:
    """Find software available on the cluster

     Searches the offering's software catalogs (EESSI, Spack, ...); with a partition, only builds for its
    CPU architecture. Returns the lines a batch script needs.

    Args:
        uuid (UUID):
        partition (Union[Unset, str]):  Default: ''.
        query (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['HpcSoftware']]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        partition=partition,
        query=query,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    partition: Union[Unset, str] = "",
    query: Union[Unset, str] = "",
) -> list["HpcSoftware"]:
    """Find software available on the cluster

     Searches the offering's software catalogs (EESSI, Spack, ...); with a partition, only builds for its
    CPU architecture. Returns the lines a batch script needs.

    Args:
        uuid (UUID):
        partition (Union[Unset, str]):  Default: ''.
        query (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['HpcSoftware']
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        partition=partition,
        query=query,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    partition: Union[Unset, str] = "",
    query: Union[Unset, str] = "",
) -> Response[list["HpcSoftware"]]:
    """Find software available on the cluster

     Searches the offering's software catalogs (EESSI, Spack, ...); with a partition, only builds for its
    CPU architecture. Returns the lines a batch script needs.

    Args:
        uuid (UUID):
        partition (Union[Unset, str]):  Default: ''.
        query (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['HpcSoftware']]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        partition=partition,
        query=query,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    partition: Union[Unset, str] = "",
    query: Union[Unset, str] = "",
) -> list["HpcSoftware"]:
    """Find software available on the cluster

     Searches the offering's software catalogs (EESSI, Spack, ...); with a partition, only builds for its
    CPU architecture. Returns the lines a batch script needs.

    Args:
        uuid (UUID):
        partition (Union[Unset, str]):  Default: ''.
        query (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['HpcSoftware']
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            partition=partition,
            query=query,
        )
    ).parsed


def sync_all(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    partition: Union[Unset, str] = "",
    query: Union[Unset, str] = "",
) -> list["HpcSoftware"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        uuid (UUID):
        partition (Union[Unset, str]):  Default: ''.
        query (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['HpcSoftware']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[HpcSoftware] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        uuid=uuid,
        partition=partition,
        query=query,
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
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    partition: Union[Unset, str] = "",
    query: Union[Unset, str] = "",
) -> list["HpcSoftware"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        uuid (UUID):
        partition (Union[Unset, str]):  Default: ''.
        query (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['HpcSoftware']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[HpcSoftware] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        uuid=uuid,
        partition=partition,
        query=query,
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
