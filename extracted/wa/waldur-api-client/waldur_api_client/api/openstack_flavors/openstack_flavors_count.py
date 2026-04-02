from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.open_stack_flavor_o_enum import OpenStackFlavorOEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cores: Union[Unset, int] = UNSET,
    cores_gte: Union[Unset, int] = UNSET,
    cores_lte: Union[Unset, int] = UNSET,
    disk: Union[Unset, int] = UNSET,
    disk_gte: Union[Unset, int] = UNSET,
    disk_lte: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    name_iregex: Union[Unset, str] = UNSET,
    o: Union[Unset, list[OpenStackFlavorOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    ram: Union[Unset, int] = UNSET,
    ram_gte: Union[Unset, int] = UNSET,
    ram_lte: Union[Unset, int] = UNSET,
    settings: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cores"] = cores

    params["cores__gte"] = cores_gte

    params["cores__lte"] = cores_lte

    params["disk"] = disk

    params["disk__gte"] = disk_gte

    params["disk__lte"] = disk_lte

    params["name"] = name

    params["name_exact"] = name_exact

    params["name_iregex"] = name_iregex

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    json_offering_uuid: Union[Unset, str] = UNSET
    if not isinstance(offering_uuid, Unset):
        json_offering_uuid = str(offering_uuid)
    params["offering_uuid"] = json_offering_uuid

    params["page"] = page

    params["page_size"] = page_size

    params["ram"] = ram

    params["ram__gte"] = ram_gte

    params["ram__lte"] = ram_lte

    params["settings"] = settings

    json_settings_uuid: Union[Unset, str] = UNSET
    if not isinstance(settings_uuid, Unset):
        json_settings_uuid = str(settings_uuid)
    params["settings_uuid"] = json_settings_uuid

    params["tenant"] = tenant

    json_tenant_uuid: Union[Unset, str] = UNSET
    if not isinstance(tenant_uuid, Unset):
        json_tenant_uuid = str(tenant_uuid)
    params["tenant_uuid"] = json_tenant_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/openstack-flavors/",
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
    cores: Union[Unset, int] = UNSET,
    cores_gte: Union[Unset, int] = UNSET,
    cores_lte: Union[Unset, int] = UNSET,
    disk: Union[Unset, int] = UNSET,
    disk_gte: Union[Unset, int] = UNSET,
    disk_lte: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    name_iregex: Union[Unset, str] = UNSET,
    o: Union[Unset, list[OpenStackFlavorOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    ram: Union[Unset, int] = UNSET,
    ram_gte: Union[Unset, int] = UNSET,
    ram_lte: Union[Unset, int] = UNSET,
    settings: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """List flavors

     Get number of items in the collection matching the request parameters.

    Args:
        cores (Union[Unset, int]):
        cores_gte (Union[Unset, int]):
        cores_lte (Union[Unset, int]):
        disk (Union[Unset, int]):
        disk_gte (Union[Unset, int]):
        disk_lte (Union[Unset, int]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        name_iregex (Union[Unset, str]):
        o (Union[Unset, list[OpenStackFlavorOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        ram (Union[Unset, int]):
        ram_gte (Union[Unset, int]):
        ram_lte (Union[Unset, int]):
        settings (Union[Unset, str]):
        settings_uuid (Union[Unset, UUID]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        cores=cores,
        cores_gte=cores_gte,
        cores_lte=cores_lte,
        disk=disk,
        disk_gte=disk_gte,
        disk_lte=disk_lte,
        name=name,
        name_exact=name_exact,
        name_iregex=name_iregex,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        ram=ram,
        ram_gte=ram_gte,
        ram_lte=ram_lte,
        settings=settings,
        settings_uuid=settings_uuid,
        tenant=tenant,
        tenant_uuid=tenant_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    cores: Union[Unset, int] = UNSET,
    cores_gte: Union[Unset, int] = UNSET,
    cores_lte: Union[Unset, int] = UNSET,
    disk: Union[Unset, int] = UNSET,
    disk_gte: Union[Unset, int] = UNSET,
    disk_lte: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    name_iregex: Union[Unset, str] = UNSET,
    o: Union[Unset, list[OpenStackFlavorOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    ram: Union[Unset, int] = UNSET,
    ram_gte: Union[Unset, int] = UNSET,
    ram_lte: Union[Unset, int] = UNSET,
    settings: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> int:
    """List flavors

     Get number of items in the collection matching the request parameters.

    Args:
        cores (Union[Unset, int]):
        cores_gte (Union[Unset, int]):
        cores_lte (Union[Unset, int]):
        disk (Union[Unset, int]):
        disk_gte (Union[Unset, int]):
        disk_lte (Union[Unset, int]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        name_iregex (Union[Unset, str]):
        o (Union[Unset, list[OpenStackFlavorOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        ram (Union[Unset, int]):
        ram_gte (Union[Unset, int]):
        ram_lte (Union[Unset, int]):
        settings (Union[Unset, str]):
        settings_uuid (Union[Unset, UUID]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        cores=cores,
        cores_gte=cores_gte,
        cores_lte=cores_lte,
        disk=disk,
        disk_gte=disk_gte,
        disk_lte=disk_lte,
        name=name,
        name_exact=name_exact,
        name_iregex=name_iregex,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        ram=ram,
        ram_gte=ram_gte,
        ram_lte=ram_lte,
        settings=settings,
        settings_uuid=settings_uuid,
        tenant=tenant,
        tenant_uuid=tenant_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    cores: Union[Unset, int] = UNSET,
    cores_gte: Union[Unset, int] = UNSET,
    cores_lte: Union[Unset, int] = UNSET,
    disk: Union[Unset, int] = UNSET,
    disk_gte: Union[Unset, int] = UNSET,
    disk_lte: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    name_iregex: Union[Unset, str] = UNSET,
    o: Union[Unset, list[OpenStackFlavorOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    ram: Union[Unset, int] = UNSET,
    ram_gte: Union[Unset, int] = UNSET,
    ram_lte: Union[Unset, int] = UNSET,
    settings: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """List flavors

     Get number of items in the collection matching the request parameters.

    Args:
        cores (Union[Unset, int]):
        cores_gte (Union[Unset, int]):
        cores_lte (Union[Unset, int]):
        disk (Union[Unset, int]):
        disk_gte (Union[Unset, int]):
        disk_lte (Union[Unset, int]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        name_iregex (Union[Unset, str]):
        o (Union[Unset, list[OpenStackFlavorOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        ram (Union[Unset, int]):
        ram_gte (Union[Unset, int]):
        ram_lte (Union[Unset, int]):
        settings (Union[Unset, str]):
        settings_uuid (Union[Unset, UUID]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        cores=cores,
        cores_gte=cores_gte,
        cores_lte=cores_lte,
        disk=disk,
        disk_gte=disk_gte,
        disk_lte=disk_lte,
        name=name,
        name_exact=name_exact,
        name_iregex=name_iregex,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        ram=ram,
        ram_gte=ram_gte,
        ram_lte=ram_lte,
        settings=settings,
        settings_uuid=settings_uuid,
        tenant=tenant,
        tenant_uuid=tenant_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    cores: Union[Unset, int] = UNSET,
    cores_gte: Union[Unset, int] = UNSET,
    cores_lte: Union[Unset, int] = UNSET,
    disk: Union[Unset, int] = UNSET,
    disk_gte: Union[Unset, int] = UNSET,
    disk_lte: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    name_iregex: Union[Unset, str] = UNSET,
    o: Union[Unset, list[OpenStackFlavorOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    ram: Union[Unset, int] = UNSET,
    ram_gte: Union[Unset, int] = UNSET,
    ram_lte: Union[Unset, int] = UNSET,
    settings: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> int:
    """List flavors

     Get number of items in the collection matching the request parameters.

    Args:
        cores (Union[Unset, int]):
        cores_gte (Union[Unset, int]):
        cores_lte (Union[Unset, int]):
        disk (Union[Unset, int]):
        disk_gte (Union[Unset, int]):
        disk_lte (Union[Unset, int]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        name_iregex (Union[Unset, str]):
        o (Union[Unset, list[OpenStackFlavorOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        ram (Union[Unset, int]):
        ram_gte (Union[Unset, int]):
        ram_lte (Union[Unset, int]):
        settings (Union[Unset, str]):
        settings_uuid (Union[Unset, UUID]):
        tenant (Union[Unset, str]):
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
            cores=cores,
            cores_gte=cores_gte,
            cores_lte=cores_lte,
            disk=disk,
            disk_gte=disk_gte,
            disk_lte=disk_lte,
            name=name,
            name_exact=name_exact,
            name_iregex=name_iregex,
            o=o,
            offering_uuid=offering_uuid,
            page=page,
            page_size=page_size,
            ram=ram,
            ram_gte=ram_gte,
            ram_lte=ram_lte,
            settings=settings,
            settings_uuid=settings_uuid,
            tenant=tenant,
            tenant_uuid=tenant_uuid,
        )
    ).parsed
