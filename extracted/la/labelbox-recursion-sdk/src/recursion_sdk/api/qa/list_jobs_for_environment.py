from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.list_jobs_for_environment_sort_direction import ListJobsForEnvironmentSortDirection
from ...models.qa_job_page_response_dto import QaJobPageResponseDto
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
    environment_id: UUID,
    *,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    sort_direction: ListJobsForEnvironmentSortDirection | Unset = UNSET,
    search: str | Unset = UNSET,
    batch_id: UUID | Unset = UNSET,
    problem_id: UUID | Unset = UNSET,
    problem_search: str | Unset = UNSET,
    problem_version_id: UUID | Unset = UNSET,
    status: str | Unset = UNSET,
    qa_config_id: str | Unset = UNSET,
    kind: str | Unset = UNSET,
    score_min: float | Unset = UNSET,
    score_max: float | Unset = UNSET,
    grade: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["cursor"] = cursor

    params["sortBy"] = sort_by

    json_sort_direction: str | Unset = UNSET
    if not isinstance(sort_direction, Unset):
        json_sort_direction = sort_direction.value

    params["sortDirection"] = json_sort_direction

    params["search"] = search

    json_batch_id: str | Unset = UNSET
    if not isinstance(batch_id, Unset):
        json_batch_id = str(batch_id)
    params["batchId"] = json_batch_id

    json_problem_id: str | Unset = UNSET
    if not isinstance(problem_id, Unset):
        json_problem_id = str(problem_id)
    params["problemId"] = json_problem_id

    params["problemSearch"] = problem_search

    json_problem_version_id: str | Unset = UNSET
    if not isinstance(problem_version_id, Unset):
        json_problem_version_id = str(problem_version_id)
    params["problemVersionId"] = json_problem_version_id

    params["status"] = status

    params["qaConfigId"] = qa_config_id

    params["kind"] = kind

    params["scoreMin"] = score_min

    params["scoreMax"] = score_max

    params["grade"] = grade


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/environments/{environment_id}/qa-jobs".format(environment_id=quote(str(environment_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> QaJobPageResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    if response.status_code == 200:
        response_200 = QaJobPageResponseDto.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[QaJobPageResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    environment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    sort_direction: ListJobsForEnvironmentSortDirection | Unset = UNSET,
    search: str | Unset = UNSET,
    batch_id: UUID | Unset = UNSET,
    problem_id: UUID | Unset = UNSET,
    problem_search: str | Unset = UNSET,
    problem_version_id: UUID | Unset = UNSET,
    status: str | Unset = UNSET,
    qa_config_id: str | Unset = UNSET,
    kind: str | Unset = UNSET,
    score_min: float | Unset = UNSET,
    score_max: float | Unset = UNSET,
    grade: str | Unset = UNSET,

) -> Response[QaJobPageResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ List QA jobs for an environment

     Each row carries a null result payload to keep responses small; fetch a single job to retrieve its
    full inline result.

    Args:
        environment_id (UUID): Stable environment identifier (UUID).
        limit (int | Unset): Maximum number of items to return in the page (1-100). Default: 10.
            Example: 20.
        cursor (str | Unset): Opaque cursor returned by a previous page response. Omit to fetch
            the first page.
        sort_by (str | Unset): Field to sort by. Allowed values depend on the entity being listed.
        sort_direction (ListJobsForEnvironmentSortDirection | Unset): Sort direction. Defaults to
            ascending when omitted.
        search (str | Unset): Free-text filter applied to the entity searchable fields.
        batch_id (UUID | Unset): Stable QA-batch identifier (UUID). Groups QA jobs that should be
            evaluated together.
        problem_id (UUID | Unset): Stable problem identifier (UUID).
        problem_search (str | Unset):
        problem_version_id (UUID | Unset): Stable problem-version identifier (UUID). Each problem
            can have many versions; this points at one specific version.
        status (str | Unset):
        qa_config_id (str | Unset):
        kind (str | Unset):
        score_min (float | Unset):
        score_max (float | Unset):
        grade (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[QaJobPageResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        environment_id=environment_id,
limit=limit,
cursor=cursor,
sort_by=sort_by,
sort_direction=sort_direction,
search=search,
batch_id=batch_id,
problem_id=problem_id,
problem_search=problem_search,
problem_version_id=problem_version_id,
status=status,
qa_config_id=qa_config_id,
kind=kind,
score_min=score_min,
score_max=score_max,
grade=grade,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    environment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    sort_direction: ListJobsForEnvironmentSortDirection | Unset = UNSET,
    search: str | Unset = UNSET,
    batch_id: UUID | Unset = UNSET,
    problem_id: UUID | Unset = UNSET,
    problem_search: str | Unset = UNSET,
    problem_version_id: UUID | Unset = UNSET,
    status: str | Unset = UNSET,
    qa_config_id: str | Unset = UNSET,
    kind: str | Unset = UNSET,
    score_min: float | Unset = UNSET,
    score_max: float | Unset = UNSET,
    grade: str | Unset = UNSET,

) -> QaJobPageResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ List QA jobs for an environment

     Each row carries a null result payload to keep responses small; fetch a single job to retrieve its
    full inline result.

    Args:
        environment_id (UUID): Stable environment identifier (UUID).
        limit (int | Unset): Maximum number of items to return in the page (1-100). Default: 10.
            Example: 20.
        cursor (str | Unset): Opaque cursor returned by a previous page response. Omit to fetch
            the first page.
        sort_by (str | Unset): Field to sort by. Allowed values depend on the entity being listed.
        sort_direction (ListJobsForEnvironmentSortDirection | Unset): Sort direction. Defaults to
            ascending when omitted.
        search (str | Unset): Free-text filter applied to the entity searchable fields.
        batch_id (UUID | Unset): Stable QA-batch identifier (UUID). Groups QA jobs that should be
            evaluated together.
        problem_id (UUID | Unset): Stable problem identifier (UUID).
        problem_search (str | Unset):
        problem_version_id (UUID | Unset): Stable problem-version identifier (UUID). Each problem
            can have many versions; this points at one specific version.
        status (str | Unset):
        qa_config_id (str | Unset):
        kind (str | Unset):
        score_min (float | Unset):
        score_max (float | Unset):
        grade (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        QaJobPageResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return sync_detailed(
        environment_id=environment_id,
client=client,
limit=limit,
cursor=cursor,
sort_by=sort_by,
sort_direction=sort_direction,
search=search,
batch_id=batch_id,
problem_id=problem_id,
problem_search=problem_search,
problem_version_id=problem_version_id,
status=status,
qa_config_id=qa_config_id,
kind=kind,
score_min=score_min,
score_max=score_max,
grade=grade,

    ).parsed

async def asyncio_detailed(
    environment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    sort_direction: ListJobsForEnvironmentSortDirection | Unset = UNSET,
    search: str | Unset = UNSET,
    batch_id: UUID | Unset = UNSET,
    problem_id: UUID | Unset = UNSET,
    problem_search: str | Unset = UNSET,
    problem_version_id: UUID | Unset = UNSET,
    status: str | Unset = UNSET,
    qa_config_id: str | Unset = UNSET,
    kind: str | Unset = UNSET,
    score_min: float | Unset = UNSET,
    score_max: float | Unset = UNSET,
    grade: str | Unset = UNSET,

) -> Response[QaJobPageResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ List QA jobs for an environment

     Each row carries a null result payload to keep responses small; fetch a single job to retrieve its
    full inline result.

    Args:
        environment_id (UUID): Stable environment identifier (UUID).
        limit (int | Unset): Maximum number of items to return in the page (1-100). Default: 10.
            Example: 20.
        cursor (str | Unset): Opaque cursor returned by a previous page response. Omit to fetch
            the first page.
        sort_by (str | Unset): Field to sort by. Allowed values depend on the entity being listed.
        sort_direction (ListJobsForEnvironmentSortDirection | Unset): Sort direction. Defaults to
            ascending when omitted.
        search (str | Unset): Free-text filter applied to the entity searchable fields.
        batch_id (UUID | Unset): Stable QA-batch identifier (UUID). Groups QA jobs that should be
            evaluated together.
        problem_id (UUID | Unset): Stable problem identifier (UUID).
        problem_search (str | Unset):
        problem_version_id (UUID | Unset): Stable problem-version identifier (UUID). Each problem
            can have many versions; this points at one specific version.
        status (str | Unset):
        qa_config_id (str | Unset):
        kind (str | Unset):
        score_min (float | Unset):
        score_max (float | Unset):
        grade (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[QaJobPageResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        environment_id=environment_id,
limit=limit,
cursor=cursor,
sort_by=sort_by,
sort_direction=sort_direction,
search=search,
batch_id=batch_id,
problem_id=problem_id,
problem_search=problem_search,
problem_version_id=problem_version_id,
status=status,
qa_config_id=qa_config_id,
kind=kind,
score_min=score_min,
score_max=score_max,
grade=grade,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    environment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    sort_direction: ListJobsForEnvironmentSortDirection | Unset = UNSET,
    search: str | Unset = UNSET,
    batch_id: UUID | Unset = UNSET,
    problem_id: UUID | Unset = UNSET,
    problem_search: str | Unset = UNSET,
    problem_version_id: UUID | Unset = UNSET,
    status: str | Unset = UNSET,
    qa_config_id: str | Unset = UNSET,
    kind: str | Unset = UNSET,
    score_min: float | Unset = UNSET,
    score_max: float | Unset = UNSET,
    grade: str | Unset = UNSET,

) -> QaJobPageResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ List QA jobs for an environment

     Each row carries a null result payload to keep responses small; fetch a single job to retrieve its
    full inline result.

    Args:
        environment_id (UUID): Stable environment identifier (UUID).
        limit (int | Unset): Maximum number of items to return in the page (1-100). Default: 10.
            Example: 20.
        cursor (str | Unset): Opaque cursor returned by a previous page response. Omit to fetch
            the first page.
        sort_by (str | Unset): Field to sort by. Allowed values depend on the entity being listed.
        sort_direction (ListJobsForEnvironmentSortDirection | Unset): Sort direction. Defaults to
            ascending when omitted.
        search (str | Unset): Free-text filter applied to the entity searchable fields.
        batch_id (UUID | Unset): Stable QA-batch identifier (UUID). Groups QA jobs that should be
            evaluated together.
        problem_id (UUID | Unset): Stable problem identifier (UUID).
        problem_search (str | Unset):
        problem_version_id (UUID | Unset): Stable problem-version identifier (UUID). Each problem
            can have many versions; this points at one specific version.
        status (str | Unset):
        qa_config_id (str | Unset):
        kind (str | Unset):
        score_min (float | Unset):
        score_max (float | Unset):
        grade (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        QaJobPageResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return (await asyncio_detailed(
        environment_id=environment_id,
client=client,
limit=limit,
cursor=cursor,
sort_by=sort_by,
sort_direction=sort_direction,
search=search,
batch_id=batch_id,
problem_id=problem_id,
problem_search=problem_search,
problem_version_id=problem_version_id,
status=status,
qa_config_id=qa_config_id,
kind=kind,
score_min=score_min,
score_max=score_max,
grade=grade,

    )).parsed
