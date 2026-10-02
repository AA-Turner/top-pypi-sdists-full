from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.api_error_status_409 import ApiErrorStatus409
from ...models.create_run_config_version_dto import CreateRunConfigVersionDto
from ...models.run_config_version_dto import RunConfigVersionDto
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
    run_config_id: UUID,
    *,
    body: CreateRunConfigVersionDto,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/run-configs/{run_config_id}/versions".format(run_config_id=quote(str(run_config_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ApiErrorStatus409 | RunConfigVersionDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    if response.status_code == 201:
        response_201 = RunConfigVersionDto.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ApiErrorStatus409 | RunConfigVersionDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
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
    body: CreateRunConfigVersionDto,

) -> Response[ApiErrorStatus409 | RunConfigVersionDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Create a new draft version on a run config

     Creates a new draft, optionally forking its payload from a parent version. Only one open draft per
    run config is allowed; passing a probe before locking is recommended but not required.

    Args:
        run_config_id (UUID): Stable run-config identifier (UUID). Versioned reusable solver /
            grader / QA / synthesizer config.
        body (CreateRunConfigVersionDto): Input for creating a new draft version under an existing
            run-config identity. Example: {'config': {'harnessImageUrl': 'us-
            central1-docker.pkg.dev/lb-ml-prod/agent-service/claude-code:v1.2.3', 'containerSize':
            'medium', 'args': '--max-turns 30', 'envVars': {'MODEL': 'claude-sonnet-4-6', 'LOG_LEVEL':
            'info'}, 'customerSecrets': [{'envVarName': 'ANTHROPIC_API_KEY'}], 'timeoutSeconds': 600,
            'mcpTools': [{'name': 'read_file', 'description': 'Read a file from the workspace.',
            'service': 'worldsim', 'category': 'filesystem', 'sortOrder': 10, 'readOnly': True,
            'timeout': 30, 'inputSchema': '{"type":"object","properties":{"path":{"type":"string"}}}',
            'serviceLabel': 'WorldSim'}]}, 'probe': {'prompt': 'Inspect the attached image and report
            whether a surface defect is visible.', 'files': [], 'qualityCheck': 'Agent identifies the
            surface defect and reports its location.'}, 'notes': 'Raised --max-turns to 30 after the
            v2 probe ran out of turns.', 'parentRunConfigVersionId':
            'b2d6f3a1-4c8e-4a7b-9f10-2e5c6d8a1b40'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiErrorStatus409 | RunConfigVersionDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
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
    body: CreateRunConfigVersionDto,

) -> ApiErrorStatus409 | RunConfigVersionDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Create a new draft version on a run config

     Creates a new draft, optionally forking its payload from a parent version. Only one open draft per
    run config is allowed; passing a probe before locking is recommended but not required.

    Args:
        run_config_id (UUID): Stable run-config identifier (UUID). Versioned reusable solver /
            grader / QA / synthesizer config.
        body (CreateRunConfigVersionDto): Input for creating a new draft version under an existing
            run-config identity. Example: {'config': {'harnessImageUrl': 'us-
            central1-docker.pkg.dev/lb-ml-prod/agent-service/claude-code:v1.2.3', 'containerSize':
            'medium', 'args': '--max-turns 30', 'envVars': {'MODEL': 'claude-sonnet-4-6', 'LOG_LEVEL':
            'info'}, 'customerSecrets': [{'envVarName': 'ANTHROPIC_API_KEY'}], 'timeoutSeconds': 600,
            'mcpTools': [{'name': 'read_file', 'description': 'Read a file from the workspace.',
            'service': 'worldsim', 'category': 'filesystem', 'sortOrder': 10, 'readOnly': True,
            'timeout': 30, 'inputSchema': '{"type":"object","properties":{"path":{"type":"string"}}}',
            'serviceLabel': 'WorldSim'}]}, 'probe': {'prompt': 'Inspect the attached image and report
            whether a surface defect is visible.', 'files': [], 'qualityCheck': 'Agent identifies the
            surface defect and reports its location.'}, 'notes': 'Raised --max-turns to 30 after the
            v2 probe ran out of turns.', 'parentRunConfigVersionId':
            'b2d6f3a1-4c8e-4a7b-9f10-2e5c6d8a1b40'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiErrorStatus409 | RunConfigVersionDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
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
    body: CreateRunConfigVersionDto,

) -> Response[ApiErrorStatus409 | RunConfigVersionDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Create a new draft version on a run config

     Creates a new draft, optionally forking its payload from a parent version. Only one open draft per
    run config is allowed; passing a probe before locking is recommended but not required.

    Args:
        run_config_id (UUID): Stable run-config identifier (UUID). Versioned reusable solver /
            grader / QA / synthesizer config.
        body (CreateRunConfigVersionDto): Input for creating a new draft version under an existing
            run-config identity. Example: {'config': {'harnessImageUrl': 'us-
            central1-docker.pkg.dev/lb-ml-prod/agent-service/claude-code:v1.2.3', 'containerSize':
            'medium', 'args': '--max-turns 30', 'envVars': {'MODEL': 'claude-sonnet-4-6', 'LOG_LEVEL':
            'info'}, 'customerSecrets': [{'envVarName': 'ANTHROPIC_API_KEY'}], 'timeoutSeconds': 600,
            'mcpTools': [{'name': 'read_file', 'description': 'Read a file from the workspace.',
            'service': 'worldsim', 'category': 'filesystem', 'sortOrder': 10, 'readOnly': True,
            'timeout': 30, 'inputSchema': '{"type":"object","properties":{"path":{"type":"string"}}}',
            'serviceLabel': 'WorldSim'}]}, 'probe': {'prompt': 'Inspect the attached image and report
            whether a surface defect is visible.', 'files': [], 'qualityCheck': 'Agent identifies the
            surface defect and reports its location.'}, 'notes': 'Raised --max-turns to 30 after the
            v2 probe ran out of turns.', 'parentRunConfigVersionId':
            'b2d6f3a1-4c8e-4a7b-9f10-2e5c6d8a1b40'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiErrorStatus409 | RunConfigVersionDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
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
    body: CreateRunConfigVersionDto,

) -> ApiErrorStatus409 | RunConfigVersionDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Create a new draft version on a run config

     Creates a new draft, optionally forking its payload from a parent version. Only one open draft per
    run config is allowed; passing a probe before locking is recommended but not required.

    Args:
        run_config_id (UUID): Stable run-config identifier (UUID). Versioned reusable solver /
            grader / QA / synthesizer config.
        body (CreateRunConfigVersionDto): Input for creating a new draft version under an existing
            run-config identity. Example: {'config': {'harnessImageUrl': 'us-
            central1-docker.pkg.dev/lb-ml-prod/agent-service/claude-code:v1.2.3', 'containerSize':
            'medium', 'args': '--max-turns 30', 'envVars': {'MODEL': 'claude-sonnet-4-6', 'LOG_LEVEL':
            'info'}, 'customerSecrets': [{'envVarName': 'ANTHROPIC_API_KEY'}], 'timeoutSeconds': 600,
            'mcpTools': [{'name': 'read_file', 'description': 'Read a file from the workspace.',
            'service': 'worldsim', 'category': 'filesystem', 'sortOrder': 10, 'readOnly': True,
            'timeout': 30, 'inputSchema': '{"type":"object","properties":{"path":{"type":"string"}}}',
            'serviceLabel': 'WorldSim'}]}, 'probe': {'prompt': 'Inspect the attached image and report
            whether a surface defect is visible.', 'files': [], 'qualityCheck': 'Agent identifies the
            surface defect and reports its location.'}, 'notes': 'Raised --max-turns to 30 after the
            v2 probe ran out of turns.', 'parentRunConfigVersionId':
            'b2d6f3a1-4c8e-4a7b-9f10-2e5c6d8a1b40'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiErrorStatus409 | RunConfigVersionDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return (await asyncio_detailed(
        run_config_id=run_config_id,
client=client,
body=body,

    )).parsed
