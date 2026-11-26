from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx2

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    code: str | Unset = UNSET,
    state: str | Unset = UNSET,
    error: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["code"] = code

    params["state"] = state

    params["error"] = error


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/connections/github/callback",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Any | Error | None:
    if response.status_code == 303:
        response_303 = cast(Any, None)
        return response_303

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Response[Any | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    code: str | Unset = UNSET,
    state: str | Unset = UNSET,
    error: str | Unset = UNSET,

) -> Response[Any | Error]:
    """ GitHub's redirect back after consent

     Checks `state` (single use, ten minutes), exchanges `code` with the
    PKCE verifier, reads the account's login, stores the token pair
    encrypted, and redirects the browser to `/setup`. Anything that goes
    wrong stores nothing and redirects to `/setup?error=<code>`
    (`SetupErrorCode`).

    Args:
        code (str | Unset):
        state (str | Unset):
        error (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = _get_kwargs(
        code=code,
state=state,
error=error,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    code: str | Unset = UNSET,
    state: str | Unset = UNSET,
    error: str | Unset = UNSET,

) -> Any | Error | None:
    """ GitHub's redirect back after consent

     Checks `state` (single use, ten minutes), exchanges `code` with the
    PKCE verifier, reads the account's login, stores the token pair
    encrypted, and redirects the browser to `/setup`. Anything that goes
    wrong stores nothing and redirects to `/setup?error=<code>`
    (`SetupErrorCode`).

    Args:
        code (str | Unset):
        state (str | Unset):
        error (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return sync_detailed(
        client=client,
code=code,
state=state,
error=error,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    code: str | Unset = UNSET,
    state: str | Unset = UNSET,
    error: str | Unset = UNSET,

) -> Response[Any | Error]:
    """ GitHub's redirect back after consent

     Checks `state` (single use, ten minutes), exchanges `code` with the
    PKCE verifier, reads the account's login, stores the token pair
    encrypted, and redirects the browser to `/setup`. Anything that goes
    wrong stores nothing and redirects to `/setup?error=<code>`
    (`SetupErrorCode`).

    Args:
        code (str | Unset):
        state (str | Unset):
        error (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = _get_kwargs(
        code=code,
state=state,
error=error,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    code: str | Unset = UNSET,
    state: str | Unset = UNSET,
    error: str | Unset = UNSET,

) -> Any | Error | None:
    """ GitHub's redirect back after consent

     Checks `state` (single use, ten minutes), exchanges `code` with the
    PKCE verifier, reads the account's login, stores the token pair
    encrypted, and redirects the browser to `/setup`. Anything that goes
    wrong stores nothing and redirects to `/setup?error=<code>`
    (`SetupErrorCode`).

    Args:
        code (str | Unset):
        state (str | Unset):
        error (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return (await asyncio_detailed(
        client=client,
code=code,
state=state,
error=error,

    )).parsed
