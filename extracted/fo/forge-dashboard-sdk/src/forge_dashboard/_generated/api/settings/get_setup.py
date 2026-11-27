from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx2

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.setup_response import SetupResponse
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/setup",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Error | SetupResponse | None:
    if response.status_code == 200:
        response_200 = SetupResponse.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Response[Error | SetupResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[Error | SetupResponse]:
    """ What the first-login setup page needs to draw itself

     Facts only, never a verdict. The page decides which step is current,
    which state a forge is in and whether Continue is enabled. Reads no
    secret: a Forgejo Client ID is public, tokens are never returned.
    `github.installations` is the signed-in GitHub account's own
    installations of the App, read live with its token; when GitHub can't
    be asked it is empty and `installationsUnavailable` is true.
    Repository counts come from the last refresh of the board, and
    `refreshed` says whether one has finished since this process started,
    so zero before that means "not known yet", not "none". It is also
    false while a forge's first read is still running.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SetupResponse]
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

) -> Error | SetupResponse | None:
    """ What the first-login setup page needs to draw itself

     Facts only, never a verdict. The page decides which step is current,
    which state a forge is in and whether Continue is enabled. Reads no
    secret: a Forgejo Client ID is public, tokens are never returned.
    `github.installations` is the signed-in GitHub account's own
    installations of the App, read live with its token; when GitHub can't
    be asked it is empty and `installationsUnavailable` is true.
    Repository counts come from the last refresh of the board, and
    `refreshed` says whether one has finished since this process started,
    so zero before that means "not known yet", not "none". It is also
    false while a forge's first read is still running.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SetupResponse
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[Error | SetupResponse]:
    """ What the first-login setup page needs to draw itself

     Facts only, never a verdict. The page decides which step is current,
    which state a forge is in and whether Continue is enabled. Reads no
    secret: a Forgejo Client ID is public, tokens are never returned.
    `github.installations` is the signed-in GitHub account's own
    installations of the App, read live with its token; when GitHub can't
    be asked it is empty and `installationsUnavailable` is true.
    Repository counts come from the last refresh of the board, and
    `refreshed` says whether one has finished since this process started,
    so zero before that means "not known yet", not "none". It is also
    false while a forge's first read is still running.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SetupResponse]
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

) -> Error | SetupResponse | None:
    """ What the first-login setup page needs to draw itself

     Facts only, never a verdict. The page decides which step is current,
    which state a forge is in and whether Continue is enabled. Reads no
    secret: a Forgejo Client ID is public, tokens are never returned.
    `github.installations` is the signed-in GitHub account's own
    installations of the App, read live with its token; when GitHub can't
    be asked it is empty and `installationsUnavailable` is true.
    Repository counts come from the last refresh of the board, and
    `refreshed` says whether one has finished since this process started,
    so zero before that means "not known yet", not "none". It is also
    false while a forge's first read is still running.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SetupResponse
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
