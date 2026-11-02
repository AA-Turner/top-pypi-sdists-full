from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.main_branches import MainBranches
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/main-branches",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | MainBranches | None:
    if response.status_code == 200:
        response_200 = MainBranches.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | MainBranches]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[Error | MainBranches]:
    """ The CI status of every tracked repository's default branch

     One row per tracked repository, showing the latest pipeline on its
    default branch: failed, passed, running or none. A repository
    ignored for pull requests is left out, as on the pull requests page.
    Every other row is returned, whatever its status, and no tally comes
    with them, so a client filters, sorts and counts locally and its pill
    counts always match what each pill lists. Rows come in no particular
    order: the client orders them.

    A row's `checks` counts tally the jobs `get_main_branch_checks`
    lists; the `CheckCounts` schema says how cancelled and held runs
    count. On GitHub the two are read separately, so they can differ
    briefly.

    Served from the snapshot the background refresh already holds, so it
    never calls a forge. On GitHub the branch's check status rides the
    repository query the refresh already makes (no extra request); on
    Forgejo the refresh lists the Actions runs of the default branch, once
    per repository.

    A forge that can't be reached keeps its last known rows, each marked
    `staleSince`, the same carry-over `forges[].staleSince`
    on GET /api/v1/dashboard reports. A forge whose rate-limit budget is
    spent is skipped until it resets and its rows are kept the same way.
    Only the signed-in user's own repositories.

    A repository with no default branch yet (empty) or no pipeline has
    status `none`. Unauthenticated GitHub access (a username with no
    token) has no rows: its budget is too small to spend on this.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | MainBranches]
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

) -> Error | MainBranches | None:
    """ The CI status of every tracked repository's default branch

     One row per tracked repository, showing the latest pipeline on its
    default branch: failed, passed, running or none. A repository
    ignored for pull requests is left out, as on the pull requests page.
    Every other row is returned, whatever its status, and no tally comes
    with them, so a client filters, sorts and counts locally and its pill
    counts always match what each pill lists. Rows come in no particular
    order: the client orders them.

    A row's `checks` counts tally the jobs `get_main_branch_checks`
    lists; the `CheckCounts` schema says how cancelled and held runs
    count. On GitHub the two are read separately, so they can differ
    briefly.

    Served from the snapshot the background refresh already holds, so it
    never calls a forge. On GitHub the branch's check status rides the
    repository query the refresh already makes (no extra request); on
    Forgejo the refresh lists the Actions runs of the default branch, once
    per repository.

    A forge that can't be reached keeps its last known rows, each marked
    `staleSince`, the same carry-over `forges[].staleSince`
    on GET /api/v1/dashboard reports. A forge whose rate-limit budget is
    spent is skipped until it resets and its rows are kept the same way.
    Only the signed-in user's own repositories.

    A repository with no default branch yet (empty) or no pipeline has
    status `none`. Unauthenticated GitHub access (a username with no
    token) has no rows: its budget is too small to spend on this.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | MainBranches
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[Error | MainBranches]:
    """ The CI status of every tracked repository's default branch

     One row per tracked repository, showing the latest pipeline on its
    default branch: failed, passed, running or none. A repository
    ignored for pull requests is left out, as on the pull requests page.
    Every other row is returned, whatever its status, and no tally comes
    with them, so a client filters, sorts and counts locally and its pill
    counts always match what each pill lists. Rows come in no particular
    order: the client orders them.

    A row's `checks` counts tally the jobs `get_main_branch_checks`
    lists; the `CheckCounts` schema says how cancelled and held runs
    count. On GitHub the two are read separately, so they can differ
    briefly.

    Served from the snapshot the background refresh already holds, so it
    never calls a forge. On GitHub the branch's check status rides the
    repository query the refresh already makes (no extra request); on
    Forgejo the refresh lists the Actions runs of the default branch, once
    per repository.

    A forge that can't be reached keeps its last known rows, each marked
    `staleSince`, the same carry-over `forges[].staleSince`
    on GET /api/v1/dashboard reports. A forge whose rate-limit budget is
    spent is skipped until it resets and its rows are kept the same way.
    Only the signed-in user's own repositories.

    A repository with no default branch yet (empty) or no pipeline has
    status `none`. Unauthenticated GitHub access (a username with no
    token) has no rows: its budget is too small to spend on this.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | MainBranches]
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

) -> Error | MainBranches | None:
    """ The CI status of every tracked repository's default branch

     One row per tracked repository, showing the latest pipeline on its
    default branch: failed, passed, running or none. A repository
    ignored for pull requests is left out, as on the pull requests page.
    Every other row is returned, whatever its status, and no tally comes
    with them, so a client filters, sorts and counts locally and its pill
    counts always match what each pill lists. Rows come in no particular
    order: the client orders them.

    A row's `checks` counts tally the jobs `get_main_branch_checks`
    lists; the `CheckCounts` schema says how cancelled and held runs
    count. On GitHub the two are read separately, so they can differ
    briefly.

    Served from the snapshot the background refresh already holds, so it
    never calls a forge. On GitHub the branch's check status rides the
    repository query the refresh already makes (no extra request); on
    Forgejo the refresh lists the Actions runs of the default branch, once
    per repository.

    A forge that can't be reached keeps its last known rows, each marked
    `staleSince`, the same carry-over `forges[].staleSince`
    on GET /api/v1/dashboard reports. A forge whose rate-limit budget is
    spent is skipped until it resets and its rows are kept the same way.
    Only the signed-in user's own repositories.

    A repository with no default branch yet (empty) or no pipeline has
    status `none`. Unauthenticated GitHub access (a username with no
    token) has no rows: its budget is too small to spend on this.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | MainBranches
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
