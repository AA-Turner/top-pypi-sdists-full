from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.action_error import ActionError
from ...models.error import Error
from ...models.issue_comment_request import IssueCommentRequest
from typing import cast



def _get_kwargs(
    *,
    body: IssueCommentRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/issues/comment",
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
    body: IssueCommentRequest,

) -> Response[ActionError | Any | Error]:
    """ Post a comment on one issue, on the signed-in user's behalf

     Posts `body` as a comment on the named issue. The dialog's "Close with
    a comment" calls this first and Close second, so when the second call
    fails the page knows the comment is already there and offers only the
    close again. On GitHub, with the App as the credential and a personal
    token saved beside it, the comment is posted as that person.

    A refusal is an `ActionError`, classified as for Close.

    Closing, reopening and commenting change the issue, so they need write
    access to issues, which reading does not: a GitHub token's Issues
    permission (or the App's) set to Read and write, or a Forgejo token's
    `write:issue` scope. Without it the forge answers 403 and this
    endpoint answers an `ActionError` with `code` `permission`, whose
    `message` names what to add.

    Args:
        body (IssueCommentRequest): Which issue to comment on, and what to say.

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
    body: IssueCommentRequest,

) -> ActionError | Any | Error | None:
    """ Post a comment on one issue, on the signed-in user's behalf

     Posts `body` as a comment on the named issue. The dialog's "Close with
    a comment" calls this first and Close second, so when the second call
    fails the page knows the comment is already there and offers only the
    close again. On GitHub, with the App as the credential and a personal
    token saved beside it, the comment is posted as that person.

    A refusal is an `ActionError`, classified as for Close.

    Closing, reopening and commenting change the issue, so they need write
    access to issues, which reading does not: a GitHub token's Issues
    permission (or the App's) set to Read and write, or a Forgejo token's
    `write:issue` scope. Without it the forge answers 403 and this
    endpoint answers an `ActionError` with `code` `permission`, whose
    `message` names what to add.

    Args:
        body (IssueCommentRequest): Which issue to comment on, and what to say.

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
    body: IssueCommentRequest,

) -> Response[ActionError | Any | Error]:
    """ Post a comment on one issue, on the signed-in user's behalf

     Posts `body` as a comment on the named issue. The dialog's "Close with
    a comment" calls this first and Close second, so when the second call
    fails the page knows the comment is already there and offers only the
    close again. On GitHub, with the App as the credential and a personal
    token saved beside it, the comment is posted as that person.

    A refusal is an `ActionError`, classified as for Close.

    Closing, reopening and commenting change the issue, so they need write
    access to issues, which reading does not: a GitHub token's Issues
    permission (or the App's) set to Read and write, or a Forgejo token's
    `write:issue` scope. Without it the forge answers 403 and this
    endpoint answers an `ActionError` with `code` `permission`, whose
    `message` names what to add.

    Args:
        body (IssueCommentRequest): Which issue to comment on, and what to say.

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
    body: IssueCommentRequest,

) -> ActionError | Any | Error | None:
    """ Post a comment on one issue, on the signed-in user's behalf

     Posts `body` as a comment on the named issue. The dialog's "Close with
    a comment" calls this first and Close second, so when the second call
    fails the page knows the comment is already there and offers only the
    close again. On GitHub, with the App as the credential and a personal
    token saved beside it, the comment is posted as that person.

    A refusal is an `ActionError`, classified as for Close.

    Closing, reopening and commenting change the issue, so they need write
    access to issues, which reading does not: a GitHub token's Issues
    permission (or the App's) set to Read and write, or a Forgejo token's
    `write:issue` scope. Without it the forge answers 403 and this
    endpoint answers an `ActionError` with `code` `permission`, whose
    `message` names what to add.

    Args:
        body (IssueCommentRequest): Which issue to comment on, and what to say.

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
