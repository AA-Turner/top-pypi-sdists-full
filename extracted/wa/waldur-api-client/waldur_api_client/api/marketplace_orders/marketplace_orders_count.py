import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.order_details_o_enum import OrderDetailsOEnum
from ...models.order_state import OrderState
from ...models.request_types import RequestTypes
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    can_approve_as_consumer: Union[Unset, bool] = UNSET,
    can_approve_as_provider: Union[Unset, bool] = UNSET,
    category_uuid: Union[Unset, UUID] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
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
        "method": "head",
        "url": "/api/marketplace-orders/",
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
    can_approve_as_consumer: Union[Unset, bool] = UNSET,
    can_approve_as_provider: Union[Unset, bool] = UNSET,
    category_uuid: Union[Unset, UUID] = UNSET,
    created: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
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
) -> Response[int]:
    """List orders

     Get number of items in the collection matching the request parameters.

    Args:
        can_approve_as_consumer (Union[Unset, bool]):
        can_approve_as_provider (Union[Unset, bool]):
        category_uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
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
        Response[int]
    """

    kwargs = _get_kwargs(
        can_approve_as_consumer=can_approve_as_consumer,
        can_approve_as_provider=can_approve_as_provider,
        category_uuid=category_uuid,
        created=created,
        customer_uuid=customer_uuid,
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
) -> int:
    """List orders

     Get number of items in the collection matching the request parameters.

    Args:
        can_approve_as_consumer (Union[Unset, bool]):
        can_approve_as_provider (Union[Unset, bool]):
        category_uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
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
        int
    """

    return sync_detailed(
        client=client,
        can_approve_as_consumer=can_approve_as_consumer,
        can_approve_as_provider=can_approve_as_provider,
        category_uuid=category_uuid,
        created=created,
        customer_uuid=customer_uuid,
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
) -> Response[int]:
    """List orders

     Get number of items in the collection matching the request parameters.

    Args:
        can_approve_as_consumer (Union[Unset, bool]):
        can_approve_as_provider (Union[Unset, bool]):
        category_uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
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
        Response[int]
    """

    kwargs = _get_kwargs(
        can_approve_as_consumer=can_approve_as_consumer,
        can_approve_as_provider=can_approve_as_provider,
        category_uuid=category_uuid,
        created=created,
        customer_uuid=customer_uuid,
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
) -> int:
    """List orders

     Get number of items in the collection matching the request parameters.

    Args:
        can_approve_as_consumer (Union[Unset, bool]):
        can_approve_as_provider (Union[Unset, bool]):
        category_uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
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
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            can_approve_as_consumer=can_approve_as_consumer,
            can_approve_as_provider=can_approve_as_provider,
            category_uuid=category_uuid,
            created=created,
            customer_uuid=customer_uuid,
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
