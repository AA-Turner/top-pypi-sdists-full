from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.core_states import CoreStates
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
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
        "method": "head",
        "url": "/api/openstack-health-monitors/",
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
    load_balancer_uuid: Union[Unset, UUID] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    pool: Union[Unset, str] = UNSET,
    pool_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """List health monitors

     Get number of items in the collection matching the request parameters.

    Args:
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
        Response[int]
    """

    kwargs = _get_kwargs(
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
    load_balancer_uuid: Union[Unset, UUID] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    pool: Union[Unset, str] = UNSET,
    pool_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> int:
    """List health monitors

     Get number of items in the collection matching the request parameters.

    Args:
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
        int
    """

    return sync_detailed(
        client=client,
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
    load_balancer_uuid: Union[Unset, UUID] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    pool: Union[Unset, str] = UNSET,
    pool_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """List health monitors

     Get number of items in the collection matching the request parameters.

    Args:
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
        Response[int]
    """

    kwargs = _get_kwargs(
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
    load_balancer_uuid: Union[Unset, UUID] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    pool: Union[Unset, str] = UNSET,
    pool_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CoreStates]] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> int:
    """List health monitors

     Get number of items in the collection matching the request parameters.

    Args:
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
        int
    """

    return (
        await asyncio_detailed(
            client=client,
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
