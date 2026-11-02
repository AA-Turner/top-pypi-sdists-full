from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.pull_request_auto_update_request import PullRequestAutoUpdateRequest
from typing import cast



def _get_kwargs(
    *,
    body: PullRequestAutoUpdateRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/pull-requests/auto-update",
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

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

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
    body: PullRequestAutoUpdateRequest,

) -> Response[Any | Error]:
    """ Turn the automatic branch update on or off for one pull request

     A pure local write: nothing is sent to the forge. The choice is kept
    only while it differs from the repo's auto-update setting
    (`/api/v1/repos/auto-update-branch/enable`), so a choice that matches
    the repo is dropped and the pull request follows the repo again, and
    a later change to the repo's setting reaches it. With `enabled`
    `null` or absent the pull request goes back to its repo's setting.
    Idempotent. A draft and a release-please pull request are never
    updated automatically, whatever is chosen: `autoUpdate.unavailable`
    in GET /api/v1/dashboard says so. The server forgets the choice once
    the pull request is no longer open, its repo is no longer tracked, or
    the repo's setting changes to match it. A pull request the dashboard
    doesn't hold is a 404.

    Args:
        body (PullRequestAutoUpdateRequest): Which pull request, and whether the dashboard should
            update its
            branch automatically.

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
    body: PullRequestAutoUpdateRequest,

) -> Any | Error | None:
    """ Turn the automatic branch update on or off for one pull request

     A pure local write: nothing is sent to the forge. The choice is kept
    only while it differs from the repo's auto-update setting
    (`/api/v1/repos/auto-update-branch/enable`), so a choice that matches
    the repo is dropped and the pull request follows the repo again, and
    a later change to the repo's setting reaches it. With `enabled`
    `null` or absent the pull request goes back to its repo's setting.
    Idempotent. A draft and a release-please pull request are never
    updated automatically, whatever is chosen: `autoUpdate.unavailable`
    in GET /api/v1/dashboard says so. The server forgets the choice once
    the pull request is no longer open, its repo is no longer tracked, or
    the repo's setting changes to match it. A pull request the dashboard
    doesn't hold is a 404.

    Args:
        body (PullRequestAutoUpdateRequest): Which pull request, and whether the dashboard should
            update its
            branch automatically.

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
    body: PullRequestAutoUpdateRequest,

) -> Response[Any | Error]:
    """ Turn the automatic branch update on or off for one pull request

     A pure local write: nothing is sent to the forge. The choice is kept
    only while it differs from the repo's auto-update setting
    (`/api/v1/repos/auto-update-branch/enable`), so a choice that matches
    the repo is dropped and the pull request follows the repo again, and
    a later change to the repo's setting reaches it. With `enabled`
    `null` or absent the pull request goes back to its repo's setting.
    Idempotent. A draft and a release-please pull request are never
    updated automatically, whatever is chosen: `autoUpdate.unavailable`
    in GET /api/v1/dashboard says so. The server forgets the choice once
    the pull request is no longer open, its repo is no longer tracked, or
    the repo's setting changes to match it. A pull request the dashboard
    doesn't hold is a 404.

    Args:
        body (PullRequestAutoUpdateRequest): Which pull request, and whether the dashboard should
            update its
            branch automatically.

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
    body: PullRequestAutoUpdateRequest,

) -> Any | Error | None:
    """ Turn the automatic branch update on or off for one pull request

     A pure local write: nothing is sent to the forge. The choice is kept
    only while it differs from the repo's auto-update setting
    (`/api/v1/repos/auto-update-branch/enable`), so a choice that matches
    the repo is dropped and the pull request follows the repo again, and
    a later change to the repo's setting reaches it. With `enabled`
    `null` or absent the pull request goes back to its repo's setting.
    Idempotent. A draft and a release-please pull request are never
    updated automatically, whatever is chosen: `autoUpdate.unavailable`
    in GET /api/v1/dashboard says so. The server forgets the choice once
    the pull request is no longer open, its repo is no longer tracked, or
    the repo's setting changes to match it. A pull request the dashboard
    doesn't hold is a 404.

    Args:
        body (PullRequestAutoUpdateRequest): Which pull request, and whether the dashboard should
            update its
            branch automatically.

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
