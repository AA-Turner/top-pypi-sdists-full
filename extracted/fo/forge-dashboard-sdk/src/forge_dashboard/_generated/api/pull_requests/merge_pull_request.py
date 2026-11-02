from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.action_error import ActionError
from ...models.error import Error
from ...models.pull_request_merge_request import PullRequestMergeRequest
from ...models.pull_request_merge_result import PullRequestMergeResult
from typing import cast



def _get_kwargs(
    *,
    body: PullRequestMergeRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/pull-requests/merge",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ActionError | Any | Error | PullRequestMergeResult | None:
    if response.status_code == 200:
        response_200 = PullRequestMergeResult.from_dict(response.json())



        return response_200

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

    if response.status_code == 409:
        response_409 = ActionError.from_dict(response.json())



        return response_409

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ActionError | Any | Error | PullRequestMergeResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: PullRequestMergeRequest,

) -> Response[ActionError | Any | Error | PullRequestMergeResult]:
    """ Merge one pull request, on the signed-in user's behalf

     Merges the named pull request using its repo's own configured
    default merge method — GitHub is asked to pick its own repo
    default, except that a base branch requiring linear history gets
    squash or rebase, never a merge commit; Forgejo's API has no such default built in, so this
    looks up the repo's configured default merge style first and
    passes that explicitly. Neither takes a method override here;
    picking one is out of scope for this endpoint.

    When the forge refuses the merge, the server re-reads the pull
    request's real current state and answers an `ActionError`: a `code`
    from a fixed set plus a short `message` safe to show a person, so
    every client gets the same reason without parsing forge text. A
    pull request that is already merged or closed answers
    `already_merged` / `already_closed`. If the re-read itself fails,
    the original forge error is returned with `code: unknown`.

    An empty pull request, whose branch is already on the target, has no
    `merge` in `allowedActions`. A Merge posted for one anyway
    gets 409 `already_up_to_date` from this server, which never asks the
    forge.

    `deleteBranch: true` also asks for the pull request's source branch
    to be deleted once the merge has landed. The merge never depends on
    it: a branch that can't or shouldn't be deleted leaves the merge
    done and is reported in `branchDeletion`. Without `deleteBranch`
    the answer is a bare 204 and the branch is left alone.

    Args:
        body (PullRequestMergeRequest): Which pull request to merge, and whether to delete its
            source branch afterwards.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ActionError | Any | Error | PullRequestMergeResult]
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
    body: PullRequestMergeRequest,

) -> ActionError | Any | Error | PullRequestMergeResult | None:
    """ Merge one pull request, on the signed-in user's behalf

     Merges the named pull request using its repo's own configured
    default merge method — GitHub is asked to pick its own repo
    default, except that a base branch requiring linear history gets
    squash or rebase, never a merge commit; Forgejo's API has no such default built in, so this
    looks up the repo's configured default merge style first and
    passes that explicitly. Neither takes a method override here;
    picking one is out of scope for this endpoint.

    When the forge refuses the merge, the server re-reads the pull
    request's real current state and answers an `ActionError`: a `code`
    from a fixed set plus a short `message` safe to show a person, so
    every client gets the same reason without parsing forge text. A
    pull request that is already merged or closed answers
    `already_merged` / `already_closed`. If the re-read itself fails,
    the original forge error is returned with `code: unknown`.

    An empty pull request, whose branch is already on the target, has no
    `merge` in `allowedActions`. A Merge posted for one anyway
    gets 409 `already_up_to_date` from this server, which never asks the
    forge.

    `deleteBranch: true` also asks for the pull request's source branch
    to be deleted once the merge has landed. The merge never depends on
    it: a branch that can't or shouldn't be deleted leaves the merge
    done and is reported in `branchDeletion`. Without `deleteBranch`
    the answer is a bare 204 and the branch is left alone.

    Args:
        body (PullRequestMergeRequest): Which pull request to merge, and whether to delete its
            source branch afterwards.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ActionError | Any | Error | PullRequestMergeResult
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: PullRequestMergeRequest,

) -> Response[ActionError | Any | Error | PullRequestMergeResult]:
    """ Merge one pull request, on the signed-in user's behalf

     Merges the named pull request using its repo's own configured
    default merge method — GitHub is asked to pick its own repo
    default, except that a base branch requiring linear history gets
    squash or rebase, never a merge commit; Forgejo's API has no such default built in, so this
    looks up the repo's configured default merge style first and
    passes that explicitly. Neither takes a method override here;
    picking one is out of scope for this endpoint.

    When the forge refuses the merge, the server re-reads the pull
    request's real current state and answers an `ActionError`: a `code`
    from a fixed set plus a short `message` safe to show a person, so
    every client gets the same reason without parsing forge text. A
    pull request that is already merged or closed answers
    `already_merged` / `already_closed`. If the re-read itself fails,
    the original forge error is returned with `code: unknown`.

    An empty pull request, whose branch is already on the target, has no
    `merge` in `allowedActions`. A Merge posted for one anyway
    gets 409 `already_up_to_date` from this server, which never asks the
    forge.

    `deleteBranch: true` also asks for the pull request's source branch
    to be deleted once the merge has landed. The merge never depends on
    it: a branch that can't or shouldn't be deleted leaves the merge
    done and is reported in `branchDeletion`. Without `deleteBranch`
    the answer is a bare 204 and the branch is left alone.

    Args:
        body (PullRequestMergeRequest): Which pull request to merge, and whether to delete its
            source branch afterwards.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ActionError | Any | Error | PullRequestMergeResult]
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
    body: PullRequestMergeRequest,

) -> ActionError | Any | Error | PullRequestMergeResult | None:
    """ Merge one pull request, on the signed-in user's behalf

     Merges the named pull request using its repo's own configured
    default merge method — GitHub is asked to pick its own repo
    default, except that a base branch requiring linear history gets
    squash or rebase, never a merge commit; Forgejo's API has no such default built in, so this
    looks up the repo's configured default merge style first and
    passes that explicitly. Neither takes a method override here;
    picking one is out of scope for this endpoint.

    When the forge refuses the merge, the server re-reads the pull
    request's real current state and answers an `ActionError`: a `code`
    from a fixed set plus a short `message` safe to show a person, so
    every client gets the same reason without parsing forge text. A
    pull request that is already merged or closed answers
    `already_merged` / `already_closed`. If the re-read itself fails,
    the original forge error is returned with `code: unknown`.

    An empty pull request, whose branch is already on the target, has no
    `merge` in `allowedActions`. A Merge posted for one anyway
    gets 409 `already_up_to_date` from this server, which never asks the
    forge.

    `deleteBranch: true` also asks for the pull request's source branch
    to be deleted once the merge has landed. The merge never depends on
    it: a branch that can't or shouldn't be deleted leaves the merge
    done and is reported in `branchDeletion`. Without `deleteBranch`
    the answer is a bare 204 and the branch is left alone.

    Args:
        body (PullRequestMergeRequest): Which pull request to merge, and whether to delete its
            source branch afterwards.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ActionError | Any | Error | PullRequestMergeResult
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
