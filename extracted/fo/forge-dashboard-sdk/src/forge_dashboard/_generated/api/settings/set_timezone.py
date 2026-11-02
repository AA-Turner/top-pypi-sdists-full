from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.timezone_request import TimezoneRequest
from ...models.timezone_response import TimezoneResponse
from typing import cast



def _get_kwargs(
    *,
    body: TimezoneRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/v1/settings/timezone",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | TimezoneResponse | None:
    if response.status_code == 200:
        response_200 = TimezoneResponse.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | TimezoneResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: TimezoneRequest,

) -> Response[Error | TimezoneResponse]:
    """ Save the signed-in user's own time zone

     A dedicated, instant save, not routed through PUT /api/v1/settings,
    which replaces every other field. Exists for browsers that report
    UTC to every page, such as Firefox with fingerprint resistance.

    Args:
        body (TimezoneRequest): See PUT /api/v1/settings/timezone's own description.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | TimezoneResponse]
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
    body: TimezoneRequest,

) -> Error | TimezoneResponse | None:
    """ Save the signed-in user's own time zone

     A dedicated, instant save, not routed through PUT /api/v1/settings,
    which replaces every other field. Exists for browsers that report
    UTC to every page, such as Firefox with fingerprint resistance.

    Args:
        body (TimezoneRequest): See PUT /api/v1/settings/timezone's own description.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | TimezoneResponse
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: TimezoneRequest,

) -> Response[Error | TimezoneResponse]:
    """ Save the signed-in user's own time zone

     A dedicated, instant save, not routed through PUT /api/v1/settings,
    which replaces every other field. Exists for browsers that report
    UTC to every page, such as Firefox with fingerprint resistance.

    Args:
        body (TimezoneRequest): See PUT /api/v1/settings/timezone's own description.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | TimezoneResponse]
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
    body: TimezoneRequest,

) -> Error | TimezoneResponse | None:
    """ Save the signed-in user's own time zone

     A dedicated, instant save, not routed through PUT /api/v1/settings,
    which replaces every other field. Exists for browsers that report
    UTC to every page, such as Firefox with fingerprint resistance.

    Args:
        body (TimezoneRequest): See PUT /api/v1/settings/timezone's own description.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | TimezoneResponse
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
