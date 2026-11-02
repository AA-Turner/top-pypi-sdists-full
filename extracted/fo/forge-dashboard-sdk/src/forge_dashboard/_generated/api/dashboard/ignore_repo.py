from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.repo_ignore_request import RepoIgnoreRequest
from typing import cast



def _get_kwargs(
    *,
    body: RepoIgnoreRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/repos/ignore",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | Error | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: RepoIgnoreRequest,

) -> Response[Any | Error]:
    """ Hide one tracked repo's pull requests, issues, or both from the dashboard and Insights

     Reversible, not destructive: the repo itself keeps
    appearing in GET /api/v1/dashboard's `repos` array with accurate
    webhook-coverage status, and keeps being fetched and counted —
    only the pullRequests and/or issues entries the request scopes
    stop appearing there and on Insights. A repeat call
    replaces the previously saved scope rather than merging with it
    (ignoring PRs only, then issues only, ends with only issues
    ignored) — idempotent for an identical repeat, not additive
    across different scopes.

    Args:
        body (RepoIgnoreRequest): Which repo to ignore, and in which scope(s). At least one
            of prs/issues must be true — a request with both false is
            rejected with 400 rather than silently doing nothing; use POST
            /api/v1/repos/unignore to clear both at once instead.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
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
    body: RepoIgnoreRequest,

) -> Any | Error | None:
    """ Hide one tracked repo's pull requests, issues, or both from the dashboard and Insights

     Reversible, not destructive: the repo itself keeps
    appearing in GET /api/v1/dashboard's `repos` array with accurate
    webhook-coverage status, and keeps being fetched and counted —
    only the pullRequests and/or issues entries the request scopes
    stop appearing there and on Insights. A repeat call
    replaces the previously saved scope rather than merging with it
    (ignoring PRs only, then issues only, ends with only issues
    ignored) — idempotent for an identical repeat, not additive
    across different scopes.

    Args:
        body (RepoIgnoreRequest): Which repo to ignore, and in which scope(s). At least one
            of prs/issues must be true — a request with both false is
            rejected with 400 rather than silently doing nothing; use POST
            /api/v1/repos/unignore to clear both at once instead.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: RepoIgnoreRequest,

) -> Response[Any | Error]:
    """ Hide one tracked repo's pull requests, issues, or both from the dashboard and Insights

     Reversible, not destructive: the repo itself keeps
    appearing in GET /api/v1/dashboard's `repos` array with accurate
    webhook-coverage status, and keeps being fetched and counted —
    only the pullRequests and/or issues entries the request scopes
    stop appearing there and on Insights. A repeat call
    replaces the previously saved scope rather than merging with it
    (ignoring PRs only, then issues only, ends with only issues
    ignored) — idempotent for an identical repeat, not additive
    across different scopes.

    Args:
        body (RepoIgnoreRequest): Which repo to ignore, and in which scope(s). At least one
            of prs/issues must be true — a request with both false is
            rejected with 400 rather than silently doing nothing; use POST
            /api/v1/repos/unignore to clear both at once instead.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
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
    body: RepoIgnoreRequest,

) -> Any | Error | None:
    """ Hide one tracked repo's pull requests, issues, or both from the dashboard and Insights

     Reversible, not destructive: the repo itself keeps
    appearing in GET /api/v1/dashboard's `repos` array with accurate
    webhook-coverage status, and keeps being fetched and counted —
    only the pullRequests and/or issues entries the request scopes
    stop appearing there and on Insights. A repeat call
    replaces the previously saved scope rather than merging with it
    (ignoring PRs only, then issues only, ends with only issues
    ignored) — idempotent for an identical repeat, not additive
    across different scopes.

    Args:
        body (RepoIgnoreRequest): Which repo to ignore, and in which scope(s). At least one
            of prs/issues must be true — a request with both false is
            rejected with 400 rather than silently doing nothing; use POST
            /api/v1/repos/unignore to clear both at once instead.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
