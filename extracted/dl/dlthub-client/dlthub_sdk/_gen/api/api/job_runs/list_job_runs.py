import datetime
from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.job_category import JobCategory
from ...models.job_type import JobType
from ...models.list_job_runs_order_type_0_item import ListJobRunsOrderType0Item
from ...models.list_job_runs_sort_type_0_item import ListJobRunsSortType0Item
from ...models.list_page_detailed_job_run_response import ListPageDetailedJobRunResponse
from ...models.run_status import RunStatus
from ...models.trigger_kind import TriggerKind
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace_id: UUID,
    *,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    q: None | str | Unset = UNSET,
    status: list[RunStatus] | None | Unset = UNSET,
    number: int | None | Unset = UNSET,
    job_id: None | Unset | UUID = UNSET,
    previous_job_run_id: None | Unset | UUID = UNSET,
    job_type: list[JobType] | None | Unset = UNSET,
    trigger: list[str] | None | Unset = UNSET,
    trigger_kind: list[TriggerKind] | None | Unset = UNSET,
    triggered_by: list[UUID] | None | Unset = UNSET,
    profile: list[str] | None | Unset = UNSET,
    min_duration_seconds: float | None | Unset = UNSET,
    max_duration_seconds: float | None | Unset = UNSET,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    timezone: str | Unset = "UTC",
    sort: list[ListJobRunsSortType0Item] | None | Unset = UNSET,
    order: list[ListJobRunsOrderType0Item] | None | Unset = UNSET,
    cursor: None | str | Unset = UNSET,
    include_system_job_runs: bool | Unset = False,
    downstream_job_runs_limit: int | None | Unset = UNSET,
    downstream_job_runs_category: JobCategory | None | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    json_q: None | str | Unset
    if isinstance(q, Unset):
        json_q = UNSET
    else:
        json_q = q
    params["q"] = json_q

    json_status: list[str] | None | Unset
    if isinstance(status, Unset):
        json_status = UNSET
    elif isinstance(status, list):
        json_status = []
        for status_type_0_item_data in status:
            status_type_0_item = status_type_0_item_data.value
            json_status.append(status_type_0_item)

    else:
        json_status = status
    params["status"] = json_status

    json_number: int | None | Unset
    if isinstance(number, Unset):
        json_number = UNSET
    else:
        json_number = number
    params["number"] = json_number

    json_job_id: None | str | Unset
    if isinstance(job_id, Unset):
        json_job_id = UNSET
    elif isinstance(job_id, UUID):
        json_job_id = str(job_id)
    else:
        json_job_id = job_id
    params["job_id"] = json_job_id

    json_previous_job_run_id: None | str | Unset
    if isinstance(previous_job_run_id, Unset):
        json_previous_job_run_id = UNSET
    elif isinstance(previous_job_run_id, UUID):
        json_previous_job_run_id = str(previous_job_run_id)
    else:
        json_previous_job_run_id = previous_job_run_id
    params["previous_job_run_id"] = json_previous_job_run_id

    json_job_type: list[str] | None | Unset
    if isinstance(job_type, Unset):
        json_job_type = UNSET
    elif isinstance(job_type, list):
        json_job_type = []
        for job_type_type_0_item_data in job_type:
            job_type_type_0_item = job_type_type_0_item_data.value
            json_job_type.append(job_type_type_0_item)

    else:
        json_job_type = job_type
    params["job_type"] = json_job_type

    json_trigger: list[str] | None | Unset
    if isinstance(trigger, Unset):
        json_trigger = UNSET
    elif isinstance(trigger, list):
        json_trigger = trigger

    else:
        json_trigger = trigger
    params["trigger"] = json_trigger

    json_trigger_kind: list[str] | None | Unset
    if isinstance(trigger_kind, Unset):
        json_trigger_kind = UNSET
    elif isinstance(trigger_kind, list):
        json_trigger_kind = []
        for trigger_kind_type_0_item_data in trigger_kind:
            trigger_kind_type_0_item = trigger_kind_type_0_item_data.value
            json_trigger_kind.append(trigger_kind_type_0_item)

    else:
        json_trigger_kind = trigger_kind
    params["trigger_kind"] = json_trigger_kind

    json_triggered_by: list[str] | None | Unset
    if isinstance(triggered_by, Unset):
        json_triggered_by = UNSET
    elif isinstance(triggered_by, list):
        json_triggered_by = []
        for triggered_by_type_0_item_data in triggered_by:
            triggered_by_type_0_item = str(triggered_by_type_0_item_data)
            json_triggered_by.append(triggered_by_type_0_item)

    else:
        json_triggered_by = triggered_by
    params["triggered_by"] = json_triggered_by

    json_profile: list[str] | None | Unset
    if isinstance(profile, Unset):
        json_profile = UNSET
    elif isinstance(profile, list):
        json_profile = profile

    else:
        json_profile = profile
    params["profile"] = json_profile

    json_min_duration_seconds: float | None | Unset
    if isinstance(min_duration_seconds, Unset):
        json_min_duration_seconds = UNSET
    else:
        json_min_duration_seconds = min_duration_seconds
    params["min_duration_seconds"] = json_min_duration_seconds

    json_max_duration_seconds: float | None | Unset
    if isinstance(max_duration_seconds, Unset):
        json_max_duration_seconds = UNSET
    else:
        json_max_duration_seconds = max_duration_seconds
    params["max_duration_seconds"] = json_max_duration_seconds

    json_start: None | str | Unset
    if isinstance(start, Unset):
        json_start = UNSET
    elif isinstance(start, datetime.datetime):
        json_start = start.isoformat()
    else:
        json_start = start
    params["start"] = json_start

    json_end: None | str | Unset
    if isinstance(end, Unset):
        json_end = UNSET
    elif isinstance(end, datetime.datetime):
        json_end = end.isoformat()
    else:
        json_end = end
    params["end"] = json_end

    params["timezone"] = timezone

    json_sort: list[str] | None | Unset
    if isinstance(sort, Unset):
        json_sort = UNSET
    elif isinstance(sort, list):
        json_sort = []
        for sort_type_0_item_data in sort:
            sort_type_0_item = sort_type_0_item_data.value
            json_sort.append(sort_type_0_item)

    else:
        json_sort = sort
    params["sort"] = json_sort

    json_order: list[str] | None | Unset
    if isinstance(order, Unset):
        json_order = UNSET
    elif isinstance(order, list):
        json_order = []
        for order_type_0_item_data in order:
            order_type_0_item = order_type_0_item_data.value
            json_order.append(order_type_0_item)

    else:
        json_order = order
    params["order"] = json_order

    json_cursor: None | str | Unset
    if isinstance(cursor, Unset):
        json_cursor = UNSET
    else:
        json_cursor = cursor
    params["cursor"] = json_cursor

    params["include_system_job_runs"] = include_system_job_runs

    json_downstream_job_runs_limit: int | None | Unset
    if isinstance(downstream_job_runs_limit, Unset):
        json_downstream_job_runs_limit = UNSET
    else:
        json_downstream_job_runs_limit = downstream_job_runs_limit
    params["downstream_job_runs_limit"] = json_downstream_job_runs_limit

    json_downstream_job_runs_category: None | str | Unset
    if isinstance(downstream_job_runs_category, Unset):
        json_downstream_job_runs_category = UNSET
    elif isinstance(downstream_job_runs_category, JobCategory):
        json_downstream_job_runs_category = downstream_job_runs_category.value
    else:
        json_downstream_job_runs_category = downstream_job_runs_category
    params["downstream_job_runs_category"] = json_downstream_job_runs_category

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/workspaces/{workspace_id}/job-runs".format(
            workspace_id=quote(str(workspace_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | ListPageDetailedJobRunResponse | None:
    if response.status_code == 200:
        response_200 = ListPageDetailedJobRunResponse.from_dict(response.json())

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

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | ListPageDetailedJobRunResponse]:
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
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    q: None | str | Unset = UNSET,
    status: list[RunStatus] | None | Unset = UNSET,
    number: int | None | Unset = UNSET,
    job_id: None | Unset | UUID = UNSET,
    previous_job_run_id: None | Unset | UUID = UNSET,
    job_type: list[JobType] | None | Unset = UNSET,
    trigger: list[str] | None | Unset = UNSET,
    trigger_kind: list[TriggerKind] | None | Unset = UNSET,
    triggered_by: list[UUID] | None | Unset = UNSET,
    profile: list[str] | None | Unset = UNSET,
    min_duration_seconds: float | None | Unset = UNSET,
    max_duration_seconds: float | None | Unset = UNSET,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    timezone: str | Unset = "UTC",
    sort: list[ListJobRunsSortType0Item] | None | Unset = UNSET,
    order: list[ListJobRunsOrderType0Item] | None | Unset = UNSET,
    cursor: None | str | Unset = UNSET,
    include_system_job_runs: bool | Unset = False,
    downstream_job_runs_limit: int | None | Unset = UNSET,
    downstream_job_runs_category: JobCategory | None | Unset = UNSET,
) -> Response[ErrorResponse | ListPageDetailedJobRunResponse]:
    """ListJobRuns

    Gets the job runs of a workspace as a paginated list, newest first.

    Search with `q` over the job name; filter by status, job, job type, trigger,
    profile, upstream run (`previous_job_run_id`, giving the runs one run triggered), or a
    time window; sort with paired `sort` and `order` lists.

    System runs, such as the dashboard job, are excluded unless `job_id` or
    `previous_job_run_id` names one, or `include_system_job_runs` is set.

    Set `downstream_job_runs_limit` to attach, to each run, the runs its outcome
    triggered.

    Requires READ permission on the organization level.

    Args:
        workspace_id (UUID):
        limit (int | Unset): Maximum number of items to return. At most 1000. Default: 100.
        offset (int | Unset): Number of items to skip. At most 10000; a list reports its total up
            to 10001, so narrow with filters instead of paging deeper. Default: 0.
        q (None | str | Unset): Case-insensitive substring match on the job name and the pipeline
            names the run produced. A numeric value also matches the exact run number.
        status (list[RunStatus] | None | Unset): Exact match on `status`. Repeat the parameter to
            match any of several values.
        number (int | None | Unset): Exact match on `number`.
        job_id (None | Unset | UUID): Exact match on `job_id`.
        previous_job_run_id (None | Unset | UUID): Exact match on `previous_job_run_id`.
        job_type (list[JobType] | None | Unset): Exact match on `job_type`. Repeat the parameter
            to match any of several values.
        trigger (list[str] | None | Unset): Exact match on `trigger`. Repeat the parameter to
            match any of several values.
        trigger_kind (list[TriggerKind] | None | Unset): Match runs by the kind of trigger that
            fired them, whatever its expression. `manual` means a person started the run.
        triggered_by (list[UUID] | None | Unset): Exact match on the identity that started the
            run. Repeat the parameter to match any of several values.
        profile (list[str] | None | Unset): Exact match on `profile`. Repeat the parameter to
            match any of several values.
        min_duration_seconds (float | None | Unset): Inclusive range over `duration_seconds`,
            given as `min_duration_seconds` and `max_duration_seconds`. Either bound may stand alone.
        max_duration_seconds (float | None | Unset): Inclusive range over `duration_seconds`,
            given as `min_duration_seconds` and `max_duration_seconds`. Either bound may stand alone.
        start (datetime.datetime | None | Unset): Start of period. Naive datetime (no offset),
            interpreted in `timezone`. E.g. `2026-03-01T00:00:00`.
        end (datetime.datetime | None | Unset): End of period. Naive datetime (no offset),
            interpreted in `timezone`. E.g. `2026-03-11T00:00:00`.
        timezone (str | Unset): IANA timezone name (e.g. 'Europe/Berlin', 'America/New_York',
            'UTC'). Used for bucket alignment and interpreting `start`/`end`. Default: 'UTC'.
        sort (list[ListJobRunsSortType0Item] | None | Unset): Keys to sort by, applied in the
            order given. Pairs positionally with `order`, which must have the same number of entries.
        order (list[ListJobRunsOrderType0Item] | None | Unset): Sort directions, one per `sort`
            key and in the same order. Required whenever `sort` is supplied.
        cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`;
            returns the rows after it under the same `sort` and `order`. Mutually exclusive with
            `offset`.
        include_system_job_runs (bool | Unset): Include runs of system jobs such as the dashboard.
            Default: False.
        downstream_job_runs_limit (int | None | Unset): Attach this many of the runs each run
            triggered, newest first. Only runs started by the run's outcome are linked.
        downstream_job_runs_category (JobCategory | None | Unset): Attach only downstream runs
            whose job declares this category, so the newest of that kind is found however many other
            runs came after it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ListPageDetailedJobRunResponse]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        limit=limit,
        offset=offset,
        q=q,
        status=status,
        number=number,
        job_id=job_id,
        previous_job_run_id=previous_job_run_id,
        job_type=job_type,
        trigger=trigger,
        trigger_kind=trigger_kind,
        triggered_by=triggered_by,
        profile=profile,
        min_duration_seconds=min_duration_seconds,
        max_duration_seconds=max_duration_seconds,
        start=start,
        end=end,
        timezone=timezone,
        sort=sort,
        order=order,
        cursor=cursor,
        include_system_job_runs=include_system_job_runs,
        downstream_job_runs_limit=downstream_job_runs_limit,
        downstream_job_runs_category=downstream_job_runs_category,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    q: None | str | Unset = UNSET,
    status: list[RunStatus] | None | Unset = UNSET,
    number: int | None | Unset = UNSET,
    job_id: None | Unset | UUID = UNSET,
    previous_job_run_id: None | Unset | UUID = UNSET,
    job_type: list[JobType] | None | Unset = UNSET,
    trigger: list[str] | None | Unset = UNSET,
    trigger_kind: list[TriggerKind] | None | Unset = UNSET,
    triggered_by: list[UUID] | None | Unset = UNSET,
    profile: list[str] | None | Unset = UNSET,
    min_duration_seconds: float | None | Unset = UNSET,
    max_duration_seconds: float | None | Unset = UNSET,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    timezone: str | Unset = "UTC",
    sort: list[ListJobRunsSortType0Item] | None | Unset = UNSET,
    order: list[ListJobRunsOrderType0Item] | None | Unset = UNSET,
    cursor: None | str | Unset = UNSET,
    include_system_job_runs: bool | Unset = False,
    downstream_job_runs_limit: int | None | Unset = UNSET,
    downstream_job_runs_category: JobCategory | None | Unset = UNSET,
) -> ErrorResponse | ListPageDetailedJobRunResponse | None:
    """ListJobRuns

    Gets the job runs of a workspace as a paginated list, newest first.

    Search with `q` over the job name; filter by status, job, job type, trigger,
    profile, upstream run (`previous_job_run_id`, giving the runs one run triggered), or a
    time window; sort with paired `sort` and `order` lists.

    System runs, such as the dashboard job, are excluded unless `job_id` or
    `previous_job_run_id` names one, or `include_system_job_runs` is set.

    Set `downstream_job_runs_limit` to attach, to each run, the runs its outcome
    triggered.

    Requires READ permission on the organization level.

    Args:
        workspace_id (UUID):
        limit (int | Unset): Maximum number of items to return. At most 1000. Default: 100.
        offset (int | Unset): Number of items to skip. At most 10000; a list reports its total up
            to 10001, so narrow with filters instead of paging deeper. Default: 0.
        q (None | str | Unset): Case-insensitive substring match on the job name and the pipeline
            names the run produced. A numeric value also matches the exact run number.
        status (list[RunStatus] | None | Unset): Exact match on `status`. Repeat the parameter to
            match any of several values.
        number (int | None | Unset): Exact match on `number`.
        job_id (None | Unset | UUID): Exact match on `job_id`.
        previous_job_run_id (None | Unset | UUID): Exact match on `previous_job_run_id`.
        job_type (list[JobType] | None | Unset): Exact match on `job_type`. Repeat the parameter
            to match any of several values.
        trigger (list[str] | None | Unset): Exact match on `trigger`. Repeat the parameter to
            match any of several values.
        trigger_kind (list[TriggerKind] | None | Unset): Match runs by the kind of trigger that
            fired them, whatever its expression. `manual` means a person started the run.
        triggered_by (list[UUID] | None | Unset): Exact match on the identity that started the
            run. Repeat the parameter to match any of several values.
        profile (list[str] | None | Unset): Exact match on `profile`. Repeat the parameter to
            match any of several values.
        min_duration_seconds (float | None | Unset): Inclusive range over `duration_seconds`,
            given as `min_duration_seconds` and `max_duration_seconds`. Either bound may stand alone.
        max_duration_seconds (float | None | Unset): Inclusive range over `duration_seconds`,
            given as `min_duration_seconds` and `max_duration_seconds`. Either bound may stand alone.
        start (datetime.datetime | None | Unset): Start of period. Naive datetime (no offset),
            interpreted in `timezone`. E.g. `2026-03-01T00:00:00`.
        end (datetime.datetime | None | Unset): End of period. Naive datetime (no offset),
            interpreted in `timezone`. E.g. `2026-03-11T00:00:00`.
        timezone (str | Unset): IANA timezone name (e.g. 'Europe/Berlin', 'America/New_York',
            'UTC'). Used for bucket alignment and interpreting `start`/`end`. Default: 'UTC'.
        sort (list[ListJobRunsSortType0Item] | None | Unset): Keys to sort by, applied in the
            order given. Pairs positionally with `order`, which must have the same number of entries.
        order (list[ListJobRunsOrderType0Item] | None | Unset): Sort directions, one per `sort`
            key and in the same order. Required whenever `sort` is supplied.
        cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`;
            returns the rows after it under the same `sort` and `order`. Mutually exclusive with
            `offset`.
        include_system_job_runs (bool | Unset): Include runs of system jobs such as the dashboard.
            Default: False.
        downstream_job_runs_limit (int | None | Unset): Attach this many of the runs each run
            triggered, newest first. Only runs started by the run's outcome are linked.
        downstream_job_runs_category (JobCategory | None | Unset): Attach only downstream runs
            whose job declares this category, so the newest of that kind is found however many other
            runs came after it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ListPageDetailedJobRunResponse
    """
    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
        limit=limit,
        offset=offset,
        q=q,
        status=status,
        number=number,
        job_id=job_id,
        previous_job_run_id=previous_job_run_id,
        job_type=job_type,
        trigger=trigger,
        trigger_kind=trigger_kind,
        triggered_by=triggered_by,
        profile=profile,
        min_duration_seconds=min_duration_seconds,
        max_duration_seconds=max_duration_seconds,
        start=start,
        end=end,
        timezone=timezone,
        sort=sort,
        order=order,
        cursor=cursor,
        include_system_job_runs=include_system_job_runs,
        downstream_job_runs_limit=downstream_job_runs_limit,
        downstream_job_runs_category=downstream_job_runs_category,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    q: None | str | Unset = UNSET,
    status: list[RunStatus] | None | Unset = UNSET,
    number: int | None | Unset = UNSET,
    job_id: None | Unset | UUID = UNSET,
    previous_job_run_id: None | Unset | UUID = UNSET,
    job_type: list[JobType] | None | Unset = UNSET,
    trigger: list[str] | None | Unset = UNSET,
    trigger_kind: list[TriggerKind] | None | Unset = UNSET,
    triggered_by: list[UUID] | None | Unset = UNSET,
    profile: list[str] | None | Unset = UNSET,
    min_duration_seconds: float | None | Unset = UNSET,
    max_duration_seconds: float | None | Unset = UNSET,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    timezone: str | Unset = "UTC",
    sort: list[ListJobRunsSortType0Item] | None | Unset = UNSET,
    order: list[ListJobRunsOrderType0Item] | None | Unset = UNSET,
    cursor: None | str | Unset = UNSET,
    include_system_job_runs: bool | Unset = False,
    downstream_job_runs_limit: int | None | Unset = UNSET,
    downstream_job_runs_category: JobCategory | None | Unset = UNSET,
) -> Response[ErrorResponse | ListPageDetailedJobRunResponse]:
    """ListJobRuns

    Gets the job runs of a workspace as a paginated list, newest first.

    Search with `q` over the job name; filter by status, job, job type, trigger,
    profile, upstream run (`previous_job_run_id`, giving the runs one run triggered), or a
    time window; sort with paired `sort` and `order` lists.

    System runs, such as the dashboard job, are excluded unless `job_id` or
    `previous_job_run_id` names one, or `include_system_job_runs` is set.

    Set `downstream_job_runs_limit` to attach, to each run, the runs its outcome
    triggered.

    Requires READ permission on the organization level.

    Args:
        workspace_id (UUID):
        limit (int | Unset): Maximum number of items to return. At most 1000. Default: 100.
        offset (int | Unset): Number of items to skip. At most 10000; a list reports its total up
            to 10001, so narrow with filters instead of paging deeper. Default: 0.
        q (None | str | Unset): Case-insensitive substring match on the job name and the pipeline
            names the run produced. A numeric value also matches the exact run number.
        status (list[RunStatus] | None | Unset): Exact match on `status`. Repeat the parameter to
            match any of several values.
        number (int | None | Unset): Exact match on `number`.
        job_id (None | Unset | UUID): Exact match on `job_id`.
        previous_job_run_id (None | Unset | UUID): Exact match on `previous_job_run_id`.
        job_type (list[JobType] | None | Unset): Exact match on `job_type`. Repeat the parameter
            to match any of several values.
        trigger (list[str] | None | Unset): Exact match on `trigger`. Repeat the parameter to
            match any of several values.
        trigger_kind (list[TriggerKind] | None | Unset): Match runs by the kind of trigger that
            fired them, whatever its expression. `manual` means a person started the run.
        triggered_by (list[UUID] | None | Unset): Exact match on the identity that started the
            run. Repeat the parameter to match any of several values.
        profile (list[str] | None | Unset): Exact match on `profile`. Repeat the parameter to
            match any of several values.
        min_duration_seconds (float | None | Unset): Inclusive range over `duration_seconds`,
            given as `min_duration_seconds` and `max_duration_seconds`. Either bound may stand alone.
        max_duration_seconds (float | None | Unset): Inclusive range over `duration_seconds`,
            given as `min_duration_seconds` and `max_duration_seconds`. Either bound may stand alone.
        start (datetime.datetime | None | Unset): Start of period. Naive datetime (no offset),
            interpreted in `timezone`. E.g. `2026-03-01T00:00:00`.
        end (datetime.datetime | None | Unset): End of period. Naive datetime (no offset),
            interpreted in `timezone`. E.g. `2026-03-11T00:00:00`.
        timezone (str | Unset): IANA timezone name (e.g. 'Europe/Berlin', 'America/New_York',
            'UTC'). Used for bucket alignment and interpreting `start`/`end`. Default: 'UTC'.
        sort (list[ListJobRunsSortType0Item] | None | Unset): Keys to sort by, applied in the
            order given. Pairs positionally with `order`, which must have the same number of entries.
        order (list[ListJobRunsOrderType0Item] | None | Unset): Sort directions, one per `sort`
            key and in the same order. Required whenever `sort` is supplied.
        cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`;
            returns the rows after it under the same `sort` and `order`. Mutually exclusive with
            `offset`.
        include_system_job_runs (bool | Unset): Include runs of system jobs such as the dashboard.
            Default: False.
        downstream_job_runs_limit (int | None | Unset): Attach this many of the runs each run
            triggered, newest first. Only runs started by the run's outcome are linked.
        downstream_job_runs_category (JobCategory | None | Unset): Attach only downstream runs
            whose job declares this category, so the newest of that kind is found however many other
            runs came after it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ListPageDetailedJobRunResponse]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        limit=limit,
        offset=offset,
        q=q,
        status=status,
        number=number,
        job_id=job_id,
        previous_job_run_id=previous_job_run_id,
        job_type=job_type,
        trigger=trigger,
        trigger_kind=trigger_kind,
        triggered_by=triggered_by,
        profile=profile,
        min_duration_seconds=min_duration_seconds,
        max_duration_seconds=max_duration_seconds,
        start=start,
        end=end,
        timezone=timezone,
        sort=sort,
        order=order,
        cursor=cursor,
        include_system_job_runs=include_system_job_runs,
        downstream_job_runs_limit=downstream_job_runs_limit,
        downstream_job_runs_category=downstream_job_runs_category,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    q: None | str | Unset = UNSET,
    status: list[RunStatus] | None | Unset = UNSET,
    number: int | None | Unset = UNSET,
    job_id: None | Unset | UUID = UNSET,
    previous_job_run_id: None | Unset | UUID = UNSET,
    job_type: list[JobType] | None | Unset = UNSET,
    trigger: list[str] | None | Unset = UNSET,
    trigger_kind: list[TriggerKind] | None | Unset = UNSET,
    triggered_by: list[UUID] | None | Unset = UNSET,
    profile: list[str] | None | Unset = UNSET,
    min_duration_seconds: float | None | Unset = UNSET,
    max_duration_seconds: float | None | Unset = UNSET,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    timezone: str | Unset = "UTC",
    sort: list[ListJobRunsSortType0Item] | None | Unset = UNSET,
    order: list[ListJobRunsOrderType0Item] | None | Unset = UNSET,
    cursor: None | str | Unset = UNSET,
    include_system_job_runs: bool | Unset = False,
    downstream_job_runs_limit: int | None | Unset = UNSET,
    downstream_job_runs_category: JobCategory | None | Unset = UNSET,
) -> ErrorResponse | ListPageDetailedJobRunResponse | None:
    """ListJobRuns

    Gets the job runs of a workspace as a paginated list, newest first.

    Search with `q` over the job name; filter by status, job, job type, trigger,
    profile, upstream run (`previous_job_run_id`, giving the runs one run triggered), or a
    time window; sort with paired `sort` and `order` lists.

    System runs, such as the dashboard job, are excluded unless `job_id` or
    `previous_job_run_id` names one, or `include_system_job_runs` is set.

    Set `downstream_job_runs_limit` to attach, to each run, the runs its outcome
    triggered.

    Requires READ permission on the organization level.

    Args:
        workspace_id (UUID):
        limit (int | Unset): Maximum number of items to return. At most 1000. Default: 100.
        offset (int | Unset): Number of items to skip. At most 10000; a list reports its total up
            to 10001, so narrow with filters instead of paging deeper. Default: 0.
        q (None | str | Unset): Case-insensitive substring match on the job name and the pipeline
            names the run produced. A numeric value also matches the exact run number.
        status (list[RunStatus] | None | Unset): Exact match on `status`. Repeat the parameter to
            match any of several values.
        number (int | None | Unset): Exact match on `number`.
        job_id (None | Unset | UUID): Exact match on `job_id`.
        previous_job_run_id (None | Unset | UUID): Exact match on `previous_job_run_id`.
        job_type (list[JobType] | None | Unset): Exact match on `job_type`. Repeat the parameter
            to match any of several values.
        trigger (list[str] | None | Unset): Exact match on `trigger`. Repeat the parameter to
            match any of several values.
        trigger_kind (list[TriggerKind] | None | Unset): Match runs by the kind of trigger that
            fired them, whatever its expression. `manual` means a person started the run.
        triggered_by (list[UUID] | None | Unset): Exact match on the identity that started the
            run. Repeat the parameter to match any of several values.
        profile (list[str] | None | Unset): Exact match on `profile`. Repeat the parameter to
            match any of several values.
        min_duration_seconds (float | None | Unset): Inclusive range over `duration_seconds`,
            given as `min_duration_seconds` and `max_duration_seconds`. Either bound may stand alone.
        max_duration_seconds (float | None | Unset): Inclusive range over `duration_seconds`,
            given as `min_duration_seconds` and `max_duration_seconds`. Either bound may stand alone.
        start (datetime.datetime | None | Unset): Start of period. Naive datetime (no offset),
            interpreted in `timezone`. E.g. `2026-03-01T00:00:00`.
        end (datetime.datetime | None | Unset): End of period. Naive datetime (no offset),
            interpreted in `timezone`. E.g. `2026-03-11T00:00:00`.
        timezone (str | Unset): IANA timezone name (e.g. 'Europe/Berlin', 'America/New_York',
            'UTC'). Used for bucket alignment and interpreting `start`/`end`. Default: 'UTC'.
        sort (list[ListJobRunsSortType0Item] | None | Unset): Keys to sort by, applied in the
            order given. Pairs positionally with `order`, which must have the same number of entries.
        order (list[ListJobRunsOrderType0Item] | None | Unset): Sort directions, one per `sort`
            key and in the same order. Required whenever `sort` is supplied.
        cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`;
            returns the rows after it under the same `sort` and `order`. Mutually exclusive with
            `offset`.
        include_system_job_runs (bool | Unset): Include runs of system jobs such as the dashboard.
            Default: False.
        downstream_job_runs_limit (int | None | Unset): Attach this many of the runs each run
            triggered, newest first. Only runs started by the run's outcome are linked.
        downstream_job_runs_category (JobCategory | None | Unset): Attach only downstream runs
            whose job declares this category, so the newest of that kind is found however many other
            runs came after it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ListPageDetailedJobRunResponse
    """
    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            limit=limit,
            offset=offset,
            q=q,
            status=status,
            number=number,
            job_id=job_id,
            previous_job_run_id=previous_job_run_id,
            job_type=job_type,
            trigger=trigger,
            trigger_kind=trigger_kind,
            triggered_by=triggered_by,
            profile=profile,
            min_duration_seconds=min_duration_seconds,
            max_duration_seconds=max_duration_seconds,
            start=start,
            end=end,
            timezone=timezone,
            sort=sort,
            order=order,
            cursor=cursor,
            include_system_job_runs=include_system_job_runs,
            downstream_job_runs_limit=downstream_job_runs_limit,
            downstream_job_runs_category=downstream_job_runs_category,
        )
    ).parsed
