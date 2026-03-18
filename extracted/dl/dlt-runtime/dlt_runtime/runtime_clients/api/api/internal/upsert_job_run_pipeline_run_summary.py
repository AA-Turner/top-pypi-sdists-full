from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response_400 import ErrorResponse400
from ...models.pipeline_run_summary_response import PipelineRunSummaryResponse
from ...models.upsert_job_run_pipeline_run_summary_request import (
    UpsertJobRunPipelineRunSummaryRequest,
)
from ...types import Response


def _get_kwargs(
    workspace_id: UUID,
    job_run_id: UUID,
    *,
    body: UpsertJobRunPipelineRunSummaryRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/v1/internal/job-run-pipeline-summaries/{workspace_id}/{job_run_id}".format(
            workspace_id=workspace_id,
            job_run_id=job_run_id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse400, PipelineRunSummaryResponse]]:
    if response.status_code == 200:
        response_200 = PipelineRunSummaryResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse400.from_dict(response.json())

        return response_400

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ErrorResponse400, PipelineRunSummaryResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: UUID,
    job_run_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpsertJobRunPipelineRunSummaryRequest,
) -> Response[Union[ErrorResponse400, PipelineRunSummaryResponse]]:
    """UpsertJobRunPipelineRunSummary

     Upsert a pipeline run summary for a job run. Called by the telemetry service.

    Args:
        workspace_id (UUID):
        job_run_id (UUID):
        body (UpsertJobRunPipelineRunSummaryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse400, PipelineRunSummaryResponse]]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        job_run_id=job_run_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: UUID,
    job_run_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpsertJobRunPipelineRunSummaryRequest,
) -> Optional[Union[ErrorResponse400, PipelineRunSummaryResponse]]:
    """UpsertJobRunPipelineRunSummary

     Upsert a pipeline run summary for a job run. Called by the telemetry service.

    Args:
        workspace_id (UUID):
        job_run_id (UUID):
        body (UpsertJobRunPipelineRunSummaryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse400, PipelineRunSummaryResponse]
    """

    return sync_detailed(
        workspace_id=workspace_id,
        job_run_id=job_run_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    job_run_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpsertJobRunPipelineRunSummaryRequest,
) -> Response[Union[ErrorResponse400, PipelineRunSummaryResponse]]:
    """UpsertJobRunPipelineRunSummary

     Upsert a pipeline run summary for a job run. Called by the telemetry service.

    Args:
        workspace_id (UUID):
        job_run_id (UUID):
        body (UpsertJobRunPipelineRunSummaryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse400, PipelineRunSummaryResponse]]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        job_run_id=job_run_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    job_run_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpsertJobRunPipelineRunSummaryRequest,
) -> Optional[Union[ErrorResponse400, PipelineRunSummaryResponse]]:
    """UpsertJobRunPipelineRunSummary

     Upsert a pipeline run summary for a job run. Called by the telemetry service.

    Args:
        workspace_id (UUID):
        job_run_id (UUID):
        body (UpsertJobRunPipelineRunSummaryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse400, PipelineRunSummaryResponse]
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            job_run_id=job_run_id,
            client=client,
            body=body,
        )
    ).parsed
