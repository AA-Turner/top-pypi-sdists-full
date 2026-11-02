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
        "url": "/api/v1/pull-requests/update-branch",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ActionError | Any | Error | None:
    if response.status_code == 202:
        response_202 = cast(Any, None)
        return response_202

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
    """ Bring one pull request's branch up to date with its base, on the signed-in user's behalf

     Merges the named pull request's base branch into its own head
    branch. GitHub can schedule this as a background job rather than
    finishing it inline — a 202 here means exactly that, not a
    failure; a follow-up refresh a moment later reflects the result.
    Forgejo's equivalent is always synchronous, so it only ever
    answers 204.

    When the forge refuses, the server re-reads the pull request and
    answers an `ActionError` (see Merge): `already_merged` or
    `already_closed` when the row was stale, otherwise a `code` and a
    plain-words `message` safe to show a person.
    `conflict` means the branches can't be merged cleanly;
    `already_up_to_date` means there was nothing to bring in.

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
    """ Bring one pull request's branch up to date with its base, on the signed-in user's behalf

     Merges the named pull request's base branch into its own head
    branch. GitHub can schedule this as a background job rather than
    finishing it inline — a 202 here means exactly that, not a
    failure; a follow-up refresh a moment later reflects the result.
    Forgejo's equivalent is always synchronous, so it only ever
    answers 204.

    When the forge refuses, the server re-reads the pull request and
    answers an `ActionError` (see Merge): `already_merged` or
    `already_closed` when the row was stale, otherwise a `code` and a
    plain-words `message` safe to show a person.
    `conflict` means the branches can't be merged cleanly;
    `already_up_to_date` means there was nothing to bring in.

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
    """ Bring one pull request's branch up to date with its base, on the signed-in user's behalf

     Merges the named pull request's base branch into its own head
    branch. GitHub can schedule this as a background job rather than
    finishing it inline — a 202 here means exactly that, not a
    failure; a follow-up refresh a moment later reflects the result.
    Forgejo's equivalent is always synchronous, so it only ever
    answers 204.

    When the forge refuses, the server re-reads the pull request and
    answers an `ActionError` (see Merge): `already_merged` or
    `already_closed` when the row was stale, otherwise a `code` and a
    plain-words `message` safe to show a person.
    `conflict` means the branches can't be merged cleanly;
    `already_up_to_date` means there was nothing to bring in.

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
    """ Bring one pull request's branch up to date with its base, on the signed-in user's behalf

     Merges the named pull request's base branch into its own head
    branch. GitHub can schedule this as a background job rather than
    finishing it inline — a 202 here means exactly that, not a
    failure; a follow-up refresh a moment later reflects the result.
    Forgejo's equivalent is always synchronous, so it only ever
    answers 204.

    When the forge refuses, the server re-reads the pull request and
    answers an `ActionError` (see Merge): `already_merged` or
    `already_closed` when the row was stale, otherwise a `code` and a
    plain-words `message` safe to show a person.
    `conflict` means the branches can't be merged cleanly;
    `already_up_to_date` means there was nothing to bring in.

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
