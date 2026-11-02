from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.version import Version
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/version",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Version | None:
    if response.status_code == 200:
        response_200 = Version.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Version]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,

) -> Response[Version]:
    """ The running server's own version

     The tag goreleaser stamped the running binary with ("dev" for a
    build outside the release pipeline). Public and unauthenticated —
    every page, including the pre-login screen, links to the matching
    GitHub release from its footer so a person can tell what's
    actually deployed without shelling into the box.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Version]
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

) -> Version | None:
    """ The running server's own version

     The tag goreleaser stamped the running binary with ("dev" for a
    build outside the release pipeline). Public and unauthenticated —
    every page, including the pre-login screen, links to the matching
    GitHub release from its footer so a person can tell what's
    actually deployed without shelling into the box.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Version
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,

) -> Response[Version]:
    """ The running server's own version

     The tag goreleaser stamped the running binary with ("dev" for a
    build outside the release pipeline). Public and unauthenticated —
    every page, including the pre-login screen, links to the matching
    GitHub release from its footer so a person can tell what's
    actually deployed without shelling into the box.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Version]
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

) -> Version | None:
    """ The running server's own version

     The tag goreleaser stamped the running binary with ("dev" for a
    build outside the release pipeline). Public and unauthenticated —
    every page, including the pre-login screen, links to the matching
    GitHub release from its footer so a person can tell what's
    actually deployed without shelling into the box.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Version
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
