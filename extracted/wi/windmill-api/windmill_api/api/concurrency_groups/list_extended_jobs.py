import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_extended_jobs_response_200 import ListExtendedJobsResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    concurrency_key: Union[Unset, None, str] = UNSET,
    row_limit: Union[Unset, None, float] = UNSET,
    created_by: Union[Unset, None, str] = UNSET,
    label: Union[Unset, None, str] = UNSET,
    parent_job: Union[Unset, None, str] = UNSET,
    script_path_exact: Union[Unset, None, str] = UNSET,
    script_path_start: Union[Unset, None, str] = UNSET,
    schedule_path: Union[Unset, None, str] = UNSET,
    script_hash: Union[Unset, None, str] = UNSET,
    started_before: Union[Unset, None, datetime.datetime] = UNSET,
    started_after: Union[Unset, None, datetime.datetime] = UNSET,
    created_or_started_before: Union[Unset, None, datetime.datetime] = UNSET,
    running: Union[Unset, None, bool] = UNSET,
    scheduled_for_before_now: Union[Unset, None, bool] = UNSET,
    created_or_started_after: Union[Unset, None, datetime.datetime] = UNSET,
    created_or_started_after_completed_jobs: Union[Unset, None, datetime.datetime] = UNSET,
    job_kinds: Union[Unset, None, str] = UNSET,
    args: Union[Unset, None, str] = UNSET,
    tag: Union[Unset, None, str] = UNSET,
    result: Union[Unset, None, str] = UNSET,
    allow_wildcards: Union[Unset, None, bool] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    is_skipped: Union[Unset, None, bool] = UNSET,
    is_flow_step: Union[Unset, None, bool] = UNSET,
    has_null_parent: Union[Unset, None, bool] = UNSET,
    success: Union[Unset, None, bool] = UNSET,
    all_workspaces: Union[Unset, None, bool] = UNSET,
    is_not_schedule: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["concurrency_key"] = concurrency_key

    params["row_limit"] = row_limit

    params["created_by"] = created_by

    params["label"] = label

    params["parent_job"] = parent_job

    params["script_path_exact"] = script_path_exact

    params["script_path_start"] = script_path_start

    params["schedule_path"] = schedule_path

    params["script_hash"] = script_hash

    json_started_before: Union[Unset, None, str] = UNSET
    if not isinstance(started_before, Unset):
        json_started_before = started_before.isoformat() if started_before else None

    params["started_before"] = json_started_before

    json_started_after: Union[Unset, None, str] = UNSET
    if not isinstance(started_after, Unset):
        json_started_after = started_after.isoformat() if started_after else None

    params["started_after"] = json_started_after

    json_created_or_started_before: Union[Unset, None, str] = UNSET
    if not isinstance(created_or_started_before, Unset):
        json_created_or_started_before = created_or_started_before.isoformat() if created_or_started_before else None

    params["created_or_started_before"] = json_created_or_started_before

    params["running"] = running

    params["scheduled_for_before_now"] = scheduled_for_before_now

    json_created_or_started_after: Union[Unset, None, str] = UNSET
    if not isinstance(created_or_started_after, Unset):
        json_created_or_started_after = created_or_started_after.isoformat() if created_or_started_after else None

    params["created_or_started_after"] = json_created_or_started_after

    json_created_or_started_after_completed_jobs: Union[Unset, None, str] = UNSET
    if not isinstance(created_or_started_after_completed_jobs, Unset):
        json_created_or_started_after_completed_jobs = (
            created_or_started_after_completed_jobs.isoformat() if created_or_started_after_completed_jobs else None
        )

    params["created_or_started_after_completed_jobs"] = json_created_or_started_after_completed_jobs

    params["job_kinds"] = job_kinds

    params["args"] = args

    params["tag"] = tag

    params["result"] = result

    params["allow_wildcards"] = allow_wildcards

    params["page"] = page

    params["per_page"] = per_page

    params["is_skipped"] = is_skipped

    params["is_flow_step"] = is_flow_step

    params["has_null_parent"] = has_null_parent

    params["success"] = success

    params["all_workspaces"] = all_workspaces

    params["is_not_schedule"] = is_not_schedule

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/concurrency_groups/list_jobs".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ListExtendedJobsResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListExtendedJobsResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ListExtendedJobsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    concurrency_key: Union[Unset, None, str] = UNSET,
    row_limit: Union[Unset, None, float] = UNSET,
    created_by: Union[Unset, None, str] = UNSET,
    label: Union[Unset, None, str] = UNSET,
    parent_job: Union[Unset, None, str] = UNSET,
    script_path_exact: Union[Unset, None, str] = UNSET,
    script_path_start: Union[Unset, None, str] = UNSET,
    schedule_path: Union[Unset, None, str] = UNSET,
    script_hash: Union[Unset, None, str] = UNSET,
    started_before: Union[Unset, None, datetime.datetime] = UNSET,
    started_after: Union[Unset, None, datetime.datetime] = UNSET,
    created_or_started_before: Union[Unset, None, datetime.datetime] = UNSET,
    running: Union[Unset, None, bool] = UNSET,
    scheduled_for_before_now: Union[Unset, None, bool] = UNSET,
    created_or_started_after: Union[Unset, None, datetime.datetime] = UNSET,
    created_or_started_after_completed_jobs: Union[Unset, None, datetime.datetime] = UNSET,
    job_kinds: Union[Unset, None, str] = UNSET,
    args: Union[Unset, None, str] = UNSET,
    tag: Union[Unset, None, str] = UNSET,
    result: Union[Unset, None, str] = UNSET,
    allow_wildcards: Union[Unset, None, bool] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    is_skipped: Union[Unset, None, bool] = UNSET,
    is_flow_step: Union[Unset, None, bool] = UNSET,
    has_null_parent: Union[Unset, None, bool] = UNSET,
    success: Union[Unset, None, bool] = UNSET,
    all_workspaces: Union[Unset, None, bool] = UNSET,
    is_not_schedule: Union[Unset, None, bool] = UNSET,
) -> Response[ListExtendedJobsResponse200]:
    """Get intervals of job runtime concurrency

    Args:
        workspace (str):
        concurrency_key (Union[Unset, None, str]):
        row_limit (Union[Unset, None, float]):
        created_by (Union[Unset, None, str]):
        label (Union[Unset, None, str]):
        parent_job (Union[Unset, None, str]):
        script_path_exact (Union[Unset, None, str]):
        script_path_start (Union[Unset, None, str]):
        schedule_path (Union[Unset, None, str]):
        script_hash (Union[Unset, None, str]):
        started_before (Union[Unset, None, datetime.datetime]):
        started_after (Union[Unset, None, datetime.datetime]):
        created_or_started_before (Union[Unset, None, datetime.datetime]):
        running (Union[Unset, None, bool]):
        scheduled_for_before_now (Union[Unset, None, bool]):
        created_or_started_after (Union[Unset, None, datetime.datetime]):
        created_or_started_after_completed_jobs (Union[Unset, None, datetime.datetime]):
        job_kinds (Union[Unset, None, str]):
        args (Union[Unset, None, str]):
        tag (Union[Unset, None, str]):
        result (Union[Unset, None, str]):
        allow_wildcards (Union[Unset, None, bool]):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):
        is_skipped (Union[Unset, None, bool]):
        is_flow_step (Union[Unset, None, bool]):
        has_null_parent (Union[Unset, None, bool]):
        success (Union[Unset, None, bool]):
        all_workspaces (Union[Unset, None, bool]):
        is_not_schedule (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListExtendedJobsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        concurrency_key=concurrency_key,
        row_limit=row_limit,
        created_by=created_by,
        label=label,
        parent_job=parent_job,
        script_path_exact=script_path_exact,
        script_path_start=script_path_start,
        schedule_path=schedule_path,
        script_hash=script_hash,
        started_before=started_before,
        started_after=started_after,
        created_or_started_before=created_or_started_before,
        running=running,
        scheduled_for_before_now=scheduled_for_before_now,
        created_or_started_after=created_or_started_after,
        created_or_started_after_completed_jobs=created_or_started_after_completed_jobs,
        job_kinds=job_kinds,
        args=args,
        tag=tag,
        result=result,
        allow_wildcards=allow_wildcards,
        page=page,
        per_page=per_page,
        is_skipped=is_skipped,
        is_flow_step=is_flow_step,
        has_null_parent=has_null_parent,
        success=success,
        all_workspaces=all_workspaces,
        is_not_schedule=is_not_schedule,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    concurrency_key: Union[Unset, None, str] = UNSET,
    row_limit: Union[Unset, None, float] = UNSET,
    created_by: Union[Unset, None, str] = UNSET,
    label: Union[Unset, None, str] = UNSET,
    parent_job: Union[Unset, None, str] = UNSET,
    script_path_exact: Union[Unset, None, str] = UNSET,
    script_path_start: Union[Unset, None, str] = UNSET,
    schedule_path: Union[Unset, None, str] = UNSET,
    script_hash: Union[Unset, None, str] = UNSET,
    started_before: Union[Unset, None, datetime.datetime] = UNSET,
    started_after: Union[Unset, None, datetime.datetime] = UNSET,
    created_or_started_before: Union[Unset, None, datetime.datetime] = UNSET,
    running: Union[Unset, None, bool] = UNSET,
    scheduled_for_before_now: Union[Unset, None, bool] = UNSET,
    created_or_started_after: Union[Unset, None, datetime.datetime] = UNSET,
    created_or_started_after_completed_jobs: Union[Unset, None, datetime.datetime] = UNSET,
    job_kinds: Union[Unset, None, str] = UNSET,
    args: Union[Unset, None, str] = UNSET,
    tag: Union[Unset, None, str] = UNSET,
    result: Union[Unset, None, str] = UNSET,
    allow_wildcards: Union[Unset, None, bool] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    is_skipped: Union[Unset, None, bool] = UNSET,
    is_flow_step: Union[Unset, None, bool] = UNSET,
    has_null_parent: Union[Unset, None, bool] = UNSET,
    success: Union[Unset, None, bool] = UNSET,
    all_workspaces: Union[Unset, None, bool] = UNSET,
    is_not_schedule: Union[Unset, None, bool] = UNSET,
) -> Optional[ListExtendedJobsResponse200]:
    """Get intervals of job runtime concurrency

    Args:
        workspace (str):
        concurrency_key (Union[Unset, None, str]):
        row_limit (Union[Unset, None, float]):
        created_by (Union[Unset, None, str]):
        label (Union[Unset, None, str]):
        parent_job (Union[Unset, None, str]):
        script_path_exact (Union[Unset, None, str]):
        script_path_start (Union[Unset, None, str]):
        schedule_path (Union[Unset, None, str]):
        script_hash (Union[Unset, None, str]):
        started_before (Union[Unset, None, datetime.datetime]):
        started_after (Union[Unset, None, datetime.datetime]):
        created_or_started_before (Union[Unset, None, datetime.datetime]):
        running (Union[Unset, None, bool]):
        scheduled_for_before_now (Union[Unset, None, bool]):
        created_or_started_after (Union[Unset, None, datetime.datetime]):
        created_or_started_after_completed_jobs (Union[Unset, None, datetime.datetime]):
        job_kinds (Union[Unset, None, str]):
        args (Union[Unset, None, str]):
        tag (Union[Unset, None, str]):
        result (Union[Unset, None, str]):
        allow_wildcards (Union[Unset, None, bool]):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):
        is_skipped (Union[Unset, None, bool]):
        is_flow_step (Union[Unset, None, bool]):
        has_null_parent (Union[Unset, None, bool]):
        success (Union[Unset, None, bool]):
        all_workspaces (Union[Unset, None, bool]):
        is_not_schedule (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListExtendedJobsResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        concurrency_key=concurrency_key,
        row_limit=row_limit,
        created_by=created_by,
        label=label,
        parent_job=parent_job,
        script_path_exact=script_path_exact,
        script_path_start=script_path_start,
        schedule_path=schedule_path,
        script_hash=script_hash,
        started_before=started_before,
        started_after=started_after,
        created_or_started_before=created_or_started_before,
        running=running,
        scheduled_for_before_now=scheduled_for_before_now,
        created_or_started_after=created_or_started_after,
        created_or_started_after_completed_jobs=created_or_started_after_completed_jobs,
        job_kinds=job_kinds,
        args=args,
        tag=tag,
        result=result,
        allow_wildcards=allow_wildcards,
        page=page,
        per_page=per_page,
        is_skipped=is_skipped,
        is_flow_step=is_flow_step,
        has_null_parent=has_null_parent,
        success=success,
        all_workspaces=all_workspaces,
        is_not_schedule=is_not_schedule,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    concurrency_key: Union[Unset, None, str] = UNSET,
    row_limit: Union[Unset, None, float] = UNSET,
    created_by: Union[Unset, None, str] = UNSET,
    label: Union[Unset, None, str] = UNSET,
    parent_job: Union[Unset, None, str] = UNSET,
    script_path_exact: Union[Unset, None, str] = UNSET,
    script_path_start: Union[Unset, None, str] = UNSET,
    schedule_path: Union[Unset, None, str] = UNSET,
    script_hash: Union[Unset, None, str] = UNSET,
    started_before: Union[Unset, None, datetime.datetime] = UNSET,
    started_after: Union[Unset, None, datetime.datetime] = UNSET,
    created_or_started_before: Union[Unset, None, datetime.datetime] = UNSET,
    running: Union[Unset, None, bool] = UNSET,
    scheduled_for_before_now: Union[Unset, None, bool] = UNSET,
    created_or_started_after: Union[Unset, None, datetime.datetime] = UNSET,
    created_or_started_after_completed_jobs: Union[Unset, None, datetime.datetime] = UNSET,
    job_kinds: Union[Unset, None, str] = UNSET,
    args: Union[Unset, None, str] = UNSET,
    tag: Union[Unset, None, str] = UNSET,
    result: Union[Unset, None, str] = UNSET,
    allow_wildcards: Union[Unset, None, bool] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    is_skipped: Union[Unset, None, bool] = UNSET,
    is_flow_step: Union[Unset, None, bool] = UNSET,
    has_null_parent: Union[Unset, None, bool] = UNSET,
    success: Union[Unset, None, bool] = UNSET,
    all_workspaces: Union[Unset, None, bool] = UNSET,
    is_not_schedule: Union[Unset, None, bool] = UNSET,
) -> Response[ListExtendedJobsResponse200]:
    """Get intervals of job runtime concurrency

    Args:
        workspace (str):
        concurrency_key (Union[Unset, None, str]):
        row_limit (Union[Unset, None, float]):
        created_by (Union[Unset, None, str]):
        label (Union[Unset, None, str]):
        parent_job (Union[Unset, None, str]):
        script_path_exact (Union[Unset, None, str]):
        script_path_start (Union[Unset, None, str]):
        schedule_path (Union[Unset, None, str]):
        script_hash (Union[Unset, None, str]):
        started_before (Union[Unset, None, datetime.datetime]):
        started_after (Union[Unset, None, datetime.datetime]):
        created_or_started_before (Union[Unset, None, datetime.datetime]):
        running (Union[Unset, None, bool]):
        scheduled_for_before_now (Union[Unset, None, bool]):
        created_or_started_after (Union[Unset, None, datetime.datetime]):
        created_or_started_after_completed_jobs (Union[Unset, None, datetime.datetime]):
        job_kinds (Union[Unset, None, str]):
        args (Union[Unset, None, str]):
        tag (Union[Unset, None, str]):
        result (Union[Unset, None, str]):
        allow_wildcards (Union[Unset, None, bool]):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):
        is_skipped (Union[Unset, None, bool]):
        is_flow_step (Union[Unset, None, bool]):
        has_null_parent (Union[Unset, None, bool]):
        success (Union[Unset, None, bool]):
        all_workspaces (Union[Unset, None, bool]):
        is_not_schedule (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListExtendedJobsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        concurrency_key=concurrency_key,
        row_limit=row_limit,
        created_by=created_by,
        label=label,
        parent_job=parent_job,
        script_path_exact=script_path_exact,
        script_path_start=script_path_start,
        schedule_path=schedule_path,
        script_hash=script_hash,
        started_before=started_before,
        started_after=started_after,
        created_or_started_before=created_or_started_before,
        running=running,
        scheduled_for_before_now=scheduled_for_before_now,
        created_or_started_after=created_or_started_after,
        created_or_started_after_completed_jobs=created_or_started_after_completed_jobs,
        job_kinds=job_kinds,
        args=args,
        tag=tag,
        result=result,
        allow_wildcards=allow_wildcards,
        page=page,
        per_page=per_page,
        is_skipped=is_skipped,
        is_flow_step=is_flow_step,
        has_null_parent=has_null_parent,
        success=success,
        all_workspaces=all_workspaces,
        is_not_schedule=is_not_schedule,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    concurrency_key: Union[Unset, None, str] = UNSET,
    row_limit: Union[Unset, None, float] = UNSET,
    created_by: Union[Unset, None, str] = UNSET,
    label: Union[Unset, None, str] = UNSET,
    parent_job: Union[Unset, None, str] = UNSET,
    script_path_exact: Union[Unset, None, str] = UNSET,
    script_path_start: Union[Unset, None, str] = UNSET,
    schedule_path: Union[Unset, None, str] = UNSET,
    script_hash: Union[Unset, None, str] = UNSET,
    started_before: Union[Unset, None, datetime.datetime] = UNSET,
    started_after: Union[Unset, None, datetime.datetime] = UNSET,
    created_or_started_before: Union[Unset, None, datetime.datetime] = UNSET,
    running: Union[Unset, None, bool] = UNSET,
    scheduled_for_before_now: Union[Unset, None, bool] = UNSET,
    created_or_started_after: Union[Unset, None, datetime.datetime] = UNSET,
    created_or_started_after_completed_jobs: Union[Unset, None, datetime.datetime] = UNSET,
    job_kinds: Union[Unset, None, str] = UNSET,
    args: Union[Unset, None, str] = UNSET,
    tag: Union[Unset, None, str] = UNSET,
    result: Union[Unset, None, str] = UNSET,
    allow_wildcards: Union[Unset, None, bool] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    is_skipped: Union[Unset, None, bool] = UNSET,
    is_flow_step: Union[Unset, None, bool] = UNSET,
    has_null_parent: Union[Unset, None, bool] = UNSET,
    success: Union[Unset, None, bool] = UNSET,
    all_workspaces: Union[Unset, None, bool] = UNSET,
    is_not_schedule: Union[Unset, None, bool] = UNSET,
) -> Optional[ListExtendedJobsResponse200]:
    """Get intervals of job runtime concurrency

    Args:
        workspace (str):
        concurrency_key (Union[Unset, None, str]):
        row_limit (Union[Unset, None, float]):
        created_by (Union[Unset, None, str]):
        label (Union[Unset, None, str]):
        parent_job (Union[Unset, None, str]):
        script_path_exact (Union[Unset, None, str]):
        script_path_start (Union[Unset, None, str]):
        schedule_path (Union[Unset, None, str]):
        script_hash (Union[Unset, None, str]):
        started_before (Union[Unset, None, datetime.datetime]):
        started_after (Union[Unset, None, datetime.datetime]):
        created_or_started_before (Union[Unset, None, datetime.datetime]):
        running (Union[Unset, None, bool]):
        scheduled_for_before_now (Union[Unset, None, bool]):
        created_or_started_after (Union[Unset, None, datetime.datetime]):
        created_or_started_after_completed_jobs (Union[Unset, None, datetime.datetime]):
        job_kinds (Union[Unset, None, str]):
        args (Union[Unset, None, str]):
        tag (Union[Unset, None, str]):
        result (Union[Unset, None, str]):
        allow_wildcards (Union[Unset, None, bool]):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):
        is_skipped (Union[Unset, None, bool]):
        is_flow_step (Union[Unset, None, bool]):
        has_null_parent (Union[Unset, None, bool]):
        success (Union[Unset, None, bool]):
        all_workspaces (Union[Unset, None, bool]):
        is_not_schedule (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListExtendedJobsResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            concurrency_key=concurrency_key,
            row_limit=row_limit,
            created_by=created_by,
            label=label,
            parent_job=parent_job,
            script_path_exact=script_path_exact,
            script_path_start=script_path_start,
            schedule_path=schedule_path,
            script_hash=script_hash,
            started_before=started_before,
            started_after=started_after,
            created_or_started_before=created_or_started_before,
            running=running,
            scheduled_for_before_now=scheduled_for_before_now,
            created_or_started_after=created_or_started_after,
            created_or_started_after_completed_jobs=created_or_started_after_completed_jobs,
            job_kinds=job_kinds,
            args=args,
            tag=tag,
            result=result,
            allow_wildcards=allow_wildcards,
            page=page,
            per_page=per_page,
            is_skipped=is_skipped,
            is_flow_step=is_flow_step,
            has_null_parent=has_null_parent,
            success=success,
            all_workspaces=all_workspaces,
            is_not_schedule=is_not_schedule,
        )
    ).parsed
