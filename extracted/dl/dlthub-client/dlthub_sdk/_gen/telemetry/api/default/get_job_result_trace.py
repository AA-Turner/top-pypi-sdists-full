from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response_400 import ErrorResponse400
from ...models.get_job_result_trace_response_200 import GetJobResultTraceResponse200
from ...types import Response


def _get_kwargs(
    workspace_id: UUID,
    run_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/telemetry/v1/workspaces/{workspace_id}/runs/{run_id}/job-result/trace".format(
            workspace_id=quote(str(workspace_id), safe=""),
            run_id=quote(str(run_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse400 | GetJobResultTraceResponse200 | None:
    if response.status_code == 200:
        response_200 = GetJobResultTraceResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse400.from_dict(response.json())

        return response_400

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse400 | GetJobResultTraceResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: UUID,
    run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse400 | GetJobResultTraceResponse200]:
    """GetJobResultTrace

    The job-result envelope exactly as the runner delivered it: the declared output, and the
    agent trace with its per-turn tool calls, token counts and stop reason.

    Returned verbatim, so this carries fields no column promotes and the platform declares no
    shape for it. `run_id` is the platform run id, not a telemetry `pipeline_run_id`.

    An envelope past the size this serves in one response answers 413 with
    `job_result_trace_too_large`; the promoted scalars stay readable at `/job-result`.

    Args:
        workspace_id (UUID):
        run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | GetJobResultTraceResponse200]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        run_id=run_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: UUID,
    run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse400 | GetJobResultTraceResponse200 | None:
    """GetJobResultTrace

    The job-result envelope exactly as the runner delivered it: the declared output, and the
    agent trace with its per-turn tool calls, token counts and stop reason.

    Returned verbatim, so this carries fields no column promotes and the platform declares no
    shape for it. `run_id` is the platform run id, not a telemetry `pipeline_run_id`.

    An envelope past the size this serves in one response answers 413 with
    `job_result_trace_too_large`; the promoted scalars stay readable at `/job-result`.

    Args:
        workspace_id (UUID):
        run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | GetJobResultTraceResponse200
    """
    return sync_detailed(
        workspace_id=workspace_id,
        run_id=run_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse400 | GetJobResultTraceResponse200]:
    """GetJobResultTrace

    The job-result envelope exactly as the runner delivered it: the declared output, and the
    agent trace with its per-turn tool calls, token counts and stop reason.

    Returned verbatim, so this carries fields no column promotes and the platform declares no
    shape for it. `run_id` is the platform run id, not a telemetry `pipeline_run_id`.

    An envelope past the size this serves in one response answers 413 with
    `job_result_trace_too_large`; the promoted scalars stay readable at `/job-result`.

    Args:
        workspace_id (UUID):
        run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | GetJobResultTraceResponse200]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        run_id=run_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse400 | GetJobResultTraceResponse200 | None:
    """GetJobResultTrace

    The job-result envelope exactly as the runner delivered it: the declared output, and the
    agent trace with its per-turn tool calls, token counts and stop reason.

    Returned verbatim, so this carries fields no column promotes and the platform declares no
    shape for it. `run_id` is the platform run id, not a telemetry `pipeline_run_id`.

    An envelope past the size this serves in one response answers 413 with
    `job_result_trace_too_large`; the promoted scalars stay readable at `/job-result`.

    Args:
        workspace_id (UUID):
        run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | GetJobResultTraceResponse200
    """
    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            run_id=run_id,
            client=client,
        )
    ).parsed
