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
    installation_id: int | Unset = UNSET,
    setup_action: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["installation_id"] = installation_id

    params["setup_action"] = setup_action


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/connections/github/installed",
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
    installation_id: int | Unset = UNSET,
    setup_action: str | Unset = UNSET,

) -> Response[Any | Error]:
    """ GitHub's redirect back after the App is installed or changed

     The GitHub App's Setup URL. After an install, or a change of repository
    access with "Redirect on update" on, GitHub sends the browser here with
    `installation_id` and `setup_action`. The redirect is not trusted: the
    ID is stored as an installation only when it is in the connected
    user's own `GET /user/installations`, read with the linked account's
    token. Otherwise nothing is stored. Redirects to `/setup`, with
    `?error=<code>` when nothing was stored. An owner who may not install
    the App sends a request to the organisation's owners instead, and
    GitHub then sends the browser here with `setup_action=request` and no
    `installation_id`: that redirects to `/setup?install=requested`.

    Args:
        installation_id (int | Unset):
        setup_action (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = _get_kwargs(
        installation_id=installation_id,
setup_action=setup_action,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    installation_id: int | Unset = UNSET,
    setup_action: str | Unset = UNSET,

) -> Any | Error | None:
    """ GitHub's redirect back after the App is installed or changed

     The GitHub App's Setup URL. After an install, or a change of repository
    access with "Redirect on update" on, GitHub sends the browser here with
    `installation_id` and `setup_action`. The redirect is not trusted: the
    ID is stored as an installation only when it is in the connected
    user's own `GET /user/installations`, read with the linked account's
    token. Otherwise nothing is stored. Redirects to `/setup`, with
    `?error=<code>` when nothing was stored. An owner who may not install
    the App sends a request to the organisation's owners instead, and
    GitHub then sends the browser here with `setup_action=request` and no
    `installation_id`: that redirects to `/setup?install=requested`.

    Args:
        installation_id (int | Unset):
        setup_action (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return sync_detailed(
        client=client,
installation_id=installation_id,
setup_action=setup_action,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    installation_id: int | Unset = UNSET,
    setup_action: str | Unset = UNSET,

) -> Response[Any | Error]:
    """ GitHub's redirect back after the App is installed or changed

     The GitHub App's Setup URL. After an install, or a change of repository
    access with "Redirect on update" on, GitHub sends the browser here with
    `installation_id` and `setup_action`. The redirect is not trusted: the
    ID is stored as an installation only when it is in the connected
    user's own `GET /user/installations`, read with the linked account's
    token. Otherwise nothing is stored. Redirects to `/setup`, with
    `?error=<code>` when nothing was stored. An owner who may not install
    the App sends a request to the organisation's owners instead, and
    GitHub then sends the browser here with `setup_action=request` and no
    `installation_id`: that redirects to `/setup?install=requested`.

    Args:
        installation_id (int | Unset):
        setup_action (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = _get_kwargs(
        installation_id=installation_id,
setup_action=setup_action,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    installation_id: int | Unset = UNSET,
    setup_action: str | Unset = UNSET,

) -> Any | Error | None:
    """ GitHub's redirect back after the App is installed or changed

     The GitHub App's Setup URL. After an install, or a change of repository
    access with "Redirect on update" on, GitHub sends the browser here with
    `installation_id` and `setup_action`. The redirect is not trusted: the
    ID is stored as an installation only when it is in the connected
    user's own `GET /user/installations`, read with the linked account's
    token. Otherwise nothing is stored. Redirects to `/setup`, with
    `?error=<code>` when nothing was stored. An owner who may not install
    the App sends a request to the organisation's owners instead, and
    GitHub then sends the browser here with `setup_action=request` and no
    `installation_id`: that redirects to `/setup?install=requested`.

    Args:
        installation_id (int | Unset):
        setup_action (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return (await asyncio_detailed(
        client=client,
installation_id=installation_id,
setup_action=setup_action,

    )).parsed
