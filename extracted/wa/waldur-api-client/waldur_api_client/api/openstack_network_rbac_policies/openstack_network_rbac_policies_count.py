from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.policy_type_enum import PolicyTypeEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    network: Union[Unset, str] = UNSET,
    network_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    policy_type: Union[Unset, PolicyTypeEnum] = UNSET,
    target_tenant: Union[Unset, str] = UNSET,
    target_tenant_uuid: Union[Unset, UUID] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["network"] = network

    json_network_uuid: Union[Unset, str] = UNSET
    if not isinstance(network_uuid, Unset):
        json_network_uuid = str(network_uuid)
    params["network_uuid"] = json_network_uuid

    params["page"] = page

    params["page_size"] = page_size

    json_policy_type: Union[Unset, str] = UNSET
    if not isinstance(policy_type, Unset):
        json_policy_type = policy_type.value

    params["policy_type"] = json_policy_type

    params["target_tenant"] = target_tenant

    json_target_tenant_uuid: Union[Unset, str] = UNSET
    if not isinstance(target_tenant_uuid, Unset):
        json_target_tenant_uuid = str(target_tenant_uuid)
    params["target_tenant_uuid"] = json_target_tenant_uuid

    params["tenant"] = tenant

    json_tenant_uuid: Union[Unset, str] = UNSET
    if not isinstance(tenant_uuid, Unset):
        json_tenant_uuid = str(tenant_uuid)
    params["tenant_uuid"] = json_tenant_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/openstack-network-rbac-policies/",
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
    network: Union[Unset, str] = UNSET,
    network_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    policy_type: Union[Unset, PolicyTypeEnum] = UNSET,
    target_tenant: Union[Unset, str] = UNSET,
    target_tenant_uuid: Union[Unset, UUID] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """List network RBAC policies

     Get number of items in the collection matching the request parameters.

    Args:
        network (Union[Unset, str]):
        network_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        policy_type (Union[Unset, PolicyTypeEnum]):
        target_tenant (Union[Unset, str]):
        target_tenant_uuid (Union[Unset, UUID]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        network=network,
        network_uuid=network_uuid,
        page=page,
        page_size=page_size,
        policy_type=policy_type,
        target_tenant=target_tenant,
        target_tenant_uuid=target_tenant_uuid,
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
    network: Union[Unset, str] = UNSET,
    network_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    policy_type: Union[Unset, PolicyTypeEnum] = UNSET,
    target_tenant: Union[Unset, str] = UNSET,
    target_tenant_uuid: Union[Unset, UUID] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> int:
    """List network RBAC policies

     Get number of items in the collection matching the request parameters.

    Args:
        network (Union[Unset, str]):
        network_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        policy_type (Union[Unset, PolicyTypeEnum]):
        target_tenant (Union[Unset, str]):
        target_tenant_uuid (Union[Unset, UUID]):
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
        network=network,
        network_uuid=network_uuid,
        page=page,
        page_size=page_size,
        policy_type=policy_type,
        target_tenant=target_tenant,
        target_tenant_uuid=target_tenant_uuid,
        tenant=tenant,
        tenant_uuid=tenant_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    network: Union[Unset, str] = UNSET,
    network_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    policy_type: Union[Unset, PolicyTypeEnum] = UNSET,
    target_tenant: Union[Unset, str] = UNSET,
    target_tenant_uuid: Union[Unset, UUID] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """List network RBAC policies

     Get number of items in the collection matching the request parameters.

    Args:
        network (Union[Unset, str]):
        network_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        policy_type (Union[Unset, PolicyTypeEnum]):
        target_tenant (Union[Unset, str]):
        target_tenant_uuid (Union[Unset, UUID]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        network=network,
        network_uuid=network_uuid,
        page=page,
        page_size=page_size,
        policy_type=policy_type,
        target_tenant=target_tenant,
        target_tenant_uuid=target_tenant_uuid,
        tenant=tenant,
        tenant_uuid=tenant_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    network: Union[Unset, str] = UNSET,
    network_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    policy_type: Union[Unset, PolicyTypeEnum] = UNSET,
    target_tenant: Union[Unset, str] = UNSET,
    target_tenant_uuid: Union[Unset, UUID] = UNSET,
    tenant: Union[Unset, str] = UNSET,
    tenant_uuid: Union[Unset, UUID] = UNSET,
) -> int:
    """List network RBAC policies

     Get number of items in the collection matching the request parameters.

    Args:
        network (Union[Unset, str]):
        network_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        policy_type (Union[Unset, PolicyTypeEnum]):
        target_tenant (Union[Unset, str]):
        target_tenant_uuid (Union[Unset, UUID]):
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
            network=network,
            network_uuid=network_uuid,
            page=page,
            page_size=page_size,
            policy_type=policy_type,
            target_tenant=target_tenant,
            target_tenant_uuid=target_tenant_uuid,
            tenant=tenant,
            tenant_uuid=tenant_uuid,
        )
    ).parsed
