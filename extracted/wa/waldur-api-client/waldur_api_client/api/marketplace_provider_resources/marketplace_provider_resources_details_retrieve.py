from http import HTTPStatus
from typing import Any, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.marketplace_provider_resources_details_retrieve_response_200 import (
    MarketplaceProviderResourcesDetailsRetrieveResponse200,
)
from ...types import Response


def _get_kwargs(
    uuid: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/marketplace-provider-resources/{uuid}/details/",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Any, MarketplaceProviderResourcesDetailsRetrieveResponse200]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = MarketplaceProviderResourcesDetailsRetrieveResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, MarketplaceProviderResourcesDetailsRetrieveResponse200]]:
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
) -> Response[Union[Any, MarketplaceProviderResourcesDetailsRetrieveResponse200]]:
    """Get resource details

     Returns the detailed representation of the backend resource associated with the marketplace
    resource. The format of the response depends on the resource type.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, MarketplaceProviderResourcesDetailsRetrieveResponse200]]
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
) -> Union[Any, MarketplaceProviderResourcesDetailsRetrieveResponse200]:
    """Get resource details

     Returns the detailed representation of the backend resource associated with the marketplace
    resource. The format of the response depends on the resource type.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, MarketplaceProviderResourcesDetailsRetrieveResponse200]
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, MarketplaceProviderResourcesDetailsRetrieveResponse200]]:
    """Get resource details

     Returns the detailed representation of the backend resource associated with the marketplace
    resource. The format of the response depends on the resource type.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, MarketplaceProviderResourcesDetailsRetrieveResponse200]]
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
) -> Union[Any, MarketplaceProviderResourcesDetailsRetrieveResponse200]:
    """Get resource details

     Returns the detailed representation of the backend resource associated with the marketplace
    resource. The format of the response depends on the resource type.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, MarketplaceProviderResourcesDetailsRetrieveResponse200]
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
        )
    ).parsed
