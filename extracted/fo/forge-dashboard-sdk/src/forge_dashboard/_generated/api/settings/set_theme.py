from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.theme_request import ThemeRequest
from ...models.theme_response import ThemeResponse
from typing import cast



def _get_kwargs(
    *,
    body: ThemeRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/v1/settings/theme",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | ThemeResponse | None:
    if response.status_code == 200:
        response_200 = ThemeResponse.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

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
    body: ThemeRequest,

) -> Response[Error | ThemeResponse]:
    """ Save the signed-in user's own theme preference

     A dedicated, instant save — deliberately not routed
    through the main PUT /api/v1/settings, whose every other field is
    a plain replace rather than a per-field merge: a request
    carrying only theme through that handler would blank every
    other saved setting. Picking a theme applies immediately, the
    same "set once and forget" convention the ticket's own research
    cites, rather than waiting on the rest of the settings form's
    own Save button.

    Args:
        body (ThemeRequest): See PUT /api/v1/settings/theme's own description.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ThemeResponse]
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
    body: ThemeRequest,

) -> Error | ThemeResponse | None:
    """ Save the signed-in user's own theme preference

     A dedicated, instant save — deliberately not routed
    through the main PUT /api/v1/settings, whose every other field is
    a plain replace rather than a per-field merge: a request
    carrying only theme through that handler would blank every
    other saved setting. Picking a theme applies immediately, the
    same "set once and forget" convention the ticket's own research
    cites, rather than waiting on the rest of the settings form's
    own Save button.

    Args:
        body (ThemeRequest): See PUT /api/v1/settings/theme's own description.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ThemeResponse
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ThemeRequest,

) -> Response[Error | ThemeResponse]:
    """ Save the signed-in user's own theme preference

     A dedicated, instant save — deliberately not routed
    through the main PUT /api/v1/settings, whose every other field is
    a plain replace rather than a per-field merge: a request
    carrying only theme through that handler would blank every
    other saved setting. Picking a theme applies immediately, the
    same "set once and forget" convention the ticket's own research
    cites, rather than waiting on the rest of the settings form's
    own Save button.

    Args:
        body (ThemeRequest): See PUT /api/v1/settings/theme's own description.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ThemeResponse]
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
    body: ThemeRequest,

) -> Error | ThemeResponse | None:
    """ Save the signed-in user's own theme preference

     A dedicated, instant save — deliberately not routed
    through the main PUT /api/v1/settings, whose every other field is
    a plain replace rather than a per-field merge: a request
    carrying only theme through that handler would blank every
    other saved setting. Picking a theme applies immediately, the
    same "set once and forget" convention the ticket's own research
    cites, rather than waiting on the rest of the settings form's
    own Save button.

    Args:
        body (ThemeRequest): See PUT /api/v1/settings/theme's own description.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ThemeResponse
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
