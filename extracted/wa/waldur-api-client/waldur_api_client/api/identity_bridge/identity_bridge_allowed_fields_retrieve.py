from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.identity_bridge_allowed_fields import IdentityBridgeAllowedFields
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/identity-bridge/allowed-fields/",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> IdentityBridgeAllowedFields:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = IdentityBridgeAllowedFields.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[IdentityBridgeAllowedFields]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[IdentityBridgeAllowedFields]:
    """Get allowed Identity Bridge fields

     Returns the list of user attribute fields that the Identity Bridge currently accepts. Useful for
    clients to pre-filter payloads. Requires staff or identity manager permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[IdentityBridgeAllowedFields]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> IdentityBridgeAllowedFields:
    """Get allowed Identity Bridge fields

     Returns the list of user attribute fields that the Identity Bridge currently accepts. Useful for
    clients to pre-filter payloads. Requires staff or identity manager permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        IdentityBridgeAllowedFields
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[IdentityBridgeAllowedFields]:
    """Get allowed Identity Bridge fields

     Returns the list of user attribute fields that the Identity Bridge currently accepts. Useful for
    clients to pre-filter payloads. Requires staff or identity manager permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[IdentityBridgeAllowedFields]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> IdentityBridgeAllowedFields:
    """Get allowed Identity Bridge fields

     Returns the list of user attribute fields that the Identity Bridge currently accepts. Useful for
    clients to pre-filter payloads. Requires staff or identity manager permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        IdentityBridgeAllowedFields
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
