from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.arrow_customer_mapping import ArrowCustomerMapping
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    arrow_company_name: Union[Unset, str] = UNSET,
    arrow_reference: Union[Unset, str] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    settings: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    waldur_customer: Union[Unset, str] = UNSET,
    waldur_customer_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["arrow_company_name"] = arrow_company_name

    params["arrow_reference"] = arrow_reference

    params["is_active"] = is_active

    params["page"] = page

    params["page_size"] = page_size

    params["settings"] = settings

    json_settings_uuid: Union[Unset, str] = UNSET
    if not isinstance(settings_uuid, Unset):
        json_settings_uuid = str(settings_uuid)
    params["settings_uuid"] = json_settings_uuid

    params["waldur_customer"] = waldur_customer

    json_waldur_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(waldur_customer_uuid, Unset):
        json_waldur_customer_uuid = str(waldur_customer_uuid)
    params["waldur_customer_uuid"] = json_waldur_customer_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/admin/arrow/customer-mappings/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["ArrowCustomerMapping"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ArrowCustomerMapping.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["ArrowCustomerMapping"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    arrow_company_name: Union[Unset, str] = UNSET,
    arrow_reference: Union[Unset, str] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    settings: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    waldur_customer: Union[Unset, str] = UNSET,
    waldur_customer_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["ArrowCustomerMapping"]]:
    """
    Args:
        arrow_company_name (Union[Unset, str]):
        arrow_reference (Union[Unset, str]):
        is_active (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        settings (Union[Unset, str]):
        settings_uuid (Union[Unset, UUID]):
        waldur_customer (Union[Unset, str]):
        waldur_customer_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ArrowCustomerMapping']]
    """

    kwargs = _get_kwargs(
        arrow_company_name=arrow_company_name,
        arrow_reference=arrow_reference,
        is_active=is_active,
        page=page,
        page_size=page_size,
        settings=settings,
        settings_uuid=settings_uuid,
        waldur_customer=waldur_customer,
        waldur_customer_uuid=waldur_customer_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    arrow_company_name: Union[Unset, str] = UNSET,
    arrow_reference: Union[Unset, str] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    settings: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    waldur_customer: Union[Unset, str] = UNSET,
    waldur_customer_uuid: Union[Unset, UUID] = UNSET,
) -> list["ArrowCustomerMapping"]:
    """
    Args:
        arrow_company_name (Union[Unset, str]):
        arrow_reference (Union[Unset, str]):
        is_active (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        settings (Union[Unset, str]):
        settings_uuid (Union[Unset, UUID]):
        waldur_customer (Union[Unset, str]):
        waldur_customer_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ArrowCustomerMapping']
    """

    return sync_detailed(
        client=client,
        arrow_company_name=arrow_company_name,
        arrow_reference=arrow_reference,
        is_active=is_active,
        page=page,
        page_size=page_size,
        settings=settings,
        settings_uuid=settings_uuid,
        waldur_customer=waldur_customer,
        waldur_customer_uuid=waldur_customer_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    arrow_company_name: Union[Unset, str] = UNSET,
    arrow_reference: Union[Unset, str] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    settings: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    waldur_customer: Union[Unset, str] = UNSET,
    waldur_customer_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["ArrowCustomerMapping"]]:
    """
    Args:
        arrow_company_name (Union[Unset, str]):
        arrow_reference (Union[Unset, str]):
        is_active (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        settings (Union[Unset, str]):
        settings_uuid (Union[Unset, UUID]):
        waldur_customer (Union[Unset, str]):
        waldur_customer_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ArrowCustomerMapping']]
    """

    kwargs = _get_kwargs(
        arrow_company_name=arrow_company_name,
        arrow_reference=arrow_reference,
        is_active=is_active,
        page=page,
        page_size=page_size,
        settings=settings,
        settings_uuid=settings_uuid,
        waldur_customer=waldur_customer,
        waldur_customer_uuid=waldur_customer_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    arrow_company_name: Union[Unset, str] = UNSET,
    arrow_reference: Union[Unset, str] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    settings: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    waldur_customer: Union[Unset, str] = UNSET,
    waldur_customer_uuid: Union[Unset, UUID] = UNSET,
) -> list["ArrowCustomerMapping"]:
    """
    Args:
        arrow_company_name (Union[Unset, str]):
        arrow_reference (Union[Unset, str]):
        is_active (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        settings (Union[Unset, str]):
        settings_uuid (Union[Unset, UUID]):
        waldur_customer (Union[Unset, str]):
        waldur_customer_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ArrowCustomerMapping']
    """

    return (
        await asyncio_detailed(
            client=client,
            arrow_company_name=arrow_company_name,
            arrow_reference=arrow_reference,
            is_active=is_active,
            page=page,
            page_size=page_size,
            settings=settings,
            settings_uuid=settings_uuid,
            waldur_customer=waldur_customer,
            waldur_customer_uuid=waldur_customer_uuid,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    arrow_company_name: Union[Unset, str] = UNSET,
    arrow_reference: Union[Unset, str] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    settings: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    waldur_customer: Union[Unset, str] = UNSET,
    waldur_customer_uuid: Union[Unset, UUID] = UNSET,
) -> list["ArrowCustomerMapping"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        arrow_company_name (Union[Unset, str]):
        arrow_reference (Union[Unset, str]):
        is_active (Union[Unset, bool]):
        settings (Union[Unset, str]):
        settings_uuid (Union[Unset, UUID]):
        waldur_customer (Union[Unset, str]):
        waldur_customer_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ArrowCustomerMapping']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[ArrowCustomerMapping] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        arrow_company_name=arrow_company_name,
        arrow_reference=arrow_reference,
        is_active=is_active,
        settings=settings,
        settings_uuid=settings_uuid,
        waldur_customer=waldur_customer,
        waldur_customer_uuid=waldur_customer_uuid,
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
    arrow_company_name: Union[Unset, str] = UNSET,
    arrow_reference: Union[Unset, str] = UNSET,
    is_active: Union[Unset, bool] = UNSET,
    settings: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    waldur_customer: Union[Unset, str] = UNSET,
    waldur_customer_uuid: Union[Unset, UUID] = UNSET,
) -> list["ArrowCustomerMapping"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        arrow_company_name (Union[Unset, str]):
        arrow_reference (Union[Unset, str]):
        is_active (Union[Unset, bool]):
        settings (Union[Unset, str]):
        settings_uuid (Union[Unset, UUID]):
        waldur_customer (Union[Unset, str]):
        waldur_customer_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ArrowCustomerMapping']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[ArrowCustomerMapping] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        arrow_company_name=arrow_company_name,
        arrow_reference=arrow_reference,
        is_active=is_active,
        settings=settings,
        settings_uuid=settings_uuid,
        waldur_customer=waldur_customer,
        waldur_customer_uuid=waldur_customer_uuid,
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
