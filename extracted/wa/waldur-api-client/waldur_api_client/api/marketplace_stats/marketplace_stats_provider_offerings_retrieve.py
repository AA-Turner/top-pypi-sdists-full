from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.provider_offering_stats import ProviderOfferingStats
from ...types import UNSET, Response


def _get_kwargs(
    *,
    provider_uuid: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["provider_uuid"] = provider_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/marketplace-stats/provider_offerings/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ProviderOfferingStats:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ProviderOfferingStats.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ProviderOfferingStats]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    provider_uuid: str,
) -> Response[ProviderOfferingStats]:
    """Return offering performance statistics for a service provider.

    Args:
        provider_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProviderOfferingStats]
    """

    kwargs = _get_kwargs(
        provider_uuid=provider_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    provider_uuid: str,
) -> ProviderOfferingStats:
    """Return offering performance statistics for a service provider.

    Args:
        provider_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProviderOfferingStats
    """

    return sync_detailed(
        client=client,
        provider_uuid=provider_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    provider_uuid: str,
) -> Response[ProviderOfferingStats]:
    """Return offering performance statistics for a service provider.

    Args:
        provider_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProviderOfferingStats]
    """

    kwargs = _get_kwargs(
        provider_uuid=provider_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    provider_uuid: str,
) -> ProviderOfferingStats:
    """Return offering performance statistics for a service provider.

    Args:
        provider_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProviderOfferingStats
    """

    return (
        await asyncio_detailed(
            client=client,
            provider_uuid=provider_uuid,
        )
    ).parsed
