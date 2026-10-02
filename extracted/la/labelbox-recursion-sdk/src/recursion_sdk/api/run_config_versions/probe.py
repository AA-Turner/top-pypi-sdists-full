from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.run_config_probe_already_in_flight_error_dto import RunConfigProbeAlreadyInFlightErrorDto
from ...models.submit_probe_response_dto import SubmitProbeResponseDto
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
    run_config_version_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/run-config-versions/{run_config_version_id}/probe".format(run_config_version_id=quote(str(run_config_version_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> RunConfigProbeAlreadyInFlightErrorDto | SubmitProbeResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    if response.status_code == 202:
        response_202 = SubmitProbeResponseDto.from_dict(response.json())



        return response_202

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
        response_409 = RunConfigProbeAlreadyInFlightErrorDto.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[RunConfigProbeAlreadyInFlightErrorDto | SubmitProbeResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    run_config_version_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Response[RunConfigProbeAlreadyInFlightErrorDto | SubmitProbeResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Submit a probe against a draft version (async)

     Submits an asynchronous probe-run against a draft version; poll the returned probe-run until it
    reaches a terminal status. A passing probe marks the version as verified. Only one probe-run may be
    in flight per version at a time.

    Args:
        run_config_version_id (UUID): Stable run-config-version identifier (UUID). Points at one
            specific version of a run config.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RunConfigProbeAlreadyInFlightErrorDto | SubmitProbeResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        run_config_version_id=run_config_version_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    run_config_version_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> RunConfigProbeAlreadyInFlightErrorDto | SubmitProbeResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Submit a probe against a draft version (async)

     Submits an asynchronous probe-run against a draft version; poll the returned probe-run until it
    reaches a terminal status. A passing probe marks the version as verified. Only one probe-run may be
    in flight per version at a time.

    Args:
        run_config_version_id (UUID): Stable run-config-version identifier (UUID). Points at one
            specific version of a run config.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RunConfigProbeAlreadyInFlightErrorDto | SubmitProbeResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return sync_detailed(
        run_config_version_id=run_config_version_id,
client=client,

    ).parsed

async def asyncio_detailed(
    run_config_version_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Response[RunConfigProbeAlreadyInFlightErrorDto | SubmitProbeResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Submit a probe against a draft version (async)

     Submits an asynchronous probe-run against a draft version; poll the returned probe-run until it
    reaches a terminal status. A passing probe marks the version as verified. Only one probe-run may be
    in flight per version at a time.

    Args:
        run_config_version_id (UUID): Stable run-config-version identifier (UUID). Points at one
            specific version of a run config.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RunConfigProbeAlreadyInFlightErrorDto | SubmitProbeResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        run_config_version_id=run_config_version_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    run_config_version_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> RunConfigProbeAlreadyInFlightErrorDto | SubmitProbeResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Submit a probe against a draft version (async)

     Submits an asynchronous probe-run against a draft version; poll the returned probe-run until it
    reaches a terminal status. A passing probe marks the version as verified. Only one probe-run may be
    in flight per version at a time.

    Args:
        run_config_version_id (UUID): Stable run-config-version identifier (UUID). Points at one
            specific version of a run config.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RunConfigProbeAlreadyInFlightErrorDto | SubmitProbeResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return (await asyncio_detailed(
        run_config_version_id=run_config_version_id,
client=client,

    )).parsed
