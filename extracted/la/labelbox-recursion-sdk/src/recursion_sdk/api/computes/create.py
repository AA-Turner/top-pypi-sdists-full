from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.api_error_status_502 import ApiErrorStatus502
from ...models.compute_active_lease_limit_reached_body_dto import ComputeActiveLeaseLimitReachedBodyDto
from ...models.compute_already_active_body_dto import ComputeAlreadyActiveBodyDto
from ...models.compute_creation_in_progress_body_dto import ComputeCreationInProgressBodyDto
from ...models.compute_result_dto import ComputeResultDto
from ...models.create_compute_request_dto import CreateComputeRequestDto
from ...models.target_api_error_forbidden import TargetApiErrorForbidden
from ...models.target_api_error_internal_error import TargetApiErrorInternalError
from ...models.target_api_error_invalid_request import TargetApiErrorInvalidRequest
from ...models.target_api_error_invariant_violation import TargetApiErrorInvariantViolation
from ...models.target_api_error_not_found import TargetApiErrorNotFound
from ...models.target_api_error_rate_limit_exceeded import TargetApiErrorRateLimitExceeded
from ...models.target_api_error_unauthorized import TargetApiErrorUnauthorized
from typing import cast



def _get_kwargs(
    *,
    body: CreateComputeRequestDto,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/computes",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ApiErrorStatus502 | ComputeActiveLeaseLimitReachedBodyDto | ComputeAlreadyActiveBodyDto | ComputeCreationInProgressBodyDto | ComputeResultDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    if response.status_code == 201:
        response_201 = ComputeResultDto.from_dict(response.json())



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
        def _parse_response_409(data: object) -> ComputeActiveLeaseLimitReachedBodyDto | ComputeAlreadyActiveBodyDto | ComputeCreationInProgressBodyDto:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_compute_create_conflict_response_dto_type_0 = ComputeAlreadyActiveBodyDto.from_dict(data)



                return componentsschemas_compute_create_conflict_response_dto_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_compute_create_conflict_response_dto_type_1 = ComputeCreationInProgressBodyDto.from_dict(data)



                return componentsschemas_compute_create_conflict_response_dto_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_compute_create_conflict_response_dto_type_2 = ComputeActiveLeaseLimitReachedBodyDto.from_dict(data)



            return componentsschemas_compute_create_conflict_response_dto_type_2

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

    if response.status_code == 502:
        response_502 = ApiErrorStatus502.from_dict(response.json())



        return response_502

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ApiErrorStatus502 | ComputeActiveLeaseLimitReachedBodyDto | ComputeAlreadyActiveBodyDto | ComputeCreationInProgressBodyDto | ComputeResultDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: CreateComputeRequestDto,

) -> Response[ApiErrorStatus502 | ComputeActiveLeaseLimitReachedBodyDto | ComputeAlreadyActiveBodyDto | ComputeCreationInProgressBodyDto | ComputeResultDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Create (spin up) a persistent compute reserved for the caller

     Provisions a long-lived compute sandbox reserved for the calling user. The caller may hold at most
    one active leased compute across environments, and no compute may be created in an environment where
    the caller already has any active compute reservation.

    Args:
        body (CreateComputeRequestDto): Request body for launching a new compute (container pod)
            inside an environment. Example: {'environmentId': '784e2386-e297-4f9d-a886-838422383b65',
            'name': 'vision-agent-dev', 'containerImage': 'us-docker.pkg.dev/example-
            project/recursion-agents/vision-agent:1.4.2', 'cpuMilli': 2000, 'memoryMib': 4096,
            'timeoutSeconds': 3600, 'idleStopAfterSeconds': 14400, 'stoppedDeleteAfterSeconds':
            604800, 'pvcSizeGi': 20, 'httpPort': 8080, 'env': {'MODEL_PROVIDER': 'anthropic',
            'LOG_LEVEL': 'info'}, 'runConfigVersionId': '39088cb6-ca62-4544-a074-fc66e10807ad'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiErrorStatus502 | ComputeActiveLeaseLimitReachedBodyDto | ComputeAlreadyActiveBodyDto | ComputeCreationInProgressBodyDto | ComputeResultDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
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
    body: CreateComputeRequestDto,

) -> ApiErrorStatus502 | ComputeActiveLeaseLimitReachedBodyDto | ComputeAlreadyActiveBodyDto | ComputeCreationInProgressBodyDto | ComputeResultDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Create (spin up) a persistent compute reserved for the caller

     Provisions a long-lived compute sandbox reserved for the calling user. The caller may hold at most
    one active leased compute across environments, and no compute may be created in an environment where
    the caller already has any active compute reservation.

    Args:
        body (CreateComputeRequestDto): Request body for launching a new compute (container pod)
            inside an environment. Example: {'environmentId': '784e2386-e297-4f9d-a886-838422383b65',
            'name': 'vision-agent-dev', 'containerImage': 'us-docker.pkg.dev/example-
            project/recursion-agents/vision-agent:1.4.2', 'cpuMilli': 2000, 'memoryMib': 4096,
            'timeoutSeconds': 3600, 'idleStopAfterSeconds': 14400, 'stoppedDeleteAfterSeconds':
            604800, 'pvcSizeGi': 20, 'httpPort': 8080, 'env': {'MODEL_PROVIDER': 'anthropic',
            'LOG_LEVEL': 'info'}, 'runConfigVersionId': '39088cb6-ca62-4544-a074-fc66e10807ad'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiErrorStatus502 | ComputeActiveLeaseLimitReachedBodyDto | ComputeAlreadyActiveBodyDto | ComputeCreationInProgressBodyDto | ComputeResultDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: CreateComputeRequestDto,

) -> Response[ApiErrorStatus502 | ComputeActiveLeaseLimitReachedBodyDto | ComputeAlreadyActiveBodyDto | ComputeCreationInProgressBodyDto | ComputeResultDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Create (spin up) a persistent compute reserved for the caller

     Provisions a long-lived compute sandbox reserved for the calling user. The caller may hold at most
    one active leased compute across environments, and no compute may be created in an environment where
    the caller already has any active compute reservation.

    Args:
        body (CreateComputeRequestDto): Request body for launching a new compute (container pod)
            inside an environment. Example: {'environmentId': '784e2386-e297-4f9d-a886-838422383b65',
            'name': 'vision-agent-dev', 'containerImage': 'us-docker.pkg.dev/example-
            project/recursion-agents/vision-agent:1.4.2', 'cpuMilli': 2000, 'memoryMib': 4096,
            'timeoutSeconds': 3600, 'idleStopAfterSeconds': 14400, 'stoppedDeleteAfterSeconds':
            604800, 'pvcSizeGi': 20, 'httpPort': 8080, 'env': {'MODEL_PROVIDER': 'anthropic',
            'LOG_LEVEL': 'info'}, 'runConfigVersionId': '39088cb6-ca62-4544-a074-fc66e10807ad'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiErrorStatus502 | ComputeActiveLeaseLimitReachedBodyDto | ComputeAlreadyActiveBodyDto | ComputeCreationInProgressBodyDto | ComputeResultDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
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
    body: CreateComputeRequestDto,

) -> ApiErrorStatus502 | ComputeActiveLeaseLimitReachedBodyDto | ComputeAlreadyActiveBodyDto | ComputeCreationInProgressBodyDto | ComputeResultDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Create (spin up) a persistent compute reserved for the caller

     Provisions a long-lived compute sandbox reserved for the calling user. The caller may hold at most
    one active leased compute across environments, and no compute may be created in an environment where
    the caller already has any active compute reservation.

    Args:
        body (CreateComputeRequestDto): Request body for launching a new compute (container pod)
            inside an environment. Example: {'environmentId': '784e2386-e297-4f9d-a886-838422383b65',
            'name': 'vision-agent-dev', 'containerImage': 'us-docker.pkg.dev/example-
            project/recursion-agents/vision-agent:1.4.2', 'cpuMilli': 2000, 'memoryMib': 4096,
            'timeoutSeconds': 3600, 'idleStopAfterSeconds': 14400, 'stoppedDeleteAfterSeconds':
            604800, 'pvcSizeGi': 20, 'httpPort': 8080, 'env': {'MODEL_PROVIDER': 'anthropic',
            'LOG_LEVEL': 'info'}, 'runConfigVersionId': '39088cb6-ca62-4544-a074-fc66e10807ad'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiErrorStatus502 | ComputeActiveLeaseLimitReachedBodyDto | ComputeAlreadyActiveBodyDto | ComputeCreationInProgressBodyDto | ComputeResultDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
