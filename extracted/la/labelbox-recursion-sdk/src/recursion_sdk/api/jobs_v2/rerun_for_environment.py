from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.api_error_status_409 import ApiErrorStatus409
from ...models.rerun_job_v2_response_dto import RerunJobV2ResponseDto
from ...models.run_config_file_clash_error_dto import RunConfigFileClashErrorDto
from ...models.run_config_file_clash_invalid_request_error_dto import RunConfigFileClashInvalidRequestErrorDto
from ...models.target_api_error_forbidden import TargetApiErrorForbidden
from ...models.target_api_error_internal_error import TargetApiErrorInternalError
from ...models.target_api_error_invariant_violation import TargetApiErrorInvariantViolation
from ...models.target_api_error_not_found import TargetApiErrorNotFound
from ...models.target_api_error_rate_limit_exceeded import TargetApiErrorRateLimitExceeded
from ...models.target_api_error_unauthorized import TargetApiErrorUnauthorized
from typing import cast
from uuid import UUID



def _get_kwargs(
    environment_id: UUID,
    job_v2_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/environments/{environment_id}/jobs-v2/{job_v2_id}/rerun".format(environment_id=quote(str(environment_id), safe=""),job_v2_id=quote(str(job_v2_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ApiErrorStatus409 | RerunJobV2ResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    if response.status_code == 201:
        response_201 = RerunJobV2ResponseDto.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ApiErrorStatus409 | RerunJobV2ResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    environment_id: UUID,
    job_v2_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Response[ApiErrorStatus409 | RerunJobV2ResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Re-execute a terminal jobs_v2 row as a fresh run

     Only job types that register a rerun hook support this; mints a new root job and returns its id. The
    original row is left untouched at its terminal status.

    Args:
        environment_id (UUID): Stable environment identifier (UUID).
        job_v2_id (UUID): Stable jobs_v2 identifier (UUID). One row per background-work unit in
            the generic, strategy-driven job framework.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiErrorStatus409 | RerunJobV2ResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        environment_id=environment_id,
job_v2_id=job_v2_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    environment_id: UUID,
    job_v2_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> ApiErrorStatus409 | RerunJobV2ResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Re-execute a terminal jobs_v2 row as a fresh run

     Only job types that register a rerun hook support this; mints a new root job and returns its id. The
    original row is left untouched at its terminal status.

    Args:
        environment_id (UUID): Stable environment identifier (UUID).
        job_v2_id (UUID): Stable jobs_v2 identifier (UUID). One row per background-work unit in
            the generic, strategy-driven job framework.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiErrorStatus409 | RerunJobV2ResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return sync_detailed(
        environment_id=environment_id,
job_v2_id=job_v2_id,
client=client,

    ).parsed

async def asyncio_detailed(
    environment_id: UUID,
    job_v2_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Response[ApiErrorStatus409 | RerunJobV2ResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Re-execute a terminal jobs_v2 row as a fresh run

     Only job types that register a rerun hook support this; mints a new root job and returns its id. The
    original row is left untouched at its terminal status.

    Args:
        environment_id (UUID): Stable environment identifier (UUID).
        job_v2_id (UUID): Stable jobs_v2 identifier (UUID). One row per background-work unit in
            the generic, strategy-driven job framework.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiErrorStatus409 | RerunJobV2ResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        environment_id=environment_id,
job_v2_id=job_v2_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    environment_id: UUID,
    job_v2_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> ApiErrorStatus409 | RerunJobV2ResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Re-execute a terminal jobs_v2 row as a fresh run

     Only job types that register a rerun hook support this; mints a new root job and returns its id. The
    original row is left untouched at its terminal status.

    Args:
        environment_id (UUID): Stable environment identifier (UUID).
        job_v2_id (UUID): Stable jobs_v2 identifier (UUID). One row per background-work unit in
            the generic, strategy-driven job framework.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiErrorStatus409 | RerunJobV2ResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return (await asyncio_detailed(
        environment_id=environment_id,
job_v2_id=job_v2_id,
client=client,

    )).parsed
