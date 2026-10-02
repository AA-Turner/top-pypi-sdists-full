from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.run_config_dto import RunConfigDto
from ...models.target_api_error_forbidden import TargetApiErrorForbidden
from ...models.target_api_error_internal_error import TargetApiErrorInternalError
from ...models.target_api_error_invalid_request import TargetApiErrorInvalidRequest
from ...models.target_api_error_invariant_violation import TargetApiErrorInvariantViolation
from ...models.target_api_error_not_found import TargetApiErrorNotFound
from ...models.target_api_error_rate_limit_exceeded import TargetApiErrorRateLimitExceeded
from ...models.target_api_error_unauthorized import TargetApiErrorUnauthorized
from ...models.update_run_config_dto import UpdateRunConfigDto
from typing import cast
from uuid import UUID



def _get_kwargs(
    run_config_id: UUID,
    *,
    body: UpdateRunConfigDto,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/v1/run-configs/{run_config_id}".format(run_config_id=quote(str(run_config_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> RunConfigDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    if response.status_code == 200:
        response_200 = RunConfigDto.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[RunConfigDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    run_config_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateRunConfigDto,

) -> Response[RunConfigDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Update a run config (identity fields only)

     Patches identity-level fields only and does not touch any version payload or default-version pin.

    Args:
        run_config_id (UUID): Stable run-config identifier (UUID). Versioned reusable solver /
            grader / QA / synthesizer config.
        body (UpdateRunConfigDto): Patch-style update body for run-config identity-level metadata.
            Omitted fields are left unchanged. Example: {'name': 'claude-sonnet-baseline',
            'description': 'Baseline Claude Sonnet solver harness for the vision-agent-eval
            environment.'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RunConfigDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        run_config_id=run_config_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    run_config_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateRunConfigDto,

) -> RunConfigDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Update a run config (identity fields only)

     Patches identity-level fields only and does not touch any version payload or default-version pin.

    Args:
        run_config_id (UUID): Stable run-config identifier (UUID). Versioned reusable solver /
            grader / QA / synthesizer config.
        body (UpdateRunConfigDto): Patch-style update body for run-config identity-level metadata.
            Omitted fields are left unchanged. Example: {'name': 'claude-sonnet-baseline',
            'description': 'Baseline Claude Sonnet solver harness for the vision-agent-eval
            environment.'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RunConfigDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return sync_detailed(
        run_config_id=run_config_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    run_config_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateRunConfigDto,

) -> Response[RunConfigDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Update a run config (identity fields only)

     Patches identity-level fields only and does not touch any version payload or default-version pin.

    Args:
        run_config_id (UUID): Stable run-config identifier (UUID). Versioned reusable solver /
            grader / QA / synthesizer config.
        body (UpdateRunConfigDto): Patch-style update body for run-config identity-level metadata.
            Omitted fields are left unchanged. Example: {'name': 'claude-sonnet-baseline',
            'description': 'Baseline Claude Sonnet solver harness for the vision-agent-eval
            environment.'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RunConfigDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        run_config_id=run_config_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    run_config_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateRunConfigDto,

) -> RunConfigDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Update a run config (identity fields only)

     Patches identity-level fields only and does not touch any version payload or default-version pin.

    Args:
        run_config_id (UUID): Stable run-config identifier (UUID). Versioned reusable solver /
            grader / QA / synthesizer config.
        body (UpdateRunConfigDto): Patch-style update body for run-config identity-level metadata.
            Omitted fields are left unchanged. Example: {'name': 'claude-sonnet-baseline',
            'description': 'Baseline Claude Sonnet solver harness for the vision-agent-eval
            environment.'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RunConfigDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return (await asyncio_detailed(
        run_config_id=run_config_id,
client=client,
body=body,

    )).parsed
