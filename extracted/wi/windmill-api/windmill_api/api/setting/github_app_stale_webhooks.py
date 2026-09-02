from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.github_app_stale_webhooks_response_200_item import GithubAppStaleWebhooksResponse200Item
from ...types import Response


def _get_kwargs() -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/settings/github_app_stale_webhooks",
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["GithubAppStaleWebhooksResponse200Item"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = GithubAppStaleWebhooksResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["GithubAppStaleWebhooksResponse200Item"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[List["GithubAppStaleWebhooksResponse200Item"]]:
    """list git-sync repositories whose webhook still points at a previous receiver

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['GithubAppStaleWebhooksResponse200Item']]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[List["GithubAppStaleWebhooksResponse200Item"]]:
    """list git-sync repositories whose webhook still points at a previous receiver

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['GithubAppStaleWebhooksResponse200Item']
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[List["GithubAppStaleWebhooksResponse200Item"]]:
    """list git-sync repositories whose webhook still points at a previous receiver

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['GithubAppStaleWebhooksResponse200Item']]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[List["GithubAppStaleWebhooksResponse200Item"]]:
    """list git-sync repositories whose webhook still points at a previous receiver

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['GithubAppStaleWebhooksResponse200Item']
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
