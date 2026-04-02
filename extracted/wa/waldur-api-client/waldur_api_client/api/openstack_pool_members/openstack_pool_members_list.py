from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.core_states import CoreStates
from ...models.open_stack_pool_member import OpenStackPoolMember
from ...models.open_stack_pool_member_field_enum import OpenStackPoolMemberFieldEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    field: Union[Unset, list[OpenStackPoolMemberFieldEnum]] = UNSET,
    load_balancer_uuid: Union[Unset, UUID] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    pool: Union[Unset, str] = UNSET,
    pool_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_field: Union[Unset, list[str]] = UNSET
    if not isinstance(field, Unset):
        json_field = []
        for field_item_data in field:
            field_item = field_item_data.value
            json_field.append(field_item)

    params["field"] = json_field

    json_load_balancer_uuid: Union[Unset, str] = UNSET
    if not isinstance(load_balancer_uuid, Unset):
        json_load_balancer_uuid = str(load_balancer_uuid)
    params["load_balancer_uuid"] = json_load_balancer_uuid

    params["name"] = name

    params["name_exact"] = name_exact

    params["page"] = page

    params["page_size"] = page_size

    params["pool"] = pool

    json_pool_uuid: Union[Unset, str] = UNSET
    if not isinstance(pool_uuid, Unset):
        json_pool_uuid = str(pool_uuid)
    params["pool_uuid"] = json_pool_uuid

    json_state: Union[Unset, list[str]] = UNSET
    if not isinstance(state, Unset):
        json_state = []
        for state_item_data in state:
            state_item = state_item_data.value
            json_state.append(state_item)

    params["state"] = json_state

    json_tenant_uuid: Union[Unset, str] = UNSET
    if not isinstance(tenant_uuid, Unset):
        json_tenant_uuid = str(tenant_uuid)
    params["tenant_uuid"] = json_tenant_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/openstack-pool-members/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["OpenStackPoolMember"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = OpenStackPoolMember.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["OpenStackPoolMember"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    field: Union[Unset, list[OpenStackPoolMemberFieldEnum]] = UNSET,
    load_balancer_uuid: Union[Unset, UUID] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    pool: Union[Unset, str] = UNSET,
    pool_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["OpenStackPoolMember"]]:
    """List pool members

     Get a list of pool members.

    Args:
        field (Union[Unset, list[OpenStackPoolMemberFieldEnum]]):
        load_balancer_uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        pool (Union[Unset, str]):
        pool_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[CoreStates]]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['OpenStackPoolMember']]
    """

    kwargs = _get_kwargs(
        field=field,
        load_balancer_uuid=load_balancer_uuid,
        name=name,
        name_exact=name_exact,
        page=page,
        page_size=page_size,
        pool=pool,
        pool_uuid=pool_uuid,
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
    field: Union[Unset, list[OpenStackPoolMemberFieldEnum]] = UNSET,
    load_balancer_uuid: Union[Unset, UUID] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    pool: Union[Unset, str] = UNSET,
    pool_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> list["OpenStackPoolMember"]:
    """List pool members

     Get a list of pool members.

    Args:
        field (Union[Unset, list[OpenStackPoolMemberFieldEnum]]):
        load_balancer_uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        pool (Union[Unset, str]):
        pool_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[CoreStates]]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OpenStackPoolMember']
    """

    return sync_detailed(
        client=client,
        field=field,
        load_balancer_uuid=load_balancer_uuid,
        name=name,
        name_exact=name_exact,
        page=page,
        page_size=page_size,
        pool=pool,
        pool_uuid=pool_uuid,
        state=state,
        tenant_uuid=tenant_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    field: Union[Unset, list[OpenStackPoolMemberFieldEnum]] = UNSET,
    load_balancer_uuid: Union[Unset, UUID] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    pool: Union[Unset, str] = UNSET,
    pool_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["OpenStackPoolMember"]]:
    """List pool members

     Get a list of pool members.

    Args:
        field (Union[Unset, list[OpenStackPoolMemberFieldEnum]]):
        load_balancer_uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        pool (Union[Unset, str]):
        pool_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[CoreStates]]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['OpenStackPoolMember']]
    """

    kwargs = _get_kwargs(
        field=field,
        load_balancer_uuid=load_balancer_uuid,
        name=name,
        name_exact=name_exact,
        page=page,
        page_size=page_size,
        pool=pool,
        pool_uuid=pool_uuid,
        state=state,
        tenant_uuid=tenant_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    field: Union[Unset, list[OpenStackPoolMemberFieldEnum]] = UNSET,
    load_balancer_uuid: Union[Unset, UUID] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    pool: Union[Unset, str] = UNSET,
    pool_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> list["OpenStackPoolMember"]:
    """List pool members

     Get a list of pool members.

    Args:
        field (Union[Unset, list[OpenStackPoolMemberFieldEnum]]):
        load_balancer_uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        pool (Union[Unset, str]):
        pool_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[CoreStates]]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OpenStackPoolMember']
    """

    return (
        await asyncio_detailed(
            client=client,
            field=field,
            load_balancer_uuid=load_balancer_uuid,
            name=name,
            name_exact=name_exact,
            page=page,
            page_size=page_size,
            pool=pool,
            pool_uuid=pool_uuid,
            state=state,
            tenant_uuid=tenant_uuid,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    field: Union[Unset, list[OpenStackPoolMemberFieldEnum]] = UNSET,
    load_balancer_uuid: Union[Unset, UUID] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    pool: Union[Unset, str] = UNSET,
    pool_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> list["OpenStackPoolMember"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        field (Union[Unset, list[OpenStackPoolMemberFieldEnum]]):
        load_balancer_uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        pool (Union[Unset, str]):
        pool_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[CoreStates]]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OpenStackPoolMember']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[OpenStackPoolMember] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        field=field,
        load_balancer_uuid=load_balancer_uuid,
        name=name,
        name_exact=name_exact,
        pool=pool,
        pool_uuid=pool_uuid,
        state=state,
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
    field: Union[Unset, list[OpenStackPoolMemberFieldEnum]] = UNSET,
    load_balancer_uuid: Union[Unset, UUID] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    pool: Union[Unset, str] = UNSET,
    pool_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> list["OpenStackPoolMember"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        field (Union[Unset, list[OpenStackPoolMemberFieldEnum]]):
        load_balancer_uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        pool (Union[Unset, str]):
        pool_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[CoreStates]]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OpenStackPoolMember']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[OpenStackPoolMember] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        field=field,
        load_balancer_uuid=load_balancer_uuid,
        name=name,
        name_exact=name_exact,
        pool=pool,
        pool_uuid=pool_uuid,
        state=state,
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
