from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.api_error_status_409 import ApiErrorStatus409
from ...models.regrade_problem_run_response_dto import RegradeProblemRunResponseDto
from ...models.target_api_error_forbidden import TargetApiErrorForbidden
from ...models.target_api_error_internal_error import TargetApiErrorInternalError
from ...models.target_api_error_invalid_request import TargetApiErrorInvalidRequest
from ...models.target_api_error_invariant_violation import TargetApiErrorInvariantViolation
from ...models.target_api_error_not_found import TargetApiErrorNotFound
from ...models.target_api_error_rate_limit_exceeded import TargetApiErrorRateLimitExceeded
from ...models.target_api_error_unauthorized import TargetApiErrorUnauthorized
from typing import cast
from uuid import UUID



def _get_kwargs(
    problem_run_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/problem-runs/{problem_run_id}/regrade".format(problem_run_id=quote(str(problem_run_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ApiErrorStatus409 | RegradeProblemRunResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    if response.status_code == 201:
        response_201 = RegradeProblemRunResponseDto.from_dict(response.json())



        return response_201

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

    if response.status_code == 409:
        response_409 = ApiErrorStatus409.from_dict(response.json())



        return response_409

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ApiErrorStatus409 | RegradeProblemRunResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
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

) -> Response[ApiErrorStatus409 | RegradeProblemRunResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Re-grade an existing problem run

     Enqueues an asynchronous re-grade that reuses the existing solver run — it does not re-run the
    solver. The response returns immediately with the new job id; poll the run to observe the new grade.
    The prior grade is archived and readable via the grade-history endpoint. Cancellation or an
    infrastructure failure before a new grade is produced restores the prior grade; a completed grading
    attempt whose computed outcome is failure remains the current failed outcome. The retained solver
    workspace it grades against expires roughly 24 hours after the run, after which a re-grade fails at
    the grader.

    Args:
        problem_run_id (UUID): Stable problem-run identifier (UUID). One solver attempt at one
            problem version.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiErrorStatus409 | RegradeProblemRunResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        problem_run_id=problem_run_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    problem_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> ApiErrorStatus409 | RegradeProblemRunResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Re-grade an existing problem run

     Enqueues an asynchronous re-grade that reuses the existing solver run — it does not re-run the
    solver. The response returns immediately with the new job id; poll the run to observe the new grade.
    The prior grade is archived and readable via the grade-history endpoint. Cancellation or an
    infrastructure failure before a new grade is produced restores the prior grade; a completed grading
    attempt whose computed outcome is failure remains the current failed outcome. The retained solver
    workspace it grades against expires roughly 24 hours after the run, after which a re-grade fails at
    the grader.

    Args:
        problem_run_id (UUID): Stable problem-run identifier (UUID). One solver attempt at one
            problem version.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiErrorStatus409 | RegradeProblemRunResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return sync_detailed(
        problem_run_id=problem_run_id,
client=client,

    ).parsed

async def asyncio_detailed(
    problem_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Response[ApiErrorStatus409 | RegradeProblemRunResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Re-grade an existing problem run

     Enqueues an asynchronous re-grade that reuses the existing solver run — it does not re-run the
    solver. The response returns immediately with the new job id; poll the run to observe the new grade.
    The prior grade is archived and readable via the grade-history endpoint. Cancellation or an
    infrastructure failure before a new grade is produced restores the prior grade; a completed grading
    attempt whose computed outcome is failure remains the current failed outcome. The retained solver
    workspace it grades against expires roughly 24 hours after the run, after which a re-grade fails at
    the grader.

    Args:
        problem_run_id (UUID): Stable problem-run identifier (UUID). One solver attempt at one
            problem version.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiErrorStatus409 | RegradeProblemRunResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        problem_run_id=problem_run_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    problem_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> ApiErrorStatus409 | RegradeProblemRunResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Re-grade an existing problem run

     Enqueues an asynchronous re-grade that reuses the existing solver run — it does not re-run the
    solver. The response returns immediately with the new job id; poll the run to observe the new grade.
    The prior grade is archived and readable via the grade-history endpoint. Cancellation or an
    infrastructure failure before a new grade is produced restores the prior grade; a completed grading
    attempt whose computed outcome is failure remains the current failed outcome. The retained solver
    workspace it grades against expires roughly 24 hours after the run, after which a re-grade fails at
    the grader.

    Args:
        problem_run_id (UUID): Stable problem-run identifier (UUID). One solver attempt at one
            problem version.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiErrorStatus409 | RegradeProblemRunResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return (await asyncio_detailed(
        problem_run_id=problem_run_id,
client=client,

    )).parsed
