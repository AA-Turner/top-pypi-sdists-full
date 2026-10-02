from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

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
    problem_version_id: UUID,
    synthesizer_run_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/versions/{problem_version_id}/synthesizer-runs/{synthesizer_run_id}/transcript".format(problem_version_id=quote(str(problem_version_id), safe=""),synthesizer_run_id=quote(str(synthesizer_run_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | str | None:
    if response.status_code == 200:
        response_200 = response.text
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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    problem_version_id: UUID,
    synthesizer_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | str]:
    """ Get the persisted transcript for a synthesizer run

     Returns the persisted transcript captured when the run reached a terminal state. In-progress runs
    have no persisted transcript yet.

    Args:
        problem_version_id (UUID): Stable problem-version identifier (UUID). Each problem can have
            many versions; this points at one specific version.
        synthesizer_run_id (UUID): Stable synthesizer-run identifier (UUID). One execution of a
            synthesizer job.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | str]
     """


    kwargs = _get_kwargs(
        problem_version_id=problem_version_id,
synthesizer_run_id=synthesizer_run_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    problem_version_id: UUID,
    synthesizer_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | str | None:
    """ Get the persisted transcript for a synthesizer run

     Returns the persisted transcript captured when the run reached a terminal state. In-progress runs
    have no persisted transcript yet.

    Args:
        problem_version_id (UUID): Stable problem-version identifier (UUID). Each problem can have
            many versions; this points at one specific version.
        synthesizer_run_id (UUID): Stable synthesizer-run identifier (UUID). One execution of a
            synthesizer job.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | str
     """


    return sync_detailed(
        problem_version_id=problem_version_id,
synthesizer_run_id=synthesizer_run_id,
client=client,

    ).parsed

async def asyncio_detailed(
    problem_version_id: UUID,
    synthesizer_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | str]:
    """ Get the persisted transcript for a synthesizer run

     Returns the persisted transcript captured when the run reached a terminal state. In-progress runs
    have no persisted transcript yet.

    Args:
        problem_version_id (UUID): Stable problem-version identifier (UUID). Each problem can have
            many versions; this points at one specific version.
        synthesizer_run_id (UUID): Stable synthesizer-run identifier (UUID). One execution of a
            synthesizer job.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | str]
     """


    kwargs = _get_kwargs(
        problem_version_id=problem_version_id,
synthesizer_run_id=synthesizer_run_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    problem_version_id: UUID,
    synthesizer_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | str | None:
    """ Get the persisted transcript for a synthesizer run

     Returns the persisted transcript captured when the run reached a terminal state. In-progress runs
    have no persisted transcript yet.

    Args:
        problem_version_id (UUID): Stable problem-version identifier (UUID). Each problem can have
            many versions; this points at one specific version.
        synthesizer_run_id (UUID): Stable synthesizer-run identifier (UUID). One execution of a
            synthesizer job.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | str
     """


    return (await asyncio_detailed(
        problem_version_id=problem_version_id,
synthesizer_run_id=synthesizer_run_id,
client=client,

    )).parsed
