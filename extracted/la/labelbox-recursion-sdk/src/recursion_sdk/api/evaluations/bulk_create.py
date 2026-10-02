from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.api_error_status_409 import ApiErrorStatus409
from ...models.create_evaluation_body_dto import CreateEvaluationBodyDto
from ...models.evaluation_detail_response_dto import EvaluationDetailResponseDto
from ...models.run_config_file_clash_error_dto import RunConfigFileClashErrorDto
from ...models.run_config_file_clash_invalid_request_error_dto import RunConfigFileClashInvalidRequestErrorDto
from ...models.target_api_error_forbidden import TargetApiErrorForbidden
from ...models.target_api_error_internal_error import TargetApiErrorInternalError
from ...models.target_api_error_invariant_violation import TargetApiErrorInvariantViolation
from ...models.target_api_error_not_found import TargetApiErrorNotFound
from ...models.target_api_error_rate_limit_exceeded import TargetApiErrorRateLimitExceeded
from ...models.target_api_error_unauthorized import TargetApiErrorUnauthorized
from typing import cast



def _get_kwargs(
    *,
    body: CreateEvaluationBodyDto,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/evaluations/bulk",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ApiErrorStatus409 | EvaluationDetailResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    if response.status_code == 201:
        response_201 = EvaluationDetailResponseDto.from_dict(response.json())



        return response_201

    if response.status_code == 400:
        def _parse_response_400(data: object) -> RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_run_config_file_clash_bad_request_dto_type_0 = RunConfigFileClashInvalidRequestErrorDto.from_dict(data)



                return componentsschemas_run_config_file_clash_bad_request_dto_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_run_config_file_clash_bad_request_dto_type_1 = RunConfigFileClashErrorDto.from_dict(data)



            return componentsschemas_run_config_file_clash_bad_request_dto_type_1

        response_400 = _parse_response_400(response.json())

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ApiErrorStatus409 | EvaluationDetailResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: CreateEvaluationBodyDto,

) -> Response[ApiErrorStatus409 | EvaluationDetailResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Bulk-create evaluations (v2)

     Creates an evaluation and spawns a jobs-v2 evaluation_run root that orchestrates all solvers and
    problems. Runs are launched asynchronously: the response returns with a pending status and zero runs
    dispatched — the job dispatcher launches the constituent runs (one per solver, problem, and attempt)
    on a later tick, so poll the evaluation or its results for progress. All referenced problem versions
    must already be locked, and all problems must belong to a single environment — multi-environment
    evaluations are rejected. Identical in behaviour to POST /evaluations.

    Args:
        body (CreateEvaluationBodyDto): Input for creating a multi-problem comparison evaluation
            across one or more solvers. Example: {'name': 'claude-sonnet-baseline', 'description':
            'Baseline run of Claude Sonnet against the surface-defect detection problem.', 'metadata':
            {'schemaVersion': 1, 'attemptsPerProblem': 3}, 'solvers': [{'displayName': 'claude-sonnet-
            baseline', 'runConfigVersionId': 'e9d0f1c2-3e4a-4b6c-8d7e-9f0a1b2c3d4e'}], 'problems':
            [{'problemId': '2d3fe029-a7d1-4747-9d09-81b976087bbb', 'problemVersionId':
            '0c3ac467-57e1-4074-b57d-b6a7be392f71', 'environmentId':
            '784e2386-e297-4f9d-a886-838422383b65'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiErrorStatus409 | EvaluationDetailResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
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
    client: AuthenticatedClient | Client,
    body: CreateEvaluationBodyDto,

) -> ApiErrorStatus409 | EvaluationDetailResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Bulk-create evaluations (v2)

     Creates an evaluation and spawns a jobs-v2 evaluation_run root that orchestrates all solvers and
    problems. Runs are launched asynchronously: the response returns with a pending status and zero runs
    dispatched — the job dispatcher launches the constituent runs (one per solver, problem, and attempt)
    on a later tick, so poll the evaluation or its results for progress. All referenced problem versions
    must already be locked, and all problems must belong to a single environment — multi-environment
    evaluations are rejected. Identical in behaviour to POST /evaluations.

    Args:
        body (CreateEvaluationBodyDto): Input for creating a multi-problem comparison evaluation
            across one or more solvers. Example: {'name': 'claude-sonnet-baseline', 'description':
            'Baseline run of Claude Sonnet against the surface-defect detection problem.', 'metadata':
            {'schemaVersion': 1, 'attemptsPerProblem': 3}, 'solvers': [{'displayName': 'claude-sonnet-
            baseline', 'runConfigVersionId': 'e9d0f1c2-3e4a-4b6c-8d7e-9f0a1b2c3d4e'}], 'problems':
            [{'problemId': '2d3fe029-a7d1-4747-9d09-81b976087bbb', 'problemVersionId':
            '0c3ac467-57e1-4074-b57d-b6a7be392f71', 'environmentId':
            '784e2386-e297-4f9d-a886-838422383b65'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiErrorStatus409 | EvaluationDetailResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: CreateEvaluationBodyDto,

) -> Response[ApiErrorStatus409 | EvaluationDetailResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Bulk-create evaluations (v2)

     Creates an evaluation and spawns a jobs-v2 evaluation_run root that orchestrates all solvers and
    problems. Runs are launched asynchronously: the response returns with a pending status and zero runs
    dispatched — the job dispatcher launches the constituent runs (one per solver, problem, and attempt)
    on a later tick, so poll the evaluation or its results for progress. All referenced problem versions
    must already be locked, and all problems must belong to a single environment — multi-environment
    evaluations are rejected. Identical in behaviour to POST /evaluations.

    Args:
        body (CreateEvaluationBodyDto): Input for creating a multi-problem comparison evaluation
            across one or more solvers. Example: {'name': 'claude-sonnet-baseline', 'description':
            'Baseline run of Claude Sonnet against the surface-defect detection problem.', 'metadata':
            {'schemaVersion': 1, 'attemptsPerProblem': 3}, 'solvers': [{'displayName': 'claude-sonnet-
            baseline', 'runConfigVersionId': 'e9d0f1c2-3e4a-4b6c-8d7e-9f0a1b2c3d4e'}], 'problems':
            [{'problemId': '2d3fe029-a7d1-4747-9d09-81b976087bbb', 'problemVersionId':
            '0c3ac467-57e1-4074-b57d-b6a7be392f71', 'environmentId':
            '784e2386-e297-4f9d-a886-838422383b65'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiErrorStatus409 | EvaluationDetailResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
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
    client: AuthenticatedClient | Client,
    body: CreateEvaluationBodyDto,

) -> ApiErrorStatus409 | EvaluationDetailResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Bulk-create evaluations (v2)

     Creates an evaluation and spawns a jobs-v2 evaluation_run root that orchestrates all solvers and
    problems. Runs are launched asynchronously: the response returns with a pending status and zero runs
    dispatched — the job dispatcher launches the constituent runs (one per solver, problem, and attempt)
    on a later tick, so poll the evaluation or its results for progress. All referenced problem versions
    must already be locked, and all problems must belong to a single environment — multi-environment
    evaluations are rejected. Identical in behaviour to POST /evaluations.

    Args:
        body (CreateEvaluationBodyDto): Input for creating a multi-problem comparison evaluation
            across one or more solvers. Example: {'name': 'claude-sonnet-baseline', 'description':
            'Baseline run of Claude Sonnet against the surface-defect detection problem.', 'metadata':
            {'schemaVersion': 1, 'attemptsPerProblem': 3}, 'solvers': [{'displayName': 'claude-sonnet-
            baseline', 'runConfigVersionId': 'e9d0f1c2-3e4a-4b6c-8d7e-9f0a1b2c3d4e'}], 'problems':
            [{'problemId': '2d3fe029-a7d1-4747-9d09-81b976087bbb', 'problemVersionId':
            '0c3ac467-57e1-4074-b57d-b6a7be392f71', 'environmentId':
            '784e2386-e297-4f9d-a886-838422383b65'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiErrorStatus409 | EvaluationDetailResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
