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
        "url": "/api/v1/pull-requests/renovate-rebase/cancel",
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
    body: PullRequestActionRequest,

) -> Response[ActionError | Any | Error]:
    """ Withdraw a requested Renovate rebase on a pull request, on the signed-in user's behalf

     Unticks the `rebase-check` checkbox in the named pull request's
    body (`- [x] <!-- rebase-check -->...` becomes `- [ ] ...`, and
    nothing else in the body changes), which takes back the rebase
    that ticking it asked for. Renovate looks at the box on its next
    run, so a rebase it has already started is not stopped. The
    pull request offers it as a `cancel_renovate_rebase` entry in
    `allowedActions`, which it does while the box is ticked. A request
    made with the rebase label has no checkbox, so it has no cancel.

    Cancelling is idempotent: a box that is already unticked is left
    alone and the answer is still 204. The pending `botRequest` of that
    rebase, if this app recorded one, is dropped from the next snapshot.

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
    """ Withdraw a requested Renovate rebase on a pull request, on the signed-in user's behalf

     Unticks the `rebase-check` checkbox in the named pull request's
    body (`- [x] <!-- rebase-check -->...` becomes `- [ ] ...`, and
    nothing else in the body changes), which takes back the rebase
    that ticking it asked for. Renovate looks at the box on its next
    run, so a rebase it has already started is not stopped. The
    pull request offers it as a `cancel_renovate_rebase` entry in
    `allowedActions`, which it does while the box is ticked. A request
    made with the rebase label has no checkbox, so it has no cancel.

    Cancelling is idempotent: a box that is already unticked is left
    alone and the answer is still 204. The pending `botRequest` of that
    rebase, if this app recorded one, is dropped from the next snapshot.

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
    """ Withdraw a requested Renovate rebase on a pull request, on the signed-in user's behalf

     Unticks the `rebase-check` checkbox in the named pull request's
    body (`- [x] <!-- rebase-check -->...` becomes `- [ ] ...`, and
    nothing else in the body changes), which takes back the rebase
    that ticking it asked for. Renovate looks at the box on its next
    run, so a rebase it has already started is not stopped. The
    pull request offers it as a `cancel_renovate_rebase` entry in
    `allowedActions`, which it does while the box is ticked. A request
    made with the rebase label has no checkbox, so it has no cancel.

    Cancelling is idempotent: a box that is already unticked is left
    alone and the answer is still 204. The pending `botRequest` of that
    rebase, if this app recorded one, is dropped from the next snapshot.

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
    """ Withdraw a requested Renovate rebase on a pull request, on the signed-in user's behalf

     Unticks the `rebase-check` checkbox in the named pull request's
    body (`- [x] <!-- rebase-check -->...` becomes `- [ ] ...`, and
    nothing else in the body changes), which takes back the rebase
    that ticking it asked for. Renovate looks at the box on its next
    run, so a rebase it has already started is not stopped. The
    pull request offers it as a `cancel_renovate_rebase` entry in
    `allowedActions`, which it does while the box is ticked. A request
    made with the rebase label has no checkbox, so it has no cancel.

    Cancelling is idempotent: a box that is already unticked is left
    alone and the answer is still 204. The pending `botRequest` of that
    rebase, if this app recorded one, is dropped from the next snapshot.

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
