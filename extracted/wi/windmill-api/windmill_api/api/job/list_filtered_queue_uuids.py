import datetime
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    order_desc: Union[Unset, None, bool] = UNSET,
    created_by: Union[Unset, None, str] = UNSET,
    parent_job: Union[Unset, None, str] = UNSET,
    script_path_exact: Union[Unset, None, str] = UNSET,
    script_path_start: Union[Unset, None, str] = UNSET,
    schedule_path: Union[Unset, None, str] = UNSET,
    script_hash: Union[Unset, None, str] = UNSET,
    started_before: Union[Unset, None, datetime.datetime] = UNSET,
    started_after: Union[Unset, None, datetime.datetime] = UNSET,
    success: Union[Unset, None, bool] = UNSET,
    scheduled_for_before_now: Union[Unset, None, bool] = UNSET,
    job_kinds: Union[Unset, None, str] = UNSET,
    suspended: Union[Unset, None, bool] = UNSET,
    running: Union[Unset, None, bool] = UNSET,
    args: Union[Unset, None, str] = UNSET,
    result: Union[Unset, None, str] = UNSET,
    allow_wildcards: Union[Unset, None, bool] = UNSET,
    tag: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    concurrency_key: Union[Unset, None, str] = UNSET,
    all_workspaces: Union[Unset, None, bool] = UNSET,
    is_not_schedule: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["order_desc"] = order_desc

    params["created_by"] = created_by

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

    params["success"] = success

    params["scheduled_for_before_now"] = scheduled_for_before_now

    params["job_kinds"] = job_kinds

    params["suspended"] = suspended

    params["running"] = running

    params["args"] = args

    params["result"] = result

    params["allow_wildcards"] = allow_wildcards

    params["tag"] = tag

    params["page"] = page

    params["per_page"] = per_page

    params["concurrency_key"] = concurrency_key

    params["all_workspaces"] = all_workspaces

    params["is_not_schedule"] = is_not_schedule

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/jobs/queue/list_filtered_uuids".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[List[str]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(List[str], response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[List[str]]:
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
    order_desc: Union[Unset, None, bool] = UNSET,
    created_by: Union[Unset, None, str] = UNSET,
    parent_job: Union[Unset, None, str] = UNSET,
    script_path_exact: Union[Unset, None, str] = UNSET,
    script_path_start: Union[Unset, None, str] = UNSET,
    schedule_path: Union[Unset, None, str] = UNSET,
    script_hash: Union[Unset, None, str] = UNSET,
    started_before: Union[Unset, None, datetime.datetime] = UNSET,
    started_after: Union[Unset, None, datetime.datetime] = UNSET,
    success: Union[Unset, None, bool] = UNSET,
    scheduled_for_before_now: Union[Unset, None, bool] = UNSET,
    job_kinds: Union[Unset, None, str] = UNSET,
    suspended: Union[Unset, None, bool] = UNSET,
    running: Union[Unset, None, bool] = UNSET,
    args: Union[Unset, None, str] = UNSET,
    result: Union[Unset, None, str] = UNSET,
    allow_wildcards: Union[Unset, None, bool] = UNSET,
    tag: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    concurrency_key: Union[Unset, None, str] = UNSET,
    all_workspaces: Union[Unset, None, bool] = UNSET,
    is_not_schedule: Union[Unset, None, bool] = UNSET,
) -> Response[List[str]]:
    """get the ids of all queued jobs matching the given filters

    Args:
        workspace (str):
        order_desc (Union[Unset, None, bool]):
        created_by (Union[Unset, None, str]):
        parent_job (Union[Unset, None, str]):
        script_path_exact (Union[Unset, None, str]):
        script_path_start (Union[Unset, None, str]):
        schedule_path (Union[Unset, None, str]):
        script_hash (Union[Unset, None, str]):
        started_before (Union[Unset, None, datetime.datetime]):
        started_after (Union[Unset, None, datetime.datetime]):
        success (Union[Unset, None, bool]):
        scheduled_for_before_now (Union[Unset, None, bool]):
        job_kinds (Union[Unset, None, str]):
        suspended (Union[Unset, None, bool]):
        running (Union[Unset, None, bool]):
        args (Union[Unset, None, str]):
        result (Union[Unset, None, str]):
        allow_wildcards (Union[Unset, None, bool]):
        tag (Union[Unset, None, str]):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):
        concurrency_key (Union[Unset, None, str]):
        all_workspaces (Union[Unset, None, bool]):
        is_not_schedule (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List[str]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        order_desc=order_desc,
        created_by=created_by,
        parent_job=parent_job,
        script_path_exact=script_path_exact,
        script_path_start=script_path_start,
        schedule_path=schedule_path,
        script_hash=script_hash,
        started_before=started_before,
        started_after=started_after,
        success=success,
        scheduled_for_before_now=scheduled_for_before_now,
        job_kinds=job_kinds,
        suspended=suspended,
        running=running,
        args=args,
        result=result,
        allow_wildcards=allow_wildcards,
        tag=tag,
        page=page,
        per_page=per_page,
        concurrency_key=concurrency_key,
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
    order_desc: Union[Unset, None, bool] = UNSET,
    created_by: Union[Unset, None, str] = UNSET,
    parent_job: Union[Unset, None, str] = UNSET,
    script_path_exact: Union[Unset, None, str] = UNSET,
    script_path_start: Union[Unset, None, str] = UNSET,
    schedule_path: Union[Unset, None, str] = UNSET,
    script_hash: Union[Unset, None, str] = UNSET,
    started_before: Union[Unset, None, datetime.datetime] = UNSET,
    started_after: Union[Unset, None, datetime.datetime] = UNSET,
    success: Union[Unset, None, bool] = UNSET,
    scheduled_for_before_now: Union[Unset, None, bool] = UNSET,
    job_kinds: Union[Unset, None, str] = UNSET,
    suspended: Union[Unset, None, bool] = UNSET,
    running: Union[Unset, None, bool] = UNSET,
    args: Union[Unset, None, str] = UNSET,
    result: Union[Unset, None, str] = UNSET,
    allow_wildcards: Union[Unset, None, bool] = UNSET,
    tag: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    concurrency_key: Union[Unset, None, str] = UNSET,
    all_workspaces: Union[Unset, None, bool] = UNSET,
    is_not_schedule: Union[Unset, None, bool] = UNSET,
) -> Optional[List[str]]:
    """get the ids of all queued jobs matching the given filters

    Args:
        workspace (str):
        order_desc (Union[Unset, None, bool]):
        created_by (Union[Unset, None, str]):
        parent_job (Union[Unset, None, str]):
        script_path_exact (Union[Unset, None, str]):
        script_path_start (Union[Unset, None, str]):
        schedule_path (Union[Unset, None, str]):
        script_hash (Union[Unset, None, str]):
        started_before (Union[Unset, None, datetime.datetime]):
        started_after (Union[Unset, None, datetime.datetime]):
        success (Union[Unset, None, bool]):
        scheduled_for_before_now (Union[Unset, None, bool]):
        job_kinds (Union[Unset, None, str]):
        suspended (Union[Unset, None, bool]):
        running (Union[Unset, None, bool]):
        args (Union[Unset, None, str]):
        result (Union[Unset, None, str]):
        allow_wildcards (Union[Unset, None, bool]):
        tag (Union[Unset, None, str]):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):
        concurrency_key (Union[Unset, None, str]):
        all_workspaces (Union[Unset, None, bool]):
        is_not_schedule (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List[str]
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        order_desc=order_desc,
        created_by=created_by,
        parent_job=parent_job,
        script_path_exact=script_path_exact,
        script_path_start=script_path_start,
        schedule_path=schedule_path,
        script_hash=script_hash,
        started_before=started_before,
        started_after=started_after,
        success=success,
        scheduled_for_before_now=scheduled_for_before_now,
        job_kinds=job_kinds,
        suspended=suspended,
        running=running,
        args=args,
        result=result,
        allow_wildcards=allow_wildcards,
        tag=tag,
        page=page,
        per_page=per_page,
        concurrency_key=concurrency_key,
        all_workspaces=all_workspaces,
        is_not_schedule=is_not_schedule,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    order_desc: Union[Unset, None, bool] = UNSET,
    created_by: Union[Unset, None, str] = UNSET,
    parent_job: Union[Unset, None, str] = UNSET,
    script_path_exact: Union[Unset, None, str] = UNSET,
    script_path_start: Union[Unset, None, str] = UNSET,
    schedule_path: Union[Unset, None, str] = UNSET,
    script_hash: Union[Unset, None, str] = UNSET,
    started_before: Union[Unset, None, datetime.datetime] = UNSET,
    started_after: Union[Unset, None, datetime.datetime] = UNSET,
    success: Union[Unset, None, bool] = UNSET,
    scheduled_for_before_now: Union[Unset, None, bool] = UNSET,
    job_kinds: Union[Unset, None, str] = UNSET,
    suspended: Union[Unset, None, bool] = UNSET,
    running: Union[Unset, None, bool] = UNSET,
    args: Union[Unset, None, str] = UNSET,
    result: Union[Unset, None, str] = UNSET,
    allow_wildcards: Union[Unset, None, bool] = UNSET,
    tag: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    concurrency_key: Union[Unset, None, str] = UNSET,
    all_workspaces: Union[Unset, None, bool] = UNSET,
    is_not_schedule: Union[Unset, None, bool] = UNSET,
) -> Response[List[str]]:
    """get the ids of all queued jobs matching the given filters

    Args:
        workspace (str):
        order_desc (Union[Unset, None, bool]):
        created_by (Union[Unset, None, str]):
        parent_job (Union[Unset, None, str]):
        script_path_exact (Union[Unset, None, str]):
        script_path_start (Union[Unset, None, str]):
        schedule_path (Union[Unset, None, str]):
        script_hash (Union[Unset, None, str]):
        started_before (Union[Unset, None, datetime.datetime]):
        started_after (Union[Unset, None, datetime.datetime]):
        success (Union[Unset, None, bool]):
        scheduled_for_before_now (Union[Unset, None, bool]):
        job_kinds (Union[Unset, None, str]):
        suspended (Union[Unset, None, bool]):
        running (Union[Unset, None, bool]):
        args (Union[Unset, None, str]):
        result (Union[Unset, None, str]):
        allow_wildcards (Union[Unset, None, bool]):
        tag (Union[Unset, None, str]):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):
        concurrency_key (Union[Unset, None, str]):
        all_workspaces (Union[Unset, None, bool]):
        is_not_schedule (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List[str]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        order_desc=order_desc,
        created_by=created_by,
        parent_job=parent_job,
        script_path_exact=script_path_exact,
        script_path_start=script_path_start,
        schedule_path=schedule_path,
        script_hash=script_hash,
        started_before=started_before,
        started_after=started_after,
        success=success,
        scheduled_for_before_now=scheduled_for_before_now,
        job_kinds=job_kinds,
        suspended=suspended,
        running=running,
        args=args,
        result=result,
        allow_wildcards=allow_wildcards,
        tag=tag,
        page=page,
        per_page=per_page,
        concurrency_key=concurrency_key,
        all_workspaces=all_workspaces,
        is_not_schedule=is_not_schedule,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    order_desc: Union[Unset, None, bool] = UNSET,
    created_by: Union[Unset, None, str] = UNSET,
    parent_job: Union[Unset, None, str] = UNSET,
    script_path_exact: Union[Unset, None, str] = UNSET,
    script_path_start: Union[Unset, None, str] = UNSET,
    schedule_path: Union[Unset, None, str] = UNSET,
    script_hash: Union[Unset, None, str] = UNSET,
    started_before: Union[Unset, None, datetime.datetime] = UNSET,
    started_after: Union[Unset, None, datetime.datetime] = UNSET,
    success: Union[Unset, None, bool] = UNSET,
    scheduled_for_before_now: Union[Unset, None, bool] = UNSET,
    job_kinds: Union[Unset, None, str] = UNSET,
    suspended: Union[Unset, None, bool] = UNSET,
    running: Union[Unset, None, bool] = UNSET,
    args: Union[Unset, None, str] = UNSET,
    result: Union[Unset, None, str] = UNSET,
    allow_wildcards: Union[Unset, None, bool] = UNSET,
    tag: Union[Unset, None, str] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    concurrency_key: Union[Unset, None, str] = UNSET,
    all_workspaces: Union[Unset, None, bool] = UNSET,
    is_not_schedule: Union[Unset, None, bool] = UNSET,
) -> Optional[List[str]]:
    """get the ids of all queued jobs matching the given filters

    Args:
        workspace (str):
        order_desc (Union[Unset, None, bool]):
        created_by (Union[Unset, None, str]):
        parent_job (Union[Unset, None, str]):
        script_path_exact (Union[Unset, None, str]):
        script_path_start (Union[Unset, None, str]):
        schedule_path (Union[Unset, None, str]):
        script_hash (Union[Unset, None, str]):
        started_before (Union[Unset, None, datetime.datetime]):
        started_after (Union[Unset, None, datetime.datetime]):
        success (Union[Unset, None, bool]):
        scheduled_for_before_now (Union[Unset, None, bool]):
        job_kinds (Union[Unset, None, str]):
        suspended (Union[Unset, None, bool]):
        running (Union[Unset, None, bool]):
        args (Union[Unset, None, str]):
        result (Union[Unset, None, str]):
        allow_wildcards (Union[Unset, None, bool]):
        tag (Union[Unset, None, str]):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):
        concurrency_key (Union[Unset, None, str]):
        all_workspaces (Union[Unset, None, bool]):
        is_not_schedule (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List[str]
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            order_desc=order_desc,
            created_by=created_by,
            parent_job=parent_job,
            script_path_exact=script_path_exact,
            script_path_start=script_path_start,
            schedule_path=schedule_path,
            script_hash=script_hash,
            started_before=started_before,
            started_after=started_after,
            success=success,
            scheduled_for_before_now=scheduled_for_before_now,
            job_kinds=job_kinds,
            suspended=suspended,
            running=running,
            args=args,
            result=result,
            allow_wildcards=allow_wildcards,
            tag=tag,
            page=page,
            per_page=per_page,
            concurrency_key=concurrency_key,
            all_workspaces=all_workspaces,
            is_not_schedule=is_not_schedule,
        )
    ).parsed
