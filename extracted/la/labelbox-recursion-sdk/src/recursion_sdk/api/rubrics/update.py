from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.api_error_status_409 import ApiErrorStatus409
from ...models.rubric_dto import RubricDto
from ...models.target_api_error_forbidden import TargetApiErrorForbidden
from ...models.target_api_error_internal_error import TargetApiErrorInternalError
from ...models.target_api_error_invalid_request import TargetApiErrorInvalidRequest
from ...models.target_api_error_invariant_violation import TargetApiErrorInvariantViolation
from ...models.target_api_error_not_found import TargetApiErrorNotFound
from ...models.target_api_error_rate_limit_exceeded import TargetApiErrorRateLimitExceeded
from ...models.target_api_error_unauthorized import TargetApiErrorUnauthorized
from ...models.update_rubric_body_dto import UpdateRubricBodyDto
from typing import cast
from uuid import UUID



def _get_kwargs(
    problem_version_id: UUID,
    rubric_id: UUID,
    *,
    body: UpdateRubricBodyDto,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/v1/versions/{problem_version_id}/rubrics/{rubric_id}".format(problem_version_id=quote(str(problem_version_id), safe=""),rubric_id=quote(str(rubric_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ApiErrorStatus409 | RubricDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    if response.status_code == 200:
        response_200 = RubricDto.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ApiErrorStatus409 | RubricDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    problem_version_id: UUID,
    rubric_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateRubricBodyDto,

) -> Response[ApiErrorStatus409 | RubricDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Update a rubric

     Honors environment-level field permission overrides. Rejects template problems.

    Args:
        problem_version_id (UUID): Stable problem-version identifier (UUID). Each problem can have
            many versions; this points at one specific version.
        rubric_id (UUID): Stable rubric identifier (UUID). Rubrics are versioned grading
            specifications attached to a problem version.
        body (UpdateRubricBodyDto): Request body for partially updating an existing rubric.
            Example: {'criterion': 'Correctly identifies all surface defects and reports none that are
            absent', 'weight': 3, 'useGraderSupport': True}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiErrorStatus409 | RubricDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        problem_version_id=problem_version_id,
rubric_id=rubric_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    problem_version_id: UUID,
    rubric_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateRubricBodyDto,

) -> ApiErrorStatus409 | RubricDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Update a rubric

     Honors environment-level field permission overrides. Rejects template problems.

    Args:
        problem_version_id (UUID): Stable problem-version identifier (UUID). Each problem can have
            many versions; this points at one specific version.
        rubric_id (UUID): Stable rubric identifier (UUID). Rubrics are versioned grading
            specifications attached to a problem version.
        body (UpdateRubricBodyDto): Request body for partially updating an existing rubric.
            Example: {'criterion': 'Correctly identifies all surface defects and reports none that are
            absent', 'weight': 3, 'useGraderSupport': True}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiErrorStatus409 | RubricDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return sync_detailed(
        problem_version_id=problem_version_id,
rubric_id=rubric_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    problem_version_id: UUID,
    rubric_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateRubricBodyDto,

) -> Response[ApiErrorStatus409 | RubricDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Update a rubric

     Honors environment-level field permission overrides. Rejects template problems.

    Args:
        problem_version_id (UUID): Stable problem-version identifier (UUID). Each problem can have
            many versions; this points at one specific version.
        rubric_id (UUID): Stable rubric identifier (UUID). Rubrics are versioned grading
            specifications attached to a problem version.
        body (UpdateRubricBodyDto): Request body for partially updating an existing rubric.
            Example: {'criterion': 'Correctly identifies all surface defects and reports none that are
            absent', 'weight': 3, 'useGraderSupport': True}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiErrorStatus409 | RubricDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        problem_version_id=problem_version_id,
rubric_id=rubric_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    problem_version_id: UUID,
    rubric_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateRubricBodyDto,

) -> ApiErrorStatus409 | RubricDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Update a rubric

     Honors environment-level field permission overrides. Rejects template problems.

    Args:
        problem_version_id (UUID): Stable problem-version identifier (UUID). Each problem can have
            many versions; this points at one specific version.
        rubric_id (UUID): Stable rubric identifier (UUID). Rubrics are versioned grading
            specifications attached to a problem version.
        body (UpdateRubricBodyDto): Request body for partially updating an existing rubric.
            Example: {'criterion': 'Correctly identifies all surface defects and reports none that are
            absent', 'weight': 3, 'useGraderSupport': True}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiErrorStatus409 | RubricDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return (await asyncio_detailed(
        problem_version_id=problem_version_id,
rubric_id=rubric_id,
client=client,
body=body,

    )).parsed
