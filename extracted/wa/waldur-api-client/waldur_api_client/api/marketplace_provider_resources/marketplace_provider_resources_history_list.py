import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.order_state import OrderState
from ...models.resource_o_enum import ResourceOEnum
from ...models.resource_state import ResourceState
from ...models.version_history import VersionHistory
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    uuid: UUID,
    *,
    backend_id: Union[Unset, str] = UNSET,
    category_uuid: Union[Unset, UUID] = UNSET,
    component_count: Union[Unset, float] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, str] = UNSET,
    created_before: Union[Unset, str] = UNSET,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    downscaled: Union[Unset, bool] = UNSET,
    has_terminate_date: Union[Unset, bool] = UNSET,
    is_attached: Union[Unset, bool] = UNSET,
    lexis_links_supported: Union[Unset, bool] = UNSET,
    limit_based: Union[Unset, bool] = UNSET,
    limit_component_count: Union[Unset, float] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ResourceOEnum]] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_billable: Union[Unset, bool] = UNSET,
    offering_shared: Union[Unset, bool] = UNSET,
    offering_slug: Union[Unset, list[str]] = UNSET,
    offering_type: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, list[UUID]] = UNSET,
    only_limit_based: Union[Unset, bool] = UNSET,
    only_usage_based: Union[Unset, bool] = UNSET,
    order_state: Union[Unset, list[OrderState]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_offering_uuid: Union[Unset, UUID] = UNSET,
    paused: Union[Unset, bool] = UNSET,
    plan_uuid: Union[Unset, UUID] = UNSET,
    project_name: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    restrict_member_access: Union[Unset, bool] = UNSET,
    runtime_state: Union[Unset, str] = UNSET,
    scope: Union[Unset, str] = UNSET,
    service_manager_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ResourceState]] = UNSET,
    usage_based: Union[Unset, bool] = UNSET,
    visible_to_providers: Union[Unset, bool] = UNSET,
    visible_to_username: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["backend_id"] = backend_id

    json_category_uuid: Union[Unset, str] = UNSET
    if not isinstance(category_uuid, Unset):
        json_category_uuid = str(category_uuid)
    params["category_uuid"] = json_category_uuid

    params["component_count"] = component_count

    json_created: Union[Unset, str] = UNSET
    if not isinstance(created, Unset):
        json_created = created.isoformat()
    params["created"] = json_created

    params["created_after"] = created_after

    params["created_before"] = created_before

    params["customer"] = customer

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    params["downscaled"] = downscaled

    params["has_terminate_date"] = has_terminate_date

    params["is_attached"] = is_attached

    params["lexis_links_supported"] = lexis_links_supported

    params["limit_based"] = limit_based

    params["limit_component_count"] = limit_component_count

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

    params["offering"] = offering

    params["offering_billable"] = offering_billable

    params["offering_shared"] = offering_shared

    json_offering_slug: Union[Unset, list[str]] = UNSET
    if not isinstance(offering_slug, Unset):
        json_offering_slug = offering_slug

    params["offering_slug"] = json_offering_slug

    params["offering_type"] = offering_type

    json_offering_uuid: Union[Unset, list[str]] = UNSET
    if not isinstance(offering_uuid, Unset):
        json_offering_uuid = []
        for offering_uuid_item_data in offering_uuid:
            offering_uuid_item = str(offering_uuid_item_data)
            json_offering_uuid.append(offering_uuid_item)

    params["offering_uuid"] = json_offering_uuid

    params["only_limit_based"] = only_limit_based

    params["only_usage_based"] = only_usage_based

    json_order_state: Union[Unset, list[str]] = UNSET
    if not isinstance(order_state, Unset):
        json_order_state = []
        for order_state_item_data in order_state:
            order_state_item = order_state_item_data.value
            json_order_state.append(order_state_item)

    params["order_state"] = json_order_state

    params["page"] = page

    params["page_size"] = page_size

    json_parent_offering_uuid: Union[Unset, str] = UNSET
    if not isinstance(parent_offering_uuid, Unset):
        json_parent_offering_uuid = str(parent_offering_uuid)
    params["parent_offering_uuid"] = json_parent_offering_uuid

    params["paused"] = paused

    json_plan_uuid: Union[Unset, str] = UNSET
    if not isinstance(plan_uuid, Unset):
        json_plan_uuid = str(plan_uuid)
    params["plan_uuid"] = json_plan_uuid

    params["project_name"] = project_name

    json_project_uuid: Union[Unset, str] = UNSET
    if not isinstance(project_uuid, Unset):
        json_project_uuid = str(project_uuid)
    params["project_uuid"] = json_project_uuid

    json_provider_uuid: Union[Unset, str] = UNSET
    if not isinstance(provider_uuid, Unset):
        json_provider_uuid = str(provider_uuid)
    params["provider_uuid"] = json_provider_uuid

    params["query"] = query

    params["restrict_member_access"] = restrict_member_access

    params["runtime_state"] = runtime_state

    params["scope"] = scope

    json_service_manager_uuid: Union[Unset, str] = UNSET
    if not isinstance(service_manager_uuid, Unset):
        json_service_manager_uuid = str(service_manager_uuid)
    params["service_manager_uuid"] = json_service_manager_uuid

    json_state: Union[Unset, list[str]] = UNSET
    if not isinstance(state, Unset):
        json_state = []
        for state_item_data in state:
            state_item = state_item_data.value
            json_state.append(state_item)

    params["state"] = json_state

    params["usage_based"] = usage_based

    params["visible_to_providers"] = visible_to_providers

    params["visible_to_username"] = visible_to_username

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/marketplace-provider-resources/{uuid}/history/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["VersionHistory"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = VersionHistory.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["VersionHistory"]]:
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
    backend_id: Union[Unset, str] = UNSET,
    category_uuid: Union[Unset, UUID] = UNSET,
    component_count: Union[Unset, float] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, str] = UNSET,
    created_before: Union[Unset, str] = UNSET,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    downscaled: Union[Unset, bool] = UNSET,
    has_terminate_date: Union[Unset, bool] = UNSET,
    is_attached: Union[Unset, bool] = UNSET,
    lexis_links_supported: Union[Unset, bool] = UNSET,
    limit_based: Union[Unset, bool] = UNSET,
    limit_component_count: Union[Unset, float] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ResourceOEnum]] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_billable: Union[Unset, bool] = UNSET,
    offering_shared: Union[Unset, bool] = UNSET,
    offering_slug: Union[Unset, list[str]] = UNSET,
    offering_type: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, list[UUID]] = UNSET,
    only_limit_based: Union[Unset, bool] = UNSET,
    only_usage_based: Union[Unset, bool] = UNSET,
    order_state: Union[Unset, list[OrderState]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_offering_uuid: Union[Unset, UUID] = UNSET,
    paused: Union[Unset, bool] = UNSET,
    plan_uuid: Union[Unset, UUID] = UNSET,
    project_name: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    restrict_member_access: Union[Unset, bool] = UNSET,
    runtime_state: Union[Unset, str] = UNSET,
    scope: Union[Unset, str] = UNSET,
    service_manager_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ResourceState]] = UNSET,
    usage_based: Union[Unset, bool] = UNSET,
    visible_to_providers: Union[Unset, bool] = UNSET,
    visible_to_username: Union[Unset, str] = UNSET,
) -> Response[list["VersionHistory"]]:
    """Get version history

     Returns the version history for this object. Only accessible by staff and support users.

    Args:
        uuid (UUID):
        backend_id (Union[Unset, str]):
        category_uuid (Union[Unset, UUID]):
        component_count (Union[Unset, float]):
        created (Union[Unset, datetime.datetime]):
        created_after (Union[Unset, str]):
        created_before (Union[Unset, str]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        downscaled (Union[Unset, bool]):
        has_terminate_date (Union[Unset, bool]):
        is_attached (Union[Unset, bool]):
        lexis_links_supported (Union[Unset, bool]):
        limit_based (Union[Unset, bool]):
        limit_component_count (Union[Unset, float]):
        modified (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, list[ResourceOEnum]]):
        offering (Union[Unset, str]):
        offering_billable (Union[Unset, bool]):
        offering_shared (Union[Unset, bool]):
        offering_slug (Union[Unset, list[str]]):
        offering_type (Union[Unset, str]):
        offering_uuid (Union[Unset, list[UUID]]):
        only_limit_based (Union[Unset, bool]):
        only_usage_based (Union[Unset, bool]):
        order_state (Union[Unset, list[OrderState]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_offering_uuid (Union[Unset, UUID]):
        paused (Union[Unset, bool]):
        plan_uuid (Union[Unset, UUID]):
        project_name (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        provider_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        restrict_member_access (Union[Unset, bool]):
        runtime_state (Union[Unset, str]):
        scope (Union[Unset, str]):
        service_manager_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[ResourceState]]):
        usage_based (Union[Unset, bool]):
        visible_to_providers (Union[Unset, bool]):
        visible_to_username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VersionHistory']]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        backend_id=backend_id,
        category_uuid=category_uuid,
        component_count=component_count,
        created=created,
        created_after=created_after,
        created_before=created_before,
        customer=customer,
        customer_uuid=customer_uuid,
        downscaled=downscaled,
        has_terminate_date=has_terminate_date,
        is_attached=is_attached,
        lexis_links_supported=lexis_links_supported,
        limit_based=limit_based,
        limit_component_count=limit_component_count,
        modified=modified,
        name=name,
        name_exact=name_exact,
        o=o,
        offering=offering,
        offering_billable=offering_billable,
        offering_shared=offering_shared,
        offering_slug=offering_slug,
        offering_type=offering_type,
        offering_uuid=offering_uuid,
        only_limit_based=only_limit_based,
        only_usage_based=only_usage_based,
        order_state=order_state,
        page=page,
        page_size=page_size,
        parent_offering_uuid=parent_offering_uuid,
        paused=paused,
        plan_uuid=plan_uuid,
        project_name=project_name,
        project_uuid=project_uuid,
        provider_uuid=provider_uuid,
        query=query,
        restrict_member_access=restrict_member_access,
        runtime_state=runtime_state,
        scope=scope,
        service_manager_uuid=service_manager_uuid,
        state=state,
        usage_based=usage_based,
        visible_to_providers=visible_to_providers,
        visible_to_username=visible_to_username,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    backend_id: Union[Unset, str] = UNSET,
    category_uuid: Union[Unset, UUID] = UNSET,
    component_count: Union[Unset, float] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, str] = UNSET,
    created_before: Union[Unset, str] = UNSET,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    downscaled: Union[Unset, bool] = UNSET,
    has_terminate_date: Union[Unset, bool] = UNSET,
    is_attached: Union[Unset, bool] = UNSET,
    lexis_links_supported: Union[Unset, bool] = UNSET,
    limit_based: Union[Unset, bool] = UNSET,
    limit_component_count: Union[Unset, float] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ResourceOEnum]] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_billable: Union[Unset, bool] = UNSET,
    offering_shared: Union[Unset, bool] = UNSET,
    offering_slug: Union[Unset, list[str]] = UNSET,
    offering_type: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, list[UUID]] = UNSET,
    only_limit_based: Union[Unset, bool] = UNSET,
    only_usage_based: Union[Unset, bool] = UNSET,
    order_state: Union[Unset, list[OrderState]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_offering_uuid: Union[Unset, UUID] = UNSET,
    paused: Union[Unset, bool] = UNSET,
    plan_uuid: Union[Unset, UUID] = UNSET,
    project_name: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    restrict_member_access: Union[Unset, bool] = UNSET,
    runtime_state: Union[Unset, str] = UNSET,
    scope: Union[Unset, str] = UNSET,
    service_manager_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ResourceState]] = UNSET,
    usage_based: Union[Unset, bool] = UNSET,
    visible_to_providers: Union[Unset, bool] = UNSET,
    visible_to_username: Union[Unset, str] = UNSET,
) -> list["VersionHistory"]:
    """Get version history

     Returns the version history for this object. Only accessible by staff and support users.

    Args:
        uuid (UUID):
        backend_id (Union[Unset, str]):
        category_uuid (Union[Unset, UUID]):
        component_count (Union[Unset, float]):
        created (Union[Unset, datetime.datetime]):
        created_after (Union[Unset, str]):
        created_before (Union[Unset, str]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        downscaled (Union[Unset, bool]):
        has_terminate_date (Union[Unset, bool]):
        is_attached (Union[Unset, bool]):
        lexis_links_supported (Union[Unset, bool]):
        limit_based (Union[Unset, bool]):
        limit_component_count (Union[Unset, float]):
        modified (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, list[ResourceOEnum]]):
        offering (Union[Unset, str]):
        offering_billable (Union[Unset, bool]):
        offering_shared (Union[Unset, bool]):
        offering_slug (Union[Unset, list[str]]):
        offering_type (Union[Unset, str]):
        offering_uuid (Union[Unset, list[UUID]]):
        only_limit_based (Union[Unset, bool]):
        only_usage_based (Union[Unset, bool]):
        order_state (Union[Unset, list[OrderState]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_offering_uuid (Union[Unset, UUID]):
        paused (Union[Unset, bool]):
        plan_uuid (Union[Unset, UUID]):
        project_name (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        provider_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        restrict_member_access (Union[Unset, bool]):
        runtime_state (Union[Unset, str]):
        scope (Union[Unset, str]):
        service_manager_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[ResourceState]]):
        usage_based (Union[Unset, bool]):
        visible_to_providers (Union[Unset, bool]):
        visible_to_username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VersionHistory']
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        backend_id=backend_id,
        category_uuid=category_uuid,
        component_count=component_count,
        created=created,
        created_after=created_after,
        created_before=created_before,
        customer=customer,
        customer_uuid=customer_uuid,
        downscaled=downscaled,
        has_terminate_date=has_terminate_date,
        is_attached=is_attached,
        lexis_links_supported=lexis_links_supported,
        limit_based=limit_based,
        limit_component_count=limit_component_count,
        modified=modified,
        name=name,
        name_exact=name_exact,
        o=o,
        offering=offering,
        offering_billable=offering_billable,
        offering_shared=offering_shared,
        offering_slug=offering_slug,
        offering_type=offering_type,
        offering_uuid=offering_uuid,
        only_limit_based=only_limit_based,
        only_usage_based=only_usage_based,
        order_state=order_state,
        page=page,
        page_size=page_size,
        parent_offering_uuid=parent_offering_uuid,
        paused=paused,
        plan_uuid=plan_uuid,
        project_name=project_name,
        project_uuid=project_uuid,
        provider_uuid=provider_uuid,
        query=query,
        restrict_member_access=restrict_member_access,
        runtime_state=runtime_state,
        scope=scope,
        service_manager_uuid=service_manager_uuid,
        state=state,
        usage_based=usage_based,
        visible_to_providers=visible_to_providers,
        visible_to_username=visible_to_username,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    backend_id: Union[Unset, str] = UNSET,
    category_uuid: Union[Unset, UUID] = UNSET,
    component_count: Union[Unset, float] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, str] = UNSET,
    created_before: Union[Unset, str] = UNSET,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    downscaled: Union[Unset, bool] = UNSET,
    has_terminate_date: Union[Unset, bool] = UNSET,
    is_attached: Union[Unset, bool] = UNSET,
    lexis_links_supported: Union[Unset, bool] = UNSET,
    limit_based: Union[Unset, bool] = UNSET,
    limit_component_count: Union[Unset, float] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ResourceOEnum]] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_billable: Union[Unset, bool] = UNSET,
    offering_shared: Union[Unset, bool] = UNSET,
    offering_slug: Union[Unset, list[str]] = UNSET,
    offering_type: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, list[UUID]] = UNSET,
    only_limit_based: Union[Unset, bool] = UNSET,
    only_usage_based: Union[Unset, bool] = UNSET,
    order_state: Union[Unset, list[OrderState]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_offering_uuid: Union[Unset, UUID] = UNSET,
    paused: Union[Unset, bool] = UNSET,
    plan_uuid: Union[Unset, UUID] = UNSET,
    project_name: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    restrict_member_access: Union[Unset, bool] = UNSET,
    runtime_state: Union[Unset, str] = UNSET,
    scope: Union[Unset, str] = UNSET,
    service_manager_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ResourceState]] = UNSET,
    usage_based: Union[Unset, bool] = UNSET,
    visible_to_providers: Union[Unset, bool] = UNSET,
    visible_to_username: Union[Unset, str] = UNSET,
) -> Response[list["VersionHistory"]]:
    """Get version history

     Returns the version history for this object. Only accessible by staff and support users.

    Args:
        uuid (UUID):
        backend_id (Union[Unset, str]):
        category_uuid (Union[Unset, UUID]):
        component_count (Union[Unset, float]):
        created (Union[Unset, datetime.datetime]):
        created_after (Union[Unset, str]):
        created_before (Union[Unset, str]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        downscaled (Union[Unset, bool]):
        has_terminate_date (Union[Unset, bool]):
        is_attached (Union[Unset, bool]):
        lexis_links_supported (Union[Unset, bool]):
        limit_based (Union[Unset, bool]):
        limit_component_count (Union[Unset, float]):
        modified (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, list[ResourceOEnum]]):
        offering (Union[Unset, str]):
        offering_billable (Union[Unset, bool]):
        offering_shared (Union[Unset, bool]):
        offering_slug (Union[Unset, list[str]]):
        offering_type (Union[Unset, str]):
        offering_uuid (Union[Unset, list[UUID]]):
        only_limit_based (Union[Unset, bool]):
        only_usage_based (Union[Unset, bool]):
        order_state (Union[Unset, list[OrderState]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_offering_uuid (Union[Unset, UUID]):
        paused (Union[Unset, bool]):
        plan_uuid (Union[Unset, UUID]):
        project_name (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        provider_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        restrict_member_access (Union[Unset, bool]):
        runtime_state (Union[Unset, str]):
        scope (Union[Unset, str]):
        service_manager_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[ResourceState]]):
        usage_based (Union[Unset, bool]):
        visible_to_providers (Union[Unset, bool]):
        visible_to_username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VersionHistory']]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        backend_id=backend_id,
        category_uuid=category_uuid,
        component_count=component_count,
        created=created,
        created_after=created_after,
        created_before=created_before,
        customer=customer,
        customer_uuid=customer_uuid,
        downscaled=downscaled,
        has_terminate_date=has_terminate_date,
        is_attached=is_attached,
        lexis_links_supported=lexis_links_supported,
        limit_based=limit_based,
        limit_component_count=limit_component_count,
        modified=modified,
        name=name,
        name_exact=name_exact,
        o=o,
        offering=offering,
        offering_billable=offering_billable,
        offering_shared=offering_shared,
        offering_slug=offering_slug,
        offering_type=offering_type,
        offering_uuid=offering_uuid,
        only_limit_based=only_limit_based,
        only_usage_based=only_usage_based,
        order_state=order_state,
        page=page,
        page_size=page_size,
        parent_offering_uuid=parent_offering_uuid,
        paused=paused,
        plan_uuid=plan_uuid,
        project_name=project_name,
        project_uuid=project_uuid,
        provider_uuid=provider_uuid,
        query=query,
        restrict_member_access=restrict_member_access,
        runtime_state=runtime_state,
        scope=scope,
        service_manager_uuid=service_manager_uuid,
        state=state,
        usage_based=usage_based,
        visible_to_providers=visible_to_providers,
        visible_to_username=visible_to_username,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    backend_id: Union[Unset, str] = UNSET,
    category_uuid: Union[Unset, UUID] = UNSET,
    component_count: Union[Unset, float] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, str] = UNSET,
    created_before: Union[Unset, str] = UNSET,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    downscaled: Union[Unset, bool] = UNSET,
    has_terminate_date: Union[Unset, bool] = UNSET,
    is_attached: Union[Unset, bool] = UNSET,
    lexis_links_supported: Union[Unset, bool] = UNSET,
    limit_based: Union[Unset, bool] = UNSET,
    limit_component_count: Union[Unset, float] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ResourceOEnum]] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_billable: Union[Unset, bool] = UNSET,
    offering_shared: Union[Unset, bool] = UNSET,
    offering_slug: Union[Unset, list[str]] = UNSET,
    offering_type: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, list[UUID]] = UNSET,
    only_limit_based: Union[Unset, bool] = UNSET,
    only_usage_based: Union[Unset, bool] = UNSET,
    order_state: Union[Unset, list[OrderState]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_offering_uuid: Union[Unset, UUID] = UNSET,
    paused: Union[Unset, bool] = UNSET,
    plan_uuid: Union[Unset, UUID] = UNSET,
    project_name: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    restrict_member_access: Union[Unset, bool] = UNSET,
    runtime_state: Union[Unset, str] = UNSET,
    scope: Union[Unset, str] = UNSET,
    service_manager_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ResourceState]] = UNSET,
    usage_based: Union[Unset, bool] = UNSET,
    visible_to_providers: Union[Unset, bool] = UNSET,
    visible_to_username: Union[Unset, str] = UNSET,
) -> list["VersionHistory"]:
    """Get version history

     Returns the version history for this object. Only accessible by staff and support users.

    Args:
        uuid (UUID):
        backend_id (Union[Unset, str]):
        category_uuid (Union[Unset, UUID]):
        component_count (Union[Unset, float]):
        created (Union[Unset, datetime.datetime]):
        created_after (Union[Unset, str]):
        created_before (Union[Unset, str]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        downscaled (Union[Unset, bool]):
        has_terminate_date (Union[Unset, bool]):
        is_attached (Union[Unset, bool]):
        lexis_links_supported (Union[Unset, bool]):
        limit_based (Union[Unset, bool]):
        limit_component_count (Union[Unset, float]):
        modified (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, list[ResourceOEnum]]):
        offering (Union[Unset, str]):
        offering_billable (Union[Unset, bool]):
        offering_shared (Union[Unset, bool]):
        offering_slug (Union[Unset, list[str]]):
        offering_type (Union[Unset, str]):
        offering_uuid (Union[Unset, list[UUID]]):
        only_limit_based (Union[Unset, bool]):
        only_usage_based (Union[Unset, bool]):
        order_state (Union[Unset, list[OrderState]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_offering_uuid (Union[Unset, UUID]):
        paused (Union[Unset, bool]):
        plan_uuid (Union[Unset, UUID]):
        project_name (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        provider_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        restrict_member_access (Union[Unset, bool]):
        runtime_state (Union[Unset, str]):
        scope (Union[Unset, str]):
        service_manager_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[ResourceState]]):
        usage_based (Union[Unset, bool]):
        visible_to_providers (Union[Unset, bool]):
        visible_to_username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VersionHistory']
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            backend_id=backend_id,
            category_uuid=category_uuid,
            component_count=component_count,
            created=created,
            created_after=created_after,
            created_before=created_before,
            customer=customer,
            customer_uuid=customer_uuid,
            downscaled=downscaled,
            has_terminate_date=has_terminate_date,
            is_attached=is_attached,
            lexis_links_supported=lexis_links_supported,
            limit_based=limit_based,
            limit_component_count=limit_component_count,
            modified=modified,
            name=name,
            name_exact=name_exact,
            o=o,
            offering=offering,
            offering_billable=offering_billable,
            offering_shared=offering_shared,
            offering_slug=offering_slug,
            offering_type=offering_type,
            offering_uuid=offering_uuid,
            only_limit_based=only_limit_based,
            only_usage_based=only_usage_based,
            order_state=order_state,
            page=page,
            page_size=page_size,
            parent_offering_uuid=parent_offering_uuid,
            paused=paused,
            plan_uuid=plan_uuid,
            project_name=project_name,
            project_uuid=project_uuid,
            provider_uuid=provider_uuid,
            query=query,
            restrict_member_access=restrict_member_access,
            runtime_state=runtime_state,
            scope=scope,
            service_manager_uuid=service_manager_uuid,
            state=state,
            usage_based=usage_based,
            visible_to_providers=visible_to_providers,
            visible_to_username=visible_to_username,
        )
    ).parsed


