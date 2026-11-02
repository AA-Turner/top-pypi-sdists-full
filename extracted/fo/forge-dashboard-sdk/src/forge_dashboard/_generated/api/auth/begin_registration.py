from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.web_authn_ceremony_options import WebAuthnCeremonyOptions
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/auth/register/begin",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | WebAuthnCeremonyOptions | None:
    if response.status_code == 200:
        response_200 = WebAuthnCeremonyOptions.from_dict(response.json())



        return response_200

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())



        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | WebAuthnCeremonyOptions]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,

) -> Response[Error | WebAuthnCeremonyOptions]:
    """ Start a passkey registration ceremony

     An instance has one user. The first registration on a fresh
    instance (see GET /api/v1/auth/registration-status) creates that
    user and the server names it, so the request carries no body. The
    options require a resident key, so the passkey can be found at
    sign-in without being named. Once any account holds a passkey, this
    answers 403.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | WebAuthnCeremonyOptions]
     """


    kwargs = _get_kwargs(
        
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,

) -> Error | WebAuthnCeremonyOptions | None:
    """ Start a passkey registration ceremony

     An instance has one user. The first registration on a fresh
    instance (see GET /api/v1/auth/registration-status) creates that
    user and the server names it, so the request carries no body. The
    options require a resident key, so the passkey can be found at
    sign-in without being named. Once any account holds a passkey, this
    answers 403.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | WebAuthnCeremonyOptions
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,

) -> Response[Error | WebAuthnCeremonyOptions]:
    """ Start a passkey registration ceremony

     An instance has one user. The first registration on a fresh
    instance (see GET /api/v1/auth/registration-status) creates that
    user and the server names it, so the request carries no body. The
    options require a resident key, so the passkey can be found at
    sign-in without being named. Once any account holds a passkey, this
    answers 403.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | WebAuthnCeremonyOptions]
     """


    kwargs = _get_kwargs(
        
    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,

) -> Error | WebAuthnCeremonyOptions | None:
    """ Start a passkey registration ceremony

     An instance has one user. The first registration on a fresh
    instance (see GET /api/v1/auth/registration-status) creates that
    user and the server names it, so the request carries no body. The
    options require a resident key, so the passkey can be found at
    sign-in without being named. Once any account holds a passkey, this
    answers 403.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | WebAuthnCeremonyOptions
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
