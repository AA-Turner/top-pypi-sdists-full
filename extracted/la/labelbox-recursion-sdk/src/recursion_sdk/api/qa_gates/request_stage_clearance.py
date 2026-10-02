from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.stage_clearance_request_body_dto_type_0 import StageClearanceRequestBodyDtoType0
from ...models.stage_clearance_request_body_dto_type_1 import StageClearanceRequestBodyDtoType1
from ...models.stage_clearance_response_dto import StageClearanceResponseDto
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
    environment_id: UUID,
    problem_version_id: UUID,
    *,
    body: StageClearanceRequestBodyDtoType0 | StageClearanceRequestBodyDtoType1,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/environments/{environment_id}/versions/{problem_version_id}/stage-clearance".format(environment_id=quote(str(environment_id), safe=""),problem_version_id=quote(str(problem_version_id), safe=""),),
    }

    
    if isinstance(body, StageClearanceRequestBodyDtoType0):
        _kwargs["json"] = body.to_dict()
    else:
        _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> StageClearanceResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    if response.status_code == 200:
        response_200 = StageClearanceResponseDto.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[StageClearanceResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    environment_id: UUID,
    problem_version_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: StageClearanceRequestBodyDtoType0 | StageClearanceRequestBodyDtoType1,

) -> Response[StageClearanceResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Request stage clearance by checking QA gates (with optional override)

     Evaluates every applicable gate for the requested stage transition and returns the clearance status
    with per-gate results. An override request lets authorised callers bypass a failing gate, recording
    the justification.

    Args:
        environment_id (UUID): Stable environment identifier (UUID).
        problem_version_id (UUID): Stable problem-version identifier (UUID). Each problem can have
            many versions; this points at one specific version.
        body (StageClearanceRequestBodyDtoType0 | StageClearanceRequestBodyDtoType1): Request body
            for clearing a QA-gated workflow stage, either via passing gates or via explicit override.
            Example: {'stage': 'submitting'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[StageClearanceResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        environment_id=environment_id,
problem_version_id=problem_version_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    environment_id: UUID,
    problem_version_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: StageClearanceRequestBodyDtoType0 | StageClearanceRequestBodyDtoType1,

) -> StageClearanceResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Request stage clearance by checking QA gates (with optional override)

     Evaluates every applicable gate for the requested stage transition and returns the clearance status
    with per-gate results. An override request lets authorised callers bypass a failing gate, recording
    the justification.

    Args:
        environment_id (UUID): Stable environment identifier (UUID).
        problem_version_id (UUID): Stable problem-version identifier (UUID). Each problem can have
            many versions; this points at one specific version.
        body (StageClearanceRequestBodyDtoType0 | StageClearanceRequestBodyDtoType1): Request body
            for clearing a QA-gated workflow stage, either via passing gates or via explicit override.
            Example: {'stage': 'submitting'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        StageClearanceResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return sync_detailed(
        environment_id=environment_id,
problem_version_id=problem_version_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    environment_id: UUID,
    problem_version_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: StageClearanceRequestBodyDtoType0 | StageClearanceRequestBodyDtoType1,

) -> Response[StageClearanceResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Request stage clearance by checking QA gates (with optional override)

     Evaluates every applicable gate for the requested stage transition and returns the clearance status
    with per-gate results. An override request lets authorised callers bypass a failing gate, recording
    the justification.

    Args:
        environment_id (UUID): Stable environment identifier (UUID).
        problem_version_id (UUID): Stable problem-version identifier (UUID). Each problem can have
            many versions; this points at one specific version.
        body (StageClearanceRequestBodyDtoType0 | StageClearanceRequestBodyDtoType1): Request body
            for clearing a QA-gated workflow stage, either via passing gates or via explicit override.
            Example: {'stage': 'submitting'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[StageClearanceResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        environment_id=environment_id,
problem_version_id=problem_version_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    environment_id: UUID,
    problem_version_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: StageClearanceRequestBodyDtoType0 | StageClearanceRequestBodyDtoType1,

) -> StageClearanceResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Request stage clearance by checking QA gates (with optional override)

     Evaluates every applicable gate for the requested stage transition and returns the clearance status
    with per-gate results. An override request lets authorised callers bypass a failing gate, recording
    the justification.

    Args:
        environment_id (UUID): Stable environment identifier (UUID).
        problem_version_id (UUID): Stable problem-version identifier (UUID). Each problem can have
            many versions; this points at one specific version.
        body (StageClearanceRequestBodyDtoType0 | StageClearanceRequestBodyDtoType1): Request body
            for clearing a QA-gated workflow stage, either via passing gates or via explicit override.
            Example: {'stage': 'submitting'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        StageClearanceResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return (await asyncio_detailed(
        environment_id=environment_id,
problem_version_id=problem_version_id,
client=client,
body=body,

    )).parsed
