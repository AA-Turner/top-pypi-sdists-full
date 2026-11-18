from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx2

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.connection_authorize_response import ConnectionAuthorizeResponse
from ...models.error import Error
from ...models.start_forgejo_connection_request import StartForgejoConnectionRequest
from typing import cast



def _get_kwargs(
    *,
    body: StartForgejoConnectionRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/connections/forgejo",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> ConnectionAuthorizeResponse | Error | None:
    if response.status_code == 200:
        response_200 = ConnectionAuthorizeResponse.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())



        return response_409

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Response[ConnectionAuthorizeResponse | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: StartForgejoConnectionRequest,

) -> Response[ConnectionAuthorizeResponse | Error]:
    """ Start linking a Forgejo account with OAuth

     Begins the authorization code flow with PKCE (RFC 9700) against the
    given Forgejo instance and returns the instance's consent page URL.
    The browser goes there; Forgejo sends it back to
    `GET /api/v1/connections/forgejo/callback`. Fails with 409 when an
    instance is already connected: the instance is locked until
    `DELETE /api/v1/connections/forgejo`, and `PUT /api/v1/settings`
    refuses to change `forgejoUrl` meanwhile. Replaces pasting a Forgejo
    token. Needs `FORGEJO_OAUTH_CLIENT_ID` and
    `FORGEJO_OAUTH_CLIENT_SECRET` on the server; see
    `SettingsResponse.forgejoOAuthConfigured`.

    Args:
        body (StartForgejoConnectionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConnectionAuthorizeResponse | Error]
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
    body: StartForgejoConnectionRequest,

) -> ConnectionAuthorizeResponse | Error | None:
    """ Start linking a Forgejo account with OAuth

     Begins the authorization code flow with PKCE (RFC 9700) against the
    given Forgejo instance and returns the instance's consent page URL.
    The browser goes there; Forgejo sends it back to
    `GET /api/v1/connections/forgejo/callback`. Fails with 409 when an
    instance is already connected: the instance is locked until
    `DELETE /api/v1/connections/forgejo`, and `PUT /api/v1/settings`
    refuses to change `forgejoUrl` meanwhile. Replaces pasting a Forgejo
    token. Needs `FORGEJO_OAUTH_CLIENT_ID` and
    `FORGEJO_OAUTH_CLIENT_SECRET` on the server; see
    `SettingsResponse.forgejoOAuthConfigured`.

    Args:
        body (StartForgejoConnectionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConnectionAuthorizeResponse | Error
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: StartForgejoConnectionRequest,

) -> Response[ConnectionAuthorizeResponse | Error]:
    """ Start linking a Forgejo account with OAuth

     Begins the authorization code flow with PKCE (RFC 9700) against the
    given Forgejo instance and returns the instance's consent page URL.
    The browser goes there; Forgejo sends it back to
    `GET /api/v1/connections/forgejo/callback`. Fails with 409 when an
    instance is already connected: the instance is locked until
    `DELETE /api/v1/connections/forgejo`, and `PUT /api/v1/settings`
    refuses to change `forgejoUrl` meanwhile. Replaces pasting a Forgejo
    token. Needs `FORGEJO_OAUTH_CLIENT_ID` and
    `FORGEJO_OAUTH_CLIENT_SECRET` on the server; see
    `SettingsResponse.forgejoOAuthConfigured`.

    Args:
        body (StartForgejoConnectionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConnectionAuthorizeResponse | Error]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    body: StartForgejoConnectionRequest,

) -> ConnectionAuthorizeResponse | Error | None:
    """ Start linking a Forgejo account with OAuth

     Begins the authorization code flow with PKCE (RFC 9700) against the
    given Forgejo instance and returns the instance's consent page URL.
    The browser goes there; Forgejo sends it back to
    `GET /api/v1/connections/forgejo/callback`. Fails with 409 when an
    instance is already connected: the instance is locked until
    `DELETE /api/v1/connections/forgejo`, and `PUT /api/v1/settings`
    refuses to change `forgejoUrl` meanwhile. Replaces pasting a Forgejo
    token. Needs `FORGEJO_OAUTH_CLIENT_ID` and
    `FORGEJO_OAUTH_CLIENT_SECRET` on the server; see
    `SettingsResponse.forgejoOAuthConfigured`.

    Args:
        body (StartForgejoConnectionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConnectionAuthorizeResponse | Error
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
