from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.access_subnet_impact import AccessSubnetImpact
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    access_subnet_uuid: Union[Unset, UUID] = UNSET,
    customer_uuid: UUID,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_access_subnet_uuid: Union[Unset, str] = UNSET
    if not isinstance(access_subnet_uuid, Unset):
        json_access_subnet_uuid = str(access_subnet_uuid)
    params["access_subnet_uuid"] = json_access_subnet_uuid

    json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/access-subnets/resource_impact/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> AccessSubnetImpact:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = AccessSubnetImpact.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[AccessSubnetImpact]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    access_subnet_uuid: Union[Unset, UUID] = UNSET,
    customer_uuid: UUID,
) -> Response[AccessSubnetImpact]:
    """Show which resources the access subnets reach

     For each of the organization's live resources of an offering that supports access subnets, the
    addresses that may reach it, where each came from, and whether the list is enforced or merely
    advisory. Resources of offerings without access subnet support are omitted: no allow-list can apply
    to them. Pass access_subnet_uuid to narrow it to the resources one address reaches.

    Args:
        access_subnet_uuid (Union[Unset, UUID]):
        customer_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccessSubnetImpact]
    """

    kwargs = _get_kwargs(
        access_subnet_uuid=access_subnet_uuid,
        customer_uuid=customer_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    access_subnet_uuid: Union[Unset, UUID] = UNSET,
    customer_uuid: UUID,
) -> AccessSubnetImpact:
    """Show which resources the access subnets reach

     For each of the organization's live resources of an offering that supports access subnets, the
    addresses that may reach it, where each came from, and whether the list is enforced or merely
    advisory. Resources of offerings without access subnet support are omitted: no allow-list can apply
    to them. Pass access_subnet_uuid to narrow it to the resources one address reaches.

    Args:
        access_subnet_uuid (Union[Unset, UUID]):
        customer_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AccessSubnetImpact
    """

    return sync_detailed(
        client=client,
        access_subnet_uuid=access_subnet_uuid,
        customer_uuid=customer_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    access_subnet_uuid: Union[Unset, UUID] = UNSET,
    customer_uuid: UUID,
) -> Response[AccessSubnetImpact]:
    """Show which resources the access subnets reach

     For each of the organization's live resources of an offering that supports access subnets, the
    addresses that may reach it, where each came from, and whether the list is enforced or merely
    advisory. Resources of offerings without access subnet support are omitted: no allow-list can apply
    to them. Pass access_subnet_uuid to narrow it to the resources one address reaches.

    Args:
        access_subnet_uuid (Union[Unset, UUID]):
        customer_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccessSubnetImpact]
    """

    kwargs = _get_kwargs(
        access_subnet_uuid=access_subnet_uuid,
        customer_uuid=customer_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    access_subnet_uuid: Union[Unset, UUID] = UNSET,
    customer_uuid: UUID,
) -> AccessSubnetImpact:
    """Show which resources the access subnets reach

     For each of the organization's live resources of an offering that supports access subnets, the
    addresses that may reach it, where each came from, and whether the list is enforced or merely
    advisory. Resources of offerings without access subnet support are omitted: no allow-list can apply
    to them. Pass access_subnet_uuid to narrow it to the resources one address reaches.

    Args:
        access_subnet_uuid (Union[Unset, UUID]):
        customer_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AccessSubnetImpact
    """

    return (
        await asyncio_detailed(
            client=client,
            access_subnet_uuid=access_subnet_uuid,
            customer_uuid=customer_uuid,
        )
    ).parsed