def sync_all(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    backend_id: Union[Unset, str] = UNSET,
    category_uuid: Union[Unset, UUID] = UNSET,
    component_count: Union[Unset, float] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, str] = UNSET,
    created_before: Union[Unset, str] = UNSET,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    downscaled: Union[Unset, bool] = UNSET,
    has_terminate_date: Union[Unset, bool] = UNSET,
    is_attached: Union[Unset, bool] = UNSET,
    lexis_links_supported: Union[Unset, bool] = UNSET,
    limit_based: Union[Unset, bool] = UNSET,
    limit_component_count: Union[Unset, float] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ResourceOEnum]] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_billable: Union[Unset, bool] = UNSET,
    offering_shared: Union[Unset, bool] = UNSET,
    offering_slug: Union[Unset, list[str]] = UNSET,
    offering_type: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, list[UUID]] = UNSET,
    only_limit_based: Union[Unset, bool] = UNSET,
    only_usage_based: Union[Unset, bool] = UNSET,
    order_state: Union[Unset, list[OrderState]] = UNSET,
    parent_offering_uuid: Union[Unset, UUID] = UNSET,
    paused: Union[Unset, bool] = UNSET,
    plan_uuid: Union[Unset, UUID] = UNSET,
    project_name: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    restrict_member_access: Union[Unset, bool] = UNSET,
    runtime_state: Union[Unset, str] = UNSET,
    scope: Union[Unset, str] = UNSET,
    service_manager_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ResourceState]] = UNSET,
    usage_based: Union[Unset, bool] = UNSET,
    visible_to_providers: Union[Unset, bool] = UNSET,
    visible_to_username: Union[Unset, str] = UNSET,
) -> list["VersionHistory"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        uuid (UUID):
        backend_id (Union[Unset, str]):
        category_uuid (Union[Unset, UUID]):
        component_count (Union[Unset, float]):
        created (Union[Unset, datetime.datetime]):
        created_after (Union[Unset, str]):
        created_before (Union[Unset, str]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        downscaled (Union[Unset, bool]):
        has_terminate_date (Union[Unset, bool]):
        is_attached (Union[Unset, bool]):
        lexis_links_supported (Union[Unset, bool]):
        limit_based (Union[Unset, bool]):
        limit_component_count (Union[Unset, float]):
        modified (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, list[ResourceOEnum]]):
        offering (Union[Unset, str]):
        offering_billable (Union[Unset, bool]):
        offering_shared (Union[Unset, bool]):
        offering_slug (Union[Unset, list[str]]):
        offering_type (Union[Unset, str]):
        offering_uuid (Union[Unset, list[UUID]]):
        only_limit_based (Union[Unset, bool]):
        only_usage_based (Union[Unset, bool]):
        order_state (Union[Unset, list[OrderState]]):
        parent_offering_uuid (Union[Unset, UUID]):
        paused (Union[Unset, bool]):
        plan_uuid (Union[Unset, UUID]):
        project_name (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        provider_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        restrict_member_access (Union[Unset, bool]):
        runtime_state (Union[Unset, str]):
        scope (Union[Unset, str]):
        service_manager_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[ResourceState]]):
        usage_based (Union[Unset, bool]):
        visible_to_providers (Union[Unset, bool]):
        visible_to_username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VersionHistory']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[VersionHistory] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        uuid=uuid,
        backend_id=backend_id,
        category_uuid=category_uuid,
        component_count=component_count,
        created=created,
        created_after=created_after,
        created_before=created_before,
        customer=customer,
        customer_uuid=customer_uuid,
        downscaled=downscaled,
        has_terminate_date=has_terminate_date,
        is_attached=is_attached,
        lexis_links_supported=lexis_links_supported,
        limit_based=limit_based,
        limit_component_count=limit_component_count,
        modified=modified,
        name=name,
        name_exact=name_exact,
        o=o,
        offering=offering,
        offering_billable=offering_billable,
        offering_shared=offering_shared,
        offering_slug=offering_slug,
        offering_type=offering_type,
        offering_uuid=offering_uuid,
        only_limit_based=only_limit_based,
        only_usage_based=only_usage_based,
        order_state=order_state,
        parent_offering_uuid=parent_offering_uuid,
        paused=paused,
        plan_uuid=plan_uuid,
        project_name=project_name,
        project_uuid=project_uuid,
        provider_uuid=provider_uuid,
        query=query,
        restrict_member_access=restrict_member_access,
        runtime_state=runtime_state,
        scope=scope,
        service_manager_uuid=service_manager_uuid,
        state=state,
        usage_based=usage_based,
        visible_to_providers=visible_to_providers,
        visible_to_username=visible_to_username,
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
    backend_id: Union[Unset, str] = UNSET,
    category_uuid: Union[Unset, UUID] = UNSET,
    component_count: Union[Unset, float] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, str] = UNSET,
    created_before: Union[Unset, str] = UNSET,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    downscaled: Union[Unset, bool] = UNSET,
    has_terminate_date: Union[Unset, bool] = UNSET,
    is_attached: Union[Unset, bool] = UNSET,
    lexis_links_supported: Union[Unset, bool] = UNSET,
    limit_based: Union[Unset, bool] = UNSET,
    limit_component_count: Union[Unset, float] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ResourceOEnum]] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_billable: Union[Unset, bool] = UNSET,
    offering_shared: Union[Unset, bool] = UNSET,
    offering_slug: Union[Unset, list[str]] = UNSET,
    offering_type: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, list[UUID]] = UNSET,
    only_limit_based: Union[Unset, bool] = UNSET,
    only_usage_based: Union[Unset, bool] = UNSET,
    order_state: Union[Unset, list[OrderState]] = UNSET,
    parent_offering_uuid: Union[Unset, UUID] = UNSET,
    paused: Union[Unset, bool] = UNSET,
    plan_uuid: Union[Unset, UUID] = UNSET,
    project_name: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    restrict_member_access: Union[Unset, bool] = UNSET,
    runtime_state: Union[Unset, str] = UNSET,
    scope: Union[Unset, str] = UNSET,
    service_manager_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ResourceState]] = UNSET,
    usage_based: Union[Unset, bool] = UNSET,
    visible_to_providers: Union[Unset, bool] = UNSET,
    visible_to_username: Union[Unset, str] = UNSET,
) -> list["VersionHistory"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        uuid (UUID):
        backend_id (Union[Unset, str]):
        category_uuid (Union[Unset, UUID]):
        component_count (Union[Unset, float]):
        created (Union[Unset, datetime.datetime]):
        created_after (Union[Unset, str]):
        created_before (Union[Unset, str]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        downscaled (Union[Unset, bool]):
        has_terminate_date (Union[Unset, bool]):
        is_attached (Union[Unset, bool]):
        lexis_links_supported (Union[Unset, bool]):
        limit_based (Union[Unset, bool]):
        limit_component_count (Union[Unset, float]):
        modified (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, list[ResourceOEnum]]):
        offering (Union[Unset, str]):
        offering_billable (Union[Unset, bool]):
        offering_shared (Union[Unset, bool]):
        offering_slug (Union[Unset, list[str]]):
        offering_type (Union[Unset, str]):
        offering_uuid (Union[Unset, list[UUID]]):
        only_limit_based (Union[Unset, bool]):
        only_usage_based (Union[Unset, bool]):
        order_state (Union[Unset, list[OrderState]]):
        parent_offering_uuid (Union[Unset, UUID]):
        paused (Union[Unset, bool]):
        plan_uuid (Union[Unset, UUID]):
        project_name (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        provider_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        restrict_member_access (Union[Unset, bool]):
        runtime_state (Union[Unset, str]):
        scope (Union[Unset, str]):
        service_manager_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[ResourceState]]):
        usage_based (Union[Unset, bool]):
        visible_to_providers (Union[Unset, bool]):
        visible_to_username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VersionHistory']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[VersionHistory] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        uuid=uuid,
        backend_id=backend_id,
        category_uuid=category_uuid,
        component_count=component_count,
        created=created,
        created_after=created_after,
        created_before=created_before,
        customer=customer,
        customer_uuid=customer_uuid,
        downscaled=downscaled,
        has_terminate_date=has_terminate_date,
        is_attached=is_attached,
        lexis_links_supported=lexis_links_supported,
        limit_based=limit_based,
        limit_component_count=limit_component_count,
        modified=modified,
        name=name,
        name_exact=name_exact,
        o=o,
        offering=offering,
        offering_billable=offering_billable,
        offering_shared=offering_shared,
        offering_slug=offering_slug,
        offering_type=offering_type,
        offering_uuid=offering_uuid,
        only_limit_based=only_limit_based,
        only_usage_based=only_usage_based,
        order_state=order_state,
        parent_offering_uuid=parent_offering_uuid,
        paused=paused,
        plan_uuid=plan_uuid,
        project_name=project_name,
        project_uuid=project_uuid,
        provider_uuid=provider_uuid,
        query=query,
        restrict_member_access=restrict_member_access,
        runtime_state=runtime_state,
        scope=scope,
        service_manager_uuid=service_manager_uuid,
        state=state,
        usage_based=usage_based,
        visible_to_providers=visible_to_providers,
        visible_to_username=visible_to_username,
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
