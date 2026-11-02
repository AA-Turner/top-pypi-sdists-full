from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.action_error import ActionError
from ...models.error import Error
from ...models.pull_request_action_request import PullRequestActionRequest
from typing import cast



def _get_kwargs(
    *,
    body: PullRequestActionRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/pull-requests/auto-merge/cancel",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ActionError | Any | Error | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 409:
        response_409 = ActionError.from_dict(response.json())



        return response_409

    if response.status_code == 502:
        response_502 = ActionError.from_dict(response.json())



        return response_502

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ActionError | Any | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: PullRequestActionRequest,

) -> Response[ActionError | Any | Error]:
    """ Cancel auto-merge on a pull request, on the signed-in user's behalf

     Forgejo: removes the intent stored by `POST /api/v1/pull-requests/auto-merge`,
    so the background pass never merges the pull request. Nothing is sent
    to the forge. Idempotent: a pull request with no intent is a 204 too.

    GitHub: turns the pull request's own auto-merge off with GitHub's
    `disablePullRequestAutoMerge` GraphQL mutation. Only a pull request
    whose `allowedActions` has a `cancel_auto_merge` entry; otherwise this
    server answers 409 itself and never asks GitHub. A refusal from
    GitHub is an `ActionError`, as for arming.

    Args:
        body (PullRequestActionRequest): Which pull request to act on.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ActionError | Any | Error]
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
    body: PullRequestActionRequest,

) -> ActionError | Any | Error | None:
    """ Cancel auto-merge on a pull request, on the signed-in user's behalf

     Forgejo: removes the intent stored by `POST /api/v1/pull-requests/auto-merge`,
    so the background pass never merges the pull request. Nothing is sent
    to the forge. Idempotent: a pull request with no intent is a 204 too.

    GitHub: turns the pull request's own auto-merge off with GitHub's
    `disablePullRequestAutoMerge` GraphQL mutation. Only a pull request
    whose `allowedActions` has a `cancel_auto_merge` entry; otherwise this
    server answers 409 itself and never asks GitHub. A refusal from
    GitHub is an `ActionError`, as for arming.

    Args:
        body (PullRequestActionRequest): Which pull request to act on.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ActionError | Any | Error
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: PullRequestActionRequest,

) -> Response[ActionError | Any | Error]:
    """ Cancel auto-merge on a pull request, on the signed-in user's behalf

     Forgejo: removes the intent stored by `POST /api/v1/pull-requests/auto-merge`,
    so the background pass never merges the pull request. Nothing is sent
    to the forge. Idempotent: a pull request with no intent is a 204 too.

    GitHub: turns the pull request's own auto-merge off with GitHub's
    `disablePullRequestAutoMerge` GraphQL mutation. Only a pull request
    whose `allowedActions` has a `cancel_auto_merge` entry; otherwise this
    server answers 409 itself and never asks GitHub. A refusal from
    GitHub is an `ActionError`, as for arming.

    Args:
        body (PullRequestActionRequest): Which pull request to act on.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ActionError | Any | Error]
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
    body: PullRequestActionRequest,

) -> ActionError | Any | Error | None:
    """ Cancel auto-merge on a pull request, on the signed-in user's behalf

     Forgejo: removes the intent stored by `POST /api/v1/pull-requests/auto-merge`,
    so the background pass never merges the pull request. Nothing is sent
    to the forge. Idempotent: a pull request with no intent is a 204 too.

    GitHub: turns the pull request's own auto-merge off with GitHub's
    `disablePullRequestAutoMerge` GraphQL mutation. Only a pull request
    whose `allowedActions` has a `cancel_auto_merge` entry; otherwise this
    server answers 409 itself and never asks GitHub. A refusal from
    GitHub is an `ActionError`, as for arming.

    Args:
        body (PullRequestActionRequest): Which pull request to act on.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ActionError | Any | Error
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
