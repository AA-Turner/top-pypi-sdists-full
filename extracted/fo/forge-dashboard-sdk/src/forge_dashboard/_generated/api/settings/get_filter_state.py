from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.filter_state import FilterState
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/settings/filter-state",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | FilterState | None:
    if response.status_code == 200:
        response_200 = FilterState.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | FilterState]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[Error | FilterState]:
    """ The signed-in user's own saved dashboard/Insights filter state

     A lightweight read of one opaque blob, deliberately not
    GET /api/v1/settings itself for the same reason GET /api/v1/settings/theme
    isn't either: this loads on every dashboard/Insights visit and
    shouldn't provision webhook credentials as a side effect.
    `{}` for a user who's never saved any filters yet, not a 404.
    These are the web UI's own state: a signed-in browser session only,
    and a personal API token is refused with 403.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FilterState]
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

) -> Error | FilterState | None:
    """ The signed-in user's own saved dashboard/Insights filter state

     A lightweight read of one opaque blob, deliberately not
    GET /api/v1/settings itself for the same reason GET /api/v1/settings/theme
    isn't either: this loads on every dashboard/Insights visit and
    shouldn't provision webhook credentials as a side effect.
    `{}` for a user who's never saved any filters yet, not a 404.
    These are the web UI's own state: a signed-in browser session only,
    and a personal API token is refused with 403.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FilterState
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[Error | FilterState]:
    """ The signed-in user's own saved dashboard/Insights filter state

     A lightweight read of one opaque blob, deliberately not
    GET /api/v1/settings itself for the same reason GET /api/v1/settings/theme
    isn't either: this loads on every dashboard/Insights visit and
    shouldn't provision webhook credentials as a side effect.
    `{}` for a user who's never saved any filters yet, not a 404.
    These are the web UI's own state: a signed-in browser session only,
    and a personal API token is refused with 403.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FilterState]
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

) -> Error | FilterState | None:
    """ The signed-in user's own saved dashboard/Insights filter state

     A lightweight read of one opaque blob, deliberately not
    GET /api/v1/settings itself for the same reason GET /api/v1/settings/theme
    isn't either: this loads on every dashboard/Insights visit and
    shouldn't provision webhook credentials as a side effect.
    `{}` for a user who's never saved any filters yet, not a 404.
    These are the web UI's own state: a signed-in browser session only,
    and a personal API token is refused with 403.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FilterState
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
