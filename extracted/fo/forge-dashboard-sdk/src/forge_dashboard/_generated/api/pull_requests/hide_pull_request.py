from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.pull_request_hide_request import PullRequestHideRequest
from typing import cast



def _get_kwargs(
    *,
    body: PullRequestHideRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/pull-requests/hide",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | Error | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: PullRequestHideRequest,

) -> Response[Any | Error]:
    """ Hide one pull request from the signed-in user's dashboard

     Reversible, not destructive, like ignoring a repo: nothing is sent to
    the forge. A hidden pull request leaves `pullRequests` in
    GET /api/v1/dashboard and everything counted from it, and is counted in
    `hiddenPullRequests` instead. It stays listed for
    `includeHidden=true`, marked `hidden`, so a client can offer a Restore.

    With `days`, the hide ends by itself that many days from now. Without
    it the pull request stays hidden until `POST /api/v1/pull-requests/unhide`.
    A repeat call replaces the earlier choice (hide until restored, then
    hide for 7 days, ends with the 7 days). The server forgets the record
    once the pull request is no longer open, so the list never grows
    without end. The pull request need not be on the board yet: hiding
    one the user can't see is still a 204.

    Args:
        body (PullRequestHideRequest): Which pull request to hide, and for how long. Without
            `days` it stays
            hidden until it is restored.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
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
    body: PullRequestHideRequest,

) -> Any | Error | None:
    """ Hide one pull request from the signed-in user's dashboard

     Reversible, not destructive, like ignoring a repo: nothing is sent to
    the forge. A hidden pull request leaves `pullRequests` in
    GET /api/v1/dashboard and everything counted from it, and is counted in
    `hiddenPullRequests` instead. It stays listed for
    `includeHidden=true`, marked `hidden`, so a client can offer a Restore.

    With `days`, the hide ends by itself that many days from now. Without
    it the pull request stays hidden until `POST /api/v1/pull-requests/unhide`.
    A repeat call replaces the earlier choice (hide until restored, then
    hide for 7 days, ends with the 7 days). The server forgets the record
    once the pull request is no longer open, so the list never grows
    without end. The pull request need not be on the board yet: hiding
    one the user can't see is still a 204.

    Args:
        body (PullRequestHideRequest): Which pull request to hide, and for how long. Without
            `days` it stays
            hidden until it is restored.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: PullRequestHideRequest,

) -> Response[Any | Error]:
    """ Hide one pull request from the signed-in user's dashboard

     Reversible, not destructive, like ignoring a repo: nothing is sent to
    the forge. A hidden pull request leaves `pullRequests` in
    GET /api/v1/dashboard and everything counted from it, and is counted in
    `hiddenPullRequests` instead. It stays listed for
    `includeHidden=true`, marked `hidden`, so a client can offer a Restore.

    With `days`, the hide ends by itself that many days from now. Without
    it the pull request stays hidden until `POST /api/v1/pull-requests/unhide`.
    A repeat call replaces the earlier choice (hide until restored, then
    hide for 7 days, ends with the 7 days). The server forgets the record
    once the pull request is no longer open, so the list never grows
    without end. The pull request need not be on the board yet: hiding
    one the user can't see is still a 204.

    Args:
        body (PullRequestHideRequest): Which pull request to hide, and for how long. Without
            `days` it stays
            hidden until it is restored.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
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
    body: PullRequestHideRequest,

) -> Any | Error | None:
    """ Hide one pull request from the signed-in user's dashboard

     Reversible, not destructive, like ignoring a repo: nothing is sent to
    the forge. A hidden pull request leaves `pullRequests` in
    GET /api/v1/dashboard and everything counted from it, and is counted in
    `hiddenPullRequests` instead. It stays listed for
    `includeHidden=true`, marked `hidden`, so a client can offer a Restore.

    With `days`, the hide ends by itself that many days from now. Without
    it the pull request stays hidden until `POST /api/v1/pull-requests/unhide`.
    A repeat call replaces the earlier choice (hide until restored, then
    hide for 7 days, ends with the 7 days). The server forgets the record
    once the pull request is no longer open, so the list never grows
    without end. The pull request need not be on the board yet: hiding
    one the user can't see is still a 204.

    Args:
        body (PullRequestHideRequest): Which pull request to hide, and for how long. Without
            `days` it stays
            hidden until it is restored.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
