from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.configuration_retrieve_response_200 import ConfigurationRetrieveResponse200
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/configuration/",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> ConfigurationRetrieveResponse200:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ConfigurationRetrieveResponse200.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ConfigurationRetrieveResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[ConfigurationRetrieveResponse200]:
    """Get public configuration

     Returns a dictionary of public settings for the Waldur deployment. This includes feature flags,
    authentication methods, and other configuration details that are safe to expose to any user.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConfigurationRetrieveResponse200]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> ConfigurationRetrieveResponse200:
    """Get public configuration

     Returns a dictionary of public settings for the Waldur deployment. This includes feature flags,
    authentication methods, and other configuration details that are safe to expose to any user.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConfigurationRetrieveResponse200
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[ConfigurationRetrieveResponse200]:
    """Get public configuration

     Returns a dictionary of public settings for the Waldur deployment. This includes feature flags,
    authentication methods, and other configuration details that are safe to expose to any user.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConfigurationRetrieveResponse200]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> ConfigurationRetrieveResponse200:
    """Get public configuration

     Returns a dictionary of public settings for the Waldur deployment. This includes feature flags,
    authentication methods, and other configuration details that are safe to expose to any user.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConfigurationRetrieveResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
