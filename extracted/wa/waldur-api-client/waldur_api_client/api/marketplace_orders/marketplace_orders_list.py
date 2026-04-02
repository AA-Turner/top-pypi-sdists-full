import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.order_details import OrderDetails
from ...models.order_details_field_enum import OrderDetailsFieldEnum
from ...models.order_details_o_enum import OrderDetailsOEnum
from ...models.order_state import OrderState
from ...models.request_types import RequestTypes
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    can_approve_as_consumer: Union[Unset, bool] = UNSET,
    can_approve_as_provider: Union[Unset, bool] = UNSET,
    category_uuid: Union[Unset, UUID] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[OrderDetailsFieldEnum]] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[OrderDetailsOEnum]] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_slug: Union[Unset, list[str]] = UNSET,
    offering_type: Union[Unset, list[str]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_offering_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    resource: Union[Unset, str] = UNSET,
    resource_name: Union[Unset, str] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    service_manager_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[OrderState]] = UNSET,
    type_: Union[Unset, list[RequestTypes]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["can_approve_as_consumer"] = can_approve_as_consumer

    params["can_approve_as_provider"] = can_approve_as_provider

    json_category_uuid: Union[Unset, str] = UNSET
    if not isinstance(category_uuid, Unset):
        json_category_uuid = str(category_uuid)
    params["category_uuid"] = json_category_uuid

    json_created: Union[Unset, str] = UNSET
    if not isinstance(created, Unset):
        json_created = created.isoformat()
    params["created"] = json_created

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

    json_modified: Union[Unset, str] = UNSET
    if not isinstance(modified, Unset):
        json_modified = modified.isoformat()
    params["modified"] = json_modified

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["offering"] = offering

    json_offering_slug: Union[Unset, list[str]] = UNSET
    if not isinstance(offering_slug, Unset):
        json_offering_slug = offering_slug

    params["offering_slug"] = json_offering_slug

    json_offering_type: Union[Unset, list[str]] = UNSET
    if not isinstance(offering_type, Unset):
        json_offering_type = offering_type

    params["offering_type"] = json_offering_type

    json_offering_uuid: Union[Unset, str] = UNSET
    if not isinstance(offering_uuid, Unset):
        json_offering_uuid = str(offering_uuid)
    params["offering_uuid"] = json_offering_uuid

    params["page"] = page

    params["page_size"] = page_size

    json_parent_offering_uuid: Union[Unset, str] = UNSET
    if not isinstance(parent_offering_uuid, Unset):
        json_parent_offering_uuid = str(parent_offering_uuid)
    params["parent_offering_uuid"] = json_parent_offering_uuid

    json_project_uuid: Union[Unset, str] = UNSET
    if not isinstance(project_uuid, Unset):
        json_project_uuid = str(project_uuid)
    params["project_uuid"] = json_project_uuid

    json_provider_uuid: Union[Unset, str] = UNSET
    if not isinstance(provider_uuid, Unset):
        json_provider_uuid = str(provider_uuid)
    params["provider_uuid"] = json_provider_uuid

    params["query"] = query

    params["resource"] = resource

    params["resource_name"] = resource_name

    json_resource_uuid: Union[Unset, str] = UNSET
    if not isinstance(resource_uuid, Unset):
        json_resource_uuid = str(resource_uuid)
    params["resource_uuid"] = json_resource_uuid

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

    json_type_: Union[Unset, list[str]] = UNSET
    if not isinstance(type_, Unset):
        json_type_ = []
        for type_item_data in type_:
            type_item = type_item_data.value
            json_type_.append(type_item)

    params["type"] = json_type_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/marketplace-orders/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["OrderDetails"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = OrderDetails.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["OrderDetails"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    can_approve_as_consumer: Union[Unset, bool] = UNSET,
    can_approve_as_provider: Union[Unset, bool] = UNSET,
    category_uuid: Union[Unset, UUID] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[OrderDetailsFieldEnum]] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[OrderDetailsOEnum]] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_slug: Union[Unset, list[str]] = UNSET,
    offering_type: Union[Unset, list[str]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_offering_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    resource: Union[Unset, str] = UNSET,
    resource_name: Union[Unset, str] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    service_manager_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[OrderState]] = UNSET,
    type_: Union[Unset, list[RequestTypes]] = UNSET,
) -> Response[list["OrderDetails"]]:
    """List orders

     Returns a paginated list of orders accessible to the current user. Orders are visible to service
    consumers (project/customer members with appropriate permissions) and service providers.

    Args:
        can_approve_as_consumer (Union[Unset, bool]):
        can_approve_as_provider (Union[Unset, bool]):
        category_uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
        field (Union[Unset, list[OrderDetailsFieldEnum]]):
        modified (Union[Unset, datetime.datetime]):
        o (Union[Unset, list[OrderDetailsOEnum]]):
        offering (Union[Unset, str]):
        offering_slug (Union[Unset, list[str]]):
        offering_type (Union[Unset, list[str]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_offering_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):
        provider_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        resource (Union[Unset, str]):
        resource_name (Union[Unset, str]):
        resource_uuid (Union[Unset, UUID]):
        service_manager_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[OrderState]]):
        type_ (Union[Unset, list[RequestTypes]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['OrderDetails']]
    """

    kwargs = _get_kwargs(
        can_approve_as_consumer=can_approve_as_consumer,
        can_approve_as_provider=can_approve_as_provider,
        category_uuid=category_uuid,
        created=created,
        customer_uuid=customer_uuid,
        field=field,
        modified=modified,
        o=o,
        offering=offering,
        offering_slug=offering_slug,
        offering_type=offering_type,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        parent_offering_uuid=parent_offering_uuid,
        project_uuid=project_uuid,
        provider_uuid=provider_uuid,
        query=query,
        resource=resource,
        resource_name=resource_name,
        resource_uuid=resource_uuid,
        service_manager_uuid=service_manager_uuid,
        state=state,
        type_=type_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    can_approve_as_consumer: Union[Unset, bool] = UNSET,
    can_approve_as_provider: Union[Unset, bool] = UNSET,
    category_uuid: Union[Unset, UUID] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[OrderDetailsFieldEnum]] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[OrderDetailsOEnum]] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_slug: Union[Unset, list[str]] = UNSET,
    offering_type: Union[Unset, list[str]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_offering_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    resource: Union[Unset, str] = UNSET,
    resource_name: Union[Unset, str] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    service_manager_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[OrderState]] = UNSET,
    type_: Union[Unset, list[RequestTypes]] = UNSET,
) -> list["OrderDetails"]:
    """List orders

     Returns a paginated list of orders accessible to the current user. Orders are visible to service
    consumers (project/customer members with appropriate permissions) and service providers.

    Args:
        can_approve_as_consumer (Union[Unset, bool]):
        can_approve_as_provider (Union[Unset, bool]):
        category_uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
        field (Union[Unset, list[OrderDetailsFieldEnum]]):
        modified (Union[Unset, datetime.datetime]):
        o (Union[Unset, list[OrderDetailsOEnum]]):
        offering (Union[Unset, str]):
        offering_slug (Union[Unset, list[str]]):
        offering_type (Union[Unset, list[str]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_offering_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):
        provider_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        resource (Union[Unset, str]):
        resource_name (Union[Unset, str]):
        resource_uuid (Union[Unset, UUID]):
        service_manager_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[OrderState]]):
        type_ (Union[Unset, list[RequestTypes]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OrderDetails']
    """

    return sync_detailed(
        client=client,
        can_approve_as_consumer=can_approve_as_consumer,
        can_approve_as_provider=can_approve_as_provider,
        category_uuid=category_uuid,
        created=created,
        customer_uuid=customer_uuid,
        field=field,
        modified=modified,
        o=o,
        offering=offering,
        offering_slug=offering_slug,
        offering_type=offering_type,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        parent_offering_uuid=parent_offering_uuid,
        project_uuid=project_uuid,
        provider_uuid=provider_uuid,
        query=query,
        resource=resource,
        resource_name=resource_name,
        resource_uuid=resource_uuid,
        service_manager_uuid=service_manager_uuid,
        state=state,
        type_=type_,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    can_approve_as_consumer: Union[Unset, bool] = UNSET,
    can_approve_as_provider: Union[Unset, bool] = UNSET,
    category_uuid: Union[Unset, UUID] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[OrderDetailsFieldEnum]] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[OrderDetailsOEnum]] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_slug: Union[Unset, list[str]] = UNSET,
    offering_type: Union[Unset, list[str]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_offering_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    resource: Union[Unset, str] = UNSET,
    resource_name: Union[Unset, str] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    service_manager_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[OrderState]] = UNSET,
    type_: Union[Unset, list[RequestTypes]] = UNSET,
) -> Response[list["OrderDetails"]]:
    """List orders

     Returns a paginated list of orders accessible to the current user. Orders are visible to service
    consumers (project/customer members with appropriate permissions) and service providers.

    Args:
        can_approve_as_consumer (Union[Unset, bool]):
        can_approve_as_provider (Union[Unset, bool]):
        category_uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
        field (Union[Unset, list[OrderDetailsFieldEnum]]):
        modified (Union[Unset, datetime.datetime]):
        o (Union[Unset, list[OrderDetailsOEnum]]):
        offering (Union[Unset, str]):
        offering_slug (Union[Unset, list[str]]):
        offering_type (Union[Unset, list[str]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_offering_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):
        provider_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        resource (Union[Unset, str]):
        resource_name (Union[Unset, str]):
        resource_uuid (Union[Unset, UUID]):
        service_manager_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[OrderState]]):
        type_ (Union[Unset, list[RequestTypes]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['OrderDetails']]
    """

    kwargs = _get_kwargs(
        can_approve_as_consumer=can_approve_as_consumer,
        can_approve_as_provider=can_approve_as_provider,
        category_uuid=category_uuid,
        created=created,
        customer_uuid=customer_uuid,
        field=field,
        modified=modified,
        o=o,
        offering=offering,
        offering_slug=offering_slug,
        offering_type=offering_type,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        parent_offering_uuid=parent_offering_uuid,
        project_uuid=project_uuid,
        provider_uuid=provider_uuid,
        query=query,
        resource=resource,
        resource_name=resource_name,
        resource_uuid=resource_uuid,
        service_manager_uuid=service_manager_uuid,
        state=state,
        type_=type_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    can_approve_as_consumer: Union[Unset, bool] = UNSET,
    can_approve_as_provider: Union[Unset, bool] = UNSET,
    category_uuid: Union[Unset, UUID] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[OrderDetailsFieldEnum]] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[OrderDetailsOEnum]] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_slug: Union[Unset, list[str]] = UNSET,
    offering_type: Union[Unset, list[str]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_offering_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    resource: Union[Unset, str] = UNSET,
    resource_name: Union[Unset, str] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    service_manager_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[OrderState]] = UNSET,
    type_: Union[Unset, list[RequestTypes]] = UNSET,
) -> list["OrderDetails"]:
    """List orders

     Returns a paginated list of orders accessible to the current user. Orders are visible to service
    consumers (project/customer members with appropriate permissions) and service providers.

    Args:
        can_approve_as_consumer (Union[Unset, bool]):
        can_approve_as_provider (Union[Unset, bool]):
        category_uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
        field (Union[Unset, list[OrderDetailsFieldEnum]]):
        modified (Union[Unset, datetime.datetime]):
        o (Union[Unset, list[OrderDetailsOEnum]]):
        offering (Union[Unset, str]):
        offering_slug (Union[Unset, list[str]]):
        offering_type (Union[Unset, list[str]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_offering_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):
        provider_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        resource (Union[Unset, str]):
        resource_name (Union[Unset, str]):
        resource_uuid (Union[Unset, UUID]):
        service_manager_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[OrderState]]):
        type_ (Union[Unset, list[RequestTypes]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OrderDetails']
    """

    return (
        await asyncio_detailed(
            client=client,
            can_approve_as_consumer=can_approve_as_consumer,
            can_approve_as_provider=can_approve_as_provider,
            category_uuid=category_uuid,
            created=created,
            customer_uuid=customer_uuid,
            field=field,
            modified=modified,
            o=o,
            offering=offering,
            offering_slug=offering_slug,
            offering_type=offering_type,
            offering_uuid=offering_uuid,
            page=page,
            page_size=page_size,
            parent_offering_uuid=parent_offering_uuid,
            project_uuid=project_uuid,
            provider_uuid=provider_uuid,
            query=query,
            resource=resource,
            resource_name=resource_name,
            resource_uuid=resource_uuid,
            service_manager_uuid=service_manager_uuid,
            state=state,
            type_=type_,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    can_approve_as_consumer: Union[Unset, bool] = UNSET,
    can_approve_as_provider: Union[Unset, bool] = UNSET,
    category_uuid: Union[Unset, UUID] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[OrderDetailsFieldEnum]] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[OrderDetailsOEnum]] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_slug: Union[Unset, list[str]] = UNSET,
    offering_type: Union[Unset, list[str]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    parent_offering_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    resource: Union[Unset, str] = UNSET,
    resource_name: Union[Unset, str] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    service_manager_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[OrderState]] = UNSET,
    type_: Union[Unset, list[RequestTypes]] = UNSET,
) -> list["OrderDetails"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        can_approve_as_consumer (Union[Unset, bool]):
        can_approve_as_provider (Union[Unset, bool]):
        category_uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
        field (Union[Unset, list[OrderDetailsFieldEnum]]):
        modified (Union[Unset, datetime.datetime]):
        o (Union[Unset, list[OrderDetailsOEnum]]):
        offering (Union[Unset, str]):
        offering_slug (Union[Unset, list[str]]):
        offering_type (Union[Unset, list[str]]):
        offering_uuid (Union[Unset, UUID]):
        parent_offering_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):
        provider_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        resource (Union[Unset, str]):
        resource_name (Union[Unset, str]):
        resource_uuid (Union[Unset, UUID]):
        service_manager_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[OrderState]]):
        type_ (Union[Unset, list[RequestTypes]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OrderDetails']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[OrderDetails] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        can_approve_as_consumer=can_approve_as_consumer,
        can_approve_as_provider=can_approve_as_provider,
        category_uuid=category_uuid,
        created=created,
        customer_uuid=customer_uuid,
        field=field,
        modified=modified,
        o=o,
        offering=offering,
        offering_slug=offering_slug,
        offering_type=offering_type,
        offering_uuid=offering_uuid,
        parent_offering_uuid=parent_offering_uuid,
        project_uuid=project_uuid,
        provider_uuid=provider_uuid,
        query=query,
        resource=resource,
        resource_name=resource_name,
        resource_uuid=resource_uuid,
        service_manager_uuid=service_manager_uuid,
        state=state,
        type_=type_,
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
    can_approve_as_consumer: Union[Unset, bool] = UNSET,
    can_approve_as_provider: Union[Unset, bool] = UNSET,
    category_uuid: Union[Unset, UUID] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[OrderDetailsFieldEnum]] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[OrderDetailsOEnum]] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_slug: Union[Unset, list[str]] = UNSET,
    offering_type: Union[Unset, list[str]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    parent_offering_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    resource: Union[Unset, str] = UNSET,
    resource_name: Union[Unset, str] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    service_manager_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[OrderState]] = UNSET,
    type_: Union[Unset, list[RequestTypes]] = UNSET,
) -> list["OrderDetails"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        can_approve_as_consumer (Union[Unset, bool]):
        can_approve_as_provider (Union[Unset, bool]):
        category_uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
        field (Union[Unset, list[OrderDetailsFieldEnum]]):
        modified (Union[Unset, datetime.datetime]):
        o (Union[Unset, list[OrderDetailsOEnum]]):
        offering (Union[Unset, str]):
        offering_slug (Union[Unset, list[str]]):
        offering_type (Union[Unset, list[str]]):
        offering_uuid (Union[Unset, UUID]):
        parent_offering_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):
        provider_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        resource (Union[Unset, str]):
        resource_name (Union[Unset, str]):
        resource_uuid (Union[Unset, UUID]):
        service_manager_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[OrderState]]):
        type_ (Union[Unset, list[RequestTypes]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OrderDetails']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[OrderDetails] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        can_approve_as_consumer=can_approve_as_consumer,
        can_approve_as_provider=can_approve_as_provider,
        category_uuid=category_uuid,
        created=created,
        customer_uuid=customer_uuid,
        field=field,
        modified=modified,
        o=o,
        offering=offering,
        offering_slug=offering_slug,
        offering_type=offering_type,
        offering_uuid=offering_uuid,
        parent_offering_uuid=parent_offering_uuid,
        project_uuid=project_uuid,
        provider_uuid=provider_uuid,
        query=query,
        resource=resource,
        resource_name=resource_name,
        resource_uuid=resource_uuid,
        service_manager_uuid=service_manager_uuid,
        state=state,
        type_=type_,
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
