from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.action_error import ActionError
from ...models.error import Error
from ...models.main_branch_rerun_request import MainBranchRerunRequest
from typing import cast



def _get_kwargs(
    *,
    body: MainBranchRerunRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/main-branches/rerun-checks",
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
    body: MainBranchRerunRequest,

) -> Response[ActionError | Any | Error]:
    """ Rerun only the failed jobs of a repository's default-branch pipeline, on the signed-in user's behalf

     The branch twin of POST /api/v1/pull-requests/rerun-checks. Asks the forge
    to rerun the failed jobs of the Actions workflow runs on the commit
    the branch's job list shows, and nothing that passed. It
    answers once the forge has queued them, not when they finish, so a
    client shows a queued state and lets the next refresh carry the result.

    A Main branches row offers it when its `status` is `failed`. A failed
    check that isn't an Actions job (a third-party check, a legacy status,
    an external CI) can't be rerun here and is skipped. Refusals are an
    `ActionError`; a 409 means the branch has no failed job to rerun, or
    that the forge is a Forgejo older than version 17, which has no rerun
    route (`ForgeHealth.rerunChecksBlocked` says so beforehand). On
    Forgejo the version is checked before the runs are looked up, as for a
    pull request, and a refusal that comes after some jobs restarted ends
    with which jobs restarted and which did not.

    Args:
        body (MainBranchRerunRequest): Which repository's default branch to rerun the failed
            checks of.

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
    body: MainBranchRerunRequest,

) -> ActionError | Any | Error | None:
    """ Rerun only the failed jobs of a repository's default-branch pipeline, on the signed-in user's behalf

     The branch twin of POST /api/v1/pull-requests/rerun-checks. Asks the forge
    to rerun the failed jobs of the Actions workflow runs on the commit
    the branch's job list shows, and nothing that passed. It
    answers once the forge has queued them, not when they finish, so a
    client shows a queued state and lets the next refresh carry the result.

    A Main branches row offers it when its `status` is `failed`. A failed
    check that isn't an Actions job (a third-party check, a legacy status,
    an external CI) can't be rerun here and is skipped. Refusals are an
    `ActionError`; a 409 means the branch has no failed job to rerun, or
    that the forge is a Forgejo older than version 17, which has no rerun
    route (`ForgeHealth.rerunChecksBlocked` says so beforehand). On
    Forgejo the version is checked before the runs are looked up, as for a
    pull request, and a refusal that comes after some jobs restarted ends
    with which jobs restarted and which did not.

    Args:
        body (MainBranchRerunRequest): Which repository's default branch to rerun the failed
            checks of.

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
    body: MainBranchRerunRequest,

) -> Response[ActionError | Any | Error]:
    """ Rerun only the failed jobs of a repository's default-branch pipeline, on the signed-in user's behalf

     The branch twin of POST /api/v1/pull-requests/rerun-checks. Asks the forge
    to rerun the failed jobs of the Actions workflow runs on the commit
    the branch's job list shows, and nothing that passed. It
    answers once the forge has queued them, not when they finish, so a
    client shows a queued state and lets the next refresh carry the result.

    A Main branches row offers it when its `status` is `failed`. A failed
    check that isn't an Actions job (a third-party check, a legacy status,
    an external CI) can't be rerun here and is skipped. Refusals are an
    `ActionError`; a 409 means the branch has no failed job to rerun, or
    that the forge is a Forgejo older than version 17, which has no rerun
    route (`ForgeHealth.rerunChecksBlocked` says so beforehand). On
    Forgejo the version is checked before the runs are looked up, as for a
    pull request, and a refusal that comes after some jobs restarted ends
    with which jobs restarted and which did not.

    Args:
        body (MainBranchRerunRequest): Which repository's default branch to rerun the failed
            checks of.

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
    body: MainBranchRerunRequest,

) -> ActionError | Any | Error | None:
    """ Rerun only the failed jobs of a repository's default-branch pipeline, on the signed-in user's behalf

     The branch twin of POST /api/v1/pull-requests/rerun-checks. Asks the forge
    to rerun the failed jobs of the Actions workflow runs on the commit
    the branch's job list shows, and nothing that passed. It
    answers once the forge has queued them, not when they finish, so a
    client shows a queued state and lets the next refresh carry the result.

    A Main branches row offers it when its `status` is `failed`. A failed
    check that isn't an Actions job (a third-party check, a legacy status,
    an external CI) can't be rerun here and is skipped. Refusals are an
    `ActionError`; a 409 means the branch has no failed job to rerun, or
    that the forge is a Forgejo older than version 17, which has no rerun
    route (`ForgeHealth.rerunChecksBlocked` says so beforehand). On
    Forgejo the version is checked before the runs are looked up, as for a
    pull request, and a refusal that comes after some jobs restarted ends
    with which jobs restarted and which did not.

    Args:
        body (MainBranchRerunRequest): Which repository's default branch to rerun the failed
            checks of.

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
