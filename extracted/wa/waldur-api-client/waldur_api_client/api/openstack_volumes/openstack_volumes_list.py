from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.core_states import CoreStates
from ...models.open_stack_volume import OpenStackVolume
from ...models.open_stack_volume_field_enum import OpenStackVolumeFieldEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    attach_instance_uuid: Union[Unset, UUID] = UNSET,
    availability_zone_name: Union[Unset, str] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    can_manage: Union[Unset, bool] = UNSET,
    customer: Union[Unset, UUID] = UNSET,
    customer_abbreviation: Union[Unset, str] = UNSET,
    customer_name: Union[Unset, str] = UNSET,
    customer_native_name: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    description: Union[Unset, str] = UNSET,
    external_ip: Union[Unset, str] = UNSET,
    field: Union[Unset, list[OpenStackVolumeFieldEnum]] = UNSET,
    instance: Union[Unset, str] = UNSET,
    instance_uuid: Union[Unset, UUID] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project: Union[Unset, UUID] = UNSET,
    project_name: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    runtime_state: Union[Unset, str] = UNSET,
    service_settings_name: Union[Unset, str] = UNSET,
    service_settings_uuid: Union[Unset, UUID] = UNSET,
    snapshot: Union[Unset, str] = UNSET,
    snapshot_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
    uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_attach_instance_uuid: Union[Unset, str] = UNSET
    if not isinstance(attach_instance_uuid, Unset):
        json_attach_instance_uuid = str(attach_instance_uuid)
    params["attach_instance_uuid"] = json_attach_instance_uuid

    params["availability_zone_name"] = availability_zone_name

    params["backend_id"] = backend_id

    params["can_manage"] = can_manage

    json_customer: Union[Unset, str] = UNSET
    if not isinstance(customer, Unset):
        json_customer = str(customer)
    params["customer"] = json_customer

    params["customer_abbreviation"] = customer_abbreviation

    params["customer_name"] = customer_name

    params["customer_native_name"] = customer_native_name

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    params["description"] = description

    params["external_ip"] = external_ip

    json_field: Union[Unset, list[str]] = UNSET
    if not isinstance(field, Unset):
        json_field = []
        for field_item_data in field:
            field_item = field_item_data.value
            json_field.append(field_item)

    params["field"] = json_field

    params["instance"] = instance

    json_instance_uuid: Union[Unset, str] = UNSET
    if not isinstance(instance_uuid, Unset):
        json_instance_uuid = str(instance_uuid)
    params["instance_uuid"] = json_instance_uuid

    params["name"] = name

    params["name_exact"] = name_exact

    params["page"] = page

    params["page_size"] = page_size

    json_project: Union[Unset, str] = UNSET
    if not isinstance(project, Unset):
        json_project = str(project)
    params["project"] = json_project

    params["project_name"] = project_name

    json_project_uuid: Union[Unset, str] = UNSET
    if not isinstance(project_uuid, Unset):
        json_project_uuid = str(project_uuid)
    params["project_uuid"] = json_project_uuid

    params["runtime_state"] = runtime_state

    params["service_settings_name"] = service_settings_name

    json_service_settings_uuid: Union[Unset, str] = UNSET
    if not isinstance(service_settings_uuid, Unset):
        json_service_settings_uuid = str(service_settings_uuid)
    params["service_settings_uuid"] = json_service_settings_uuid

    params["snapshot"] = snapshot

    json_snapshot_uuid: Union[Unset, str] = UNSET
    if not isinstance(snapshot_uuid, Unset):
        json_snapshot_uuid = str(snapshot_uuid)
    params["snapshot_uuid"] = json_snapshot_uuid

    json_state: Union[Unset, list[str]] = UNSET
    if not isinstance(state, Unset):
        json_state = []
        for state_item_data in state:
            state_item = state_item_data.value
            json_state.append(state_item)

    params["state"] = json_state

    params["tenant"] = tenant

    json_tenant_uuid: Union[Unset, str] = UNSET
    if not isinstance(tenant_uuid, Unset):
        json_tenant_uuid = str(tenant_uuid)
    params["tenant_uuid"] = json_tenant_uuid

    json_uuid: Union[Unset, str] = UNSET
    if not isinstance(uuid, Unset):
        json_uuid = str(uuid)
    params["uuid"] = json_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/openstack-volumes/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["OpenStackVolume"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = OpenStackVolume.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["OpenStackVolume"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    attach_instance_uuid: Union[Unset, UUID] = UNSET,
    availability_zone_name: Union[Unset, str] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    can_manage: Union[Unset, bool] = UNSET,
    customer: Union[Unset, UUID] = UNSET,
    customer_abbreviation: Union[Unset, str] = UNSET,
    customer_name: Union[Unset, str] = UNSET,
    customer_native_name: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    description: Union[Unset, str] = UNSET,
    external_ip: Union[Unset, str] = UNSET,
    field: Union[Unset, list[OpenStackVolumeFieldEnum]] = UNSET,
    instance: Union[Unset, str] = UNSET,
    instance_uuid: Union[Unset, UUID] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project: Union[Unset, UUID] = UNSET,
    project_name: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    runtime_state: Union[Unset, str] = UNSET,
    service_settings_name: Union[Unset, str] = UNSET,
    service_settings_uuid: Union[Unset, UUID] = UNSET,
    snapshot: Union[Unset, str] = UNSET,
    snapshot_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
    uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["OpenStackVolume"]]:
    """List volumes

     Get a list of volumes.

    Args:
        attach_instance_uuid (Union[Unset, UUID]):
        availability_zone_name (Union[Unset, str]):
        backend_id (Union[Unset, str]):
        can_manage (Union[Unset, bool]):
        customer (Union[Unset, UUID]):
        customer_abbreviation (Union[Unset, str]):
        customer_name (Union[Unset, str]):
        customer_native_name (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        description (Union[Unset, str]):
        external_ip (Union[Unset, str]):
        field (Union[Unset, list[OpenStackVolumeFieldEnum]]):
        instance (Union[Unset, str]):
        instance_uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project (Union[Unset, UUID]):
        project_name (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        runtime_state (Union[Unset, str]):
        service_settings_name (Union[Unset, str]):
        service_settings_uuid (Union[Unset, UUID]):
        snapshot (Union[Unset, str]):
        snapshot_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[CoreStates]]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):
        uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['OpenStackVolume']]
    """

    kwargs = _get_kwargs(
        attach_instance_uuid=attach_instance_uuid,
        availability_zone_name=availability_zone_name,
        backend_id=backend_id,
        can_manage=can_manage,
        customer=customer,
        customer_abbreviation=customer_abbreviation,
        customer_name=customer_name,
        customer_native_name=customer_native_name,
        customer_uuid=customer_uuid,
        description=description,
        external_ip=external_ip,
        field=field,
        instance=instance,
        instance_uuid=instance_uuid,
        name=name,
        name_exact=name_exact,
        page=page,
        page_size=page_size,
        project=project,
        project_name=project_name,
        project_uuid=project_uuid,
        runtime_state=runtime_state,
        service_settings_name=service_settings_name,
        service_settings_uuid=service_settings_uuid,
        snapshot=snapshot,
        snapshot_uuid=snapshot_uuid,
        state=state,
        tenant=tenant,
        tenant_uuid=tenant_uuid,
        uuid=uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    attach_instance_uuid: Union[Unset, UUID] = UNSET,
    availability_zone_name: Union[Unset, str] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    can_manage: Union[Unset, bool] = UNSET,
    customer: Union[Unset, UUID] = UNSET,
    customer_abbreviation: Union[Unset, str] = UNSET,
    customer_name: Union[Unset, str] = UNSET,
    customer_native_name: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    description: Union[Unset, str] = UNSET,
    external_ip: Union[Unset, str] = UNSET,
    field: Union[Unset, list[OpenStackVolumeFieldEnum]] = UNSET,
    instance: Union[Unset, str] = UNSET,
    instance_uuid: Union[Unset, UUID] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project: Union[Unset, UUID] = UNSET,
    project_name: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    runtime_state: Union[Unset, str] = UNSET,
    service_settings_name: Union[Unset, str] = UNSET,
    service_settings_uuid: Union[Unset, UUID] = UNSET,
    snapshot: Union[Unset, str] = UNSET,
    snapshot_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
    uuid: Union[Unset, UUID] = UNSET,
) -> list["OpenStackVolume"]:
    """List volumes

     Get a list of volumes.

    Args:
        attach_instance_uuid (Union[Unset, UUID]):
        availability_zone_name (Union[Unset, str]):
        backend_id (Union[Unset, str]):
        can_manage (Union[Unset, bool]):
        customer (Union[Unset, UUID]):
        customer_abbreviation (Union[Unset, str]):
        customer_name (Union[Unset, str]):
        customer_native_name (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        description (Union[Unset, str]):
        external_ip (Union[Unset, str]):
        field (Union[Unset, list[OpenStackVolumeFieldEnum]]):
        instance (Union[Unset, str]):
        instance_uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project (Union[Unset, UUID]):
        project_name (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        runtime_state (Union[Unset, str]):
        service_settings_name (Union[Unset, str]):
        service_settings_uuid (Union[Unset, UUID]):
        snapshot (Union[Unset, str]):
        snapshot_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[CoreStates]]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):
        uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OpenStackVolume']
    """

    return sync_detailed(
        client=client,
        attach_instance_uuid=attach_instance_uuid,
        availability_zone_name=availability_zone_name,
        backend_id=backend_id,
        can_manage=can_manage,
        customer=customer,
        customer_abbreviation=customer_abbreviation,
        customer_name=customer_name,
        customer_native_name=customer_native_name,
        customer_uuid=customer_uuid,
        description=description,
        external_ip=external_ip,
        field=field,
        instance=instance,
        instance_uuid=instance_uuid,
        name=name,
        name_exact=name_exact,
        page=page,
        page_size=page_size,
        project=project,
        project_name=project_name,
        project_uuid=project_uuid,
        runtime_state=runtime_state,
        service_settings_name=service_settings_name,
        service_settings_uuid=service_settings_uuid,
        snapshot=snapshot,
        snapshot_uuid=snapshot_uuid,
        state=state,
        tenant=tenant,
        tenant_uuid=tenant_uuid,
        uuid=uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    attach_instance_uuid: Union[Unset, UUID] = UNSET,
    availability_zone_name: Union[Unset, str] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    can_manage: Union[Unset, bool] = UNSET,
    customer: Union[Unset, UUID] = UNSET,
    customer_abbreviation: Union[Unset, str] = UNSET,
    customer_name: Union[Unset, str] = UNSET,
    customer_native_name: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    description: Union[Unset, str] = UNSET,
    external_ip: Union[Unset, str] = UNSET,
    field: Union[Unset, list[OpenStackVolumeFieldEnum]] = UNSET,
    instance: Union[Unset, str] = UNSET,
    instance_uuid: Union[Unset, UUID] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project: Union[Unset, UUID] = UNSET,
    project_name: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    runtime_state: Union[Unset, str] = UNSET,
    service_settings_name: Union[Unset, str] = UNSET,
    service_settings_uuid: Union[Unset, UUID] = UNSET,
    snapshot: Union[Unset, str] = UNSET,
    snapshot_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
    uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["OpenStackVolume"]]:
    """List volumes

     Get a list of volumes.

    Args:
        attach_instance_uuid (Union[Unset, UUID]):
        availability_zone_name (Union[Unset, str]):
        backend_id (Union[Unset, str]):
        can_manage (Union[Unset, bool]):
        customer (Union[Unset, UUID]):
        customer_abbreviation (Union[Unset, str]):
        customer_name (Union[Unset, str]):
        customer_native_name (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        description (Union[Unset, str]):
        external_ip (Union[Unset, str]):
        field (Union[Unset, list[OpenStackVolumeFieldEnum]]):
        instance (Union[Unset, str]):
        instance_uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project (Union[Unset, UUID]):
        project_name (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        runtime_state (Union[Unset, str]):
        service_settings_name (Union[Unset, str]):
        service_settings_uuid (Union[Unset, UUID]):
        snapshot (Union[Unset, str]):
        snapshot_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[CoreStates]]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):
        uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['OpenStackVolume']]
    """

    kwargs = _get_kwargs(
        attach_instance_uuid=attach_instance_uuid,
        availability_zone_name=availability_zone_name,
        backend_id=backend_id,
        can_manage=can_manage,
        customer=customer,
        customer_abbreviation=customer_abbreviation,
        customer_name=customer_name,
        customer_native_name=customer_native_name,
        customer_uuid=customer_uuid,
        description=description,
        external_ip=external_ip,
        field=field,
        instance=instance,
        instance_uuid=instance_uuid,
        name=name,
        name_exact=name_exact,
        page=page,
        page_size=page_size,
        project=project,
        project_name=project_name,
        project_uuid=project_uuid,
        runtime_state=runtime_state,
        service_settings_name=service_settings_name,
        service_settings_uuid=service_settings_uuid,
        snapshot=snapshot,
        snapshot_uuid=snapshot_uuid,
        state=state,
        tenant=tenant,
        tenant_uuid=tenant_uuid,
        uuid=uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    attach_instance_uuid: Union[Unset, UUID] = UNSET,
    availability_zone_name: Union[Unset, str] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    can_manage: Union[Unset, bool] = UNSET,
    customer: Union[Unset, UUID] = UNSET,
    customer_abbreviation: Union[Unset, str] = UNSET,
    customer_name: Union[Unset, str] = UNSET,
    customer_native_name: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    description: Union[Unset, str] = UNSET,
    external_ip: Union[Unset, str] = UNSET,
    field: Union[Unset, list[OpenStackVolumeFieldEnum]] = UNSET,
    instance: Union[Unset, str] = UNSET,
    instance_uuid: Union[Unset, UUID] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project: Union[Unset, UUID] = UNSET,
    project_name: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    runtime_state: Union[Unset, str] = UNSET,
    service_settings_name: Union[Unset, str] = UNSET,
    service_settings_uuid: Union[Unset, UUID] = UNSET,
    snapshot: Union[Unset, str] = UNSET,
    snapshot_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
    uuid: Union[Unset, UUID] = UNSET,
) -> list["OpenStackVolume"]:
    """List volumes

     Get a list of volumes.

    Args:
        attach_instance_uuid (Union[Unset, UUID]):
        availability_zone_name (Union[Unset, str]):
        backend_id (Union[Unset, str]):
        can_manage (Union[Unset, bool]):
        customer (Union[Unset, UUID]):
        customer_abbreviation (Union[Unset, str]):
        customer_name (Union[Unset, str]):
        customer_native_name (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        description (Union[Unset, str]):
        external_ip (Union[Unset, str]):
        field (Union[Unset, list[OpenStackVolumeFieldEnum]]):
        instance (Union[Unset, str]):
        instance_uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project (Union[Unset, UUID]):
        project_name (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        runtime_state (Union[Unset, str]):
        service_settings_name (Union[Unset, str]):
        service_settings_uuid (Union[Unset, UUID]):
        snapshot (Union[Unset, str]):
        snapshot_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[CoreStates]]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):
        uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OpenStackVolume']
    """

    return (
        await asyncio_detailed(
            client=client,
            attach_instance_uuid=attach_instance_uuid,
            availability_zone_name=availability_zone_name,
            backend_id=backend_id,
            can_manage=can_manage,
            customer=customer,
            customer_abbreviation=customer_abbreviation,
            customer_name=customer_name,
            customer_native_name=customer_native_name,
            customer_uuid=customer_uuid,
            description=description,
            external_ip=external_ip,
            field=field,
            instance=instance,
            instance_uuid=instance_uuid,
            name=name,
            name_exact=name_exact,
            page=page,
            page_size=page_size,
            project=project,
            project_name=project_name,
            project_uuid=project_uuid,
            runtime_state=runtime_state,
            service_settings_name=service_settings_name,
            service_settings_uuid=service_settings_uuid,
            snapshot=snapshot,
            snapshot_uuid=snapshot_uuid,
            state=state,
            tenant=tenant,
            tenant_uuid=tenant_uuid,
            uuid=uuid,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    attach_instance_uuid: Union[Unset, UUID] = UNSET,
    availability_zone_name: Union[Unset, str] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    can_manage: Union[Unset, bool] = UNSET,
    customer: Union[Unset, UUID] = UNSET,
    customer_abbreviation: Union[Unset, str] = UNSET,
    customer_name: Union[Unset, str] = UNSET,
    customer_native_name: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    description: Union[Unset, str] = UNSET,
    external_ip: Union[Unset, str] = UNSET,
    field: Union[Unset, list[OpenStackVolumeFieldEnum]] = UNSET,
    instance: Union[Unset, str] = UNSET,
    instance_uuid: Union[Unset, UUID] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    project: Union[Unset, UUID] = UNSET,
    project_name: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    runtime_state: Union[Unset, str] = UNSET,
    service_settings_name: Union[Unset, str] = UNSET,
    service_settings_uuid: Union[Unset, UUID] = UNSET,
    snapshot: Union[Unset, str] = UNSET,
    snapshot_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
    uuid: Union[Unset, UUID] = UNSET,
) -> list["OpenStackVolume"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        attach_instance_uuid (Union[Unset, UUID]):
        availability_zone_name (Union[Unset, str]):
        backend_id (Union[Unset, str]):
        can_manage (Union[Unset, bool]):
        customer (Union[Unset, UUID]):
        customer_abbreviation (Union[Unset, str]):
        customer_name (Union[Unset, str]):
        customer_native_name (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        description (Union[Unset, str]):
        external_ip (Union[Unset, str]):
        field (Union[Unset, list[OpenStackVolumeFieldEnum]]):
        instance (Union[Unset, str]):
        instance_uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        project (Union[Unset, UUID]):
        project_name (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        runtime_state (Union[Unset, str]):
        service_settings_name (Union[Unset, str]):
        service_settings_uuid (Union[Unset, UUID]):
        snapshot (Union[Unset, str]):
        snapshot_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[CoreStates]]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):
        uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OpenStackVolume']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[OpenStackVolume] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        attach_instance_uuid=attach_instance_uuid,
        availability_zone_name=availability_zone_name,
        backend_id=backend_id,
        can_manage=can_manage,
        customer=customer,
        customer_abbreviation=customer_abbreviation,
        customer_name=customer_name,
        customer_native_name=customer_native_name,
        customer_uuid=customer_uuid,
        description=description,
        external_ip=external_ip,
        field=field,
        instance=instance,
        instance_uuid=instance_uuid,
        name=name,
        name_exact=name_exact,
        project=project,
        project_name=project_name,
        project_uuid=project_uuid,
        runtime_state=runtime_state,
        service_settings_name=service_settings_name,
        service_settings_uuid=service_settings_uuid,
        snapshot=snapshot,
        snapshot_uuid=snapshot_uuid,
        state=state,
        tenant=tenant,
        tenant_uuid=tenant_uuid,
        uuid=uuid,
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
    attach_instance_uuid: Union[Unset, UUID] = UNSET,
    availability_zone_name: Union[Unset, str] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    can_manage: Union[Unset, bool] = UNSET,
    customer: Union[Unset, UUID] = UNSET,
    customer_abbreviation: Union[Unset, str] = UNSET,
    customer_name: Union[Unset, str] = UNSET,
    customer_native_name: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    description: Union[Unset, str] = UNSET,
    external_ip: Union[Unset, str] = UNSET,
    field: Union[Unset, list[OpenStackVolumeFieldEnum]] = UNSET,
    instance: Union[Unset, str] = UNSET,
    instance_uuid: Union[Unset, UUID] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    project: Union[Unset, UUID] = UNSET,
    project_name: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    runtime_state: Union[Unset, str] = UNSET,
    service_settings_name: Union[Unset, str] = UNSET,
    service_settings_uuid: Union[Unset, UUID] = UNSET,
    snapshot: Union[Unset, str] = UNSET,
    snapshot_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
    uuid: Union[Unset, UUID] = UNSET,
) -> list["OpenStackVolume"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        attach_instance_uuid (Union[Unset, UUID]):
        availability_zone_name (Union[Unset, str]):
        backend_id (Union[Unset, str]):
        can_manage (Union[Unset, bool]):
        customer (Union[Unset, UUID]):
        customer_abbreviation (Union[Unset, str]):
        customer_name (Union[Unset, str]):
        customer_native_name (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        description (Union[Unset, str]):
        external_ip (Union[Unset, str]):
        field (Union[Unset, list[OpenStackVolumeFieldEnum]]):
        instance (Union[Unset, str]):
        instance_uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        project (Union[Unset, UUID]):
        project_name (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        runtime_state (Union[Unset, str]):
        service_settings_name (Union[Unset, str]):
        service_settings_uuid (Union[Unset, UUID]):
        snapshot (Union[Unset, str]):
        snapshot_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[CoreStates]]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):
        uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OpenStackVolume']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[OpenStackVolume] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        attach_instance_uuid=attach_instance_uuid,
        availability_zone_name=availability_zone_name,
        backend_id=backend_id,
        can_manage=can_manage,
        customer=customer,
        customer_abbreviation=customer_abbreviation,
        customer_name=customer_name,
        customer_native_name=customer_native_name,
        customer_uuid=customer_uuid,
        description=description,
        external_ip=external_ip,
        field=field,
        instance=instance,
        instance_uuid=instance_uuid,
        name=name,
        name_exact=name_exact,
        project=project,
        project_name=project_name,
        project_uuid=project_uuid,
        runtime_state=runtime_state,
        service_settings_name=service_settings_name,
        service_settings_uuid=service_settings_uuid,
        snapshot=snapshot,
        snapshot_uuid=snapshot_uuid,
        state=state,
        tenant=tenant,
        tenant_uuid=tenant_uuid,
        uuid=uuid,
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
