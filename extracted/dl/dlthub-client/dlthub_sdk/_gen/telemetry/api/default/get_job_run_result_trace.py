from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.job_result_trace_response import JobResultTraceResponse
from ...types import Response


def _get_kwargs(
    workspace_id: UUID,
    job_run_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/telemetry/v1/workspaces/{workspace_id}/job-runs/{job_run_id}/result-trace".format(
            workspace_id=quote(str(workspace_id), safe=""),
            job_run_id=quote(str(job_run_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | JobResultTraceResponse | None:
    if response.status_code == 200:
        response_200 = JobResultTraceResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 413:
        response_413 = ErrorResponse.from_dict(response.json())

        return response_413

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | JobResultTraceResponse]:
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
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | JobResultTraceResponse]:
    """GetJobResultTrace

    The full result exactly as the job delivered it, including the agent's per-turn tool calls.
    Fields beyond `type` and `job_ref` are passed through unchanged. `job_run_id` is the job run's
    id from the runtime API, not a `pipeline_run_id`. Answers 404 when the run declared no result.

    Results over 8 MiB answer 413 `job_result_trace_too_large`; the summary fields stay
    available at `/result`.

    Args:
        workspace_id (UUID):
        job_run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | JobResultTraceResponse]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        job_run_id=job_run_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: UUID,
    job_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | JobResultTraceResponse | None:
    """GetJobResultTrace

    The full result exactly as the job delivered it, including the agent's per-turn tool calls.
    Fields beyond `type` and `job_ref` are passed through unchanged. `job_run_id` is the job run's
    id from the runtime API, not a `pipeline_run_id`. Answers 404 when the run declared no result.

    Results over 8 MiB answer 413 `job_result_trace_too_large`; the summary fields stay
    available at `/result`.

    Args:
        workspace_id (UUID):
        job_run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | JobResultTraceResponse
    """
    return sync_detailed(
        workspace_id=workspace_id,
        job_run_id=job_run_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    job_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | JobResultTraceResponse]:
    """GetJobResultTrace

    The full result exactly as the job delivered it, including the agent's per-turn tool calls.
    Fields beyond `type` and `job_ref` are passed through unchanged. `job_run_id` is the job run's
    id from the runtime API, not a `pipeline_run_id`. Answers 404 when the run declared no result.

    Results over 8 MiB answer 413 `job_result_trace_too_large`; the summary fields stay
    available at `/result`.

    Args:
        workspace_id (UUID):
        job_run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | JobResultTraceResponse]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        job_run_id=job_run_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    job_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | JobResultTraceResponse | None:
    """GetJobResultTrace

    The full result exactly as the job delivered it, including the agent's per-turn tool calls.
    Fields beyond `type` and `job_ref` are passed through unchanged. `job_run_id` is the job run's
    id from the runtime API, not a `pipeline_run_id`. Answers 404 when the run declared no result.

    Results over 8 MiB answer 413 `job_result_trace_too_large`; the summary fields stay
    available at `/result`.

    Args:
        workspace_id (UUID):
        job_run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | JobResultTraceResponse
    """
    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            job_run_id=job_run_id,
            client=client,
        )
    ).parsed
