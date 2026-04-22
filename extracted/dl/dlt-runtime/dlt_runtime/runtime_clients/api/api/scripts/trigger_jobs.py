from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response_400 import ErrorResponse400
from ...models.error_response_401 import ErrorResponse401
from ...models.error_response_403 import ErrorResponse403
from ...models.error_response_404 import ErrorResponse404
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
        "url": "/v1/workspaces/{workspace_id}/scripts/trigger".format(
            workspace_id=workspace_id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        ErrorResponse400,
        ErrorResponse401,
        ErrorResponse403,
        ErrorResponse404,
        TriggerJobsResponse,
    ]
]:
    if response.status_code == 201:
        response_201 = TriggerJobsResponse.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = ErrorResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorResponse404.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        ErrorResponse400,
        ErrorResponse401,
        ErrorResponse403,
        ErrorResponse404,
        TriggerJobsResponse,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: TriggerJobsRequest,
) -> Response[
    Union[
        ErrorResponse400,
        ErrorResponse401,
        ErrorResponse403,
        ErrorResponse404,
        TriggerJobsResponse,
    ]
]:
    """TriggerJobs


    Triggers jobs by `selectors` (fnmatch patterns matched against each script's triggers array,
    e.g. 'tag:backfill', 'schedule:*', 'batch') and/or by `job_refs` (per-script invocation
    that fires each script via its `default_trigger`, or `manual:<ref>` if no default exists).

    When the same script matches both `selectors` and `job_refs`, the union of matched
    triggers is fed to `pick_trigger`, which prefers `default_trigger` if present.

    Jobs are ordered by dependencies and freshness gating is mandatory — downstream jobs
    whose upstream isn't fresh are skipped (`status='skipped_fresh'`). For single-job bypass,
    use the `create_run` endpoint with `skip_freshness=True`.

    Supports dry_run mode to preview matched jobs without creating runs.

    Requires CREATE_RUN permission (workspace viewers can trigger interactive jobs).

    Args:
        workspace_id (UUID):
        body (TriggerJobsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse400, ErrorResponse401, ErrorResponse403, ErrorResponse404, TriggerJobsResponse]]
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
    client: Union[AuthenticatedClient, Client],
    body: TriggerJobsRequest,
) -> Optional[
    Union[
        ErrorResponse400,
        ErrorResponse401,
        ErrorResponse403,
        ErrorResponse404,
        TriggerJobsResponse,
    ]
]:
    """TriggerJobs


    Triggers jobs by `selectors` (fnmatch patterns matched against each script's triggers array,
    e.g. 'tag:backfill', 'schedule:*', 'batch') and/or by `job_refs` (per-script invocation
    that fires each script via its `default_trigger`, or `manual:<ref>` if no default exists).

    When the same script matches both `selectors` and `job_refs`, the union of matched
    triggers is fed to `pick_trigger`, which prefers `default_trigger` if present.

    Jobs are ordered by dependencies and freshness gating is mandatory — downstream jobs
    whose upstream isn't fresh are skipped (`status='skipped_fresh'`). For single-job bypass,
    use the `create_run` endpoint with `skip_freshness=True`.

    Supports dry_run mode to preview matched jobs without creating runs.

    Requires CREATE_RUN permission (workspace viewers can trigger interactive jobs).

    Args:
        workspace_id (UUID):
        body (TriggerJobsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse400, ErrorResponse401, ErrorResponse403, ErrorResponse404, TriggerJobsResponse]
    """

    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: TriggerJobsRequest,
) -> Response[
    Union[
        ErrorResponse400,
        ErrorResponse401,
        ErrorResponse403,
        ErrorResponse404,
        TriggerJobsResponse,
    ]
]:
    """TriggerJobs


    Triggers jobs by `selectors` (fnmatch patterns matched against each script's triggers array,
    e.g. 'tag:backfill', 'schedule:*', 'batch') and/or by `job_refs` (per-script invocation
    that fires each script via its `default_trigger`, or `manual:<ref>` if no default exists).

    When the same script matches both `selectors` and `job_refs`, the union of matched
    triggers is fed to `pick_trigger`, which prefers `default_trigger` if present.

    Jobs are ordered by dependencies and freshness gating is mandatory — downstream jobs
    whose upstream isn't fresh are skipped (`status='skipped_fresh'`). For single-job bypass,
    use the `create_run` endpoint with `skip_freshness=True`.

    Supports dry_run mode to preview matched jobs without creating runs.

    Requires CREATE_RUN permission (workspace viewers can trigger interactive jobs).

    Args:
        workspace_id (UUID):
        body (TriggerJobsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse400, ErrorResponse401, ErrorResponse403, ErrorResponse404, TriggerJobsResponse]]
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
    client: Union[AuthenticatedClient, Client],
    body: TriggerJobsRequest,
) -> Optional[
    Union[
        ErrorResponse400,
        ErrorResponse401,
        ErrorResponse403,
        ErrorResponse404,
        TriggerJobsResponse,
    ]
]:
    """TriggerJobs


    Triggers jobs by `selectors` (fnmatch patterns matched against each script's triggers array,
    e.g. 'tag:backfill', 'schedule:*', 'batch') and/or by `job_refs` (per-script invocation
    that fires each script via its `default_trigger`, or `manual:<ref>` if no default exists).

    When the same script matches both `selectors` and `job_refs`, the union of matched
    triggers is fed to `pick_trigger`, which prefers `default_trigger` if present.

    Jobs are ordered by dependencies and freshness gating is mandatory — downstream jobs
    whose upstream isn't fresh are skipped (`status='skipped_fresh'`). For single-job bypass,
    use the `create_run` endpoint with `skip_freshness=True`.

    Supports dry_run mode to preview matched jobs without creating runs.

    Requires CREATE_RUN permission (workspace viewers can trigger interactive jobs).

    Args:
        workspace_id (UUID):
        body (TriggerJobsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse400, ErrorResponse401, ErrorResponse403, ErrorResponse404, TriggerJobsResponse]
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            body=body,
        )
    ).parsed
