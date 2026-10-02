from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.form_answer_dto import FormAnswerDto
from ...models.form_problem_version_locked_error_dto import FormProblemVersionLockedErrorDto
from ...models.form_version_not_published_error_dto import FormVersionNotPublishedErrorDto
from ...models.target_api_error_forbidden import TargetApiErrorForbidden
from ...models.target_api_error_internal_error import TargetApiErrorInternalError
from ...models.target_api_error_invalid_request import TargetApiErrorInvalidRequest
from ...models.target_api_error_invariant_violation import TargetApiErrorInvariantViolation
from ...models.target_api_error_not_found import TargetApiErrorNotFound
from ...models.target_api_error_rate_limit_exceeded import TargetApiErrorRateLimitExceeded
from ...models.target_api_error_unauthorized import TargetApiErrorUnauthorized
from ...models.upsert_form_answer_body_dto import UpsertFormAnswerBodyDto
from typing import cast
from uuid import UUID



def _get_kwargs(
    problem_version_id: UUID,
    *,
    body: UpsertFormAnswerBodyDto,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/v1/problem-versions/{problem_version_id}/form-answers".format(problem_version_id=quote(str(problem_version_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> FormAnswerDto | FormProblemVersionLockedErrorDto | FormVersionNotPublishedErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    if response.status_code == 200:
        response_200 = FormAnswerDto.from_dict(response.json())



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
        def _parse_response_409(data: object) -> FormProblemVersionLockedErrorDto | FormVersionNotPublishedErrorDto:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_upsert_form_answer_conflict_response_dto_type_0 = FormVersionNotPublishedErrorDto.from_dict(data)



                return componentsschemas_upsert_form_answer_conflict_response_dto_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_upsert_form_answer_conflict_response_dto_type_1 = FormProblemVersionLockedErrorDto.from_dict(data)



            return componentsschemas_upsert_form_answer_conflict_response_dto_type_1

        response_409 = _parse_response_409(response.json())

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[FormAnswerDto | FormProblemVersionLockedErrorDto | FormVersionNotPublishedErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    problem_version_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UpsertFormAnswerBodyDto,

) -> Response[FormAnswerDto | FormProblemVersionLockedErrorDto | FormVersionNotPublishedErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Upsert answers for a problem version

     Idempotent: repeated calls overwrite the caller's previous answers in place. The form version must
    be published and the problem version must be unlocked.

    Args:
        problem_version_id (UUID): Stable problem-version identifier (UUID). Each problem can have
            many versions; this points at one specific version.
        body (UpsertFormAnswerBodyDto): Request body for creating or updating a form answer on a
            problem version. Example: {'formVersionId': '77e4ffc9-3d40-472c-b160-f163e02df324',
            'answers': {'severity': 'major', 'notes': 'Visible scratch along the top-left bezel.'}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FormAnswerDto | FormProblemVersionLockedErrorDto | FormVersionNotPublishedErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        problem_version_id=problem_version_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    problem_version_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UpsertFormAnswerBodyDto,

) -> FormAnswerDto | FormProblemVersionLockedErrorDto | FormVersionNotPublishedErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Upsert answers for a problem version

     Idempotent: repeated calls overwrite the caller's previous answers in place. The form version must
    be published and the problem version must be unlocked.

    Args:
        problem_version_id (UUID): Stable problem-version identifier (UUID). Each problem can have
            many versions; this points at one specific version.
        body (UpsertFormAnswerBodyDto): Request body for creating or updating a form answer on a
            problem version. Example: {'formVersionId': '77e4ffc9-3d40-472c-b160-f163e02df324',
            'answers': {'severity': 'major', 'notes': 'Visible scratch along the top-left bezel.'}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FormAnswerDto | FormProblemVersionLockedErrorDto | FormVersionNotPublishedErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return sync_detailed(
        problem_version_id=problem_version_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    problem_version_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UpsertFormAnswerBodyDto,

) -> Response[FormAnswerDto | FormProblemVersionLockedErrorDto | FormVersionNotPublishedErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Upsert answers for a problem version

     Idempotent: repeated calls overwrite the caller's previous answers in place. The form version must
    be published and the problem version must be unlocked.

    Args:
        problem_version_id (UUID): Stable problem-version identifier (UUID). Each problem can have
            many versions; this points at one specific version.
        body (UpsertFormAnswerBodyDto): Request body for creating or updating a form answer on a
            problem version. Example: {'formVersionId': '77e4ffc9-3d40-472c-b160-f163e02df324',
            'answers': {'severity': 'major', 'notes': 'Visible scratch along the top-left bezel.'}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FormAnswerDto | FormProblemVersionLockedErrorDto | FormVersionNotPublishedErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        problem_version_id=problem_version_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    problem_version_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UpsertFormAnswerBodyDto,

) -> FormAnswerDto | FormProblemVersionLockedErrorDto | FormVersionNotPublishedErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Upsert answers for a problem version

     Idempotent: repeated calls overwrite the caller's previous answers in place. The form version must
    be published and the problem version must be unlocked.

    Args:
        problem_version_id (UUID): Stable problem-version identifier (UUID). Each problem can have
            many versions; this points at one specific version.
        body (UpsertFormAnswerBodyDto): Request body for creating or updating a form answer on a
            problem version. Example: {'formVersionId': '77e4ffc9-3d40-472c-b160-f163e02df324',
            'answers': {'severity': 'major', 'notes': 'Visible scratch along the top-left bezel.'}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FormAnswerDto | FormProblemVersionLockedErrorDto | FormVersionNotPublishedErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return (await asyncio_detailed(
        problem_version_id=problem_version_id,
client=client,
body=body,

    )).parsed
