from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.action_error import ActionError
from ...models.cancel_run_request import CancelRunRequest
from ...models.error import Error
from typing import cast



def _get_kwargs(
    *,
    body: CancelRunRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/checks/cancel-run",
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
    body: CancelRunRequest,

) -> Response[ActionError | Any | Error]:
    """ Cancel one running or queued Actions workflow run, on the signed-in user's behalf

     Asks the forge to cancel a whole workflow run: every job of it stops,
    because neither GitHub nor Forgejo can stop one job of a running
    workflow. A client takes `runId` from a check in a `run` event on
    GET /api/v1/dashboard/stream, from a job that is still queued or running.
    A check with no `runId` (a third-party check, a legacy commit status,
    an external CI) belongs to no Actions run and can't be cancelled
    here.

    It answers once the forge has accepted the cancel, not when the run
    has stopped, so a client shows the run as cancelling and lets the next
    snapshot carry the result. A pull request offers it as a `cancel_run`
    entry in `allowedActions` while any of its checks is running or
    waiting, even when another check has already failed. The list can't
    tell an Actions check from an external CI, so a pull request whose
    only running check is an external one (on Forgejo, a pending commit
    status too) still offers it, and the checks list then has no `runId`
    to send.

    It is never queued for a rate-limit reset. After the reset the run may
    be a different one, started by a newer push, and a cancel can't be
    undone. A rate limit arrives as a 429 and the person decides again.

    Refusals are an `ActionError` (see Merge) and carry the forge's own
    plain-words `message`: the token may not write to Actions, the run
    already finished, or a Forgejo instance too old to have the route.
    An old Forgejo answers the missing route with a 404, which looks the
    same as a run that is gone, so it is reported as that and doesn't
    stop the dialog offering the action.

    Args:
        body (CancelRunRequest):

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
    body: CancelRunRequest,

) -> ActionError | Any | Error | None:
    """ Cancel one running or queued Actions workflow run, on the signed-in user's behalf

     Asks the forge to cancel a whole workflow run: every job of it stops,
    because neither GitHub nor Forgejo can stop one job of a running
    workflow. A client takes `runId` from a check in a `run` event on
    GET /api/v1/dashboard/stream, from a job that is still queued or running.
    A check with no `runId` (a third-party check, a legacy commit status,
    an external CI) belongs to no Actions run and can't be cancelled
    here.

    It answers once the forge has accepted the cancel, not when the run
    has stopped, so a client shows the run as cancelling and lets the next
    snapshot carry the result. A pull request offers it as a `cancel_run`
    entry in `allowedActions` while any of its checks is running or
    waiting, even when another check has already failed. The list can't
    tell an Actions check from an external CI, so a pull request whose
    only running check is an external one (on Forgejo, a pending commit
    status too) still offers it, and the checks list then has no `runId`
    to send.

    It is never queued for a rate-limit reset. After the reset the run may
    be a different one, started by a newer push, and a cancel can't be
    undone. A rate limit arrives as a 429 and the person decides again.

    Refusals are an `ActionError` (see Merge) and carry the forge's own
    plain-words `message`: the token may not write to Actions, the run
    already finished, or a Forgejo instance too old to have the route.
    An old Forgejo answers the missing route with a 404, which looks the
    same as a run that is gone, so it is reported as that and doesn't
    stop the dialog offering the action.

    Args:
        body (CancelRunRequest):

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
    body: CancelRunRequest,

) -> Response[ActionError | Any | Error]:
    """ Cancel one running or queued Actions workflow run, on the signed-in user's behalf

     Asks the forge to cancel a whole workflow run: every job of it stops,
    because neither GitHub nor Forgejo can stop one job of a running
    workflow. A client takes `runId` from a check in a `run` event on
    GET /api/v1/dashboard/stream, from a job that is still queued or running.
    A check with no `runId` (a third-party check, a legacy commit status,
    an external CI) belongs to no Actions run and can't be cancelled
    here.

    It answers once the forge has accepted the cancel, not when the run
    has stopped, so a client shows the run as cancelling and lets the next
    snapshot carry the result. A pull request offers it as a `cancel_run`
    entry in `allowedActions` while any of its checks is running or
    waiting, even when another check has already failed. The list can't
    tell an Actions check from an external CI, so a pull request whose
    only running check is an external one (on Forgejo, a pending commit
    status too) still offers it, and the checks list then has no `runId`
    to send.

    It is never queued for a rate-limit reset. After the reset the run may
    be a different one, started by a newer push, and a cancel can't be
    undone. A rate limit arrives as a 429 and the person decides again.

    Refusals are an `ActionError` (see Merge) and carry the forge's own
    plain-words `message`: the token may not write to Actions, the run
    already finished, or a Forgejo instance too old to have the route.
    An old Forgejo answers the missing route with a 404, which looks the
    same as a run that is gone, so it is reported as that and doesn't
    stop the dialog offering the action.

    Args:
        body (CancelRunRequest):

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
    body: CancelRunRequest,

) -> ActionError | Any | Error | None:
    """ Cancel one running or queued Actions workflow run, on the signed-in user's behalf

     Asks the forge to cancel a whole workflow run: every job of it stops,
    because neither GitHub nor Forgejo can stop one job of a running
    workflow. A client takes `runId` from a check in a `run` event on
    GET /api/v1/dashboard/stream, from a job that is still queued or running.
    A check with no `runId` (a third-party check, a legacy commit status,
    an external CI) belongs to no Actions run and can't be cancelled
    here.

    It answers once the forge has accepted the cancel, not when the run
    has stopped, so a client shows the run as cancelling and lets the next
    snapshot carry the result. A pull request offers it as a `cancel_run`
    entry in `allowedActions` while any of its checks is running or
    waiting, even when another check has already failed. The list can't
    tell an Actions check from an external CI, so a pull request whose
    only running check is an external one (on Forgejo, a pending commit
    status too) still offers it, and the checks list then has no `runId`
    to send.

    It is never queued for a rate-limit reset. After the reset the run may
    be a different one, started by a newer push, and a cancel can't be
    undone. A rate limit arrives as a 429 and the person decides again.

    Refusals are an `ActionError` (see Merge) and carry the forge's own
    plain-words `message`: the token may not write to Actions, the run
    already finished, or a Forgejo instance too old to have the route.
    An old Forgejo answers the missing route with a 404, which looks the
    same as a run that is gone, so it is reported as that and doesn't
    stop the dialog offering the action.

    Args:
        body (CancelRunRequest):

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
