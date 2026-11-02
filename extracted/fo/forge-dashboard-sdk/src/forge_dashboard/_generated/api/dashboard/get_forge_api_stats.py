from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.forge_api_stats import ForgeApiStats
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/stats/forge-api",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | ForgeApiStats | None:
    if response.status_code == 200:
        response_200 = ForgeApiStats.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | ForgeApiStats]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[Error | ForgeApiStats]:
    """ How many forge API calls the dashboard has spent, and on what

     Counts the forge requests made since the server started, so a change
    to what the dashboard refreshes can be shown to have saved budget, and
    a rate-limit incident traced to the refresh that caused it. One bucket
    per forge, credential, refresh `kind` and repository, each with the
    REST calls made, the GraphQL calls made, the GraphQL `rateLimit.cost`
    they were charged, and the requests answered `304 Not Modified`. A 304
    is not charged against the REST budget, so it is counted on its own and
    not as a REST call.

    `kind` says why the request was made: `full` (a whole-account
    refresh), `scoped_webhook` (one repository, after a webhook),
    `ci_poll` (one repository, waiting on a running check),
    `auto_merge_poll` (one repository, waiting on an armed auto-merge),
    `details` (a dialog or check list opened), `hook_maintenance`
    (checking, adding or upgrading webhooks), `advisories` (reading a
    repository's open Dependabot alerts, or a Forgejo repository's lockfiles), `user_action` (a button
    pressed, a queued action, or something the dashboard does for you such
    as auto-merge) and `unknown` (a request nobody tagged, which is a bug
    to report). A request that names no repository, such as listing an
    account's repositories, has an empty `repo`.

    The counters live in memory and start from zero on every start;
    `since` says when counting began. `credential` names the connected
    account or App installation by a label that carries no secret and no
    user id (`app:<installation id>`, `token:<short hash>`,
    `public:<username>`). Only the buckets of the caller's own
    credentials are returned. They are matched to the credentials
    the caller has saved, and a GitHub App installation id is a number the
    caller types in, so until the dashboard has one user, someone who saves
    another account's installation id sees that installation's counts. `budgets` are the rate limits
    each forge last
    reported, the same figures as `forges` on GET /api/v1/dashboard.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ForgeApiStats]
     """


    kwargs = _get_kwargs(
        
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,

) -> Error | ForgeApiStats | None:
    """ How many forge API calls the dashboard has spent, and on what

     Counts the forge requests made since the server started, so a change
    to what the dashboard refreshes can be shown to have saved budget, and
    a rate-limit incident traced to the refresh that caused it. One bucket
    per forge, credential, refresh `kind` and repository, each with the
    REST calls made, the GraphQL calls made, the GraphQL `rateLimit.cost`
    they were charged, and the requests answered `304 Not Modified`. A 304
    is not charged against the REST budget, so it is counted on its own and
    not as a REST call.

    `kind` says why the request was made: `full` (a whole-account
    refresh), `scoped_webhook` (one repository, after a webhook),
    `ci_poll` (one repository, waiting on a running check),
    `auto_merge_poll` (one repository, waiting on an armed auto-merge),
    `details` (a dialog or check list opened), `hook_maintenance`
    (checking, adding or upgrading webhooks), `advisories` (reading a
    repository's open Dependabot alerts, or a Forgejo repository's lockfiles), `user_action` (a button
    pressed, a queued action, or something the dashboard does for you such
    as auto-merge) and `unknown` (a request nobody tagged, which is a bug
    to report). A request that names no repository, such as listing an
    account's repositories, has an empty `repo`.

    The counters live in memory and start from zero on every start;
    `since` says when counting began. `credential` names the connected
    account or App installation by a label that carries no secret and no
    user id (`app:<installation id>`, `token:<short hash>`,
    `public:<username>`). Only the buckets of the caller's own
    credentials are returned. They are matched to the credentials
    the caller has saved, and a GitHub App installation id is a number the
    caller types in, so until the dashboard has one user, someone who saves
    another account's installation id sees that installation's counts. `budgets` are the rate limits
    each forge last
    reported, the same figures as `forges` on GET /api/v1/dashboard.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ForgeApiStats
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[Error | ForgeApiStats]:
    """ How many forge API calls the dashboard has spent, and on what

     Counts the forge requests made since the server started, so a change
    to what the dashboard refreshes can be shown to have saved budget, and
    a rate-limit incident traced to the refresh that caused it. One bucket
    per forge, credential, refresh `kind` and repository, each with the
    REST calls made, the GraphQL calls made, the GraphQL `rateLimit.cost`
    they were charged, and the requests answered `304 Not Modified`. A 304
    is not charged against the REST budget, so it is counted on its own and
    not as a REST call.

    `kind` says why the request was made: `full` (a whole-account
    refresh), `scoped_webhook` (one repository, after a webhook),
    `ci_poll` (one repository, waiting on a running check),
    `auto_merge_poll` (one repository, waiting on an armed auto-merge),
    `details` (a dialog or check list opened), `hook_maintenance`
    (checking, adding or upgrading webhooks), `advisories` (reading a
    repository's open Dependabot alerts, or a Forgejo repository's lockfiles), `user_action` (a button
    pressed, a queued action, or something the dashboard does for you such
    as auto-merge) and `unknown` (a request nobody tagged, which is a bug
    to report). A request that names no repository, such as listing an
    account's repositories, has an empty `repo`.

    The counters live in memory and start from zero on every start;
    `since` says when counting began. `credential` names the connected
    account or App installation by a label that carries no secret and no
    user id (`app:<installation id>`, `token:<short hash>`,
    `public:<username>`). Only the buckets of the caller's own
    credentials are returned. They are matched to the credentials
    the caller has saved, and a GitHub App installation id is a number the
    caller types in, so until the dashboard has one user, someone who saves
    another account's installation id sees that installation's counts. `budgets` are the rate limits
    each forge last
    reported, the same figures as `forges` on GET /api/v1/dashboard.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ForgeApiStats]
     """


    kwargs = _get_kwargs(
        
    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,

) -> Error | ForgeApiStats | None:
    """ How many forge API calls the dashboard has spent, and on what

     Counts the forge requests made since the server started, so a change
    to what the dashboard refreshes can be shown to have saved budget, and
    a rate-limit incident traced to the refresh that caused it. One bucket
    per forge, credential, refresh `kind` and repository, each with the
    REST calls made, the GraphQL calls made, the GraphQL `rateLimit.cost`
    they were charged, and the requests answered `304 Not Modified`. A 304
    is not charged against the REST budget, so it is counted on its own and
    not as a REST call.

    `kind` says why the request was made: `full` (a whole-account
    refresh), `scoped_webhook` (one repository, after a webhook),
    `ci_poll` (one repository, waiting on a running check),
    `auto_merge_poll` (one repository, waiting on an armed auto-merge),
    `details` (a dialog or check list opened), `hook_maintenance`
    (checking, adding or upgrading webhooks), `advisories` (reading a
    repository's open Dependabot alerts, or a Forgejo repository's lockfiles), `user_action` (a button
    pressed, a queued action, or something the dashboard does for you such
    as auto-merge) and `unknown` (a request nobody tagged, which is a bug
    to report). A request that names no repository, such as listing an
    account's repositories, has an empty `repo`.

    The counters live in memory and start from zero on every start;
    `since` says when counting began. `credential` names the connected
    account or App installation by a label that carries no secret and no
    user id (`app:<installation id>`, `token:<short hash>`,
    `public:<username>`). Only the buckets of the caller's own
    credentials are returned. They are matched to the credentials
    the caller has saved, and a GitHub App installation id is a number the
    caller types in, so until the dashboard has one user, someone who saves
    another account's installation id sees that installation's counts. `budgets` are the rate limits
    each forge last
    reported, the same figures as `forges` on GET /api/v1/dashboard.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ForgeApiStats
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
