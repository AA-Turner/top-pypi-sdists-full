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
        "url": "/api/v1/pull-requests/auto-merge",
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

    if response.status_code == 403:
        response_403 = ActionError.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = ActionError.from_dict(response.json())



        return response_404

    if response.status_code == 429:
        response_429 = ActionError.from_dict(response.json())



        return response_429

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
    """ Arm auto-merge on a pull request, on the signed-in user's behalf

     Forgejo: this app keeps the intent itself and merges the pull
    request from its background pass once its checks pass (Forgejo's
    own scheduled merge has no way to read its state back). Nothing is
    sent to the forge now. The intent is stored per signed-in user and
    pull request, and the pull request then reports
    `autoMergeEnabled: true` and offers `cancel_auto_merge`. A repeat
    call is a 204. Only a pull request the user armed here is ever
    merged this way.

    GitHub: enables the named pull request's own
    auto-merge via GitHub's `enablePullRequestAutoMerge` GraphQL
    mutation — REST has no equivalent endpoint. Unlike Merge, that
    mutation asks for an explicit merge method rather than picking
    the repo's own default itself, so this looks the repo's allowed
    methods up first and picks one with the same merge > squash >
    rebase precedence Merge already uses, skipping merge when the
    default branch requires linear history; no override is exposed
    here either. The pull request stays open and unmerged until the
    forge's own required checks pass on their own.

    When the forge refuses, the server re-reads the pull request and
    answers an `ActionError` (see Merge): `already_merged` or
    `already_closed` when the row was stale, otherwise a `code` and a
    plain-words `message` safe to show a person.

    When the pull request is on the signed-in user's board and its
    `allowedActions` has no `auto_merge` entry, this server answers 409
    itself and never asks the forge: `auto_merge_not_allowed`,
    `already_up_to_date`, `conflict`, `stacked` or `ready_to_merge` for
    the reasons the board already knows, and `not_mergeable` for
    auto-merge already on or a forge that has none.
    `auto_merge_not_allowed` means the repo doesn't allow auto-merge
    (or not for this pull request); `ready_to_merge` means it is
    already clean, so there is nothing to wait for and Merge is the
    action; `checks_pending` means a non-required check is still
    running, so trying again later can work.

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
    """ Arm auto-merge on a pull request, on the signed-in user's behalf

     Forgejo: this app keeps the intent itself and merges the pull
    request from its background pass once its checks pass (Forgejo's
    own scheduled merge has no way to read its state back). Nothing is
    sent to the forge now. The intent is stored per signed-in user and
    pull request, and the pull request then reports
    `autoMergeEnabled: true` and offers `cancel_auto_merge`. A repeat
    call is a 204. Only a pull request the user armed here is ever
    merged this way.

    GitHub: enables the named pull request's own
    auto-merge via GitHub's `enablePullRequestAutoMerge` GraphQL
    mutation — REST has no equivalent endpoint. Unlike Merge, that
    mutation asks for an explicit merge method rather than picking
    the repo's own default itself, so this looks the repo's allowed
    methods up first and picks one with the same merge > squash >
    rebase precedence Merge already uses, skipping merge when the
    default branch requires linear history; no override is exposed
    here either. The pull request stays open and unmerged until the
    forge's own required checks pass on their own.

    When the forge refuses, the server re-reads the pull request and
    answers an `ActionError` (see Merge): `already_merged` or
    `already_closed` when the row was stale, otherwise a `code` and a
    plain-words `message` safe to show a person.

    When the pull request is on the signed-in user's board and its
    `allowedActions` has no `auto_merge` entry, this server answers 409
    itself and never asks the forge: `auto_merge_not_allowed`,
    `already_up_to_date`, `conflict`, `stacked` or `ready_to_merge` for
    the reasons the board already knows, and `not_mergeable` for
    auto-merge already on or a forge that has none.
    `auto_merge_not_allowed` means the repo doesn't allow auto-merge
    (or not for this pull request); `ready_to_merge` means it is
    already clean, so there is nothing to wait for and Merge is the
    action; `checks_pending` means a non-required check is still
    running, so trying again later can work.

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
    """ Arm auto-merge on a pull request, on the signed-in user's behalf

     Forgejo: this app keeps the intent itself and merges the pull
    request from its background pass once its checks pass (Forgejo's
    own scheduled merge has no way to read its state back). Nothing is
    sent to the forge now. The intent is stored per signed-in user and
    pull request, and the pull request then reports
    `autoMergeEnabled: true` and offers `cancel_auto_merge`. A repeat
    call is a 204. Only a pull request the user armed here is ever
    merged this way.

    GitHub: enables the named pull request's own
    auto-merge via GitHub's `enablePullRequestAutoMerge` GraphQL
    mutation — REST has no equivalent endpoint. Unlike Merge, that
    mutation asks for an explicit merge method rather than picking
    the repo's own default itself, so this looks the repo's allowed
    methods up first and picks one with the same merge > squash >
    rebase precedence Merge already uses, skipping merge when the
    default branch requires linear history; no override is exposed
    here either. The pull request stays open and unmerged until the
    forge's own required checks pass on their own.

    When the forge refuses, the server re-reads the pull request and
    answers an `ActionError` (see Merge): `already_merged` or
    `already_closed` when the row was stale, otherwise a `code` and a
    plain-words `message` safe to show a person.

    When the pull request is on the signed-in user's board and its
    `allowedActions` has no `auto_merge` entry, this server answers 409
    itself and never asks the forge: `auto_merge_not_allowed`,
    `already_up_to_date`, `conflict`, `stacked` or `ready_to_merge` for
    the reasons the board already knows, and `not_mergeable` for
    auto-merge already on or a forge that has none.
    `auto_merge_not_allowed` means the repo doesn't allow auto-merge
    (or not for this pull request); `ready_to_merge` means it is
    already clean, so there is nothing to wait for and Merge is the
    action; `checks_pending` means a non-required check is still
    running, so trying again later can work.

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
    """ Arm auto-merge on a pull request, on the signed-in user's behalf

     Forgejo: this app keeps the intent itself and merges the pull
    request from its background pass once its checks pass (Forgejo's
    own scheduled merge has no way to read its state back). Nothing is
    sent to the forge now. The intent is stored per signed-in user and
    pull request, and the pull request then reports
    `autoMergeEnabled: true` and offers `cancel_auto_merge`. A repeat
    call is a 204. Only a pull request the user armed here is ever
    merged this way.

    GitHub: enables the named pull request's own
    auto-merge via GitHub's `enablePullRequestAutoMerge` GraphQL
    mutation — REST has no equivalent endpoint. Unlike Merge, that
    mutation asks for an explicit merge method rather than picking
    the repo's own default itself, so this looks the repo's allowed
    methods up first and picks one with the same merge > squash >
    rebase precedence Merge already uses, skipping merge when the
    default branch requires linear history; no override is exposed
    here either. The pull request stays open and unmerged until the
    forge's own required checks pass on their own.

    When the forge refuses, the server re-reads the pull request and
    answers an `ActionError` (see Merge): `already_merged` or
    `already_closed` when the row was stale, otherwise a `code` and a
    plain-words `message` safe to show a person.

    When the pull request is on the signed-in user's board and its
    `allowedActions` has no `auto_merge` entry, this server answers 409
    itself and never asks the forge: `auto_merge_not_allowed`,
    `already_up_to_date`, `conflict`, `stacked` or `ready_to_merge` for
    the reasons the board already knows, and `not_mergeable` for
    auto-merge already on or a forge that has none.
    `auto_merge_not_allowed` means the repo doesn't allow auto-merge
    (or not for this pull request); `ready_to_merge` means it is
    already clean, so there is nothing to wait for and Merge is the
    action; `checks_pending` means a non-required check is still
    running, so trying again later can work.

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
