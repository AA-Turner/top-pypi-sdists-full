from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.offering_access_subnets import OfferingAccessSubnets
from ...types import Response


def _get_kwargs(
    uuid: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/marketplace-provider-offerings/{uuid}/access_subnets/",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> OfferingAccessSubnets:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = OfferingAccessSubnets.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[OfferingAccessSubnets]:
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
) -> Response[OfferingAccessSubnets]:
    """List access subnets for an offering

     Returns the access subnets consumers defined for the offering, in two forms: 'expanded' — every
    subnet with its customer and offering context; and 'packed' — the same subnets collapsed into the
    minimal set of CIDRs (adjacent/overlapping networks merged). Consumer subnets are defined per
    (customer, offering) pair and apply to all of that customer's resources of the offering. Intended
    for service providers building an external firewall allow-list. Available to staff, support, the
    offering's service manager and the offering customer owner.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OfferingAccessSubnets]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> OfferingAccessSubnets:
    """List access subnets for an offering

     Returns the access subnets consumers defined for the offering, in two forms: 'expanded' — every
    subnet with its customer and offering context; and 'packed' — the same subnets collapsed into the
    minimal set of CIDRs (adjacent/overlapping networks merged). Consumer subnets are defined per
    (customer, offering) pair and apply to all of that customer's resources of the offering. Intended
    for service providers building an external firewall allow-list. Available to staff, support, the
    offering's service manager and the offering customer owner.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OfferingAccessSubnets
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[OfferingAccessSubnets]:
    """List access subnets for an offering

     Returns the access subnets consumers defined for the offering, in two forms: 'expanded' — every
    subnet with its customer and offering context; and 'packed' — the same subnets collapsed into the
    minimal set of CIDRs (adjacent/overlapping networks merged). Consumer subnets are defined per
    (customer, offering) pair and apply to all of that customer's resources of the offering. Intended
    for service providers building an external firewall allow-list. Available to staff, support, the
    offering's service manager and the offering customer owner.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OfferingAccessSubnets]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> OfferingAccessSubnets:
    """List access subnets for an offering

     Returns the access subnets consumers defined for the offering, in two forms: 'expanded' — every
    subnet with its customer and offering context; and 'packed' — the same subnets collapsed into the
    minimal set of CIDRs (adjacent/overlapping networks merged). Consumer subnets are defined per
    (customer, offering) pair and apply to all of that customer's resources of the offering. Intended
    for service providers building an external firewall allow-list. Available to staff, support, the
    offering's service manager and the offering customer owner.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OfferingAccessSubnets
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
        )
    ).parsed
