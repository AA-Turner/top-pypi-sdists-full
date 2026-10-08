from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.trigger_jobs_request import TriggerJobsRequest
from ...models.trigger_jobs_response import TriggerJobsResponse
from ...types import Response


def _get_kwargs(
    workspace_id: UUID,
    *,
    body: TriggerJobsRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/workspaces/{workspace_id}/jobs/-trigger".format(
            workspace_id=quote(str(workspace_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | TriggerJobsResponse | None:
    if response.status_code == 200:
        response_200 = TriggerJobsResponse.from_dict(response.json())

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
) -> Response[ErrorResponse | TriggerJobsResponse]:
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
    body: TriggerJobsRequest,
) -> Response[ErrorResponse | TriggerJobsResponse]:
    """TriggerJobs

    Triggers jobs by `job_ids` (each fires via its `default_trigger`, or `manual:<ref>` if it has
    none) and/or by `selectors` (fnmatch patterns matched against each job's triggers, e.g.
    'tag:backfill', 'schedule:*', 'batch'; a matching job fires the trigger it matched).

    When the same job is named both ways, the union of matched triggers is fed to `pick_trigger`,
    which prefers `default_trigger` if present.

    Jobs are ordered by dependencies and freshness gating is mandatory — a downstream job whose
    upstream isn't fresh is skipped (`status='skipped_fresh'`). For single-job bypass, use
    `create_job_run` with `skip_freshness=True`.

    Answers a receipt: `succeeded` jobs started a run, `skipped` jobs did not (their `status` and
    `reasons` say why), `failed` lists requested ids that name no job. `dry_run` previews it.

    Requires CREATE_RUN permission (workspace viewers can trigger interactive jobs).

    Args:
        workspace_id (UUID):
        body (TriggerJobsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | TriggerJobsResponse]
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
    body: TriggerJobsRequest,
) -> ErrorResponse | TriggerJobsResponse | None:
    """TriggerJobs

    Triggers jobs by `job_ids` (each fires via its `default_trigger`, or `manual:<ref>` if it has
    none) and/or by `selectors` (fnmatch patterns matched against each job's triggers, e.g.
    'tag:backfill', 'schedule:*', 'batch'; a matching job fires the trigger it matched).

    When the same job is named both ways, the union of matched triggers is fed to `pick_trigger`,
    which prefers `default_trigger` if present.

    Jobs are ordered by dependencies and freshness gating is mandatory — a downstream job whose
    upstream isn't fresh is skipped (`status='skipped_fresh'`). For single-job bypass, use
    `create_job_run` with `skip_freshness=True`.

    Answers a receipt: `succeeded` jobs started a run, `skipped` jobs did not (their `status` and
    `reasons` say why), `failed` lists requested ids that name no job. `dry_run` previews it.

    Requires CREATE_RUN permission (workspace viewers can trigger interactive jobs).

    Args:
        workspace_id (UUID):
        body (TriggerJobsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | TriggerJobsResponse
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
    body: TriggerJobsRequest,
) -> Response[ErrorResponse | TriggerJobsResponse]:
    """TriggerJobs

    Triggers jobs by `job_ids` (each fires via its `default_trigger`, or `manual:<ref>` if it has
    none) and/or by `selectors` (fnmatch patterns matched against each job's triggers, e.g.
    'tag:backfill', 'schedule:*', 'batch'; a matching job fires the trigger it matched).

    When the same job is named both ways, the union of matched triggers is fed to `pick_trigger`,
    which prefers `default_trigger` if present.

    Jobs are ordered by dependencies and freshness gating is mandatory — a downstream job whose
    upstream isn't fresh is skipped (`status='skipped_fresh'`). For single-job bypass, use
    `create_job_run` with `skip_freshness=True`.

    Answers a receipt: `succeeded` jobs started a run, `skipped` jobs did not (their `status` and
    `reasons` say why), `failed` lists requested ids that name no job. `dry_run` previews it.

    Requires CREATE_RUN permission (workspace viewers can trigger interactive jobs).

    Args:
        workspace_id (UUID):
        body (TriggerJobsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | TriggerJobsResponse]
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
    body: TriggerJobsRequest,
) -> ErrorResponse | TriggerJobsResponse | None:
    """TriggerJobs

    Triggers jobs by `job_ids` (each fires via its `default_trigger`, or `manual:<ref>` if it has
    none) and/or by `selectors` (fnmatch patterns matched against each job's triggers, e.g.
    'tag:backfill', 'schedule:*', 'batch'; a matching job fires the trigger it matched).

    When the same job is named both ways, the union of matched triggers is fed to `pick_trigger`,
    which prefers `default_trigger` if present.

    Jobs are ordered by dependencies and freshness gating is mandatory — a downstream job whose
    upstream isn't fresh is skipped (`status='skipped_fresh'`). For single-job bypass, use
    `create_job_run` with `skip_freshness=True`.

    Answers a receipt: `succeeded` jobs started a run, `skipped` jobs did not (their `status` and
    `reasons` say why), `failed` lists requested ids that name no job. `dry_run` previews it.

    Requires CREATE_RUN permission (workspace viewers can trigger interactive jobs).

    Args:
        workspace_id (UUID):
        body (TriggerJobsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | TriggerJobsResponse
    """
    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            body=body,
        )
    ).parsed
