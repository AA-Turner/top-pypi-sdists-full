from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_job_run_request import CreateJobRunRequest
from ...models.detailed_job_run_response import DetailedJobRunResponse
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    workspace_id: UUID,
    *,
    body: CreateJobRunRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/workspaces/{workspace_id}/job-runs".format(
            workspace_id=quote(str(workspace_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DetailedJobRunResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = DetailedJobRunResponse.from_dict(response.json())

        return response_200

    if response.status_code == 201:
        response_201 = DetailedJobRunResponse.from_dict(response.json())

        return response_201

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

    if response.status_code == 409:
        response_409 = ErrorResponse.from_dict(response.json())

        return response_409

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[DetailedJobRunResponse | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: CreateJobRunRequest,
) -> Response[DetailedJobRunResponse | ErrorResponse]:
    """CreateJobRun

    Starts a run of the job's latest version with the workspace's latest deployment and
    configuration, under `profile` or the job's own profile. A paused job still runs; pausing
    only stops scheduled runs.

    `mode` controls run creation:
    - `always` (default): always creates a new run (201).
    - `when_not_running`: returns the job's pending, starting or running run (200) if it has one,
      otherwise creates a new one (201).

    Answers 400 for an archived job, and 404 when the job has no version or the workspace has no
    deployment or configuration yet. A run the platform declines to start answers 409 or 403 with
    a `code` naming why and the reasons in `extra`: `upstream_not_fresh`, `outside_job_interval`,
    `job_concurrency_limit`, `organization_concurrency_limit` (409), `trial_expired`,
    `compute_minutes_exhausted` (403), or `run_not_started` for any other reason (409).

    Requires the viewer role (or higher) in the workspace. Viewers may only run jobs that use the
    read-only `access` profile (by default interactive and agent jobs); any other profile needs
    the developer role and answers 403.

    Args:
        workspace_id (UUID):
        body (CreateJobRunRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DetailedJobRunResponse | ErrorResponse]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: CreateJobRunRequest,
) -> DetailedJobRunResponse | ErrorResponse | None:
    """CreateJobRun

    Starts a run of the job's latest version with the workspace's latest deployment and
    configuration, under `profile` or the job's own profile. A paused job still runs; pausing
    only stops scheduled runs.

    `mode` controls run creation:
    - `always` (default): always creates a new run (201).
    - `when_not_running`: returns the job's pending, starting or running run (200) if it has one,
      otherwise creates a new one (201).

    Answers 400 for an archived job, and 404 when the job has no version or the workspace has no
    deployment or configuration yet. A run the platform declines to start answers 409 or 403 with
    a `code` naming why and the reasons in `extra`: `upstream_not_fresh`, `outside_job_interval`,
    `job_concurrency_limit`, `organization_concurrency_limit` (409), `trial_expired`,
    `compute_minutes_exhausted` (403), or `run_not_started` for any other reason (409).

    Requires the viewer role (or higher) in the workspace. Viewers may only run jobs that use the
    read-only `access` profile (by default interactive and agent jobs); any other profile needs
    the developer role and answers 403.

    Args:
        workspace_id (UUID):
        body (CreateJobRunRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DetailedJobRunResponse | ErrorResponse
    """
    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: CreateJobRunRequest,
) -> Response[DetailedJobRunResponse | ErrorResponse]:
    """CreateJobRun

    Starts a run of the job's latest version with the workspace's latest deployment and
    configuration, under `profile` or the job's own profile. A paused job still runs; pausing
    only stops scheduled runs.

    `mode` controls run creation:
    - `always` (default): always creates a new run (201).
    - `when_not_running`: returns the job's pending, starting or running run (200) if it has one,
      otherwise creates a new one (201).

    Answers 400 for an archived job, and 404 when the job has no version or the workspace has no
    deployment or configuration yet. A run the platform declines to start answers 409 or 403 with
    a `code` naming why and the reasons in `extra`: `upstream_not_fresh`, `outside_job_interval`,
    `job_concurrency_limit`, `organization_concurrency_limit` (409), `trial_expired`,
    `compute_minutes_exhausted` (403), or `run_not_started` for any other reason (409).

    Requires the viewer role (or higher) in the workspace. Viewers may only run jobs that use the
    read-only `access` profile (by default interactive and agent jobs); any other profile needs
    the developer role and answers 403.

    Args:
        workspace_id (UUID):
        body (CreateJobRunRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DetailedJobRunResponse | ErrorResponse]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: CreateJobRunRequest,
) -> DetailedJobRunResponse | ErrorResponse | None:
    """CreateJobRun

    Starts a run of the job's latest version with the workspace's latest deployment and
    configuration, under `profile` or the job's own profile. A paused job still runs; pausing
    only stops scheduled runs.

    `mode` controls run creation:
    - `always` (default): always creates a new run (201).
    - `when_not_running`: returns the job's pending, starting or running run (200) if it has one,
      otherwise creates a new one (201).

    Answers 400 for an archived job, and 404 when the job has no version or the workspace has no
    deployment or configuration yet. A run the platform declines to start answers 409 or 403 with
    a `code` naming why and the reasons in `extra`: `upstream_not_fresh`, `outside_job_interval`,
    `job_concurrency_limit`, `organization_concurrency_limit` (409), `trial_expired`,
    `compute_minutes_exhausted` (403), or `run_not_started` for any other reason (409).

    Requires the viewer role (or higher) in the workspace. Viewers may only run jobs that use the
    read-only `access` profile (by default interactive and agent jobs); any other profile needs
    the developer role and answers 403.

    Args:
        workspace_id (UUID):
        body (CreateJobRunRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DetailedJobRunResponse | ErrorResponse
    """
    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            body=body,
        )
    ).parsed
