from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.settings_response import SettingsResponse
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/settings",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | SettingsResponse | None:
    if response.status_code == 200:
        response_200 = SettingsResponse.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | SettingsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[Error | SettingsResponse]:
    """ The signed-in user's own forge configuration

     Forge tokens are never returned, only whether one is set. The
    webhook token and secret are returned, since the user pastes them
    into the forge's webhook setup, and a first read creates them. For
    a read that creates nothing and omits both, see
    `GET /api/v1/settings/summary`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SettingsResponse]
     """


    kwargs = _get_kwargs(
        
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,

) -> Error | SettingsResponse | None:
    """ The signed-in user's own forge configuration

     Forge tokens are never returned, only whether one is set. The
    webhook token and secret are returned, since the user pastes them
    into the forge's webhook setup, and a first read creates them. For
    a read that creates nothing and omits both, see
    `GET /api/v1/settings/summary`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SettingsResponse
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[Error | SettingsResponse]:
    """ The signed-in user's own forge configuration

     Forge tokens are never returned, only whether one is set. The
    webhook token and secret are returned, since the user pastes them
    into the forge's webhook setup, and a first read creates them. For
    a read that creates nothing and omits both, see
    `GET /api/v1/settings/summary`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SettingsResponse]
     """


    kwargs = _get_kwargs(
        
    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,

) -> Error | SettingsResponse | None:
    """ The signed-in user's own forge configuration

     Forge tokens are never returned, only whether one is set. The
    webhook token and secret are returned, since the user pastes them
    into the forge's webhook setup, and a first read creates them. For
    a read that creates nothing and omits both, see
    `GET /api/v1/settings/summary`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SettingsResponse
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
