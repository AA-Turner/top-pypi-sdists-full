from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.config_create_request import ConfigCreateRequest
from ...models.config_response import ConfigResponse


def _get_kwargs(
    *,
    body: ConfigCreateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/configs",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/vnd.api+json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ConfigResponse | None:
    if response.status_code == 201:
        response_201 = ConfigResponse.from_dict(response.json())

        return response_201

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ConfigResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ConfigCreateRequest,
) -> Response[ConfigResponse]:
    """Create Config

     Create a config for this account.

    The caller supplies the config's key as `data.id`. Keys are unique
    within an account and immutable for the lifetime of the config.

    Args:
        body (ConfigCreateRequest): JSON:API request envelope for creating a config.

            Distinct from :class:`ConfigRequest` because create requires
            caller-supplied ``data.id`` while update does not.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConfigResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: ConfigCreateRequest,
) -> ConfigResponse | None:
    """Create Config

     Create a config for this account.

    The caller supplies the config's key as `data.id`. Keys are unique
    within an account and immutable for the lifetime of the config.

    Args:
        body (ConfigCreateRequest): JSON:API request envelope for creating a config.

            Distinct from :class:`ConfigRequest` because create requires
            caller-supplied ``data.id`` while update does not.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConfigResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ConfigCreateRequest,
) -> Response[ConfigResponse]:
    """Create Config

     Create a config for this account.

    The caller supplies the config's key as `data.id`. Keys are unique
    within an account and immutable for the lifetime of the config.

    Args:
        body (ConfigCreateRequest): JSON:API request envelope for creating a config.

            Distinct from :class:`ConfigRequest` because create requires
            caller-supplied ``data.id`` while update does not.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConfigResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ConfigCreateRequest,
) -> ConfigResponse | None:
    """Create Config

     Create a config for this account.

    The caller supplies the config's key as `data.id`. Keys are unique
    within an account and immutable for the lifetime of the config.

    Args:
        body (ConfigCreateRequest): JSON:API request envelope for creating a config.

            Distinct from :class:`ConfigRequest` because create requires
            caller-supplied ``data.id`` while update does not.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConfigResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
