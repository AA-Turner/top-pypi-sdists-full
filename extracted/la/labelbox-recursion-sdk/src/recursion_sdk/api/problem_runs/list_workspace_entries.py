from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.list_workspace_entries_response_dto import ListWorkspaceEntriesResponseDto
from ...models.target_api_error_forbidden import TargetApiErrorForbidden
from ...models.target_api_error_internal_error import TargetApiErrorInternalError
from ...models.target_api_error_invalid_request import TargetApiErrorInvalidRequest
from ...models.target_api_error_invariant_violation import TargetApiErrorInvariantViolation
from ...models.target_api_error_not_found import TargetApiErrorNotFound
from ...models.target_api_error_rate_limit_exceeded import TargetApiErrorRateLimitExceeded
from ...models.target_api_error_unauthorized import TargetApiErrorUnauthorized
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    problem_run_id: UUID,
    *,
    path: str | Unset = '',
    limit: int | Unset = 100,
    cursor: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["path"] = path

    params["limit"] = limit

    params["cursor"] = cursor


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/problem-runs/{problem_run_id}/workspace-entries".format(problem_run_id=quote(str(problem_run_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ListWorkspaceEntriesResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    if response.status_code == 200:
        response_200 = ListWorkspaceEntriesResponseDto.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = TargetApiErrorInvalidRequest.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = TargetApiErrorUnauthorized.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = TargetApiErrorForbidden.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = TargetApiErrorNotFound.from_dict(response.json())



        return response_404

    if response.status_code == 429:
        response_429 = TargetApiErrorRateLimitExceeded.from_dict(response.json())



        return response_429

    if response.status_code == 500:
        def _parse_response_500(data: object) -> TargetApiErrorInternalError | TargetApiErrorInvariantViolation:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_500_type_0 = TargetApiErrorInternalError.from_dict(data)



                return response_500_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_500_type_1 = TargetApiErrorInvariantViolation.from_dict(data)



            return response_500_type_1

        response_500 = _parse_response_500(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ListWorkspaceEntriesResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    problem_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    path: str | Unset = '',
    limit: int | Unset = 100,
    cursor: str | Unset = UNSET,

) -> Response[ListWorkspaceEntriesResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ List one directory level of a run's live output workspace

     Reads the live agent-service workspace, which is retained for roughly 24 hours after run completion;
    afterwards the response is empty with the availability flag cleared. Complements the persisted
    output files, whose ingestion is capped for large trees.

    Args:
        problem_run_id (UUID): Stable problem-run identifier (UUID). One solver attempt at one
            problem version.
        path (str | Unset): Directory to list, relative to the run's output directory. Empty or
            omitted for the root. Default: ''.
        limit (int | Unset): Maximum number of entries to return in the page (1-100). Default:
            100. Example: 100.
        cursor (str | Unset): Opaque cursor returned by a previous page response. Omit to fetch
            the first page.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListWorkspaceEntriesResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        problem_run_id=problem_run_id,
path=path,
limit=limit,
cursor=cursor,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    problem_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    path: str | Unset = '',
    limit: int | Unset = 100,
    cursor: str | Unset = UNSET,

) -> ListWorkspaceEntriesResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ List one directory level of a run's live output workspace

     Reads the live agent-service workspace, which is retained for roughly 24 hours after run completion;
    afterwards the response is empty with the availability flag cleared. Complements the persisted
    output files, whose ingestion is capped for large trees.

    Args:
        problem_run_id (UUID): Stable problem-run identifier (UUID). One solver attempt at one
            problem version.
        path (str | Unset): Directory to list, relative to the run's output directory. Empty or
            omitted for the root. Default: ''.
        limit (int | Unset): Maximum number of entries to return in the page (1-100). Default:
            100. Example: 100.
        cursor (str | Unset): Opaque cursor returned by a previous page response. Omit to fetch
            the first page.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListWorkspaceEntriesResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return sync_detailed(
        problem_run_id=problem_run_id,
client=client,
path=path,
limit=limit,
cursor=cursor,

    ).parsed

async def asyncio_detailed(
    problem_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    path: str | Unset = '',
    limit: int | Unset = 100,
    cursor: str | Unset = UNSET,

) -> Response[ListWorkspaceEntriesResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ List one directory level of a run's live output workspace

     Reads the live agent-service workspace, which is retained for roughly 24 hours after run completion;
    afterwards the response is empty with the availability flag cleared. Complements the persisted
    output files, whose ingestion is capped for large trees.

    Args:
        problem_run_id (UUID): Stable problem-run identifier (UUID). One solver attempt at one
            problem version.
        path (str | Unset): Directory to list, relative to the run's output directory. Empty or
            omitted for the root. Default: ''.
        limit (int | Unset): Maximum number of entries to return in the page (1-100). Default:
            100. Example: 100.
        cursor (str | Unset): Opaque cursor returned by a previous page response. Omit to fetch
            the first page.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListWorkspaceEntriesResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        problem_run_id=problem_run_id,
path=path,
limit=limit,
cursor=cursor,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    problem_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    path: str | Unset = '',
    limit: int | Unset = 100,
    cursor: str | Unset = UNSET,

) -> ListWorkspaceEntriesResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ List one directory level of a run's live output workspace

     Reads the live agent-service workspace, which is retained for roughly 24 hours after run completion;
    afterwards the response is empty with the availability flag cleared. Complements the persisted
    output files, whose ingestion is capped for large trees.

    Args:
        problem_run_id (UUID): Stable problem-run identifier (UUID). One solver attempt at one
            problem version.
        path (str | Unset): Directory to list, relative to the run's output directory. Empty or
            omitted for the root. Default: ''.
        limit (int | Unset): Maximum number of entries to return in the page (1-100). Default:
            100. Example: 100.
        cursor (str | Unset): Opaque cursor returned by a previous page response. Omit to fetch
            the first page.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListWorkspaceEntriesResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return (await asyncio_detailed(
        problem_run_id=problem_run_id,
client=client,
path=path,
limit=limit,
cursor=cursor,

    )).parsed
