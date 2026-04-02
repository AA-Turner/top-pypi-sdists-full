import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.marketplace_provider_customer_project_o_enum import MarketplaceProviderCustomerProjectOEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    accounting_is_running: Union[Unset, bool] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    can_admin: Union[Unset, bool] = UNSET,
    can_manage: Union[Unset, bool] = UNSET,
    conceal_finished_projects: Union[Unset, bool] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    customer: Union[Unset, list[UUID]] = UNSET,
    customer_abbreviation: Union[Unset, str] = UNSET,
    customer_name: Union[Unset, str] = UNSET,
    customer_native_name: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    include_terminated: Union[Unset, bool] = UNSET,
    is_removed: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[MarketplaceProviderCustomerProjectOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    slug: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["accounting_is_running"] = accounting_is_running

    params["backend_id"] = backend_id

    params["can_admin"] = can_admin

    params["can_manage"] = can_manage

    params["conceal_finished_projects"] = conceal_finished_projects

    json_created: Union[Unset, str] = UNSET
    if not isinstance(created, Unset):
        json_created = created.isoformat()
    params["created"] = json_created

    json_customer: Union[Unset, list[str]] = UNSET
    if not isinstance(customer, Unset):
        json_customer = []
        for customer_item_data in customer:
            customer_item = str(customer_item_data)
            json_customer.append(customer_item)

    params["customer"] = json_customer

    params["customer_abbreviation"] = customer_abbreviation

    params["customer_name"] = customer_name

    params["customer_native_name"] = customer_native_name

    params["description"] = description

    params["include_terminated"] = include_terminated

    params["is_removed"] = is_removed

    json_modified: Union[Unset, str] = UNSET
    if not isinstance(modified, Unset):
        json_modified = modified.isoformat()
    params["modified"] = json_modified

    params["name"] = name

    params["name_exact"] = name_exact

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

    params["slug"] = slug

    json_user_uuid: Union[Unset, str] = UNSET
    if not isinstance(user_uuid, Unset):
        json_user_uuid = str(user_uuid)
    params["user_uuid"] = json_user_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/openportal-unmanaged-projects/",
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
    accounting_is_running: Union[Unset, bool] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    can_admin: Union[Unset, bool] = UNSET,
    can_manage: Union[Unset, bool] = UNSET,
    conceal_finished_projects: Union[Unset, bool] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    customer: Union[Unset, list[UUID]] = UNSET,
    customer_abbreviation: Union[Unset, str] = UNSET,
    customer_name: Union[Unset, str] = UNSET,
    customer_native_name: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    include_terminated: Union[Unset, bool] = UNSET,
    is_removed: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[MarketplaceProviderCustomerProjectOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    slug: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """List projects

     Get number of items in the collection matching the request parameters.

    Args:
        accounting_is_running (Union[Unset, bool]):
        backend_id (Union[Unset, str]):
        can_admin (Union[Unset, bool]):
        can_manage (Union[Unset, bool]):
        conceal_finished_projects (Union[Unset, bool]):
        created (Union[Unset, datetime.datetime]):
        customer (Union[Unset, list[UUID]]):
        customer_abbreviation (Union[Unset, str]):
        customer_name (Union[Unset, str]):
        customer_native_name (Union[Unset, str]):
        description (Union[Unset, str]):
        include_terminated (Union[Unset, bool]):
        is_removed (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, list[MarketplaceProviderCustomerProjectOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        slug (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        accounting_is_running=accounting_is_running,
        backend_id=backend_id,
        can_admin=can_admin,
        can_manage=can_manage,
        conceal_finished_projects=conceal_finished_projects,
        created=created,
        customer=customer,
        customer_abbreviation=customer_abbreviation,
        customer_name=customer_name,
        customer_native_name=customer_native_name,
        description=description,
        include_terminated=include_terminated,
        is_removed=is_removed,
        modified=modified,
        name=name,
        name_exact=name_exact,
        o=o,
        page=page,
        page_size=page_size,
        query=query,
        slug=slug,
        user_uuid=user_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    accounting_is_running: Union[Unset, bool] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    can_admin: Union[Unset, bool] = UNSET,
    can_manage: Union[Unset, bool] = UNSET,
    conceal_finished_projects: Union[Unset, bool] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    customer: Union[Unset, list[UUID]] = UNSET,
    customer_abbreviation: Union[Unset, str] = UNSET,
    customer_name: Union[Unset, str] = UNSET,
    customer_native_name: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    include_terminated: Union[Unset, bool] = UNSET,
    is_removed: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[MarketplaceProviderCustomerProjectOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    slug: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> int:
    """List projects

     Get number of items in the collection matching the request parameters.

    Args:
        accounting_is_running (Union[Unset, bool]):
        backend_id (Union[Unset, str]):
        can_admin (Union[Unset, bool]):
        can_manage (Union[Unset, bool]):
        conceal_finished_projects (Union[Unset, bool]):
        created (Union[Unset, datetime.datetime]):
        customer (Union[Unset, list[UUID]]):
        customer_abbreviation (Union[Unset, str]):
        customer_name (Union[Unset, str]):
        customer_native_name (Union[Unset, str]):
        description (Union[Unset, str]):
        include_terminated (Union[Unset, bool]):
        is_removed (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, list[MarketplaceProviderCustomerProjectOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        slug (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        accounting_is_running=accounting_is_running,
        backend_id=backend_id,
        can_admin=can_admin,
        can_manage=can_manage,
        conceal_finished_projects=conceal_finished_projects,
        created=created,
        customer=customer,
        customer_abbreviation=customer_abbreviation,
        customer_name=customer_name,
        customer_native_name=customer_native_name,
        description=description,
        include_terminated=include_terminated,
        is_removed=is_removed,
        modified=modified,
        name=name,
        name_exact=name_exact,
        o=o,
        page=page,
        page_size=page_size,
        query=query,
        slug=slug,
        user_uuid=user_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    accounting_is_running: Union[Unset, bool] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    can_admin: Union[Unset, bool] = UNSET,
    can_manage: Union[Unset, bool] = UNSET,
    conceal_finished_projects: Union[Unset, bool] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    customer: Union[Unset, list[UUID]] = UNSET,
    customer_abbreviation: Union[Unset, str] = UNSET,
    customer_name: Union[Unset, str] = UNSET,
    customer_native_name: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    include_terminated: Union[Unset, bool] = UNSET,
    is_removed: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[MarketplaceProviderCustomerProjectOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    slug: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """List projects

     Get number of items in the collection matching the request parameters.

    Args:
        accounting_is_running (Union[Unset, bool]):
        backend_id (Union[Unset, str]):
        can_admin (Union[Unset, bool]):
        can_manage (Union[Unset, bool]):
        conceal_finished_projects (Union[Unset, bool]):
        created (Union[Unset, datetime.datetime]):
        customer (Union[Unset, list[UUID]]):
        customer_abbreviation (Union[Unset, str]):
        customer_name (Union[Unset, str]):
        customer_native_name (Union[Unset, str]):
        description (Union[Unset, str]):
        include_terminated (Union[Unset, bool]):
        is_removed (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, list[MarketplaceProviderCustomerProjectOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        slug (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        accounting_is_running=accounting_is_running,
        backend_id=backend_id,
        can_admin=can_admin,
        can_manage=can_manage,
        conceal_finished_projects=conceal_finished_projects,
        created=created,
        customer=customer,
        customer_abbreviation=customer_abbreviation,
        customer_name=customer_name,
        customer_native_name=customer_native_name,
        description=description,
        include_terminated=include_terminated,
        is_removed=is_removed,
        modified=modified,
        name=name,
        name_exact=name_exact,
        o=o,
        page=page,
        page_size=page_size,
        query=query,
        slug=slug,
        user_uuid=user_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    accounting_is_running: Union[Unset, bool] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    can_admin: Union[Unset, bool] = UNSET,
    can_manage: Union[Unset, bool] = UNSET,
    conceal_finished_projects: Union[Unset, bool] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    customer: Union[Unset, list[UUID]] = UNSET,
    customer_abbreviation: Union[Unset, str] = UNSET,
    customer_name: Union[Unset, str] = UNSET,
    customer_native_name: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    include_terminated: Union[Unset, bool] = UNSET,
    is_removed: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[MarketplaceProviderCustomerProjectOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    slug: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> int:
    """List projects

     Get number of items in the collection matching the request parameters.

    Args:
        accounting_is_running (Union[Unset, bool]):
        backend_id (Union[Unset, str]):
        can_admin (Union[Unset, bool]):
        can_manage (Union[Unset, bool]):
        conceal_finished_projects (Union[Unset, bool]):
        created (Union[Unset, datetime.datetime]):
        customer (Union[Unset, list[UUID]]):
        customer_abbreviation (Union[Unset, str]):
        customer_name (Union[Unset, str]):
        customer_native_name (Union[Unset, str]):
        description (Union[Unset, str]):
        include_terminated (Union[Unset, bool]):
        is_removed (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, list[MarketplaceProviderCustomerProjectOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        slug (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            accounting_is_running=accounting_is_running,
            backend_id=backend_id,
            can_admin=can_admin,
            can_manage=can_manage,
            conceal_finished_projects=conceal_finished_projects,
            created=created,
            customer=customer,
            customer_abbreviation=customer_abbreviation,
            customer_name=customer_name,
            customer_native_name=customer_native_name,
            description=description,
            include_terminated=include_terminated,
            is_removed=is_removed,
            modified=modified,
            name=name,
            name_exact=name_exact,
            o=o,
            page=page,
            page_size=page_size,
            query=query,
            slug=slug,
            user_uuid=user_uuid,
        )
    ).parsed
