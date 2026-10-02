from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.available_external_network import AvailableExternalNetwork
from ...models.core_states import CoreStates
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    uuid: UUID,
    *,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["name"] = name

    params["name_exact"] = name_exact

    params["page"] = page

    params["page_size"] = page_size

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

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/openstack-routers/{uuid}/available_external_networks/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["AvailableExternalNetwork"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = AvailableExternalNetwork.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["AvailableExternalNetwork"]]:
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
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["AvailableExternalNetwork"]]:
    """List available external networks

     Returns a merged list of external networks available for this router's tenant, from both global
    external networks and RBAC-exposed networks.

    Args:
        uuid (UUID):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, list[CoreStates]]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AvailableExternalNetwork']]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        name=name,
        name_exact=name_exact,
        page=page,
        page_size=page_size,
        state=state,
        tenant=tenant,
        tenant_uuid=tenant_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> list["AvailableExternalNetwork"]:
    """List available external networks

     Returns a merged list of external networks available for this router's tenant, from both global
    external networks and RBAC-exposed networks.

    Args:
        uuid (UUID):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, list[CoreStates]]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AvailableExternalNetwork']
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        name=name,
        name_exact=name_exact,
        page=page,
        page_size=page_size,
        state=state,
        tenant=tenant,
        tenant_uuid=tenant_uuid,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["AvailableExternalNetwork"]]:
    """List available external networks

     Returns a merged list of external networks available for this router's tenant, from both global
    external networks and RBAC-exposed networks.

    Args:
        uuid (UUID):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, list[CoreStates]]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AvailableExternalNetwork']]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        name=name,
        name_exact=name_exact,
        page=page,
        page_size=page_size,
        state=state,
        tenant=tenant,
        tenant_uuid=tenant_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> list["AvailableExternalNetwork"]:
    """List available external networks

     Returns a merged list of external networks available for this router's tenant, from both global
    external networks and RBAC-exposed networks.

    Args:
        uuid (UUID):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, list[CoreStates]]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AvailableExternalNetwork']
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            name=name,
            name_exact=name_exact,
            page=page,
            page_size=page_size,
            state=state,
            tenant=tenant,
            tenant_uuid=tenant_uuid,
        )
    ).parsed


def sync_all(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> list["AvailableExternalNetwork"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        uuid (UUID):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        state (Union[Unset, list[CoreStates]]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AvailableExternalNetwork']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[AvailableExternalNetwork] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        uuid=uuid,
        name=name,
        name_exact=name_exact,
        state=state,
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
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> list["AvailableExternalNetwork"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        uuid (UUID):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        state (Union[Unset, list[CoreStates]]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AvailableExternalNetwork']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[AvailableExternalNetwork] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        uuid=uuid,
        name=name,
        name_exact=name_exact,
        state=state,
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
