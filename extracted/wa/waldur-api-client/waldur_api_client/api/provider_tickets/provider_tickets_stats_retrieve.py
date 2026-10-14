from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.provider_stats import ProviderStats
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    provider_helpdesk_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_provider_helpdesk_uuid: Union[Unset, str] = UNSET
    if not isinstance(provider_helpdesk_uuid, Unset):
        json_provider_helpdesk_uuid = str(provider_helpdesk_uuid)
    params["provider_helpdesk_uuid"] = json_provider_helpdesk_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/provider-tickets/stats/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ProviderStats:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ProviderStats.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ProviderStats]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    provider_helpdesk_uuid: Union[Unset, UUID] = UNSET,
) -> Response[ProviderStats]:
    """Get statistics for provider tickets

    Args:
        provider_helpdesk_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProviderStats]
    """

    kwargs = _get_kwargs(
        provider_helpdesk_uuid=provider_helpdesk_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    provider_helpdesk_uuid: Union[Unset, UUID] = UNSET,
) -> ProviderStats:
    """Get statistics for provider tickets

    Args:
        provider_helpdesk_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProviderStats
    """

    return sync_detailed(
        client=client,
        provider_helpdesk_uuid=provider_helpdesk_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    provider_helpdesk_uuid: Union[Unset, UUID] = UNSET,
) -> Response[ProviderStats]:
    """Get statistics for provider tickets

    Args:
        provider_helpdesk_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProviderStats]
    """

    kwargs = _get_kwargs(
        provider_helpdesk_uuid=provider_helpdesk_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    provider_helpdesk_uuid: Union[Unset, UUID] = UNSET,
) -> ProviderStats:
    """Get statistics for provider tickets

    Args:
        provider_helpdesk_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProviderStats
    """

    return (
        await asyncio_detailed(
            client=client,
            provider_helpdesk_uuid=provider_helpdesk_uuid,
        )
    ).parsed
