from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.maintenance_type_enum import MaintenanceTypeEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    customer_uuid: Union[Unset, UUID] = UNSET,
    customers_offerings_state: Union[Unset, list[MaintenanceTypeEnum]] = UNSET,
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
        "method": "head",
        "url": "/api/marketplace-categories/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> int:
    if response.status_code == HTTPStatus.OK:
        try:
            return int(response.headers["x-result-count"])
        except KeyError:
            raise errors.UnexpectedStatus(
                response.status_code,
                b"Expected 'X-Result-Count' header for HEAD request, but it was not found.",
                response.url,
            )
        except ValueError:
            count_val = response.headers.get("x-result-count")
            msg = f"Expected 'X-Result-Count' header to be an integer, but got '{count_val}'."
            raise errors.UnexpectedStatus(response.status_code, msg.encode(), response.url)
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[int]:
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
    group_uuid: Union[Unset, UUID] = UNSET,
    has_shared: Union[Unset, bool] = UNSET,
    offering_name: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    resource_customer_uuid: Union[Unset, UUID] = UNSET,
    resource_project_uuid: Union[Unset, UUID] = UNSET,
    title: Union[Unset, str] = UNSET,
) -> Response[int]:
    """List categories

     Get number of items in the collection matching the request parameters.

    Args:
        customer_uuid (Union[Unset, UUID]):
        customers_offerings_state (Union[Unset, list[MaintenanceTypeEnum]]):
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
        Response[int]
    """

    kwargs = _get_kwargs(
        customer_uuid=customer_uuid,
        customers_offerings_state=customers_offerings_state,
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
    group_uuid: Union[Unset, UUID] = UNSET,
    has_shared: Union[Unset, bool] = UNSET,
    offering_name: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    resource_customer_uuid: Union[Unset, UUID] = UNSET,
    resource_project_uuid: Union[Unset, UUID] = UNSET,
    title: Union[Unset, str] = UNSET,
) -> int:
    """List categories

     Get number of items in the collection matching the request parameters.

    Args:
        customer_uuid (Union[Unset, UUID]):
        customers_offerings_state (Union[Unset, list[MaintenanceTypeEnum]]):
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
        int
    """

    return sync_detailed(
        client=client,
        customer_uuid=customer_uuid,
        customers_offerings_state=customers_offerings_state,
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
    group_uuid: Union[Unset, UUID] = UNSET,
    has_shared: Union[Unset, bool] = UNSET,
    offering_name: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    resource_customer_uuid: Union[Unset, UUID] = UNSET,
    resource_project_uuid: Union[Unset, UUID] = UNSET,
    title: Union[Unset, str] = UNSET,
) -> Response[int]:
    """List categories

     Get number of items in the collection matching the request parameters.

    Args:
        customer_uuid (Union[Unset, UUID]):
        customers_offerings_state (Union[Unset, list[MaintenanceTypeEnum]]):
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
        Response[int]
    """

    kwargs = _get_kwargs(
        customer_uuid=customer_uuid,
        customers_offerings_state=customers_offerings_state,
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
    group_uuid: Union[Unset, UUID] = UNSET,
    has_shared: Union[Unset, bool] = UNSET,
    offering_name: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    resource_customer_uuid: Union[Unset, UUID] = UNSET,
    resource_project_uuid: Union[Unset, UUID] = UNSET,
    title: Union[Unset, str] = UNSET,
) -> int:
    """List categories

     Get number of items in the collection matching the request parameters.

    Args:
        customer_uuid (Union[Unset, UUID]):
        customers_offerings_state (Union[Unset, list[MaintenanceTypeEnum]]):
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
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            customer_uuid=customer_uuid,
            customers_offerings_state=customers_offerings_state,
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
