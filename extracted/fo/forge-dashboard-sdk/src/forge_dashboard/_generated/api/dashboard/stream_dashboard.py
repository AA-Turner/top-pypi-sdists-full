from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.dashboard import Dashboard
from ...models.error import Error
from ...models.run_event import RunEvent
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    include_drafts: bool | Unset = False,
    include_hidden: bool | Unset = False,
    sid: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["includeDrafts"] = include_drafts

    params["includeHidden"] = include_hidden

    params["sid"] = sid


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/dashboard/stream",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Dashboard | RunEvent | Error | None:
    if response.status_code == 200:
        def _parse_response_200(data: object) -> Dashboard | RunEvent:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = Dashboard.from_dict(data)



                return response_200_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_1 = RunEvent.from_dict(data)



            return response_200_type_1

        response_200 = _parse_response_200(response.text)

        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Dashboard | RunEvent | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    include_drafts: bool | Unset = False,
    include_hidden: bool | Unset = False,
    sid: str | Unset = UNSET,

) -> Response[Dashboard | RunEvent | Error]:
    """ Server-Sent Events stream of the signed-in user's own dashboard

     Pushes a fresh snapshot every time this user's background
    refresh produces one — most notably right after a verified
    webhook delivery (see the webhooks tag) triggers an immediate
    one, which is what turns that into a live update instead of
    something only the next scheduled refresh picks up.

    The frontend's own 30-second poll against GET /api/v1/dashboard
    keeps running unconditionally, connected or not — a browser or
    proxy that can't hold an SSE connection open just never
    benefits from this, rather than the dashboard going stale
    silently.

    `includeDrafts` is read once, when the connection opens, and
    applies to every event on it. A client that changes its mind
    reconnects with the new value.

    A client that passes `sid` can also follow the job lists of the
    pull requests and default branches it has open, through
    `POST /api/v1/dashboard/stream/watch`. Each list arrives as named
    `run` events on this stream, one for each workflow run attempt, so a
    client that only listens for default messages never sees one. A
    reconnect reuses the same `sid` with nothing watched, so the client
    sends its watch again.

    Args:
        include_drafts (bool | Unset):  Default: False.
        include_hidden (bool | Unset):  Default: False.
        sid (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Dashboard | RunEvent | Error]
     """


    kwargs = _get_kwargs(
        include_drafts=include_drafts,
include_hidden=include_hidden,
sid=sid,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    include_drafts: bool | Unset = False,
    include_hidden: bool | Unset = False,
    sid: str | Unset = UNSET,

) -> Dashboard | RunEvent | Error | None:
    """ Server-Sent Events stream of the signed-in user's own dashboard

     Pushes a fresh snapshot every time this user's background
    refresh produces one — most notably right after a verified
    webhook delivery (see the webhooks tag) triggers an immediate
    one, which is what turns that into a live update instead of
    something only the next scheduled refresh picks up.

    The frontend's own 30-second poll against GET /api/v1/dashboard
    keeps running unconditionally, connected or not — a browser or
    proxy that can't hold an SSE connection open just never
    benefits from this, rather than the dashboard going stale
    silently.

    `includeDrafts` is read once, when the connection opens, and
    applies to every event on it. A client that changes its mind
    reconnects with the new value.

    A client that passes `sid` can also follow the job lists of the
    pull requests and default branches it has open, through
    `POST /api/v1/dashboard/stream/watch`. Each list arrives as named
    `run` events on this stream, one for each workflow run attempt, so a
    client that only listens for default messages never sees one. A
    reconnect reuses the same `sid` with nothing watched, so the client
    sends its watch again.

    Args:
        include_drafts (bool | Unset):  Default: False.
        include_hidden (bool | Unset):  Default: False.
        sid (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Dashboard | RunEvent | Error
     """


    return sync_detailed(
        client=client,
include_drafts=include_drafts,
include_hidden=include_hidden,
sid=sid,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    include_drafts: bool | Unset = False,
    include_hidden: bool | Unset = False,
    sid: str | Unset = UNSET,

) -> Response[Dashboard | RunEvent | Error]:
    """ Server-Sent Events stream of the signed-in user's own dashboard

     Pushes a fresh snapshot every time this user's background
    refresh produces one — most notably right after a verified
    webhook delivery (see the webhooks tag) triggers an immediate
    one, which is what turns that into a live update instead of
    something only the next scheduled refresh picks up.

    The frontend's own 30-second poll against GET /api/v1/dashboard
    keeps running unconditionally, connected or not — a browser or
    proxy that can't hold an SSE connection open just never
    benefits from this, rather than the dashboard going stale
    silently.

    `includeDrafts` is read once, when the connection opens, and
    applies to every event on it. A client that changes its mind
    reconnects with the new value.

    A client that passes `sid` can also follow the job lists of the
    pull requests and default branches it has open, through
    `POST /api/v1/dashboard/stream/watch`. Each list arrives as named
    `run` events on this stream, one for each workflow run attempt, so a
    client that only listens for default messages never sees one. A
    reconnect reuses the same `sid` with nothing watched, so the client
    sends its watch again.

    Args:
        include_drafts (bool | Unset):  Default: False.
        include_hidden (bool | Unset):  Default: False.
        sid (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Dashboard | RunEvent | Error]
     """


    kwargs = _get_kwargs(
        include_drafts=include_drafts,
include_hidden=include_hidden,
sid=sid,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    include_drafts: bool | Unset = False,
    include_hidden: bool | Unset = False,
    sid: str | Unset = UNSET,

) -> Dashboard | RunEvent | Error | None:
    """ Server-Sent Events stream of the signed-in user's own dashboard

     Pushes a fresh snapshot every time this user's background
    refresh produces one — most notably right after a verified
    webhook delivery (see the webhooks tag) triggers an immediate
    one, which is what turns that into a live update instead of
    something only the next scheduled refresh picks up.

    The frontend's own 30-second poll against GET /api/v1/dashboard
    keeps running unconditionally, connected or not — a browser or
    proxy that can't hold an SSE connection open just never
    benefits from this, rather than the dashboard going stale
    silently.

    `includeDrafts` is read once, when the connection opens, and
    applies to every event on it. A client that changes its mind
    reconnects with the new value.

    A client that passes `sid` can also follow the job lists of the
    pull requests and default branches it has open, through
    `POST /api/v1/dashboard/stream/watch`. Each list arrives as named
    `run` events on this stream, one for each workflow run attempt, so a
    client that only listens for default messages never sees one. A
    reconnect reuses the same `sid` with nothing watched, so the client
    sends its watch again.

    Args:
        include_drafts (bool | Unset):  Default: False.
        include_hidden (bool | Unset):  Default: False.
        sid (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Dashboard | RunEvent | Error
     """


    return (await asyncio_detailed(
        client=client,
include_drafts=include_drafts,
include_hidden=include_hidden,
sid=sid,

    )).parsed
