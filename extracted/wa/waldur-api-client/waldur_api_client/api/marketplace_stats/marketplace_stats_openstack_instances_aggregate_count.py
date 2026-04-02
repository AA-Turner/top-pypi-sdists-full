from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.open_stack_instance_aggregate_group_by_enum import OpenStackInstanceAggregateGroupByEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    customer_uuid: Union[Unset, UUID] = UNSET,
    flavor_name: Union[Unset, str] = UNSET,
    group_by: OpenStackInstanceAggregateGroupByEnum,
    hypervisor_hostname: Union[Unset, str] = UNSET,
    image_name: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    runtime_state: Union[Unset, str] = UNSET,
    service_settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    params["flavor_name"] = flavor_name

    json_group_by = group_by.value
    params["group_by"] = json_group_by

    params["hypervisor_hostname"] = hypervisor_hostname

    params["image_name"] = image_name

    params["name"] = name

    params["page"] = page

    params["page_size"] = page_size

    json_project_uuid: Union[Unset, str] = UNSET
    if not isinstance(project_uuid, Unset):
        json_project_uuid = str(project_uuid)
    params["project_uuid"] = json_project_uuid

    params["runtime_state"] = runtime_state

    json_service_settings_uuid: Union[Unset, str] = UNSET
    if not isinstance(service_settings_uuid, Unset):
        json_service_settings_uuid = str(service_settings_uuid)
    params["service_settings_uuid"] = json_service_settings_uuid

    params["state"] = state

    json_tenant_uuid: Union[Unset, str] = UNSET
    if not isinstance(tenant_uuid, Unset):
        json_tenant_uuid = str(tenant_uuid)
    params["tenant_uuid"] = json_tenant_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/marketplace-stats/openstack_instances_aggregate/",
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
    flavor_name: Union[Unset, str] = UNSET,
    group_by: OpenStackInstanceAggregateGroupByEnum,
    hypervisor_hostname: Union[Unset, str] = UNSET,
    image_name: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    runtime_state: Union[Unset, str] = UNSET,
    service_settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """Aggregate OpenStack instances by a dimension.

     Get number of items in the collection matching the request parameters.

    Args:
        customer_uuid (Union[Unset, UUID]):
        flavor_name (Union[Unset, str]):
        group_by (OpenStackInstanceAggregateGroupByEnum):
        hypervisor_hostname (Union[Unset, str]):
        image_name (Union[Unset, str]):
        name (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_uuid (Union[Unset, UUID]):
        runtime_state (Union[Unset, str]):
        service_settings_uuid (Union[Unset, UUID]):
        state (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        customer_uuid=customer_uuid,
        flavor_name=flavor_name,
        group_by=group_by,
        hypervisor_hostname=hypervisor_hostname,
        image_name=image_name,
        name=name,
        page=page,
        page_size=page_size,
        project_uuid=project_uuid,
        runtime_state=runtime_state,
        service_settings_uuid=service_settings_uuid,
        state=state,
        tenant_uuid=tenant_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    flavor_name: Union[Unset, str] = UNSET,
    group_by: OpenStackInstanceAggregateGroupByEnum,
    hypervisor_hostname: Union[Unset, str] = UNSET,
    image_name: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    runtime_state: Union[Unset, str] = UNSET,
    service_settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> int:
    """Aggregate OpenStack instances by a dimension.

     Get number of items in the collection matching the request parameters.

    Args:
        customer_uuid (Union[Unset, UUID]):
        flavor_name (Union[Unset, str]):
        group_by (OpenStackInstanceAggregateGroupByEnum):
        hypervisor_hostname (Union[Unset, str]):
        image_name (Union[Unset, str]):
        name (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_uuid (Union[Unset, UUID]):
        runtime_state (Union[Unset, str]):
        service_settings_uuid (Union[Unset, UUID]):
        state (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        customer_uuid=customer_uuid,
        flavor_name=flavor_name,
        group_by=group_by,
        hypervisor_hostname=hypervisor_hostname,
        image_name=image_name,
        name=name,
        page=page,
        page_size=page_size,
        project_uuid=project_uuid,
        runtime_state=runtime_state,
        service_settings_uuid=service_settings_uuid,
        state=state,
        tenant_uuid=tenant_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    flavor_name: Union[Unset, str] = UNSET,
    group_by: OpenStackInstanceAggregateGroupByEnum,
    hypervisor_hostname: Union[Unset, str] = UNSET,
    image_name: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    runtime_state: Union[Unset, str] = UNSET,
    service_settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """Aggregate OpenStack instances by a dimension.

     Get number of items in the collection matching the request parameters.

    Args:
        customer_uuid (Union[Unset, UUID]):
        flavor_name (Union[Unset, str]):
        group_by (OpenStackInstanceAggregateGroupByEnum):
        hypervisor_hostname (Union[Unset, str]):
        image_name (Union[Unset, str]):
        name (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_uuid (Union[Unset, UUID]):
        runtime_state (Union[Unset, str]):
        service_settings_uuid (Union[Unset, UUID]):
        state (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        customer_uuid=customer_uuid,
        flavor_name=flavor_name,
        group_by=group_by,
        hypervisor_hostname=hypervisor_hostname,
        image_name=image_name,
        name=name,
        page=page,
        page_size=page_size,
        project_uuid=project_uuid,
        runtime_state=runtime_state,
        service_settings_uuid=service_settings_uuid,
        state=state,
        tenant_uuid=tenant_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    flavor_name: Union[Unset, str] = UNSET,
    group_by: OpenStackInstanceAggregateGroupByEnum,
    hypervisor_hostname: Union[Unset, str] = UNSET,
    image_name: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    runtime_state: Union[Unset, str] = UNSET,
    service_settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> int:
    """Aggregate OpenStack instances by a dimension.

     Get number of items in the collection matching the request parameters.

    Args:
        customer_uuid (Union[Unset, UUID]):
        flavor_name (Union[Unset, str]):
        group_by (OpenStackInstanceAggregateGroupByEnum):
        hypervisor_hostname (Union[Unset, str]):
        image_name (Union[Unset, str]):
        name (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_uuid (Union[Unset, UUID]):
        runtime_state (Union[Unset, str]):
        service_settings_uuid (Union[Unset, UUID]):
        state (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):

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
            flavor_name=flavor_name,
            group_by=group_by,
            hypervisor_hostname=hypervisor_hostname,
            image_name=image_name,
            name=name,
            page=page,
            page_size=page_size,
            project_uuid=project_uuid,
            runtime_state=runtime_state,
            service_settings_uuid=service_settings_uuid,
            state=state,
            tenant_uuid=tenant_uuid,
        )
    ).parsed
