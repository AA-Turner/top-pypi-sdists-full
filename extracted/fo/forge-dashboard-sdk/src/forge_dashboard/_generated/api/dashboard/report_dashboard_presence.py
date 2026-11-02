from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.presence_answer import PresenceAnswer
from ...models.presence_report import PresenceReport
from typing import cast



def _get_kwargs(
    *,
    body: PresenceReport,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/presence",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | PresenceAnswer | None:
    if response.status_code == 200:
        response_200 = PresenceAnswer.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | PresenceAnswer]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: PresenceReport,

) -> Response[Error | PresenceAnswer]:
    """ Say whether a browser tab of the dashboard is being looked at

     The page calls this when its tab becomes visible or hidden
    (`document.visibilityState`), when the person stops or resumes
    using it, and on a slow heartbeat while it is visible. While at
    least one tab is visible, has had input recently and keeps sending
    heartbeats, the dashboard counts as in use and the scheduled
    background refresh keeps running. When every tab has said it is
    hidden, or has stopped sending heartbeats for three heartbeat
    periods (a closed laptop, a crashed browser), the dashboard counts
    as unused and, after the idle period, the scheduled refresh rests
    (see `IDLE_AFTER`). A tab that becomes visible after the refresh
    rested makes it run once.

    This call is the only way the server learns whether a tab is
    looked at. An open live stream says nothing about it, and neither
    does a read carrying `X-Background-Read`. The call itself is not a
    request that counts as use; only a visible report is.

    A browser session only: a personal API token is refused with 403,
    so a script cannot hold the refresh active.

    The answer carries the two timings the page follows, so neither
    is hard-coded in the browser.

    Args:
        body (PresenceReport):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PresenceAnswer]
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
    body: PresenceReport,

) -> Error | PresenceAnswer | None:
    """ Say whether a browser tab of the dashboard is being looked at

     The page calls this when its tab becomes visible or hidden
    (`document.visibilityState`), when the person stops or resumes
    using it, and on a slow heartbeat while it is visible. While at
    least one tab is visible, has had input recently and keeps sending
    heartbeats, the dashboard counts as in use and the scheduled
    background refresh keeps running. When every tab has said it is
    hidden, or has stopped sending heartbeats for three heartbeat
    periods (a closed laptop, a crashed browser), the dashboard counts
    as unused and, after the idle period, the scheduled refresh rests
    (see `IDLE_AFTER`). A tab that becomes visible after the refresh
    rested makes it run once.

    This call is the only way the server learns whether a tab is
    looked at. An open live stream says nothing about it, and neither
    does a read carrying `X-Background-Read`. The call itself is not a
    request that counts as use; only a visible report is.

    A browser session only: a personal API token is refused with 403,
    so a script cannot hold the refresh active.

    The answer carries the two timings the page follows, so neither
    is hard-coded in the browser.

    Args:
        body (PresenceReport):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PresenceAnswer
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: PresenceReport,

) -> Response[Error | PresenceAnswer]:
    """ Say whether a browser tab of the dashboard is being looked at

     The page calls this when its tab becomes visible or hidden
    (`document.visibilityState`), when the person stops or resumes
    using it, and on a slow heartbeat while it is visible. While at
    least one tab is visible, has had input recently and keeps sending
    heartbeats, the dashboard counts as in use and the scheduled
    background refresh keeps running. When every tab has said it is
    hidden, or has stopped sending heartbeats for three heartbeat
    periods (a closed laptop, a crashed browser), the dashboard counts
    as unused and, after the idle period, the scheduled refresh rests
    (see `IDLE_AFTER`). A tab that becomes visible after the refresh
    rested makes it run once.

    This call is the only way the server learns whether a tab is
    looked at. An open live stream says nothing about it, and neither
    does a read carrying `X-Background-Read`. The call itself is not a
    request that counts as use; only a visible report is.

    A browser session only: a personal API token is refused with 403,
    so a script cannot hold the refresh active.

    The answer carries the two timings the page follows, so neither
    is hard-coded in the browser.

    Args:
        body (PresenceReport):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PresenceAnswer]
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
    body: PresenceReport,

) -> Error | PresenceAnswer | None:
    """ Say whether a browser tab of the dashboard is being looked at

     The page calls this when its tab becomes visible or hidden
    (`document.visibilityState`), when the person stops or resumes
    using it, and on a slow heartbeat while it is visible. While at
    least one tab is visible, has had input recently and keeps sending
    heartbeats, the dashboard counts as in use and the scheduled
    background refresh keeps running. When every tab has said it is
    hidden, or has stopped sending heartbeats for three heartbeat
    periods (a closed laptop, a crashed browser), the dashboard counts
    as unused and, after the idle period, the scheduled refresh rests
    (see `IDLE_AFTER`). A tab that becomes visible after the refresh
    rested makes it run once.

    This call is the only way the server learns whether a tab is
    looked at. An open live stream says nothing about it, and neither
    does a read carrying `X-Background-Read`. The call itself is not a
    request that counts as use; only a visible report is.

    A browser session only: a personal API token is refused with 403,
    so a script cannot hold the refresh active.

    The answer carries the two timings the page follows, so neither
    is hard-coded in the browser.

    Args:
        body (PresenceReport):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PresenceAnswer
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
