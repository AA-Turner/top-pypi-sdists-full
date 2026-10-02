from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.posix_id_pool import PosixIdPool
from ...models.posix_id_pool_field_enum import PosixIdPoolFieldEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    customer_uuid: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[PosixIdPoolFieldEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    json_field: Union[Unset, list[str]] = UNSET
    if not isinstance(field, Unset):
        json_field = []
        for field_item_data in field:
            field_item = field_item_data.value
            json_field.append(field_item)

    params["field"] = json_field

    json_offering_uuid: Union[Unset, str] = UNSET
    if not isinstance(offering_uuid, Unset):
        json_offering_uuid = str(offering_uuid)
    params["offering_uuid"] = json_offering_uuid

    params["page"] = page

    params["page_size"] = page_size

    json_service_provider_uuid: Union[Unset, str] = UNSET
    if not isinstance(service_provider_uuid, Unset):
        json_service_provider_uuid = str(service_provider_uuid)
    params["service_provider_uuid"] = json_service_provider_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/marketplace-posix-id-pools/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["PosixIdPool"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = PosixIdPool.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["PosixIdPool"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[PosixIdPoolFieldEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["PosixIdPool"]]:
    """
    Args:
        customer_uuid (Union[Unset, UUID]):
        field (Union[Unset, list[PosixIdPoolFieldEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        service_provider_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['PosixIdPool']]
    """

    kwargs = _get_kwargs(
        customer_uuid=customer_uuid,
        field=field,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        service_provider_uuid=service_provider_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[PosixIdPoolFieldEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
) -> list["PosixIdPool"]:
    """
    Args:
        customer_uuid (Union[Unset, UUID]):
        field (Union[Unset, list[PosixIdPoolFieldEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        service_provider_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PosixIdPool']
    """

    return sync_detailed(
        client=client,
        customer_uuid=customer_uuid,
        field=field,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        service_provider_uuid=service_provider_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[PosixIdPoolFieldEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["PosixIdPool"]]:
    """
    Args:
        customer_uuid (Union[Unset, UUID]):
        field (Union[Unset, list[PosixIdPoolFieldEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        service_provider_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['PosixIdPool']]
    """

    kwargs = _get_kwargs(
        customer_uuid=customer_uuid,
        field=field,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        service_provider_uuid=service_provider_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[PosixIdPoolFieldEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
) -> list["PosixIdPool"]:
    """
    Args:
        customer_uuid (Union[Unset, UUID]):
        field (Union[Unset, list[PosixIdPoolFieldEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        service_provider_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PosixIdPool']
    """

    return (
        await asyncio_detailed(
            client=client,
            customer_uuid=customer_uuid,
            field=field,
            offering_uuid=offering_uuid,
            page=page,
            page_size=page_size,
            service_provider_uuid=service_provider_uuid,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[PosixIdPoolFieldEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
) -> list["PosixIdPool"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        customer_uuid (Union[Unset, UUID]):
        field (Union[Unset, list[PosixIdPoolFieldEnum]]):
        offering_uuid (Union[Unset, UUID]):
        service_provider_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PosixIdPool']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[PosixIdPool] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        customer_uuid=customer_uuid,
        field=field,
        offering_uuid=offering_uuid,
        service_provider_uuid=service_provider_uuid,
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
    customer_uuid: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[PosixIdPoolFieldEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
) -> list["PosixIdPool"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        customer_uuid (Union[Unset, UUID]):
        field (Union[Unset, list[PosixIdPoolFieldEnum]]):
        offering_uuid (Union[Unset, UUID]):
        service_provider_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PosixIdPool']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[PosixIdPool] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        customer_uuid=customer_uuid,
        field=field,
        offering_uuid=offering_uuid,
        service_provider_uuid=service_provider_uuid,
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
