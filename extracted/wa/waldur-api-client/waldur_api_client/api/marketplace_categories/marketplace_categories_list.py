from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.maintenance_type_enum import MaintenanceTypeEnum
from ...models.marketplace_category import MarketplaceCategory
from ...models.marketplace_category_field_enum import MarketplaceCategoryFieldEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    customer_uuid: Union[Unset, UUID] = UNSET,
    customers_offerings_state: Union[Unset, list[MaintenanceTypeEnum]] = UNSET,
    field: Union[Unset, list[MarketplaceCategoryFieldEnum]] = UNSET,
    group_uuid: Union[Unset, UUID] = UNSET,
    has_shared: Union[Unset, bool] = UNSET,
    offering_name: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    resource_customer_uuid: Union[Unset, UUID] = UNSET,
    resource_project_uuid: Union[Unset, UUID] = UNSET,
    title: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    json_customers_offerings_state: Union[Unset, list[int]] = UNSET
    if not isinstance(customers_offerings_state, Unset):
        json_customers_offerings_state = []
        for customers_offerings_state_item_data in customers_offerings_state:
            customers_offerings_state_item = customers_offerings_state_item_data.value
            json_customers_offerings_state.append(customers_offerings_state_item)

    params["customers_offerings_state"] = json_customers_offerings_state

    json_field: Union[Unset, list[str]] = UNSET
    if not isinstance(field, Unset):
        json_field = []
        for field_item_data in field:
            field_item = field_item_data.value
            json_field.append(field_item)

    params["field"] = json_field

    json_group_uuid: Union[Unset, str] = UNSET
    if not isinstance(group_uuid, Unset):
        json_group_uuid = str(group_uuid)
    params["group_uuid"] = json_group_uuid

    params["has_shared"] = has_shared

    params["offering_name"] = offering_name

    params["page"] = page

    params["page_size"] = page_size

    json_resource_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(resource_customer_uuid, Unset):
        json_resource_customer_uuid = str(resource_customer_uuid)
    params["resource_customer_uuid"] = json_resource_customer_uuid

    json_resource_project_uuid: Union[Unset, str] = UNSET
    if not isinstance(resource_project_uuid, Unset):
        json_resource_project_uuid = str(resource_project_uuid)
    params["resource_project_uuid"] = json_resource_project_uuid

    params["title"] = title

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/marketplace-categories/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["MarketplaceCategory"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = MarketplaceCategory.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["MarketplaceCategory"]]:
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
    customers_offerings_state: Union[Unset, list[MaintenanceTypeEnum]] = UNSET,
    field: Union[Unset, list[MarketplaceCategoryFieldEnum]] = UNSET,
    group_uuid: Union[Unset, UUID] = UNSET,
    has_shared: Union[Unset, bool] = UNSET,
    offering_name: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    resource_customer_uuid: Union[Unset, UUID] = UNSET,
    resource_project_uuid: Union[Unset, UUID] = UNSET,
    title: Union[Unset, str] = UNSET,
) -> Response[list["MarketplaceCategory"]]:
    """List categories

     Returns a paginated list of marketplace categories.

    Args:
        customer_uuid (Union[Unset, UUID]):
        customers_offerings_state (Union[Unset, list[MaintenanceTypeEnum]]):
        field (Union[Unset, list[MarketplaceCategoryFieldEnum]]):
        group_uuid (Union[Unset, UUID]):
        has_shared (Union[Unset, bool]):
        offering_name (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        resource_customer_uuid (Union[Unset, UUID]):
        resource_project_uuid (Union[Unset, UUID]):
        title (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['MarketplaceCategory']]
    """

    kwargs = _get_kwargs(
        customer_uuid=customer_uuid,
        customers_offerings_state=customers_offerings_state,
        field=field,
        group_uuid=group_uuid,
        has_shared=has_shared,
        offering_name=offering_name,
        page=page,
        page_size=page_size,
        resource_customer_uuid=resource_customer_uuid,
        resource_project_uuid=resource_project_uuid,
        title=title,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    customers_offerings_state: Union[Unset, list[MaintenanceTypeEnum]] = UNSET,
    field: Union[Unset, list[MarketplaceCategoryFieldEnum]] = UNSET,
    group_uuid: Union[Unset, UUID] = UNSET,
    has_shared: Union[Unset, bool] = UNSET,
    offering_name: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    resource_customer_uuid: Union[Unset, UUID] = UNSET,
    resource_project_uuid: Union[Unset, UUID] = UNSET,
    title: Union[Unset, str] = UNSET,
) -> list["MarketplaceCategory"]:
    """List categories

     Returns a paginated list of marketplace categories.

    Args:
        customer_uuid (Union[Unset, UUID]):
        customers_offerings_state (Union[Unset, list[MaintenanceTypeEnum]]):
        field (Union[Unset, list[MarketplaceCategoryFieldEnum]]):
        group_uuid (Union[Unset, UUID]):
        has_shared (Union[Unset, bool]):
        offering_name (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        resource_customer_uuid (Union[Unset, UUID]):
        resource_project_uuid (Union[Unset, UUID]):
        title (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['MarketplaceCategory']
    """

    return sync_detailed(
        client=client,
        customer_uuid=customer_uuid,
        customers_offerings_state=customers_offerings_state,
        field=field,
        group_uuid=group_uuid,
        has_shared=has_shared,
        offering_name=offering_name,
        page=page,
        page_size=page_size,
        resource_customer_uuid=resource_customer_uuid,
        resource_project_uuid=resource_project_uuid,
        title=title,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    customers_offerings_state: Union[Unset, list[MaintenanceTypeEnum]] = UNSET,
    field: Union[Unset, list[MarketplaceCategoryFieldEnum]] = UNSET,
    group_uuid: Union[Unset, UUID] = UNSET,
    has_shared: Union[Unset, bool] = UNSET,
    offering_name: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    resource_customer_uuid: Union[Unset, UUID] = UNSET,
    resource_project_uuid: Union[Unset, UUID] = UNSET,
    title: Union[Unset, str] = UNSET,
) -> Response[list["MarketplaceCategory"]]:
    """List categories

     Returns a paginated list of marketplace categories.

    Args:
        customer_uuid (Union[Unset, UUID]):
        customers_offerings_state (Union[Unset, list[MaintenanceTypeEnum]]):
        field (Union[Unset, list[MarketplaceCategoryFieldEnum]]):
        group_uuid (Union[Unset, UUID]):
        has_shared (Union[Unset, bool]):
        offering_name (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        resource_customer_uuid (Union[Unset, UUID]):
        resource_project_uuid (Union[Unset, UUID]):
        title (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['MarketplaceCategory']]
    """

    kwargs = _get_kwargs(
        customer_uuid=customer_uuid,
        customers_offerings_state=customers_offerings_state,
        field=field,
        group_uuid=group_uuid,
        has_shared=has_shared,
        offering_name=offering_name,
        page=page,
        page_size=page_size,
        resource_customer_uuid=resource_customer_uuid,
        resource_project_uuid=resource_project_uuid,
        title=title,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    customers_offerings_state: Union[Unset, list[MaintenanceTypeEnum]] = UNSET,
    field: Union[Unset, list[MarketplaceCategoryFieldEnum]] = UNSET,
    group_uuid: Union[Unset, UUID] = UNSET,
    has_shared: Union[Unset, bool] = UNSET,
    offering_name: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    resource_customer_uuid: Union[Unset, UUID] = UNSET,
    resource_project_uuid: Union[Unset, UUID] = UNSET,
    title: Union[Unset, str] = UNSET,
) -> list["MarketplaceCategory"]:
    """List categories

     Returns a paginated list of marketplace categories.

    Args:
        customer_uuid (Union[Unset, UUID]):
        customers_offerings_state (Union[Unset, list[MaintenanceTypeEnum]]):
        field (Union[Unset, list[MarketplaceCategoryFieldEnum]]):
        group_uuid (Union[Unset, UUID]):
        has_shared (Union[Unset, bool]):
        offering_name (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        resource_customer_uuid (Union[Unset, UUID]):
        resource_project_uuid (Union[Unset, UUID]):
        title (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['MarketplaceCategory']
    """

    return (
        await asyncio_detailed(
            client=client,
            customer_uuid=customer_uuid,
            customers_offerings_state=customers_offerings_state,
            field=field,
            group_uuid=group_uuid,
            has_shared=has_shared,
            offering_name=offering_name,
            page=page,
            page_size=page_size,
            resource_customer_uuid=resource_customer_uuid,
            resource_project_uuid=resource_project_uuid,
            title=title,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    customers_offerings_state: Union[Unset, list[MaintenanceTypeEnum]] = UNSET,
    field: Union[Unset, list[MarketplaceCategoryFieldEnum]] = UNSET,
    group_uuid: Union[Unset, UUID] = UNSET,
    has_shared: Union[Unset, bool] = UNSET,
    offering_name: Union[Unset, str] = UNSET,
    resource_customer_uuid: Union[Unset, UUID] = UNSET,
    resource_project_uuid: Union[Unset, UUID] = UNSET,
    title: Union[Unset, str] = UNSET,
) -> list["MarketplaceCategory"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        customer_uuid (Union[Unset, UUID]):
        customers_offerings_state (Union[Unset, list[MaintenanceTypeEnum]]):
        field (Union[Unset, list[MarketplaceCategoryFieldEnum]]):
        group_uuid (Union[Unset, UUID]):
        has_shared (Union[Unset, bool]):
        offering_name (Union[Unset, str]):
        resource_customer_uuid (Union[Unset, UUID]):
        resource_project_uuid (Union[Unset, UUID]):
        title (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['MarketplaceCategory']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[MarketplaceCategory] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        customer_uuid=customer_uuid,
        customers_offerings_state=customers_offerings_state,
        field=field,
        group_uuid=group_uuid,
        has_shared=has_shared,
        offering_name=offering_name,
        resource_customer_uuid=resource_customer_uuid,
        resource_project_uuid=resource_project_uuid,
        title=title,
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
    customers_offerings_state: Union[Unset, list[MaintenanceTypeEnum]] = UNSET,
    field: Union[Unset, list[MarketplaceCategoryFieldEnum]] = UNSET,
    group_uuid: Union[Unset, UUID] = UNSET,
    has_shared: Union[Unset, bool] = UNSET,
    offering_name: Union[Unset, str] = UNSET,
    resource_customer_uuid: Union[Unset, UUID] = UNSET,
    resource_project_uuid: Union[Unset, UUID] = UNSET,
    title: Union[Unset, str] = UNSET,
) -> list["MarketplaceCategory"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        customer_uuid (Union[Unset, UUID]):
        customers_offerings_state (Union[Unset, list[MaintenanceTypeEnum]]):
        field (Union[Unset, list[MarketplaceCategoryFieldEnum]]):
        group_uuid (Union[Unset, UUID]):
        has_shared (Union[Unset, bool]):
        offering_name (Union[Unset, str]):
        resource_customer_uuid (Union[Unset, UUID]):
        resource_project_uuid (Union[Unset, UUID]):
        title (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['MarketplaceCategory']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[MarketplaceCategory] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        customer_uuid=customer_uuid,
        customers_offerings_state=customers_offerings_state,
        field=field,
        group_uuid=group_uuid,
        has_shared=has_shared,
        offering_name=offering_name,
        resource_customer_uuid=resource_customer_uuid,
        resource_project_uuid=resource_project_uuid,
        title=title,
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
