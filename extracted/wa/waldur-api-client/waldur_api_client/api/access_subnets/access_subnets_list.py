from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.access_subnet import AccessSubnet
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    applies_to_portal: Union[Unset, bool] = UNSET,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    description: Union[Unset, str] = UNSET,
    inet: Union[Unset, str] = UNSET,
    is_staff_managed: Union[Unset, bool] = UNSET,
    o: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["applies_to_portal"] = applies_to_portal

    params["customer"] = customer

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    params["description"] = description

    params["inet"] = inet

    params["is_staff_managed"] = is_staff_managed

    params["o"] = o

    json_offering_uuid: Union[Unset, str] = UNSET
    if not isinstance(offering_uuid, Unset):
        json_offering_uuid = str(offering_uuid)
    params["offering_uuid"] = json_offering_uuid

    params["page"] = page

    params["page_size"] = page_size

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/access-subnets/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["AccessSubnet"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = AccessSubnet.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["AccessSubnet"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    applies_to_portal: Union[Unset, bool] = UNSET,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    description: Union[Unset, str] = UNSET,
    inet: Union[Unset, str] = UNSET,
    is_staff_managed: Union[Unset, bool] = UNSET,
    o: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> Response[list["AccessSubnet"]]:
    """List access subnets

     Retrieve a list of access subnets. Staff and support users can see all subnets, while other users
    can only see subnets associated with customers they have a role in.

    Args:
        applies_to_portal (Union[Unset, bool]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        description (Union[Unset, str]):
        inet (Union[Unset, str]):
        is_staff_managed (Union[Unset, bool]):
        o (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AccessSubnet']]
    """

    kwargs = _get_kwargs(
        applies_to_portal=applies_to_portal,
        customer=customer,
        customer_uuid=customer_uuid,
        description=description,
        inet=inet,
        is_staff_managed=is_staff_managed,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    applies_to_portal: Union[Unset, bool] = UNSET,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    description: Union[Unset, str] = UNSET,
    inet: Union[Unset, str] = UNSET,
    is_staff_managed: Union[Unset, bool] = UNSET,
    o: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> list["AccessSubnet"]:
    """List access subnets

     Retrieve a list of access subnets. Staff and support users can see all subnets, while other users
    can only see subnets associated with customers they have a role in.

    Args:
        applies_to_portal (Union[Unset, bool]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        description (Union[Unset, str]):
        inet (Union[Unset, str]):
        is_staff_managed (Union[Unset, bool]):
        o (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AccessSubnet']
    """

    return sync_detailed(
        client=client,
        applies_to_portal=applies_to_portal,
        customer=customer,
        customer_uuid=customer_uuid,
        description=description,
        inet=inet,
        is_staff_managed=is_staff_managed,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    applies_to_portal: Union[Unset, bool] = UNSET,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    description: Union[Unset, str] = UNSET,
    inet: Union[Unset, str] = UNSET,
    is_staff_managed: Union[Unset, bool] = UNSET,
    o: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> Response[list["AccessSubnet"]]:
    """List access subnets

     Retrieve a list of access subnets. Staff and support users can see all subnets, while other users
    can only see subnets associated with customers they have a role in.

    Args:
        applies_to_portal (Union[Unset, bool]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        description (Union[Unset, str]):
        inet (Union[Unset, str]):
        is_staff_managed (Union[Unset, bool]):
        o (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AccessSubnet']]
    """

    kwargs = _get_kwargs(
        applies_to_portal=applies_to_portal,
        customer=customer,
        customer_uuid=customer_uuid,
        description=description,
        inet=inet,
        is_staff_managed=is_staff_managed,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    applies_to_portal: Union[Unset, bool] = UNSET,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    description: Union[Unset, str] = UNSET,
    inet: Union[Unset, str] = UNSET,
    is_staff_managed: Union[Unset, bool] = UNSET,
    o: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> list["AccessSubnet"]:
    """List access subnets

     Retrieve a list of access subnets. Staff and support users can see all subnets, while other users
    can only see subnets associated with customers they have a role in.

    Args:
        applies_to_portal (Union[Unset, bool]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        description (Union[Unset, str]):
        inet (Union[Unset, str]):
        is_staff_managed (Union[Unset, bool]):
        o (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AccessSubnet']
    """

    return (
        await asyncio_detailed(
            client=client,
            applies_to_portal=applies_to_portal,
            customer=customer,
            customer_uuid=customer_uuid,
            description=description,
            inet=inet,
            is_staff_managed=is_staff_managed,
            o=o,
            offering_uuid=offering_uuid,
            page=page,
            page_size=page_size,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    applies_to_portal: Union[Unset, bool] = UNSET,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    description: Union[Unset, str] = UNSET,
    inet: Union[Unset, str] = UNSET,
    is_staff_managed: Union[Unset, bool] = UNSET,
    o: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
) -> list["AccessSubnet"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        applies_to_portal (Union[Unset, bool]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        description (Union[Unset, str]):
        inet (Union[Unset, str]):
        is_staff_managed (Union[Unset, bool]):
        o (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AccessSubnet']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[AccessSubnet] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        applies_to_portal=applies_to_portal,
        customer=customer,
        customer_uuid=customer_uuid,
        description=description,
        inet=inet,
        is_staff_managed=is_staff_managed,
        o=o,
        offering_uuid=offering_uuid,
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
    applies_to_portal: Union[Unset, bool] = UNSET,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    description: Union[Unset, str] = UNSET,
    inet: Union[Unset, str] = UNSET,
    is_staff_managed: Union[Unset, bool] = UNSET,
    o: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
) -> list["AccessSubnet"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        applies_to_portal (Union[Unset, bool]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        description (Union[Unset, str]):
        inet (Union[Unset, str]):
        is_staff_managed (Union[Unset, bool]):
        o (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AccessSubnet']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[AccessSubnet] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        applies_to_portal=applies_to_portal,
        customer=customer,
        customer_uuid=customer_uuid,
        description=description,
        inet=inet,
        is_staff_managed=is_staff_managed,
        o=o,
        offering_uuid=offering_uuid,
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
