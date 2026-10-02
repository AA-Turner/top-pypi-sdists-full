from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    availability_zone_name: Union[Unset, str] = UNSET,
    cores_max: Union[Unset, int] = UNSET,
    cores_min: Union[Unset, int] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    disk_max: Union[Unset, int] = UNSET,
    disk_min: Union[Unset, int] = UNSET,
    flavor_name: Union[Unset, str] = UNSET,
    hypervisor_hostname: Union[Unset, str] = UNSET,
    image_name: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    ram_max: Union[Unset, int] = UNSET,
    ram_min: Union[Unset, int] = UNSET,
    runtime_state: Union[Unset, str] = UNSET,
    service_settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["availability_zone_name"] = availability_zone_name

    params["cores_max"] = cores_max

    params["cores_min"] = cores_min

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    params["disk_max"] = disk_max

    params["disk_min"] = disk_min

    params["flavor_name"] = flavor_name

    params["hypervisor_hostname"] = hypervisor_hostname

    params["image_name"] = image_name

    params["name"] = name

    params["o"] = o

    params["page"] = page

    params["page_size"] = page_size

    json_project_uuid: Union[Unset, str] = UNSET
    if not isinstance(project_uuid, Unset):
        json_project_uuid = str(project_uuid)
    params["project_uuid"] = json_project_uuid

    params["ram_max"] = ram_max

    params["ram_min"] = ram_min

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
        "url": "/api/marketplace-stats/openstack_instances/",
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
    availability_zone_name: Union[Unset, str] = UNSET,
    cores_max: Union[Unset, int] = UNSET,
    cores_min: Union[Unset, int] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    disk_max: Union[Unset, int] = UNSET,
    disk_min: Union[Unset, int] = UNSET,
    flavor_name: Union[Unset, str] = UNSET,
    hypervisor_hostname: Union[Unset, str] = UNSET,
    image_name: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    ram_max: Union[Unset, int] = UNSET,
    ram_min: Union[Unset, int] = UNSET,
    runtime_state: Union[Unset, str] = UNSET,
    service_settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """List all OpenStack instances with infrastructure details.

     Get number of items in the collection matching the request parameters.

    Args:
        availability_zone_name (Union[Unset, str]):
        cores_max (Union[Unset, int]):
        cores_min (Union[Unset, int]):
        customer_uuid (Union[Unset, UUID]):
        disk_max (Union[Unset, int]):
        disk_min (Union[Unset, int]):
        flavor_name (Union[Unset, str]):
        hypervisor_hostname (Union[Unset, str]):
        image_name (Union[Unset, str]):
        name (Union[Unset, str]):
        o (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_uuid (Union[Unset, UUID]):
        ram_max (Union[Unset, int]):
        ram_min (Union[Unset, int]):
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
        availability_zone_name=availability_zone_name,
        cores_max=cores_max,
        cores_min=cores_min,
        customer_uuid=customer_uuid,
        disk_max=disk_max,
        disk_min=disk_min,
        flavor_name=flavor_name,
        hypervisor_hostname=hypervisor_hostname,
        image_name=image_name,
        name=name,
        o=o,
        page=page,
        page_size=page_size,
        project_uuid=project_uuid,
        ram_max=ram_max,
        ram_min=ram_min,
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
    availability_zone_name: Union[Unset, str] = UNSET,
    cores_max: Union[Unset, int] = UNSET,
    cores_min: Union[Unset, int] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    disk_max: Union[Unset, int] = UNSET,
    disk_min: Union[Unset, int] = UNSET,
    flavor_name: Union[Unset, str] = UNSET,
    hypervisor_hostname: Union[Unset, str] = UNSET,
    image_name: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    ram_max: Union[Unset, int] = UNSET,
    ram_min: Union[Unset, int] = UNSET,
    runtime_state: Union[Unset, str] = UNSET,
    service_settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> int:
    """List all OpenStack instances with infrastructure details.

     Get number of items in the collection matching the request parameters.

    Args:
        availability_zone_name (Union[Unset, str]):
        cores_max (Union[Unset, int]):
        cores_min (Union[Unset, int]):
        customer_uuid (Union[Unset, UUID]):
        disk_max (Union[Unset, int]):
        disk_min (Union[Unset, int]):
        flavor_name (Union[Unset, str]):
        hypervisor_hostname (Union[Unset, str]):
        image_name (Union[Unset, str]):
        name (Union[Unset, str]):
        o (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_uuid (Union[Unset, UUID]):
        ram_max (Union[Unset, int]):
        ram_min (Union[Unset, int]):
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
        availability_zone_name=availability_zone_name,
        cores_max=cores_max,
        cores_min=cores_min,
        customer_uuid=customer_uuid,
        disk_max=disk_max,
        disk_min=disk_min,
        flavor_name=flavor_name,
        hypervisor_hostname=hypervisor_hostname,
        image_name=image_name,
        name=name,
        o=o,
        page=page,
        page_size=page_size,
        project_uuid=project_uuid,
        ram_max=ram_max,
        ram_min=ram_min,
        runtime_state=runtime_state,
        service_settings_uuid=service_settings_uuid,
        state=state,
        tenant_uuid=tenant_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    availability_zone_name: Union[Unset, str] = UNSET,
    cores_max: Union[Unset, int] = UNSET,
    cores_min: Union[Unset, int] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    disk_max: Union[Unset, int] = UNSET,
    disk_min: Union[Unset, int] = UNSET,
    flavor_name: Union[Unset, str] = UNSET,
    hypervisor_hostname: Union[Unset, str] = UNSET,
    image_name: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    ram_max: Union[Unset, int] = UNSET,
    ram_min: Union[Unset, int] = UNSET,
    runtime_state: Union[Unset, str] = UNSET,
    service_settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """List all OpenStack instances with infrastructure details.

     Get number of items in the collection matching the request parameters.

    Args:
        availability_zone_name (Union[Unset, str]):
        cores_max (Union[Unset, int]):
        cores_min (Union[Unset, int]):
        customer_uuid (Union[Unset, UUID]):
        disk_max (Union[Unset, int]):
        disk_min (Union[Unset, int]):
        flavor_name (Union[Unset, str]):
        hypervisor_hostname (Union[Unset, str]):
        image_name (Union[Unset, str]):
        name (Union[Unset, str]):
        o (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_uuid (Union[Unset, UUID]):
        ram_max (Union[Unset, int]):
        ram_min (Union[Unset, int]):
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
        availability_zone_name=availability_zone_name,
        cores_max=cores_max,
        cores_min=cores_min,
        customer_uuid=customer_uuid,
        disk_max=disk_max,
        disk_min=disk_min,
        flavor_name=flavor_name,
        hypervisor_hostname=hypervisor_hostname,
        image_name=image_name,
        name=name,
        o=o,
        page=page,
        page_size=page_size,
        project_uuid=project_uuid,
        ram_max=ram_max,
        ram_min=ram_min,
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
    availability_zone_name: Union[Unset, str] = UNSET,
    cores_max: Union[Unset, int] = UNSET,
    cores_min: Union[Unset, int] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    disk_max: Union[Unset, int] = UNSET,
    disk_min: Union[Unset, int] = UNSET,
    flavor_name: Union[Unset, str] = UNSET,
    hypervisor_hostname: Union[Unset, str] = UNSET,
    image_name: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    ram_max: Union[Unset, int] = UNSET,
    ram_min: Union[Unset, int] = UNSET,
    runtime_state: Union[Unset, str] = UNSET,
    service_settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> int:
    """List all OpenStack instances with infrastructure details.

     Get number of items in the collection matching the request parameters.

    Args:
        availability_zone_name (Union[Unset, str]):
        cores_max (Union[Unset, int]):
        cores_min (Union[Unset, int]):
        customer_uuid (Union[Unset, UUID]):
        disk_max (Union[Unset, int]):
        disk_min (Union[Unset, int]):
        flavor_name (Union[Unset, str]):
        hypervisor_hostname (Union[Unset, str]):
        image_name (Union[Unset, str]):
        name (Union[Unset, str]):
        o (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_uuid (Union[Unset, UUID]):
        ram_max (Union[Unset, int]):
        ram_min (Union[Unset, int]):
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
            availability_zone_name=availability_zone_name,
            cores_max=cores_max,
            cores_min=cores_min,
            customer_uuid=customer_uuid,
            disk_max=disk_max,
            disk_min=disk_min,
            flavor_name=flavor_name,
            hypervisor_hostname=hypervisor_hostname,
            image_name=image_name,
            name=name,
            o=o,
            page=page,
            page_size=page_size,
            project_uuid=project_uuid,
            ram_max=ram_max,
            ram_min=ram_min,
            runtime_state=runtime_state,
            service_settings_uuid=service_settings_uuid,
            state=state,
            tenant_uuid=tenant_uuid,
        )
    ).parsed
