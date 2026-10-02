from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_tuning_run_dto import CreateTuningRunDto
from ...models.target_api_error_forbidden import TargetApiErrorForbidden
from ...models.target_api_error_internal_error import TargetApiErrorInternalError
from ...models.target_api_error_invalid_request import TargetApiErrorInvalidRequest
from ...models.target_api_error_invariant_violation import TargetApiErrorInvariantViolation
from ...models.target_api_error_not_found import TargetApiErrorNotFound
from ...models.target_api_error_rate_limit_exceeded import TargetApiErrorRateLimitExceeded
from ...models.target_api_error_unauthorized import TargetApiErrorUnauthorized
from ...models.tuning_run_response_dto import TuningRunResponseDto
from typing import cast
from uuid import UUID



def _get_kwargs(
    organization_id: UUID,
    *,
    body: CreateTuningRunDto,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/organizations/{organization_id}/tuning-runs".format(organization_id=quote(str(organization_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | TuningRunResponseDto | None:
    if response.status_code == 201:
        response_201 = TuningRunResponseDto.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | TuningRunResponseDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    organization_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: CreateTuningRunDto,

) -> Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | TuningRunResponseDto]:
    """ Start a tuning session: train a run-config, evaluate checkpoints on a cadence

     Enqueues an asynchronous jobs_v2 row; the response returns immediately with the run id — poll the
    job resource to observe progress.

    Args:
        organization_id (UUID): Stable organization identifier (UUID). Top-level tenant boundary.
        body (CreateTuningRunDto): Create-request body for a tuning session: trainer run-config,
            per-checkpoint eval template, training problem set, cadence, and eval-concurrency cap
            (organizationId is stamped from the route). Example: {'runName': 'llama-grpo-session',
            'trainerRunConfigVersionId': '11111111-1111-4111-8111-111111111111', 'trainerConfig': {},
            'evalTemplate': {'environmentId': '11111111-1111-4111-8111-111111111111',
            'solverRunConfigVersionId': '11111111-1111-4111-8111-111111111111',
            'graderRunConfigVersionId': '11111111-1111-4111-8111-111111111111', 'problems':
            [{'problemId': '11111111-1111-4111-8111-111111111111', 'problemVersionId':
            '11111111-1111-4111-8111-111111111111', 'environmentId':
            '11111111-1111-4111-8111-111111111111'}]}, 'trainingTemplate': {'environmentId':
            '11111111-1111-4111-8111-111111111111', 'problems': [{'problemId':
            '11111111-1111-4111-8111-111111111111', 'problemVersionId':
            '11111111-1111-4111-8111-111111111111', 'environmentId':
            '11111111-1111-4111-8111-111111111111'}]}, 'cadence': {'type': 'every_n_steps', 'n': 5},
            'evalConcurrencyCap': 4}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | TuningRunResponseDto]
     """


    kwargs = _get_kwargs(
        organization_id=organization_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    organization_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: CreateTuningRunDto,

) -> TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | TuningRunResponseDto | None:
    """ Start a tuning session: train a run-config, evaluate checkpoints on a cadence

     Enqueues an asynchronous jobs_v2 row; the response returns immediately with the run id — poll the
    job resource to observe progress.

    Args:
        organization_id (UUID): Stable organization identifier (UUID). Top-level tenant boundary.
        body (CreateTuningRunDto): Create-request body for a tuning session: trainer run-config,
            per-checkpoint eval template, training problem set, cadence, and eval-concurrency cap
            (organizationId is stamped from the route). Example: {'runName': 'llama-grpo-session',
            'trainerRunConfigVersionId': '11111111-1111-4111-8111-111111111111', 'trainerConfig': {},
            'evalTemplate': {'environmentId': '11111111-1111-4111-8111-111111111111',
            'solverRunConfigVersionId': '11111111-1111-4111-8111-111111111111',
            'graderRunConfigVersionId': '11111111-1111-4111-8111-111111111111', 'problems':
            [{'problemId': '11111111-1111-4111-8111-111111111111', 'problemVersionId':
            '11111111-1111-4111-8111-111111111111', 'environmentId':
            '11111111-1111-4111-8111-111111111111'}]}, 'trainingTemplate': {'environmentId':
            '11111111-1111-4111-8111-111111111111', 'problems': [{'problemId':
            '11111111-1111-4111-8111-111111111111', 'problemVersionId':
            '11111111-1111-4111-8111-111111111111', 'environmentId':
            '11111111-1111-4111-8111-111111111111'}]}, 'cadence': {'type': 'every_n_steps', 'n': 5},
            'evalConcurrencyCap': 4}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | TuningRunResponseDto
     """


    return sync_detailed(
        organization_id=organization_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    organization_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: CreateTuningRunDto,

) -> Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | TuningRunResponseDto]:
    """ Start a tuning session: train a run-config, evaluate checkpoints on a cadence

     Enqueues an asynchronous jobs_v2 row; the response returns immediately with the run id — poll the
    job resource to observe progress.

    Args:
        organization_id (UUID): Stable organization identifier (UUID). Top-level tenant boundary.
        body (CreateTuningRunDto): Create-request body for a tuning session: trainer run-config,
            per-checkpoint eval template, training problem set, cadence, and eval-concurrency cap
            (organizationId is stamped from the route). Example: {'runName': 'llama-grpo-session',
            'trainerRunConfigVersionId': '11111111-1111-4111-8111-111111111111', 'trainerConfig': {},
            'evalTemplate': {'environmentId': '11111111-1111-4111-8111-111111111111',
            'solverRunConfigVersionId': '11111111-1111-4111-8111-111111111111',
            'graderRunConfigVersionId': '11111111-1111-4111-8111-111111111111', 'problems':
            [{'problemId': '11111111-1111-4111-8111-111111111111', 'problemVersionId':
            '11111111-1111-4111-8111-111111111111', 'environmentId':
            '11111111-1111-4111-8111-111111111111'}]}, 'trainingTemplate': {'environmentId':
            '11111111-1111-4111-8111-111111111111', 'problems': [{'problemId':
            '11111111-1111-4111-8111-111111111111', 'problemVersionId':
            '11111111-1111-4111-8111-111111111111', 'environmentId':
            '11111111-1111-4111-8111-111111111111'}]}, 'cadence': {'type': 'every_n_steps', 'n': 5},
            'evalConcurrencyCap': 4}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | TuningRunResponseDto]
     """


    kwargs = _get_kwargs(
        organization_id=organization_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    organization_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: CreateTuningRunDto,

) -> TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | TuningRunResponseDto | None:
    """ Start a tuning session: train a run-config, evaluate checkpoints on a cadence

     Enqueues an asynchronous jobs_v2 row; the response returns immediately with the run id — poll the
    job resource to observe progress.

    Args:
        organization_id (UUID): Stable organization identifier (UUID). Top-level tenant boundary.
        body (CreateTuningRunDto): Create-request body for a tuning session: trainer run-config,
            per-checkpoint eval template, training problem set, cadence, and eval-concurrency cap
            (organizationId is stamped from the route). Example: {'runName': 'llama-grpo-session',
            'trainerRunConfigVersionId': '11111111-1111-4111-8111-111111111111', 'trainerConfig': {},
            'evalTemplate': {'environmentId': '11111111-1111-4111-8111-111111111111',
            'solverRunConfigVersionId': '11111111-1111-4111-8111-111111111111',
            'graderRunConfigVersionId': '11111111-1111-4111-8111-111111111111', 'problems':
            [{'problemId': '11111111-1111-4111-8111-111111111111', 'problemVersionId':
            '11111111-1111-4111-8111-111111111111', 'environmentId':
            '11111111-1111-4111-8111-111111111111'}]}, 'trainingTemplate': {'environmentId':
            '11111111-1111-4111-8111-111111111111', 'problems': [{'problemId':
            '11111111-1111-4111-8111-111111111111', 'problemVersionId':
            '11111111-1111-4111-8111-111111111111', 'environmentId':
            '11111111-1111-4111-8111-111111111111'}]}, 'cadence': {'type': 'every_n_steps', 'n': 5},
            'evalConcurrencyCap': 4}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | TuningRunResponseDto
     """


    return (await asyncio_detailed(
        organization_id=organization_id,
client=client,
body=body,

    )).parsed
