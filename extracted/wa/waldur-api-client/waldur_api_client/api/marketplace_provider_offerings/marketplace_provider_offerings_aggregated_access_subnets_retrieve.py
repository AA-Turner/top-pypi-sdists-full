from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.aggregated_access_subnets import AggregatedAccessSubnets
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    include_organization_subnets: Union[Unset, bool] = UNSET,
    offering_uuid: list[UUID],
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["include_organization_subnets"] = include_organization_subnets

    json_offering_uuid = []
    for offering_uuid_item_data in offering_uuid:
        offering_uuid_item = str(offering_uuid_item_data)
        json_offering_uuid.append(offering_uuid_item)

    params["offering_uuid"] = json_offering_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/marketplace-provider-offerings/aggregated_access_subnets/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> AggregatedAccessSubnets:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = AggregatedAccessSubnets.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[AggregatedAccessSubnets]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    include_organization_subnets: Union[Unset, bool] = UNSET,
    offering_uuid: list[UUID],
) -> Response[AggregatedAccessSubnets]:
    """Aggregate access subnets across offerings

     Returns the combined access-subnet allow-list of the given offerings: 'expanded' — every consumer
    subnet with its customer and offering context; 'defaults' — the provider-default subnets of each
    offering; 'organization_subnets' — organization-level access subnets of customers owning non-
    terminated resources of the offerings (populated only when include_organization_subnets is true);
    and 'packed' — all of the above collapsed into the minimal set of CIDRs. Intended for service
    providers building an external firewall allow-list spanning several offerings. The caller must be
    staff, support, a service manager of every requested offering or an owner of its customer.

    Args:
        include_organization_subnets (Union[Unset, bool]):
        offering_uuid (list[UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AggregatedAccessSubnets]
    """

    kwargs = _get_kwargs(
        include_organization_subnets=include_organization_subnets,
        offering_uuid=offering_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    include_organization_subnets: Union[Unset, bool] = UNSET,
    offering_uuid: list[UUID],
) -> AggregatedAccessSubnets:
    """Aggregate access subnets across offerings

     Returns the combined access-subnet allow-list of the given offerings: 'expanded' — every consumer
    subnet with its customer and offering context; 'defaults' — the provider-default subnets of each
    offering; 'organization_subnets' — organization-level access subnets of customers owning non-
    terminated resources of the offerings (populated only when include_organization_subnets is true);
    and 'packed' — all of the above collapsed into the minimal set of CIDRs. Intended for service
    providers building an external firewall allow-list spanning several offerings. The caller must be
    staff, support, a service manager of every requested offering or an owner of its customer.

    Args:
        include_organization_subnets (Union[Unset, bool]):
        offering_uuid (list[UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AggregatedAccessSubnets
    """

    return sync_detailed(
        client=client,
        include_organization_subnets=include_organization_subnets,
        offering_uuid=offering_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    include_organization_subnets: Union[Unset, bool] = UNSET,
    offering_uuid: list[UUID],
) -> Response[AggregatedAccessSubnets]:
    """Aggregate access subnets across offerings

     Returns the combined access-subnet allow-list of the given offerings: 'expanded' — every consumer
    subnet with its customer and offering context; 'defaults' — the provider-default subnets of each
    offering; 'organization_subnets' — organization-level access subnets of customers owning non-
    terminated resources of the offerings (populated only when include_organization_subnets is true);
    and 'packed' — all of the above collapsed into the minimal set of CIDRs. Intended for service
    providers building an external firewall allow-list spanning several offerings. The caller must be
    staff, support, a service manager of every requested offering or an owner of its customer.

    Args:
        include_organization_subnets (Union[Unset, bool]):
        offering_uuid (list[UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AggregatedAccessSubnets]
    """

    kwargs = _get_kwargs(
        include_organization_subnets=include_organization_subnets,
        offering_uuid=offering_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    include_organization_subnets: Union[Unset, bool] = UNSET,
    offering_uuid: list[UUID],
) -> AggregatedAccessSubnets:
    """Aggregate access subnets across offerings

     Returns the combined access-subnet allow-list of the given offerings: 'expanded' — every consumer
    subnet with its customer and offering context; 'defaults' — the provider-default subnets of each
    offering; 'organization_subnets' — organization-level access subnets of customers owning non-
    terminated resources of the offerings (populated only when include_organization_subnets is true);
    and 'packed' — all of the above collapsed into the minimal set of CIDRs. Intended for service
    providers building an external firewall allow-list spanning several offerings. The caller must be
    staff, support, a service manager of every requested offering or an owner of its customer.

    Args:
        include_organization_subnets (Union[Unset, bool]):
        offering_uuid (list[UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AggregatedAccessSubnets
    """

    return (
        await asyncio_detailed(
            client=client,
            include_organization_subnets=include_organization_subnets,
            offering_uuid=offering_uuid,
        )
    ).parsed
