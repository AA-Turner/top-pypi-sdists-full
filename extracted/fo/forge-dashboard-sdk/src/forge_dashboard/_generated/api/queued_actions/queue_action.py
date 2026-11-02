from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.action_error import ActionError
from ...models.error import Error
from ...models.queued_action import QueuedAction
from ...models.queued_action_request import QueuedActionRequest
from typing import cast



def _get_kwargs(
    *,
    body: QueuedActionRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/queued-actions",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ActionError | Error | QueuedAction | None:
    if response.status_code == 200:
        response_200 = QueuedAction.from_dict(response.json())



        return response_200

    if response.status_code == 201:
        response_201 = QueuedAction.from_dict(response.json())



        return response_201

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 409:
        response_409 = ActionError.from_dict(response.json())



        return response_409

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ActionError | Error | QueuedAction]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: QueuedActionRequest,

) -> Response[ActionError | Error | QueuedAction]:
    """ Queue a safe action to run when a rate-limited forge resets

     Stores the intent server-side. When the forge's budget comes back
    the server reads the pull request again and runs the action only
    if it still applies; otherwise it records why it did nothing. It
    survives a page reload and a server restart.

    Only safe, idempotent actions can be queued: `update_branch`,
    `dependabot_rebase` and `renovate_rebase`. Merge and Close are not
    queueable and answer 400: they would act unattended on a pull
    request whose checks or commits may have changed. To merge once
    the limit lifts, use the forge's own auto-merge.

    The forge must be rate limited right now (a spent budget in
    `forges[].rateLimitRest` or `rateLimitGraphql` whose `resetsAt` is
    ahead), otherwise there is nothing to wait for and the action
    should be taken directly: 409 `not_rate_limited`. The pull request
    must be on the signed-in user's board and offer the action
    (`allowedActions`) and be behind its base branch, with the same
    409 codes the direct action answers. The queued item runs with
    the user's own saved credentials for that forge, never anyone
    else's. Queueing the same action on the same pull request twice
    returns the first item with 200.

    Args:
        body (QueuedActionRequest): Which safe action to queue, on which pull request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ActionError | Error | QueuedAction]
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
    body: QueuedActionRequest,

) -> ActionError | Error | QueuedAction | None:
    """ Queue a safe action to run when a rate-limited forge resets

     Stores the intent server-side. When the forge's budget comes back
    the server reads the pull request again and runs the action only
    if it still applies; otherwise it records why it did nothing. It
    survives a page reload and a server restart.

    Only safe, idempotent actions can be queued: `update_branch`,
    `dependabot_rebase` and `renovate_rebase`. Merge and Close are not
    queueable and answer 400: they would act unattended on a pull
    request whose checks or commits may have changed. To merge once
    the limit lifts, use the forge's own auto-merge.

    The forge must be rate limited right now (a spent budget in
    `forges[].rateLimitRest` or `rateLimitGraphql` whose `resetsAt` is
    ahead), otherwise there is nothing to wait for and the action
    should be taken directly: 409 `not_rate_limited`. The pull request
    must be on the signed-in user's board and offer the action
    (`allowedActions`) and be behind its base branch, with the same
    409 codes the direct action answers. The queued item runs with
    the user's own saved credentials for that forge, never anyone
    else's. Queueing the same action on the same pull request twice
    returns the first item with 200.

    Args:
        body (QueuedActionRequest): Which safe action to queue, on which pull request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ActionError | Error | QueuedAction
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: QueuedActionRequest,

) -> Response[ActionError | Error | QueuedAction]:
    """ Queue a safe action to run when a rate-limited forge resets

     Stores the intent server-side. When the forge's budget comes back
    the server reads the pull request again and runs the action only
    if it still applies; otherwise it records why it did nothing. It
    survives a page reload and a server restart.

    Only safe, idempotent actions can be queued: `update_branch`,
    `dependabot_rebase` and `renovate_rebase`. Merge and Close are not
    queueable and answer 400: they would act unattended on a pull
    request whose checks or commits may have changed. To merge once
    the limit lifts, use the forge's own auto-merge.

    The forge must be rate limited right now (a spent budget in
    `forges[].rateLimitRest` or `rateLimitGraphql` whose `resetsAt` is
    ahead), otherwise there is nothing to wait for and the action
    should be taken directly: 409 `not_rate_limited`. The pull request
    must be on the signed-in user's board and offer the action
    (`allowedActions`) and be behind its base branch, with the same
    409 codes the direct action answers. The queued item runs with
    the user's own saved credentials for that forge, never anyone
    else's. Queueing the same action on the same pull request twice
    returns the first item with 200.

    Args:
        body (QueuedActionRequest): Which safe action to queue, on which pull request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ActionError | Error | QueuedAction]
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
    body: QueuedActionRequest,

) -> ActionError | Error | QueuedAction | None:
    """ Queue a safe action to run when a rate-limited forge resets

     Stores the intent server-side. When the forge's budget comes back
    the server reads the pull request again and runs the action only
    if it still applies; otherwise it records why it did nothing. It
    survives a page reload and a server restart.

    Only safe, idempotent actions can be queued: `update_branch`,
    `dependabot_rebase` and `renovate_rebase`. Merge and Close are not
    queueable and answer 400: they would act unattended on a pull
    request whose checks or commits may have changed. To merge once
    the limit lifts, use the forge's own auto-merge.

    The forge must be rate limited right now (a spent budget in
    `forges[].rateLimitRest` or `rateLimitGraphql` whose `resetsAt` is
    ahead), otherwise there is nothing to wait for and the action
    should be taken directly: 409 `not_rate_limited`. The pull request
    must be on the signed-in user's board and offer the action
    (`allowedActions`) and be behind its base branch, with the same
    409 codes the direct action answers. The queued item runs with
    the user's own saved credentials for that forge, never anyone
    else's. Queueing the same action on the same pull request twice
    returns the first item with 200.

    Args:
        body (QueuedActionRequest): Which safe action to queue, on which pull request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ActionError | Error | QueuedAction
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
