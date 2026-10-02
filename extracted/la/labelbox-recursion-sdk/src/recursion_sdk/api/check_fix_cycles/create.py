from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.check_fix_cycle_response_dto import CheckFixCycleResponseDto
from ...models.create_check_fix_cycle_dto import CreateCheckFixCycleDto
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
    organization_id: UUID,
    *,
    body: CreateCheckFixCycleDto,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/organizations/{organization_id}/check-fix-cycles".format(organization_id=quote(str(organization_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> CheckFixCycleResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    if response.status_code == 201:
        response_201 = CheckFixCycleResponseDto.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[CheckFixCycleResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
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
    body: CreateCheckFixCycleDto,

) -> Response[CheckFixCycleResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Start an autofix cycle: check a fork PR each wave and spawn a fix attempt on red

     Enqueues an asynchronous job; the response returns immediately with the cycle id — poll the job
    resource to observe progress.

    Args:
        organization_id (UUID): Stable organization identifier (UUID). Top-level tenant boundary.
        body (CreateCheckFixCycleDto): Create-request body for a check_fix_cycle: the problem
            under repair, the fork/commit target, the check run-config versions run each wave, the fix
            step, the submit run-config version, and the fix-attempt cap (organizationId is stamped
            from the route). Example: {'problemId': '11111111-1111-4111-8111-111111111111', 'target':
            {'kind': 'git_fork', 'forkRepo': 'acme-org/fork-repo', 'baseSha':
            '0123456789abcdef0123456789abcdef01234567', 'headSha':
            'fedcba9876543210fedcba9876543210fedcba98', 'headRef': 'submission-branch', 'problemDir':
            'problems/example-task'}, 'checkRunConfigVersionIds':
            ['11111111-1111-4111-8111-111111111111'], 'fixStep': {'kind': 'run_config',
            'runConfigVersionId': '22222222-2222-4222-8222-222222222222'}, 'submitRunConfigVersionId':
            '33333333-3333-4333-8333-333333333333', 'maxFixAttempts': 3}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CheckFixCycleResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
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
    body: CreateCheckFixCycleDto,

) -> CheckFixCycleResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Start an autofix cycle: check a fork PR each wave and spawn a fix attempt on red

     Enqueues an asynchronous job; the response returns immediately with the cycle id — poll the job
    resource to observe progress.

    Args:
        organization_id (UUID): Stable organization identifier (UUID). Top-level tenant boundary.
        body (CreateCheckFixCycleDto): Create-request body for a check_fix_cycle: the problem
            under repair, the fork/commit target, the check run-config versions run each wave, the fix
            step, the submit run-config version, and the fix-attempt cap (organizationId is stamped
            from the route). Example: {'problemId': '11111111-1111-4111-8111-111111111111', 'target':
            {'kind': 'git_fork', 'forkRepo': 'acme-org/fork-repo', 'baseSha':
            '0123456789abcdef0123456789abcdef01234567', 'headSha':
            'fedcba9876543210fedcba9876543210fedcba98', 'headRef': 'submission-branch', 'problemDir':
            'problems/example-task'}, 'checkRunConfigVersionIds':
            ['11111111-1111-4111-8111-111111111111'], 'fixStep': {'kind': 'run_config',
            'runConfigVersionId': '22222222-2222-4222-8222-222222222222'}, 'submitRunConfigVersionId':
            '33333333-3333-4333-8333-333333333333', 'maxFixAttempts': 3}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CheckFixCycleResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
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
    body: CreateCheckFixCycleDto,

) -> Response[CheckFixCycleResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Start an autofix cycle: check a fork PR each wave and spawn a fix attempt on red

     Enqueues an asynchronous job; the response returns immediately with the cycle id — poll the job
    resource to observe progress.

    Args:
        organization_id (UUID): Stable organization identifier (UUID). Top-level tenant boundary.
        body (CreateCheckFixCycleDto): Create-request body for a check_fix_cycle: the problem
            under repair, the fork/commit target, the check run-config versions run each wave, the fix
            step, the submit run-config version, and the fix-attempt cap (organizationId is stamped
            from the route). Example: {'problemId': '11111111-1111-4111-8111-111111111111', 'target':
            {'kind': 'git_fork', 'forkRepo': 'acme-org/fork-repo', 'baseSha':
            '0123456789abcdef0123456789abcdef01234567', 'headSha':
            'fedcba9876543210fedcba9876543210fedcba98', 'headRef': 'submission-branch', 'problemDir':
            'problems/example-task'}, 'checkRunConfigVersionIds':
            ['11111111-1111-4111-8111-111111111111'], 'fixStep': {'kind': 'run_config',
            'runConfigVersionId': '22222222-2222-4222-8222-222222222222'}, 'submitRunConfigVersionId':
            '33333333-3333-4333-8333-333333333333', 'maxFixAttempts': 3}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CheckFixCycleResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
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
    body: CreateCheckFixCycleDto,

) -> CheckFixCycleResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Start an autofix cycle: check a fork PR each wave and spawn a fix attempt on red

     Enqueues an asynchronous job; the response returns immediately with the cycle id — poll the job
    resource to observe progress.

    Args:
        organization_id (UUID): Stable organization identifier (UUID). Top-level tenant boundary.
        body (CreateCheckFixCycleDto): Create-request body for a check_fix_cycle: the problem
            under repair, the fork/commit target, the check run-config versions run each wave, the fix
            step, the submit run-config version, and the fix-attempt cap (organizationId is stamped
            from the route). Example: {'problemId': '11111111-1111-4111-8111-111111111111', 'target':
            {'kind': 'git_fork', 'forkRepo': 'acme-org/fork-repo', 'baseSha':
            '0123456789abcdef0123456789abcdef01234567', 'headSha':
            'fedcba9876543210fedcba9876543210fedcba98', 'headRef': 'submission-branch', 'problemDir':
            'problems/example-task'}, 'checkRunConfigVersionIds':
            ['11111111-1111-4111-8111-111111111111'], 'fixStep': {'kind': 'run_config',
            'runConfigVersionId': '22222222-2222-4222-8222-222222222222'}, 'submitRunConfigVersionId':
            '33333333-3333-4333-8333-333333333333', 'maxFixAttempts': 3}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CheckFixCycleResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return (await asyncio_detailed(
        organization_id=organization_id,
client=client,
body=body,

    )).parsed
