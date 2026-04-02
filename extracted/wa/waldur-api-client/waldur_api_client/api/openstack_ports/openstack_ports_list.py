from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.open_stack_port import OpenStackPort
from ...models.open_stack_port_field_enum import OpenStackPortFieldEnum
from ...models.open_stack_port_o_enum import OpenStackPortOEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    admin_state_up: Union[Unset, bool] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    device_id: Union[Unset, str] = UNSET,
    device_owner: Union[Unset, str] = UNSET,
    exclude_subnet_uuids: Union[Unset, str] = UNSET,
    field: Union[Unset, list[OpenStackPortFieldEnum]] = UNSET,
    fixed_ips: Union[Unset, str] = UNSET,
    has_device_owner: Union[Unset, bool] = UNSET,
    mac_address: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    network_name: Union[Unset, str] = UNSET,
    network_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[OpenStackPortOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["admin_state_up"] = admin_state_up

    params["backend_id"] = backend_id

    params["device_id"] = device_id

    params["device_owner"] = device_owner

    params["exclude_subnet_uuids"] = exclude_subnet_uuids

    json_field: Union[Unset, list[str]] = UNSET
    if not isinstance(field, Unset):
        json_field = []
        for field_item_data in field:
            field_item = field_item_data.value
            json_field.append(field_item)

    params["field"] = json_field

    params["fixed_ips"] = fixed_ips

    params["has_device_owner"] = has_device_owner

    params["mac_address"] = mac_address

    params["name"] = name

    params["name_exact"] = name_exact

    params["network_name"] = network_name

    json_network_uuid: Union[Unset, str] = UNSET
    if not isinstance(network_uuid, Unset):
        json_network_uuid = str(network_uuid)
    params["network_uuid"] = json_network_uuid

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

    params["status"] = status

    params["tenant"] = tenant

    json_tenant_uuid: Union[Unset, str] = UNSET
    if not isinstance(tenant_uuid, Unset):
        json_tenant_uuid = str(tenant_uuid)
    params["tenant_uuid"] = json_tenant_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/openstack-ports/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["OpenStackPort"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = OpenStackPort.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["OpenStackPort"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    admin_state_up: Union[Unset, bool] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    device_id: Union[Unset, str] = UNSET,
    device_owner: Union[Unset, str] = UNSET,
    exclude_subnet_uuids: Union[Unset, str] = UNSET,
    field: Union[Unset, list[OpenStackPortFieldEnum]] = UNSET,
    fixed_ips: Union[Unset, str] = UNSET,
    has_device_owner: Union[Unset, bool] = UNSET,
    mac_address: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    network_name: Union[Unset, str] = UNSET,
    network_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[OpenStackPortOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["OpenStackPort"]]:
    """List ports

     Get a list of network ports.

    Args:
        admin_state_up (Union[Unset, bool]):
        backend_id (Union[Unset, str]):
        device_id (Union[Unset, str]):
        device_owner (Union[Unset, str]):
        exclude_subnet_uuids (Union[Unset, str]):
        field (Union[Unset, list[OpenStackPortFieldEnum]]):
        fixed_ips (Union[Unset, str]):
        has_device_owner (Union[Unset, bool]):
        mac_address (Union[Unset, str]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        network_name (Union[Unset, str]):
        network_uuid (Union[Unset, UUID]):
        o (Union[Unset, list[OpenStackPortOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        status (Union[Unset, str]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['OpenStackPort']]
    """

    kwargs = _get_kwargs(
        admin_state_up=admin_state_up,
        backend_id=backend_id,
        device_id=device_id,
        device_owner=device_owner,
        exclude_subnet_uuids=exclude_subnet_uuids,
        field=field,
        fixed_ips=fixed_ips,
        has_device_owner=has_device_owner,
        mac_address=mac_address,
        name=name,
        name_exact=name_exact,
        network_name=network_name,
        network_uuid=network_uuid,
        o=o,
        page=page,
        page_size=page_size,
        query=query,
        status=status,
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
    admin_state_up: Union[Unset, bool] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    device_id: Union[Unset, str] = UNSET,
    device_owner: Union[Unset, str] = UNSET,
    exclude_subnet_uuids: Union[Unset, str] = UNSET,
    field: Union[Unset, list[OpenStackPortFieldEnum]] = UNSET,
    fixed_ips: Union[Unset, str] = UNSET,
    has_device_owner: Union[Unset, bool] = UNSET,
    mac_address: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    network_name: Union[Unset, str] = UNSET,
    network_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[OpenStackPortOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> list["OpenStackPort"]:
    """List ports

     Get a list of network ports.

    Args:
        admin_state_up (Union[Unset, bool]):
        backend_id (Union[Unset, str]):
        device_id (Union[Unset, str]):
        device_owner (Union[Unset, str]):
        exclude_subnet_uuids (Union[Unset, str]):
        field (Union[Unset, list[OpenStackPortFieldEnum]]):
        fixed_ips (Union[Unset, str]):
        has_device_owner (Union[Unset, bool]):
        mac_address (Union[Unset, str]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        network_name (Union[Unset, str]):
        network_uuid (Union[Unset, UUID]):
        o (Union[Unset, list[OpenStackPortOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        status (Union[Unset, str]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OpenStackPort']
    """

    return sync_detailed(
        client=client,
        admin_state_up=admin_state_up,
        backend_id=backend_id,
        device_id=device_id,
        device_owner=device_owner,
        exclude_subnet_uuids=exclude_subnet_uuids,
        field=field,
        fixed_ips=fixed_ips,
        has_device_owner=has_device_owner,
        mac_address=mac_address,
        name=name,
        name_exact=name_exact,
        network_name=network_name,
        network_uuid=network_uuid,
        o=o,
        page=page,
        page_size=page_size,
        query=query,
        status=status,
        tenant=tenant,
        tenant_uuid=tenant_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    admin_state_up: Union[Unset, bool] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    device_id: Union[Unset, str] = UNSET,
    device_owner: Union[Unset, str] = UNSET,
    exclude_subnet_uuids: Union[Unset, str] = UNSET,
    field: Union[Unset, list[OpenStackPortFieldEnum]] = UNSET,
    fixed_ips: Union[Unset, str] = UNSET,
    has_device_owner: Union[Unset, bool] = UNSET,
    mac_address: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    network_name: Union[Unset, str] = UNSET,
    network_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[OpenStackPortOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["OpenStackPort"]]:
    """List ports

     Get a list of network ports.

    Args:
        admin_state_up (Union[Unset, bool]):
        backend_id (Union[Unset, str]):
        device_id (Union[Unset, str]):
        device_owner (Union[Unset, str]):
        exclude_subnet_uuids (Union[Unset, str]):
        field (Union[Unset, list[OpenStackPortFieldEnum]]):
        fixed_ips (Union[Unset, str]):
        has_device_owner (Union[Unset, bool]):
        mac_address (Union[Unset, str]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        network_name (Union[Unset, str]):
        network_uuid (Union[Unset, UUID]):
        o (Union[Unset, list[OpenStackPortOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        status (Union[Unset, str]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['OpenStackPort']]
    """

    kwargs = _get_kwargs(
        admin_state_up=admin_state_up,
        backend_id=backend_id,
        device_id=device_id,
        device_owner=device_owner,
        exclude_subnet_uuids=exclude_subnet_uuids,
        field=field,
        fixed_ips=fixed_ips,
        has_device_owner=has_device_owner,
        mac_address=mac_address,
        name=name,
        name_exact=name_exact,
        network_name=network_name,
        network_uuid=network_uuid,
        o=o,
        page=page,
        page_size=page_size,
        query=query,
        status=status,
        tenant=tenant,
        tenant_uuid=tenant_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    admin_state_up: Union[Unset, bool] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    device_id: Union[Unset, str] = UNSET,
    device_owner: Union[Unset, str] = UNSET,
    exclude_subnet_uuids: Union[Unset, str] = UNSET,
    field: Union[Unset, list[OpenStackPortFieldEnum]] = UNSET,
    fixed_ips: Union[Unset, str] = UNSET,
    has_device_owner: Union[Unset, bool] = UNSET,
    mac_address: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    network_name: Union[Unset, str] = UNSET,
    network_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[OpenStackPortOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> list["OpenStackPort"]:
    """List ports

     Get a list of network ports.

    Args:
        admin_state_up (Union[Unset, bool]):
        backend_id (Union[Unset, str]):
        device_id (Union[Unset, str]):
        device_owner (Union[Unset, str]):
        exclude_subnet_uuids (Union[Unset, str]):
        field (Union[Unset, list[OpenStackPortFieldEnum]]):
        fixed_ips (Union[Unset, str]):
        has_device_owner (Union[Unset, bool]):
        mac_address (Union[Unset, str]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        network_name (Union[Unset, str]):
        network_uuid (Union[Unset, UUID]):
        o (Union[Unset, list[OpenStackPortOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        status (Union[Unset, str]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OpenStackPort']
    """

    return (
        await asyncio_detailed(
            client=client,
            admin_state_up=admin_state_up,
            backend_id=backend_id,
            device_id=device_id,
            device_owner=device_owner,
            exclude_subnet_uuids=exclude_subnet_uuids,
            field=field,
            fixed_ips=fixed_ips,
            has_device_owner=has_device_owner,
            mac_address=mac_address,
            name=name,
            name_exact=name_exact,
            network_name=network_name,
            network_uuid=network_uuid,
            o=o,
            page=page,
            page_size=page_size,
            query=query,
            status=status,
            tenant=tenant,
            tenant_uuid=tenant_uuid,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    admin_state_up: Union[Unset, bool] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    device_id: Union[Unset, str] = UNSET,
    device_owner: Union[Unset, str] = UNSET,
    exclude_subnet_uuids: Union[Unset, str] = UNSET,
    field: Union[Unset, list[OpenStackPortFieldEnum]] = UNSET,
    fixed_ips: Union[Unset, str] = UNSET,
    has_device_owner: Union[Unset, bool] = UNSET,
    mac_address: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    network_name: Union[Unset, str] = UNSET,
    network_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[OpenStackPortOEnum]] = UNSET,
    query: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> list["OpenStackPort"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        admin_state_up (Union[Unset, bool]):
        backend_id (Union[Unset, str]):
        device_id (Union[Unset, str]):
        device_owner (Union[Unset, str]):
        exclude_subnet_uuids (Union[Unset, str]):
        field (Union[Unset, list[OpenStackPortFieldEnum]]):
        fixed_ips (Union[Unset, str]):
        has_device_owner (Union[Unset, bool]):
        mac_address (Union[Unset, str]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        network_name (Union[Unset, str]):
        network_uuid (Union[Unset, UUID]):
        o (Union[Unset, list[OpenStackPortOEnum]]):
        query (Union[Unset, str]):
        status (Union[Unset, str]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OpenStackPort']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[OpenStackPort] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        admin_state_up=admin_state_up,
        backend_id=backend_id,
        device_id=device_id,
        device_owner=device_owner,
        exclude_subnet_uuids=exclude_subnet_uuids,
        field=field,
        fixed_ips=fixed_ips,
        has_device_owner=has_device_owner,
        mac_address=mac_address,
        name=name,
        name_exact=name_exact,
        network_name=network_name,
        network_uuid=network_uuid,
        o=o,
        query=query,
        status=status,
        tenant=tenant,
        tenant_uuid=tenant_uuid,
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
    admin_state_up: Union[Unset, bool] = UNSET,
    backend_id: Union[Unset, str] = UNSET,
    device_id: Union[Unset, str] = UNSET,
    device_owner: Union[Unset, str] = UNSET,
    exclude_subnet_uuids: Union[Unset, str] = UNSET,
    field: Union[Unset, list[OpenStackPortFieldEnum]] = UNSET,
    fixed_ips: Union[Unset, str] = UNSET,
    has_device_owner: Union[Unset, bool] = UNSET,
    mac_address: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    network_name: Union[Unset, str] = UNSET,
    network_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[OpenStackPortOEnum]] = UNSET,
    query: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> list["OpenStackPort"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        admin_state_up (Union[Unset, bool]):
        backend_id (Union[Unset, str]):
        device_id (Union[Unset, str]):
        device_owner (Union[Unset, str]):
        exclude_subnet_uuids (Union[Unset, str]):
        field (Union[Unset, list[OpenStackPortFieldEnum]]):
        fixed_ips (Union[Unset, str]):
        has_device_owner (Union[Unset, bool]):
        mac_address (Union[Unset, str]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        network_name (Union[Unset, str]):
        network_uuid (Union[Unset, UUID]):
        o (Union[Unset, list[OpenStackPortOEnum]]):
        query (Union[Unset, str]):
        status (Union[Unset, str]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OpenStackPort']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[OpenStackPort] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        admin_state_up=admin_state_up,
        backend_id=backend_id,
        device_id=device_id,
        device_owner=device_owner,
        exclude_subnet_uuids=exclude_subnet_uuids,
        field=field,
        fixed_ips=fixed_ips,
        has_device_owner=has_device_owner,
        mac_address=mac_address,
        name=name,
        name_exact=name_exact,
        network_name=network_name,
        network_uuid=network_uuid,
        o=o,
        query=query,
        status=status,
        tenant=tenant,
        tenant_uuid=tenant_uuid,
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
