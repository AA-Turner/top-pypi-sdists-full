from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx2

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.forge import Forge
from ...models.get_pull_request_rerunnable_response_200 import GetPullRequestRerunnableResponse200
from typing import cast



def _get_kwargs(
    *,
    forge: Forge,
    full_name: str,
    number: int,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_forge = forge.value
    params["forge"] = json_forge

    params["fullName"] = full_name

    params["number"] = number


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/pull-requests/rerunnable",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Error | GetPullRequestRerunnableResponse200 | None:
    if response.status_code == 200:
        response_200 = GetPullRequestRerunnableResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())



        return response_429

    if response.status_code == 502:
        response_502 = Error.from_dict(response.json())



        return response_502

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Response[Error | GetPullRequestRerunnableResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    forge: Forge,
    full_name: str,
    number: int,

) -> Response[Error | GetPullRequestRerunnableResponse200]:
    """ Say whether Rerun failed checks would find a job on one pull request, without rerunning anything

     Reads what POST /api/v1/pull-requests/rerun-checks reads and restarts
    nothing: on GitHub the failed check runs on the head commit, each mapped
    to its workflow run; on Forgejo the failed Actions runs on the head
    commit, after the same version check. The bulk "Rerun failed checks"
    control asks it for each failing row, to sort them before it sends a
    request.

    "No" is an answer, not an error: `rerunnable` is false and `reason`
    carries the same sentence the rerun's 409 would (only non-Actions checks
    failed, nothing ran, a Forgejo older than 17). A forge that can't be read
    keeps its own status. The forge can still refuse the rerun itself (the
    run is too old, the token can't write to Actions), which only the rerun
    learns.

    This costs forge requests on every call (the pull request, its check
    runs and one job lookup per failed check on GitHub), so it is never part
    of the snapshot.

    Args:
        forge (Forge):
        full_name (str):
        number (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetPullRequestRerunnableResponse200]
     """


    kwargs = _get_kwargs(
        forge=forge,
full_name=full_name,
number=number,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    forge: Forge,
    full_name: str,
    number: int,

) -> Error | GetPullRequestRerunnableResponse200 | None:
    """ Say whether Rerun failed checks would find a job on one pull request, without rerunning anything

     Reads what POST /api/v1/pull-requests/rerun-checks reads and restarts
    nothing: on GitHub the failed check runs on the head commit, each mapped
    to its workflow run; on Forgejo the failed Actions runs on the head
    commit, after the same version check. The bulk "Rerun failed checks"
    control asks it for each failing row, to sort them before it sends a
    request.

    "No" is an answer, not an error: `rerunnable` is false and `reason`
    carries the same sentence the rerun's 409 would (only non-Actions checks
    failed, nothing ran, a Forgejo older than 17). A forge that can't be read
    keeps its own status. The forge can still refuse the rerun itself (the
    run is too old, the token can't write to Actions), which only the rerun
    learns.

    This costs forge requests on every call (the pull request, its check
    runs and one job lookup per failed check on GitHub), so it is never part
    of the snapshot.

    Args:
        forge (Forge):
        full_name (str):
        number (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetPullRequestRerunnableResponse200
     """


    return sync_detailed(
        client=client,
forge=forge,
full_name=full_name,
number=number,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    forge: Forge,
    full_name: str,
    number: int,

) -> Response[Error | GetPullRequestRerunnableResponse200]:
    """ Say whether Rerun failed checks would find a job on one pull request, without rerunning anything

     Reads what POST /api/v1/pull-requests/rerun-checks reads and restarts
    nothing: on GitHub the failed check runs on the head commit, each mapped
    to its workflow run; on Forgejo the failed Actions runs on the head
    commit, after the same version check. The bulk "Rerun failed checks"
    control asks it for each failing row, to sort them before it sends a
    request.

    "No" is an answer, not an error: `rerunnable` is false and `reason`
    carries the same sentence the rerun's 409 would (only non-Actions checks
    failed, nothing ran, a Forgejo older than 17). A forge that can't be read
    keeps its own status. The forge can still refuse the rerun itself (the
    run is too old, the token can't write to Actions), which only the rerun
    learns.

    This costs forge requests on every call (the pull request, its check
    runs and one job lookup per failed check on GitHub), so it is never part
    of the snapshot.

    Args:
        forge (Forge):
        full_name (str):
        number (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetPullRequestRerunnableResponse200]
     """


    kwargs = _get_kwargs(
        forge=forge,
full_name=full_name,
number=number,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    forge: Forge,
    full_name: str,
    number: int,

) -> Error | GetPullRequestRerunnableResponse200 | None:
    """ Say whether Rerun failed checks would find a job on one pull request, without rerunning anything

     Reads what POST /api/v1/pull-requests/rerun-checks reads and restarts
    nothing: on GitHub the failed check runs on the head commit, each mapped
    to its workflow run; on Forgejo the failed Actions runs on the head
    commit, after the same version check. The bulk "Rerun failed checks"
    control asks it for each failing row, to sort them before it sends a
    request.

    "No" is an answer, not an error: `rerunnable` is false and `reason`
    carries the same sentence the rerun's 409 would (only non-Actions checks
    failed, nothing ran, a Forgejo older than 17). A forge that can't be read
    keeps its own status. The forge can still refuse the rerun itself (the
    run is too old, the token can't write to Actions), which only the rerun
    learns.

    This costs forge requests on every call (the pull request, its check
    runs and one job lookup per failed check on GitHub), so it is never part
    of the snapshot.

    Args:
        forge (Forge):
        full_name (str):
        number (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetPullRequestRerunnableResponse200
     """


    return (await asyncio_detailed(
        client=client,
forge=forge,
full_name=full_name,
number=number,

    )).parsed
