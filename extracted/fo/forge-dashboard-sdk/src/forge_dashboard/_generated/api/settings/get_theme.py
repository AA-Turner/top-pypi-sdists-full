from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.theme_response import ThemeResponse
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/settings/theme",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | ThemeResponse | None:
    if response.status_code == 200:
        response_200 = ThemeResponse.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | ThemeResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[Error | ThemeResponse]:
    """ The signed-in user's own saved theme preference

     A lightweight, side-effect-free read of one field — theme — for
    every page to check on load. Deliberately not
    GET /api/v1/settings itself: that handler also provisions webhook
    credentials on first call (EnsureWebhookCredentials), which
    every page loading shouldn't trigger for a user who's never
    opened Settings at all.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ThemeResponse]
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

) -> Error | ThemeResponse | None:
    """ The signed-in user's own saved theme preference

     A lightweight, side-effect-free read of one field — theme — for
    every page to check on load. Deliberately not
    GET /api/v1/settings itself: that handler also provisions webhook
    credentials on first call (EnsureWebhookCredentials), which
    every page loading shouldn't trigger for a user who's never
    opened Settings at all.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ThemeResponse
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[Error | ThemeResponse]:
    """ The signed-in user's own saved theme preference

     A lightweight, side-effect-free read of one field — theme — for
    every page to check on load. Deliberately not
    GET /api/v1/settings itself: that handler also provisions webhook
    credentials on first call (EnsureWebhookCredentials), which
    every page loading shouldn't trigger for a user who's never
    opened Settings at all.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ThemeResponse]
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

) -> Error | ThemeResponse | None:
    """ The signed-in user's own saved theme preference

     A lightweight, side-effect-free read of one field — theme — for
    every page to check on load. Deliberately not
    GET /api/v1/settings itself: that handler also provisions webhook
    credentials on first call (EnsureWebhookCredentials), which
    every page loading shouldn't trigger for a user who's never
    opened Settings at all.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ThemeResponse
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
