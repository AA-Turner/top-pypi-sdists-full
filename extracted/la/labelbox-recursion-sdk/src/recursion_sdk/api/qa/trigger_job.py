from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.qa_job_response_dto import QaJobResponseDto
from ...models.run_config_file_clash_error_dto import RunConfigFileClashErrorDto
from ...models.run_config_file_clash_invalid_request_error_dto import RunConfigFileClashInvalidRequestErrorDto
from ...models.target_api_error_forbidden import TargetApiErrorForbidden
from ...models.target_api_error_internal_error import TargetApiErrorInternalError
from ...models.target_api_error_invariant_violation import TargetApiErrorInvariantViolation
from ...models.target_api_error_not_found import TargetApiErrorNotFound
from ...models.target_api_error_rate_limit_exceeded import TargetApiErrorRateLimitExceeded
from ...models.target_api_error_unauthorized import TargetApiErrorUnauthorized
from ...models.trigger_qa_job_body_dto import TriggerQaJobBodyDto
from typing import cast
from uuid import UUID



def _get_kwargs(
    environment_id: UUID,
    *,
    body: TriggerQaJobBodyDto,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/environments/{environment_id}/qa-jobs".format(environment_id=quote(str(environment_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> QaJobResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    if response.status_code == 202:
        response_202 = QaJobResponseDto.from_dict(response.json())



        return response_202

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[QaJobResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    environment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: TriggerQaJobBodyDto,

) -> Response[QaJobResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Trigger an individual QA job

     Asynchronously submits a QA job that runs a config against one problem version and returns the
    pending job record. Poll the job to observe progress and final result.

    Args:
        environment_id (UUID): Stable environment identifier (UUID).
        body (TriggerQaJobBodyDto): Payload for triggering a single QA job against one problem
            (optionally pinned to a specific version). Example: {'qaConfigId':
            'd6bcc57c-7b71-4369-98da-ab69d9571bb9', 'problemId':
            '2d3fe029-a7d1-4747-9d09-81b976087bbb', 'problemVersionId':
            '0c3ac467-57e1-4074-b57d-b6a7be392f71', 'timeoutSeconds': 600}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[QaJobResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        environment_id=environment_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    environment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: TriggerQaJobBodyDto,

) -> QaJobResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Trigger an individual QA job

     Asynchronously submits a QA job that runs a config against one problem version and returns the
    pending job record. Poll the job to observe progress and final result.

    Args:
        environment_id (UUID): Stable environment identifier (UUID).
        body (TriggerQaJobBodyDto): Payload for triggering a single QA job against one problem
            (optionally pinned to a specific version). Example: {'qaConfigId':
            'd6bcc57c-7b71-4369-98da-ab69d9571bb9', 'problemId':
            '2d3fe029-a7d1-4747-9d09-81b976087bbb', 'problemVersionId':
            '0c3ac467-57e1-4074-b57d-b6a7be392f71', 'timeoutSeconds': 600}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        QaJobResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return sync_detailed(
        environment_id=environment_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    environment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: TriggerQaJobBodyDto,

) -> Response[QaJobResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Trigger an individual QA job

     Asynchronously submits a QA job that runs a config against one problem version and returns the
    pending job record. Poll the job to observe progress and final result.

    Args:
        environment_id (UUID): Stable environment identifier (UUID).
        body (TriggerQaJobBodyDto): Payload for triggering a single QA job against one problem
            (optionally pinned to a specific version). Example: {'qaConfigId':
            'd6bcc57c-7b71-4369-98da-ab69d9571bb9', 'problemId':
            '2d3fe029-a7d1-4747-9d09-81b976087bbb', 'problemVersionId':
            '0c3ac467-57e1-4074-b57d-b6a7be392f71', 'timeoutSeconds': 600}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[QaJobResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        environment_id=environment_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    environment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: TriggerQaJobBodyDto,

) -> QaJobResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Trigger an individual QA job

     Asynchronously submits a QA job that runs a config against one problem version and returns the
    pending job record. Poll the job to observe progress and final result.

    Args:
        environment_id (UUID): Stable environment identifier (UUID).
        body (TriggerQaJobBodyDto): Payload for triggering a single QA job against one problem
            (optionally pinned to a specific version). Example: {'qaConfigId':
            'd6bcc57c-7b71-4369-98da-ab69d9571bb9', 'problemId':
            '2d3fe029-a7d1-4747-9d09-81b976087bbb', 'problemVersionId':
            '0c3ac467-57e1-4074-b57d-b6a7be392f71', 'timeoutSeconds': 600}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        QaJobResponseDto | RunConfigFileClashErrorDto | RunConfigFileClashInvalidRequestErrorDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return (await asyncio_detailed(
        environment_id=environment_id,
client=client,
body=body,

    )).parsed
