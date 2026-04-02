import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.booking_resource_o_enum import BookingResourceOEnum
from ...models.order_state import OrderState
from ...models.resource_state import ResourceState
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    backend_id: Union[Unset, str] = UNSET,
    category_uuid: Union[Unset, UUID] = UNSET,
    component_count: Union[Unset, float] = UNSET,
    connected_customer_uuid: Union[Unset, UUID] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
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
    o: Union[Unset, list[BookingResourceOEnum]] = UNSET,
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

    json_connected_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(connected_customer_uuid, Unset):
        json_connected_customer_uuid = str(connected_customer_uuid)
    params["connected_customer_uuid"] = json_connected_customer_uuid

    json_created: Union[Unset, str] = UNSET
    if not isinstance(created, Unset):
        json_created = created.isoformat()
    params["created"] = json_created

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
        "method": "head",
        "url": "/api/booking-resources/",
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
    backend_id: Union[Unset, str] = UNSET,
    category_uuid: Union[Unset, UUID] = UNSET,
    component_count: Union[Unset, float] = UNSET,
    connected_customer_uuid: Union[Unset, UUID] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
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
    o: Union[Unset, list[BookingResourceOEnum]] = UNSET,
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
    service_manager_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ResourceState]] = UNSET,
    usage_based: Union[Unset, bool] = UNSET,
    visible_to_providers: Union[Unset, bool] = UNSET,
    visible_to_username: Union[Unset, str] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        backend_id (Union[Unset, str]):
        category_uuid (Union[Unset, UUID]):
        component_count (Union[Unset, float]):
        connected_customer_uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
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
        o (Union[Unset, list[BookingResourceOEnum]]):
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
        service_manager_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[ResourceState]]):
        usage_based (Union[Unset, bool]):
        visible_to_providers (Union[Unset, bool]):
        visible_to_username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        backend_id=backend_id,
        category_uuid=category_uuid,
        component_count=component_count,
        connected_customer_uuid=connected_customer_uuid,
        created=created,
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
    *,
    client: AuthenticatedClient,
    backend_id: Union[Unset, str] = UNSET,
    category_uuid: Union[Unset, UUID] = UNSET,
    component_count: Union[Unset, float] = UNSET,
    connected_customer_uuid: Union[Unset, UUID] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
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
    o: Union[Unset, list[BookingResourceOEnum]] = UNSET,
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
    service_manager_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ResourceState]] = UNSET,
    usage_based: Union[Unset, bool] = UNSET,
    visible_to_providers: Union[Unset, bool] = UNSET,
    visible_to_username: Union[Unset, str] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        backend_id (Union[Unset, str]):
        category_uuid (Union[Unset, UUID]):
        component_count (Union[Unset, float]):
        connected_customer_uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
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
        o (Union[Unset, list[BookingResourceOEnum]]):
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
        service_manager_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[ResourceState]]):
        usage_based (Union[Unset, bool]):
        visible_to_providers (Union[Unset, bool]):
        visible_to_username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        backend_id=backend_id,
        category_uuid=category_uuid,
        component_count=component_count,
        connected_customer_uuid=connected_customer_uuid,
        created=created,
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
        service_manager_uuid=service_manager_uuid,
        state=state,
        usage_based=usage_based,
        visible_to_providers=visible_to_providers,
        visible_to_username=visible_to_username,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    backend_id: Union[Unset, str] = UNSET,
    category_uuid: Union[Unset, UUID] = UNSET,
    component_count: Union[Unset, float] = UNSET,
    connected_customer_uuid: Union[Unset, UUID] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
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
    o: Union[Unset, list[BookingResourceOEnum]] = UNSET,
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
    service_manager_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ResourceState]] = UNSET,
    usage_based: Union[Unset, bool] = UNSET,
    visible_to_providers: Union[Unset, bool] = UNSET,
    visible_to_username: Union[Unset, str] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        backend_id (Union[Unset, str]):
        category_uuid (Union[Unset, UUID]):
        component_count (Union[Unset, float]):
        connected_customer_uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
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
        o (Union[Unset, list[BookingResourceOEnum]]):
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
        service_manager_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[ResourceState]]):
        usage_based (Union[Unset, bool]):
        visible_to_providers (Union[Unset, bool]):
        visible_to_username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        backend_id=backend_id,
        category_uuid=category_uuid,
        component_count=component_count,
        connected_customer_uuid=connected_customer_uuid,
        created=created,
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
        service_manager_uuid=service_manager_uuid,
        state=state,
        usage_based=usage_based,
        visible_to_providers=visible_to_providers,
        visible_to_username=visible_to_username,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    backend_id: Union[Unset, str] = UNSET,
    category_uuid: Union[Unset, UUID] = UNSET,
    component_count: Union[Unset, float] = UNSET,
    connected_customer_uuid: Union[Unset, UUID] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
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
    o: Union[Unset, list[BookingResourceOEnum]] = UNSET,
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
    service_manager_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ResourceState]] = UNSET,
    usage_based: Union[Unset, bool] = UNSET,
    visible_to_providers: Union[Unset, bool] = UNSET,
    visible_to_username: Union[Unset, str] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        backend_id (Union[Unset, str]):
        category_uuid (Union[Unset, UUID]):
        component_count (Union[Unset, float]):
        connected_customer_uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
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
        o (Union[Unset, list[BookingResourceOEnum]]):
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
        service_manager_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[ResourceState]]):
        usage_based (Union[Unset, bool]):
        visible_to_providers (Union[Unset, bool]):
        visible_to_username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            backend_id=backend_id,
            category_uuid=category_uuid,
            component_count=component_count,
            connected_customer_uuid=connected_customer_uuid,
            created=created,
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
            service_manager_uuid=service_manager_uuid,
            state=state,
            usage_based=usage_based,
            visible_to_providers=visible_to_providers,
            visible_to_username=visible_to_username,
        )
    ).parsed
