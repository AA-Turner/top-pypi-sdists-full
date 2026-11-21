from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx2

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.version import Version
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/version",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Error | Version | None:
    if response.status_code == 200:
        response_200 = Version.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Response[Error | Version]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[Error | Version]:
    """ The running server's own version

     The tag goreleaser stamped the running binary with ("dev" for a
    build outside the release pipeline). Needs a session or an API
    token: a signed-out visitor learns nothing about the release,
    since a version tells an attacker which known weaknesses to try.
    The footer of every signed-in page reads it. It stays at this
    address, outside `/api/v1`, because it says which major versions
    the server speaks.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Version]
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

) -> Error | Version | None:
    """ The running server's own version

     The tag goreleaser stamped the running binary with ("dev" for a
    build outside the release pipeline). Needs a session or an API
    token: a signed-out visitor learns nothing about the release,
    since a version tells an attacker which known weaknesses to try.
    The footer of every signed-in page reads it. It stays at this
    address, outside `/api/v1`, because it says which major versions
    the server speaks.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Version
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[Error | Version]:
    """ The running server's own version

     The tag goreleaser stamped the running binary with ("dev" for a
    build outside the release pipeline). Needs a session or an API
    token: a signed-out visitor learns nothing about the release,
    since a version tells an attacker which known weaknesses to try.
    The footer of every signed-in page reads it. It stays at this
    address, outside `/api/v1`, because it says which major versions
    the server speaks.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Version]
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

) -> Error | Version | None:
    """ The running server's own version

     The tag goreleaser stamped the running binary with ("dev" for a
    build outside the release pipeline). Needs a session or an API
    token: a signed-out visitor learns nothing about the release,
    since a version tells an attacker which known weaknesses to try.
    The footer of every signed-in page reads it. It stays at this
    address, outside `/api/v1`, because it says which major versions
    the server speaks.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Version
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
