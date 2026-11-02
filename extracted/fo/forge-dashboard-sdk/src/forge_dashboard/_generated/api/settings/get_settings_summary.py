from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.settings_summary import SettingsSummary
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/settings/summary",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | SettingsSummary | None:
    if response.status_code == 200:
        response_200 = SettingsSummary.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | SettingsSummary]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[Error | SettingsSummary]:
    """ The signed-in user's settings, read without side effects

     The same data as `GET /api/v1/settings`, minus the webhook token and
    secret, plus `webhookConfigured`. It never provisions webhook
    credentials: for a user who has none yet it answers
    `webhookConfigured: false` and creates nothing. Forge tokens are
    never returned, only whether one is set. It returns exactly what
    the `get_settings` MCP tool returns.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SettingsSummary]
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

) -> Error | SettingsSummary | None:
    """ The signed-in user's settings, read without side effects

     The same data as `GET /api/v1/settings`, minus the webhook token and
    secret, plus `webhookConfigured`. It never provisions webhook
    credentials: for a user who has none yet it answers
    `webhookConfigured: false` and creates nothing. Forge tokens are
    never returned, only whether one is set. It returns exactly what
    the `get_settings` MCP tool returns.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SettingsSummary
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[Error | SettingsSummary]:
    """ The signed-in user's settings, read without side effects

     The same data as `GET /api/v1/settings`, minus the webhook token and
    secret, plus `webhookConfigured`. It never provisions webhook
    credentials: for a user who has none yet it answers
    `webhookConfigured: false` and creates nothing. Forge tokens are
    never returned, only whether one is set. It returns exactly what
    the `get_settings` MCP tool returns.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SettingsSummary]
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

) -> Error | SettingsSummary | None:
    """ The signed-in user's settings, read without side effects

     The same data as `GET /api/v1/settings`, minus the webhook token and
    secret, plus `webhookConfigured`. It never provisions webhook
    credentials: for a user who has none yet it answers
    `webhookConfigured: false` and creates nothing. Forge tokens are
    never returned, only whether one is set. It returns exactly what
    the `get_settings` MCP tool returns.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SettingsSummary
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
