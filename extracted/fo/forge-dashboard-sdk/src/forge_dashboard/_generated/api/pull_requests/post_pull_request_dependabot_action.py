from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.action_error import ActionError
from ...models.error import Error
from ...models.pull_request_dependabot_action_request import PullRequestDependabotActionRequest
from typing import cast



def _get_kwargs(
    *,
    body: PullRequestDependabotActionRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/pull-requests/dependabot-action",
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
    body: PullRequestDependabotActionRequest,

) -> Response[ActionError | Any | Error]:
    """ Post one of Dependabot's own documented PR-comment commands on a pull request, on the signed-in
    user's behalf

     Posts exactly `@dependabot rebase` or `@dependabot recreate` as a
    comment on the named pull request — Dependabot's own documented
    comment-command interface, not a generic "post any comment"
    endpoint; `action` is validated server-side to one of the two
    values below and nothing else is ever sent. GitHub only —
    Dependabot doesn't run on Forgejo.

    When the forge refuses, the server re-reads the pull request and
    answers an `ActionError` (see Merge): `already_merged` or
    `already_closed` when the row was stale, otherwise a `code` and a
    plain-words `message` safe to show a person.
    A connected App with no personal token saved is `permission`, with
    the reason in `message`; nothing is posted.

    Args:
        body (PullRequestDependabotActionRequest): Which pull request to act on, and which of
            Dependabot's own comment commands to send.

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
    body: PullRequestDependabotActionRequest,

) -> ActionError | Any | Error | None:
    """ Post one of Dependabot's own documented PR-comment commands on a pull request, on the signed-in
    user's behalf

     Posts exactly `@dependabot rebase` or `@dependabot recreate` as a
    comment on the named pull request — Dependabot's own documented
    comment-command interface, not a generic "post any comment"
    endpoint; `action` is validated server-side to one of the two
    values below and nothing else is ever sent. GitHub only —
    Dependabot doesn't run on Forgejo.

    When the forge refuses, the server re-reads the pull request and
    answers an `ActionError` (see Merge): `already_merged` or
    `already_closed` when the row was stale, otherwise a `code` and a
    plain-words `message` safe to show a person.
    A connected App with no personal token saved is `permission`, with
    the reason in `message`; nothing is posted.

    Args:
        body (PullRequestDependabotActionRequest): Which pull request to act on, and which of
            Dependabot's own comment commands to send.

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
    body: PullRequestDependabotActionRequest,

) -> Response[ActionError | Any | Error]:
    """ Post one of Dependabot's own documented PR-comment commands on a pull request, on the signed-in
    user's behalf

     Posts exactly `@dependabot rebase` or `@dependabot recreate` as a
    comment on the named pull request — Dependabot's own documented
    comment-command interface, not a generic "post any comment"
    endpoint; `action` is validated server-side to one of the two
    values below and nothing else is ever sent. GitHub only —
    Dependabot doesn't run on Forgejo.

    When the forge refuses, the server re-reads the pull request and
    answers an `ActionError` (see Merge): `already_merged` or
    `already_closed` when the row was stale, otherwise a `code` and a
    plain-words `message` safe to show a person.
    A connected App with no personal token saved is `permission`, with
    the reason in `message`; nothing is posted.

    Args:
        body (PullRequestDependabotActionRequest): Which pull request to act on, and which of
            Dependabot's own comment commands to send.

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
    body: PullRequestDependabotActionRequest,

) -> ActionError | Any | Error | None:
    """ Post one of Dependabot's own documented PR-comment commands on a pull request, on the signed-in
    user's behalf

     Posts exactly `@dependabot rebase` or `@dependabot recreate` as a
    comment on the named pull request — Dependabot's own documented
    comment-command interface, not a generic "post any comment"
    endpoint; `action` is validated server-side to one of the two
    values below and nothing else is ever sent. GitHub only —
    Dependabot doesn't run on Forgejo.

    When the forge refuses, the server re-reads the pull request and
    answers an `ActionError` (see Merge): `already_merged` or
    `already_closed` when the row was stale, otherwise a `code` and a
    plain-words `message` safe to show a person.
    A connected App with no personal token saved is `permission`, with
    the reason in `message`; nothing is posted.

    Args:
        body (PullRequestDependabotActionRequest): Which pull request to act on, and which of
            Dependabot's own comment commands to send.

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
