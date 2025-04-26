import datetime
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_jobs_response_200_item_type_0 import ListJobsResponse200ItemType0
from ...models.list_jobs_response_200_item_type_1 import ListJobsResponse200ItemType1
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    created_by: Union[Unset, None, str] = UNSET,
    label: Union[Unset, None, str] = UNSET,
    worker: Union[Unset, None, str] = UNSET,
    parent_job: Union[Unset, None, str] = UNSET,
    script_path_exact: Union[Unset, None, str] = UNSET,
    script_path_start: Union[Unset, None, str] = UNSET,
    schedule_path: Union[Unset, None, str] = UNSET,
    script_hash: Union[Unset, None, str] = UNSET,
    started_before: Union[Unset, None, datetime.datetime] = UNSET,
    started_after: Union[Unset, None, datetime.datetime] = UNSET,
    created_before: Union[Unset, None, datetime.datetime] = UNSET,
    created_after: Union[Unset, None, datetime.datetime] = UNSET,
    created_or_started_before: Union[Unset, None, datetime.datetime] = UNSET,
    running: Union[Unset, None, bool] = UNSET,
    scheduled_for_before_now: Union[Unset, None, bool] = UNSET,
    created_or_started_after: Union[Unset, None, datetime.datetime] = UNSET,
    created_or_started_after_completed_jobs: Union[Unset, None, datetime.datetime] = UNSET,
    job_kinds: Union[Unset, None, str] = UNSET,
    suspended: Union[Unset, None, bool] = UNSET,
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
    params["created_by"] = created_by

    params["label"] = label

    params["worker"] = worker

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

    json_created_before: Union[Unset, None, str] = UNSET
    if not isinstance(created_before, Unset):
        json_created_before = created_before.isoformat() if created_before else None

    params["created_before"] = json_created_before

    json_created_after: Union[Unset, None, str] = UNSET
    if not isinstance(created_after, Unset):
        json_created_after = created_after.isoformat() if created_after else None

    params["created_after"] = json_created_after

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

    params["suspended"] = suspended

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
        "url": "/w/{workspace}/jobs/list".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List[Union["ListJobsResponse200ItemType0", "ListJobsResponse200ItemType1"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:

            def _parse_response_200_item(
                data: object,
            ) -> Union["ListJobsResponse200ItemType0", "ListJobsResponse200ItemType1"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    response_200_item_type_0 = ListJobsResponse200ItemType0.from_dict(data)

                    return response_200_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_item_type_1 = ListJobsResponse200ItemType1.from_dict(data)

                return response_200_item_type_1

            response_200_item = _parse_response_200_item(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List[Union["ListJobsResponse200ItemType0", "ListJobsResponse200ItemType1"]]]:
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
    created_by: Union[Unset, None, str] = UNSET,
    label: Union[Unset, None, str] = UNSET,
    worker: Union[Unset, None, str] = UNSET,
    parent_job: Union[Unset, None, str] = UNSET,
    script_path_exact: Union[Unset, None, str] = UNSET,
    script_path_start: Union[Unset, None, str] = UNSET,
    schedule_path: Union[Unset, None, str] = UNSET,
    script_hash: Union[Unset, None, str] = UNSET,
    started_before: Union[Unset, None, datetime.datetime] = UNSET,
    started_after: Union[Unset, None, datetime.datetime] = UNSET,
    created_before: Union[Unset, None, datetime.datetime] = UNSET,
    created_after: Union[Unset, None, datetime.datetime] = UNSET,
    created_or_started_before: Union[Unset, None, datetime.datetime] = UNSET,
    running: Union[Unset, None, bool] = UNSET,
    scheduled_for_before_now: Union[Unset, None, bool] = UNSET,
    created_or_started_after: Union[Unset, None, datetime.datetime] = UNSET,
    created_or_started_after_completed_jobs: Union[Unset, None, datetime.datetime] = UNSET,
    job_kinds: Union[Unset, None, str] = UNSET,
    suspended: Union[Unset, None, bool] = UNSET,
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
) -> Response[List[Union["ListJobsResponse200ItemType0", "ListJobsResponse200ItemType1"]]]:
    """list all jobs

    Args:
        workspace (str):
        created_by (Union[Unset, None, str]):
        label (Union[Unset, None, str]):
        worker (Union[Unset, None, str]):
        parent_job (Union[Unset, None, str]):
        script_path_exact (Union[Unset, None, str]):
        script_path_start (Union[Unset, None, str]):
        schedule_path (Union[Unset, None, str]):
        script_hash (Union[Unset, None, str]):
        started_before (Union[Unset, None, datetime.datetime]):
        started_after (Union[Unset, None, datetime.datetime]):
        created_before (Union[Unset, None, datetime.datetime]):
        created_after (Union[Unset, None, datetime.datetime]):
        created_or_started_before (Union[Unset, None, datetime.datetime]):
        running (Union[Unset, None, bool]):
        scheduled_for_before_now (Union[Unset, None, bool]):
        created_or_started_after (Union[Unset, None, datetime.datetime]):
        created_or_started_after_completed_jobs (Union[Unset, None, datetime.datetime]):
        job_kinds (Union[Unset, None, str]):
        suspended (Union[Unset, None, bool]):
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
        Response[List[Union['ListJobsResponse200ItemType0', 'ListJobsResponse200ItemType1']]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        created_by=created_by,
        label=label,
        worker=worker,
        parent_job=parent_job,
        script_path_exact=script_path_exact,
        script_path_start=script_path_start,
        schedule_path=schedule_path,
        script_hash=script_hash,
        started_before=started_before,
        started_after=started_after,
        created_before=created_before,
        created_after=created_after,
        created_or_started_before=created_or_started_before,
        running=running,
        scheduled_for_before_now=scheduled_for_before_now,
        created_or_started_after=created_or_started_after,
        created_or_started_after_completed_jobs=created_or_started_after_completed_jobs,
        job_kinds=job_kinds,
        suspended=suspended,
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
    created_by: Union[Unset, None, str] = UNSET,
    label: Union[Unset, None, str] = UNSET,
    worker: Union[Unset, None, str] = UNSET,
    parent_job: Union[Unset, None, str] = UNSET,
    script_path_exact: Union[Unset, None, str] = UNSET,
    script_path_start: Union[Unset, None, str] = UNSET,
    schedule_path: Union[Unset, None, str] = UNSET,
    script_hash: Union[Unset, None, str] = UNSET,
    started_before: Union[Unset, None, datetime.datetime] = UNSET,
    started_after: Union[Unset, None, datetime.datetime] = UNSET,
    created_before: Union[Unset, None, datetime.datetime] = UNSET,
    created_after: Union[Unset, None, datetime.datetime] = UNSET,
    created_or_started_before: Union[Unset, None, datetime.datetime] = UNSET,
    running: Union[Unset, None, bool] = UNSET,
    scheduled_for_before_now: Union[Unset, None, bool] = UNSET,
    created_or_started_after: Union[Unset, None, datetime.datetime] = UNSET,
    created_or_started_after_completed_jobs: Union[Unset, None, datetime.datetime] = UNSET,
    job_kinds: Union[Unset, None, str] = UNSET,
    suspended: Union[Unset, None, bool] = UNSET,
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
) -> Optional[List[Union["ListJobsResponse200ItemType0", "ListJobsResponse200ItemType1"]]]:
    """list all jobs

    Args:
        workspace (str):
        created_by (Union[Unset, None, str]):
        label (Union[Unset, None, str]):
        worker (Union[Unset, None, str]):
        parent_job (Union[Unset, None, str]):
        script_path_exact (Union[Unset, None, str]):
        script_path_start (Union[Unset, None, str]):
        schedule_path (Union[Unset, None, str]):
        script_hash (Union[Unset, None, str]):
        started_before (Union[Unset, None, datetime.datetime]):
        started_after (Union[Unset, None, datetime.datetime]):
        created_before (Union[Unset, None, datetime.datetime]):
        created_after (Union[Unset, None, datetime.datetime]):
        created_or_started_before (Union[Unset, None, datetime.datetime]):
        running (Union[Unset, None, bool]):
        scheduled_for_before_now (Union[Unset, None, bool]):
        created_or_started_after (Union[Unset, None, datetime.datetime]):
        created_or_started_after_completed_jobs (Union[Unset, None, datetime.datetime]):
        job_kinds (Union[Unset, None, str]):
        suspended (Union[Unset, None, bool]):
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
        List[Union['ListJobsResponse200ItemType0', 'ListJobsResponse200ItemType1']]
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        created_by=created_by,
        label=label,
        worker=worker,
        parent_job=parent_job,
        script_path_exact=script_path_exact,
        script_path_start=script_path_start,
        schedule_path=schedule_path,
        script_hash=script_hash,
        started_before=started_before,
        started_after=started_after,
        created_before=created_before,
        created_after=created_after,
        created_or_started_before=created_or_started_before,
        running=running,
        scheduled_for_before_now=scheduled_for_before_now,
        created_or_started_after=created_or_started_after,
        created_or_started_after_completed_jobs=created_or_started_after_completed_jobs,
        job_kinds=job_kinds,
        suspended=suspended,
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
    created_by: Union[Unset, None, str] = UNSET,
    label: Union[Unset, None, str] = UNSET,
    worker: Union[Unset, None, str] = UNSET,
    parent_job: Union[Unset, None, str] = UNSET,
    script_path_exact: Union[Unset, None, str] = UNSET,
    script_path_start: Union[Unset, None, str] = UNSET,
    schedule_path: Union[Unset, None, str] = UNSET,
    script_hash: Union[Unset, None, str] = UNSET,
    started_before: Union[Unset, None, datetime.datetime] = UNSET,
    started_after: Union[Unset, None, datetime.datetime] = UNSET,
    created_before: Union[Unset, None, datetime.datetime] = UNSET,
    created_after: Union[Unset, None, datetime.datetime] = UNSET,
    created_or_started_before: Union[Unset, None, datetime.datetime] = UNSET,
    running: Union[Unset, None, bool] = UNSET,
    scheduled_for_before_now: Union[Unset, None, bool] = UNSET,
    created_or_started_after: Union[Unset, None, datetime.datetime] = UNSET,
    created_or_started_after_completed_jobs: Union[Unset, None, datetime.datetime] = UNSET,
    job_kinds: Union[Unset, None, str] = UNSET,
    suspended: Union[Unset, None, bool] = UNSET,
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
) -> Response[List[Union["ListJobsResponse200ItemType0", "ListJobsResponse200ItemType1"]]]:
    """list all jobs

    Args:
        workspace (str):
        created_by (Union[Unset, None, str]):
        label (Union[Unset, None, str]):
        worker (Union[Unset, None, str]):
        parent_job (Union[Unset, None, str]):
        script_path_exact (Union[Unset, None, str]):
        script_path_start (Union[Unset, None, str]):
        schedule_path (Union[Unset, None, str]):
        script_hash (Union[Unset, None, str]):
        started_before (Union[Unset, None, datetime.datetime]):
        started_after (Union[Unset, None, datetime.datetime]):
        created_before (Union[Unset, None, datetime.datetime]):
        created_after (Union[Unset, None, datetime.datetime]):
        created_or_started_before (Union[Unset, None, datetime.datetime]):
        running (Union[Unset, None, bool]):
        scheduled_for_before_now (Union[Unset, None, bool]):
        created_or_started_after (Union[Unset, None, datetime.datetime]):
        created_or_started_after_completed_jobs (Union[Unset, None, datetime.datetime]):
        job_kinds (Union[Unset, None, str]):
        suspended (Union[Unset, None, bool]):
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
        Response[List[Union['ListJobsResponse200ItemType0', 'ListJobsResponse200ItemType1']]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        created_by=created_by,
        label=label,
        worker=worker,
        parent_job=parent_job,
        script_path_exact=script_path_exact,
        script_path_start=script_path_start,
        schedule_path=schedule_path,
        script_hash=script_hash,
        started_before=started_before,
        started_after=started_after,
        created_before=created_before,
        created_after=created_after,
        created_or_started_before=created_or_started_before,
        running=running,
        scheduled_for_before_now=scheduled_for_before_now,
        created_or_started_after=created_or_started_after,
        created_or_started_after_completed_jobs=created_or_started_after_completed_jobs,
        job_kinds=job_kinds,
        suspended=suspended,
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
    created_by: Union[Unset, None, str] = UNSET,
    label: Union[Unset, None, str] = UNSET,
    worker: Union[Unset, None, str] = UNSET,
    parent_job: Union[Unset, None, str] = UNSET,
    script_path_exact: Union[Unset, None, str] = UNSET,
    script_path_start: Union[Unset, None, str] = UNSET,
    schedule_path: Union[Unset, None, str] = UNSET,
    script_hash: Union[Unset, None, str] = UNSET,
    started_before: Union[Unset, None, datetime.datetime] = UNSET,
    started_after: Union[Unset, None, datetime.datetime] = UNSET,
    created_before: Union[Unset, None, datetime.datetime] = UNSET,
    created_after: Union[Unset, None, datetime.datetime] = UNSET,
    created_or_started_before: Union[Unset, None, datetime.datetime] = UNSET,
    running: Union[Unset, None, bool] = UNSET,
    scheduled_for_before_now: Union[Unset, None, bool] = UNSET,
    created_or_started_after: Union[Unset, None, datetime.datetime] = UNSET,
    created_or_started_after_completed_jobs: Union[Unset, None, datetime.datetime] = UNSET,
    job_kinds: Union[Unset, None, str] = UNSET,
    suspended: Union[Unset, None, bool] = UNSET,
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
) -> Optional[List[Union["ListJobsResponse200ItemType0", "ListJobsResponse200ItemType1"]]]:
    """list all jobs

    Args:
        workspace (str):
        created_by (Union[Unset, None, str]):
        label (Union[Unset, None, str]):
        worker (Union[Unset, None, str]):
        parent_job (Union[Unset, None, str]):
        script_path_exact (Union[Unset, None, str]):
        script_path_start (Union[Unset, None, str]):
        schedule_path (Union[Unset, None, str]):
        script_hash (Union[Unset, None, str]):
        started_before (Union[Unset, None, datetime.datetime]):
        started_after (Union[Unset, None, datetime.datetime]):
        created_before (Union[Unset, None, datetime.datetime]):
        created_after (Union[Unset, None, datetime.datetime]):
        created_or_started_before (Union[Unset, None, datetime.datetime]):
        running (Union[Unset, None, bool]):
        scheduled_for_before_now (Union[Unset, None, bool]):
        created_or_started_after (Union[Unset, None, datetime.datetime]):
        created_or_started_after_completed_jobs (Union[Unset, None, datetime.datetime]):
        job_kinds (Union[Unset, None, str]):
        suspended (Union[Unset, None, bool]):
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
        List[Union['ListJobsResponse200ItemType0', 'ListJobsResponse200ItemType1']]
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            created_by=created_by,
            label=label,
            worker=worker,
            parent_job=parent_job,
            script_path_exact=script_path_exact,
            script_path_start=script_path_start,
            schedule_path=schedule_path,
            script_hash=script_hash,
            started_before=started_before,
            started_after=started_after,
            created_before=created_before,
            created_after=created_after,
            created_or_started_before=created_or_started_before,
            running=running,
            scheduled_for_before_now=scheduled_for_before_now,
            created_or_started_after=created_or_started_after,
            created_or_started_after_completed_jobs=created_or_started_after_completed_jobs,
            job_kinds=job_kinds,
            suspended=suspended,
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
