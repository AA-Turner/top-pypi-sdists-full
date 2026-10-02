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
    service_provider_uuid: UUID,
    *,
    affiliation_name: Union[Unset, str] = UNSET,
    affiliation_uuid: Union[Unset, list[UUID]] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    can_admin: Union[Unset, bool] = UNSET,
    can_manage: Union[Unset, bool] = UNSET,
    conceal_finished_projects: Union[Unset, bool] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    current_user_has_role: Union[Unset, list[str]] = UNSET,
    customer: Union[Unset, list[UUID]] = UNSET,
    customer_abbreviation: Union[Unset, str] = UNSET,
    customer_name: Union[Unset, str] = UNSET,
    customer_native_name: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    has_affiliation: Union[Unset, bool] = UNSET,
    is_removed: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[MarketplaceProviderCustomerProjectOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_customer_uuid: UUID,
    query: Union[Unset, str] = UNSET,
    science_domain_uuid: Union[Unset, UUID] = UNSET,
    science_sub_domain_uuid: Union[Unset, UUID] = UNSET,
    slug: Union[Unset, str] = UNSET,
    user_uuid_with_active_role: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["affiliation_name"] = affiliation_name

    json_affiliation_uuid: Union[Unset, list[str]] = UNSET
    if not isinstance(affiliation_uuid, Unset):
        json_affiliation_uuid = []
        for affiliation_uuid_item_data in affiliation_uuid:
            affiliation_uuid_item = str(affiliation_uuid_item_data)
            json_affiliation_uuid.append(affiliation_uuid_item)

    params["affiliation_uuid"] = json_affiliation_uuid

    params["backend_id"] = backend_id

    params["can_admin"] = can_admin

    params["can_manage"] = can_manage

    params["conceal_finished_projects"] = conceal_finished_projects

    json_created: Union[Unset, str] = UNSET
    if not isinstance(created, Unset):
        json_created = created.isoformat()
    params["created"] = json_created

    json_created_before: Union[Unset, str] = UNSET
    if not isinstance(created_before, Unset):
        json_created_before = created_before.isoformat()
    params["created_before"] = json_created_before

    json_current_user_has_role: Union[Unset, list[str]] = UNSET
    if not isinstance(current_user_has_role, Unset):
        json_current_user_has_role = current_user_has_role

    params["current_user_has_role"] = json_current_user_has_role

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

    params["has_affiliation"] = has_affiliation

    params["is_removed"] = is_removed

    json_modified: Union[Unset, str] = UNSET
    if not isinstance(modified, Unset):
        json_modified = modified.isoformat()
    params["modified"] = json_modified

    json_modified_before: Union[Unset, str] = UNSET
    if not isinstance(modified_before, Unset):
        json_modified_before = modified_before.isoformat()
    params["modified_before"] = json_modified_before

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

    json_project_customer_uuid = str(project_customer_uuid)
    params["project_customer_uuid"] = json_project_customer_uuid

    params["query"] = query

    json_science_domain_uuid: Union[Unset, str] = UNSET
    if not isinstance(science_domain_uuid, Unset):
        json_science_domain_uuid = str(science_domain_uuid)
    params["science_domain_uuid"] = json_science_domain_uuid

    json_science_sub_domain_uuid: Union[Unset, str] = UNSET
    if not isinstance(science_sub_domain_uuid, Unset):
        json_science_sub_domain_uuid = str(science_sub_domain_uuid)
    params["science_sub_domain_uuid"] = json_science_sub_domain_uuid

    params["slug"] = slug

    json_user_uuid_with_active_role: Union[Unset, str] = UNSET
    if not isinstance(user_uuid_with_active_role, Unset):
        json_user_uuid_with_active_role = str(user_uuid_with_active_role)
    params["user_uuid_with_active_role"] = json_user_uuid_with_active_role

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": f"/api/marketplace-service-providers/{service_provider_uuid}/customer_projects/",
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
    service_provider_uuid: UUID,
    *,
    client: AuthenticatedClient,
    affiliation_name: Union[Unset, str] = UNSET,
    affiliation_uuid: Union[Unset, list[UUID]] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    can_admin: Union[Unset, bool] = UNSET,
    can_manage: Union[Unset, bool] = UNSET,
    conceal_finished_projects: Union[Unset, bool] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    current_user_has_role: Union[Unset, list[str]] = UNSET,
    customer: Union[Unset, list[UUID]] = UNSET,
    customer_abbreviation: Union[Unset, str] = UNSET,
    customer_name: Union[Unset, str] = UNSET,
    customer_native_name: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    has_affiliation: Union[Unset, bool] = UNSET,
    is_removed: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[MarketplaceProviderCustomerProjectOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_customer_uuid: UUID,
    query: Union[Unset, str] = UNSET,
    science_domain_uuid: Union[Unset, UUID] = UNSET,
    science_sub_domain_uuid: Union[Unset, UUID] = UNSET,
    slug: Union[Unset, str] = UNSET,
    user_uuid_with_active_role: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """List customer projects of a service provider

     Get number of items in the collection matching the request parameters.

    Args:
        service_provider_uuid (UUID):
        affiliation_name (Union[Unset, str]):
        affiliation_uuid (Union[Unset, list[UUID]]):
        backend_id (Union[Unset, str]):
        can_admin (Union[Unset, bool]):
        can_manage (Union[Unset, bool]):
        conceal_finished_projects (Union[Unset, bool]):
        created (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        current_user_has_role (Union[Unset, list[str]]):
        customer (Union[Unset, list[UUID]]):
        customer_abbreviation (Union[Unset, str]):
        customer_name (Union[Unset, str]):
        customer_native_name (Union[Unset, str]):
        description (Union[Unset, str]):
        has_affiliation (Union[Unset, bool]):
        is_removed (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        modified_before (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, list[MarketplaceProviderCustomerProjectOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_customer_uuid (UUID):
        query (Union[Unset, str]):
        science_domain_uuid (Union[Unset, UUID]):
        science_sub_domain_uuid (Union[Unset, UUID]):
        slug (Union[Unset, str]):
        user_uuid_with_active_role (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        service_provider_uuid=service_provider_uuid,
        affiliation_name=affiliation_name,
        affiliation_uuid=affiliation_uuid,
        backend_id=backend_id,
        can_admin=can_admin,
        can_manage=can_manage,
        conceal_finished_projects=conceal_finished_projects,
        created=created,
        created_before=created_before,
        current_user_has_role=current_user_has_role,
        customer=customer,
        customer_abbreviation=customer_abbreviation,
        customer_name=customer_name,
        customer_native_name=customer_native_name,
        description=description,
        has_affiliation=has_affiliation,
        is_removed=is_removed,
        modified=modified,
        modified_before=modified_before,
        name=name,
        name_exact=name_exact,
        o=o,
        page=page,
        page_size=page_size,
        project_customer_uuid=project_customer_uuid,
        query=query,
        science_domain_uuid=science_domain_uuid,
        science_sub_domain_uuid=science_sub_domain_uuid,
        slug=slug,
        user_uuid_with_active_role=user_uuid_with_active_role,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    service_provider_uuid: UUID,
    *,
    client: AuthenticatedClient,
    affiliation_name: Union[Unset, str] = UNSET,
    affiliation_uuid: Union[Unset, list[UUID]] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    can_admin: Union[Unset, bool] = UNSET,
    can_manage: Union[Unset, bool] = UNSET,
    conceal_finished_projects: Union[Unset, bool] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    current_user_has_role: Union[Unset, list[str]] = UNSET,
    customer: Union[Unset, list[UUID]] = UNSET,
    customer_abbreviation: Union[Unset, str] = UNSET,
    customer_name: Union[Unset, str] = UNSET,
    customer_native_name: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    has_affiliation: Union[Unset, bool] = UNSET,
    is_removed: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[MarketplaceProviderCustomerProjectOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_customer_uuid: UUID,
    query: Union[Unset, str] = UNSET,
    science_domain_uuid: Union[Unset, UUID] = UNSET,
    science_sub_domain_uuid: Union[Unset, UUID] = UNSET,
    slug: Union[Unset, str] = UNSET,
    user_uuid_with_active_role: Union[Unset, UUID] = UNSET,
) -> int:
    """List customer projects of a service provider

     Get number of items in the collection matching the request parameters.

    Args:
        service_provider_uuid (UUID):
        affiliation_name (Union[Unset, str]):
        affiliation_uuid (Union[Unset, list[UUID]]):
        backend_id (Union[Unset, str]):
        can_admin (Union[Unset, bool]):
        can_manage (Union[Unset, bool]):
        conceal_finished_projects (Union[Unset, bool]):
        created (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        current_user_has_role (Union[Unset, list[str]]):
        customer (Union[Unset, list[UUID]]):
        customer_abbreviation (Union[Unset, str]):
        customer_name (Union[Unset, str]):
        customer_native_name (Union[Unset, str]):
        description (Union[Unset, str]):
        has_affiliation (Union[Unset, bool]):
        is_removed (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        modified_before (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, list[MarketplaceProviderCustomerProjectOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_customer_uuid (UUID):
        query (Union[Unset, str]):
        science_domain_uuid (Union[Unset, UUID]):
        science_sub_domain_uuid (Union[Unset, UUID]):
        slug (Union[Unset, str]):
        user_uuid_with_active_role (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        service_provider_uuid=service_provider_uuid,
        client=client,
        affiliation_name=affiliation_name,
        affiliation_uuid=affiliation_uuid,
        backend_id=backend_id,
        can_admin=can_admin,
        can_manage=can_manage,
        conceal_finished_projects=conceal_finished_projects,
        created=created,
        created_before=created_before,
        current_user_has_role=current_user_has_role,
        customer=customer,
        customer_abbreviation=customer_abbreviation,
        customer_name=customer_name,
        customer_native_name=customer_native_name,
        description=description,
        has_affiliation=has_affiliation,
        is_removed=is_removed,
        modified=modified,
        modified_before=modified_before,
        name=name,
        name_exact=name_exact,
        o=o,
        page=page,
        page_size=page_size,
        project_customer_uuid=project_customer_uuid,
        query=query,
        science_domain_uuid=science_domain_uuid,
        science_sub_domain_uuid=science_sub_domain_uuid,
        slug=slug,
        user_uuid_with_active_role=user_uuid_with_active_role,
    ).parsed


async def asyncio_detailed(
    service_provider_uuid: UUID,
    *,
    client: AuthenticatedClient,
    affiliation_name: Union[Unset, str] = UNSET,
    affiliation_uuid: Union[Unset, list[UUID]] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    can_admin: Union[Unset, bool] = UNSET,
    can_manage: Union[Unset, bool] = UNSET,
    conceal_finished_projects: Union[Unset, bool] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    current_user_has_role: Union[Unset, list[str]] = UNSET,
    customer: Union[Unset, list[UUID]] = UNSET,
    customer_abbreviation: Union[Unset, str] = UNSET,
    customer_name: Union[Unset, str] = UNSET,
    customer_native_name: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    has_affiliation: Union[Unset, bool] = UNSET,
    is_removed: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[MarketplaceProviderCustomerProjectOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_customer_uuid: UUID,
    query: Union[Unset, str] = UNSET,
    science_domain_uuid: Union[Unset, UUID] = UNSET,
    science_sub_domain_uuid: Union[Unset, UUID] = UNSET,
    slug: Union[Unset, str] = UNSET,
    user_uuid_with_active_role: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """List customer projects of a service provider

     Get number of items in the collection matching the request parameters.

    Args:
        service_provider_uuid (UUID):
        affiliation_name (Union[Unset, str]):
        affiliation_uuid (Union[Unset, list[UUID]]):
        backend_id (Union[Unset, str]):
        can_admin (Union[Unset, bool]):
        can_manage (Union[Unset, bool]):
        conceal_finished_projects (Union[Unset, bool]):
        created (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        current_user_has_role (Union[Unset, list[str]]):
        customer (Union[Unset, list[UUID]]):
        customer_abbreviation (Union[Unset, str]):
        customer_name (Union[Unset, str]):
        customer_native_name (Union[Unset, str]):
        description (Union[Unset, str]):
        has_affiliation (Union[Unset, bool]):
        is_removed (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        modified_before (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, list[MarketplaceProviderCustomerProjectOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_customer_uuid (UUID):
        query (Union[Unset, str]):
        science_domain_uuid (Union[Unset, UUID]):
        science_sub_domain_uuid (Union[Unset, UUID]):
        slug (Union[Unset, str]):
        user_uuid_with_active_role (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        service_provider_uuid=service_provider_uuid,
        affiliation_name=affiliation_name,
        affiliation_uuid=affiliation_uuid,
        backend_id=backend_id,
        can_admin=can_admin,
        can_manage=can_manage,
        conceal_finished_projects=conceal_finished_projects,
        created=created,
        created_before=created_before,
        current_user_has_role=current_user_has_role,
        customer=customer,
        customer_abbreviation=customer_abbreviation,
        customer_name=customer_name,
        customer_native_name=customer_native_name,
        description=description,
        has_affiliation=has_affiliation,
        is_removed=is_removed,
        modified=modified,
        modified_before=modified_before,
        name=name,
        name_exact=name_exact,
        o=o,
        page=page,
        page_size=page_size,
        project_customer_uuid=project_customer_uuid,
        query=query,
        science_domain_uuid=science_domain_uuid,
        science_sub_domain_uuid=science_sub_domain_uuid,
        slug=slug,
        user_uuid_with_active_role=user_uuid_with_active_role,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_provider_uuid: UUID,
    *,
    client: AuthenticatedClient,
    affiliation_name: Union[Unset, str] = UNSET,
    affiliation_uuid: Union[Unset, list[UUID]] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    can_admin: Union[Unset, bool] = UNSET,
    can_manage: Union[Unset, bool] = UNSET,
    conceal_finished_projects: Union[Unset, bool] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    current_user_has_role: Union[Unset, list[str]] = UNSET,
    customer: Union[Unset, list[UUID]] = UNSET,
    customer_abbreviation: Union[Unset, str] = UNSET,
    customer_name: Union[Unset, str] = UNSET,
    customer_native_name: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    has_affiliation: Union[Unset, bool] = UNSET,
    is_removed: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[MarketplaceProviderCustomerProjectOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_customer_uuid: UUID,
    query: Union[Unset, str] = UNSET,
    science_domain_uuid: Union[Unset, UUID] = UNSET,
    science_sub_domain_uuid: Union[Unset, UUID] = UNSET,
    slug: Union[Unset, str] = UNSET,
    user_uuid_with_active_role: Union[Unset, UUID] = UNSET,
) -> int:
    """List customer projects of a service provider

     Get number of items in the collection matching the request parameters.

    Args:
        service_provider_uuid (UUID):
        affiliation_name (Union[Unset, str]):
        affiliation_uuid (Union[Unset, list[UUID]]):
        backend_id (Union[Unset, str]):
        can_admin (Union[Unset, bool]):
        can_manage (Union[Unset, bool]):
        conceal_finished_projects (Union[Unset, bool]):
        created (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        current_user_has_role (Union[Unset, list[str]]):
        customer (Union[Unset, list[UUID]]):
        customer_abbreviation (Union[Unset, str]):
        customer_name (Union[Unset, str]):
        customer_native_name (Union[Unset, str]):
        description (Union[Unset, str]):
        has_affiliation (Union[Unset, bool]):
        is_removed (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        modified_before (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, list[MarketplaceProviderCustomerProjectOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_customer_uuid (UUID):
        query (Union[Unset, str]):
        science_domain_uuid (Union[Unset, UUID]):
        science_sub_domain_uuid (Union[Unset, UUID]):
        slug (Union[Unset, str]):
        user_uuid_with_active_role (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            service_provider_uuid=service_provider_uuid,
            client=client,
            affiliation_name=affiliation_name,
            affiliation_uuid=affiliation_uuid,
            backend_id=backend_id,
            can_admin=can_admin,
            can_manage=can_manage,
            conceal_finished_projects=conceal_finished_projects,
            created=created,
            created_before=created_before,
            current_user_has_role=current_user_has_role,
            customer=customer,
            customer_abbreviation=customer_abbreviation,
            customer_name=customer_name,
            customer_native_name=customer_native_name,
            description=description,
            has_affiliation=has_affiliation,
            is_removed=is_removed,
            modified=modified,
            modified_before=modified_before,
            name=name,
            name_exact=name_exact,
            o=o,
            page=page,
            page_size=page_size,
            project_customer_uuid=project_customer_uuid,
            query=query,
            science_domain_uuid=science_domain_uuid,
            science_sub_domain_uuid=science_sub_domain_uuid,
            slug=slug,
            user_uuid_with_active_role=user_uuid_with_active_role,
        )
    ).parsed
