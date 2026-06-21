from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.list_runs_sort import ListRunsSort
from ...models.run_list_response import RunListResponse
from ...types import Unset


def _get_kwargs(
    *,
    filterjob: None | str | Unset = UNSET,
    filterstatus: None | str | Unset = UNSET,
    filterenvironment: None | str | Unset = UNSET,
    filtertrigger: None | str | Unset = UNSET,
    filtercreated_at: None | str | Unset = UNSET,
    filterstarted_at: None | str | Unset = UNSET,
    filterfinished_at: None | str | Unset = UNSET,
    filterscheduled_for: None | str | Unset = UNSET,
    last_run_only: bool | Unset = False,
    pagesize: int | None | Unset = UNSET,
    pageafter: None | str | Unset = UNSET,
    sort: ListRunsSort | Unset = "-created_at",
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_filterjob: None | str | Unset
    if isinstance(filterjob, Unset):
        json_filterjob = UNSET
    else:
        json_filterjob = filterjob
    params["filter[job]"] = json_filterjob

    json_filterstatus: None | str | Unset
    if isinstance(filterstatus, Unset):
        json_filterstatus = UNSET
    else:
        json_filterstatus = filterstatus
    params["filter[status]"] = json_filterstatus

    json_filterenvironment: None | str | Unset
    if isinstance(filterenvironment, Unset):
        json_filterenvironment = UNSET
    else:
        json_filterenvironment = filterenvironment
    params["filter[environment]"] = json_filterenvironment

    json_filtertrigger: None | str | Unset
    if isinstance(filtertrigger, Unset):
        json_filtertrigger = UNSET
    else:
        json_filtertrigger = filtertrigger
    params["filter[trigger]"] = json_filtertrigger

    json_filtercreated_at: None | str | Unset
    if isinstance(filtercreated_at, Unset):
        json_filtercreated_at = UNSET
    else:
        json_filtercreated_at = filtercreated_at
    params["filter[created_at]"] = json_filtercreated_at

    json_filterstarted_at: None | str | Unset
    if isinstance(filterstarted_at, Unset):
        json_filterstarted_at = UNSET
    else:
        json_filterstarted_at = filterstarted_at
    params["filter[started_at]"] = json_filterstarted_at

    json_filterfinished_at: None | str | Unset
    if isinstance(filterfinished_at, Unset):
        json_filterfinished_at = UNSET
    else:
        json_filterfinished_at = filterfinished_at
    params["filter[finished_at]"] = json_filterfinished_at

    json_filterscheduled_for: None | str | Unset
    if isinstance(filterscheduled_for, Unset):
        json_filterscheduled_for = UNSET
    else:
        json_filterscheduled_for = filterscheduled_for
    params["filter[scheduled_for]"] = json_filterscheduled_for

    params["last_run_only"] = last_run_only

    json_pagesize: int | None | Unset
    if isinstance(pagesize, Unset):
        json_pagesize = UNSET
    else:
        json_pagesize = pagesize
    params["page[size]"] = json_pagesize

    json_pageafter: None | str | Unset
    if isinstance(pageafter, Unset):
        json_pageafter = UNSET
    else:
        json_pageafter = pageafter
    params["page[after]"] = json_pageafter

    json_sort: str | Unset = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort

    params["sort"] = json_sort

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/runs",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> RunListResponse | None:
    if response.status_code == 200:
        response_200 = RunListResponse.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[RunListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    filterjob: None | str | Unset = UNSET,
    filterstatus: None | str | Unset = UNSET,
    filterenvironment: None | str | Unset = UNSET,
    filtertrigger: None | str | Unset = UNSET,
    filtercreated_at: None | str | Unset = UNSET,
    filterstarted_at: None | str | Unset = UNSET,
    filterfinished_at: None | str | Unset = UNSET,
    filterscheduled_for: None | str | Unset = UNSET,
    last_run_only: bool | Unset = False,
    pagesize: int | None | Unset = UNSET,
    pageafter: None | str | Unset = UNSET,
    sort: ListRunsSort | Unset = "-created_at",
) -> Response[RunListResponse]:
    r"""List Runs

     List runs for this account (cursor paginated).

    Default sort is `-created_at` (newest first). Sort by `created_at`,
    `started_at`, `finished_at`, `scheduled_for`, `status`, `job`, or
    `total_duration_ms`, ascending or descending (prefix `-` for descending).
    Keep the same `sort` value across paginated requests so the cursor stays
    consistent. Runs that have not reached the relevant lifecycle point
    (`started_at`, `finished_at`, `scheduled_for`, `total_duration_ms` unset)
    sort to the end regardless of direction.

    Filters compose with AND:

    - `filter[job]={id}` — a single job's run history.
    - `filter[status]` — one state or a comma-separated list (any-of).
    - `filter[trigger]` — one trigger (`SCHEDULE`, `MANUAL`, `RERUN`, `RETRY`)
      or a comma-separated list of them (any-of).
    - `filter[environment]` — one environment key or a comma-separated list
      (any-of); omitted covers every environment you can access.
    - `filter[created_at]` / `filter[started_at]` / `filter[finished_at]` /
      `filter[scheduled_for]` — half-open `[start,end)` date ranges (see each
      parameter for the interval syntax).

    Set `last_run_only=true` to collapse the result to the last completed run
    for each job-and-environment combination. \"Completed\" means a terminal state
    — succeeded, failed, or canceled; in-flight runs (pending or running) are
    not included, so a job that is mid-run still surfaces its previous completed
    result and a combination with no completed run yet returns nothing. The
    filters above still apply, evaluated before the collapse, so each row is the
    most recent completed run in its group that also satisfies them.

    Args:
        filterjob (None | str | Unset):
        filterstatus (None | str | Unset): Restrict to runs in the given lifecycle state. One of
            `PENDING`, `RUNNING`, `SUCCEEDED`, `FAILED`, `CANCELED`, or a comma-separated list of them
            to match any (e.g. `SUCCEEDED,FAILED`).
        filterenvironment (None | str | Unset): Comma-separated list of environment keys to scope
            results to (e.g. `production,staging`). When omitted, results cover every environment you
            can access.
        filtertrigger (None | str | Unset): Restrict to runs with the given trigger. One of
            `SCHEDULE`, `MANUAL`, `RERUN`, `RETRY`, or a comma-separated list of them to match any
            (e.g. `SCHEDULE,RETRY` to see a job's automatic runs).
        filtercreated_at (None | str | Unset): Restrict to runs whose `created_at` falls in a
            half-open `[start,end)` interval. Bounds are ISO-8601 timestamps; `*` leaves a bound open.
            The leading bracket is `[` (inclusive) or `(` (exclusive) and the trailing bracket is `]`
            (inclusive) or `)` (exclusive). Example: `[2026-06-01T00:00:00Z,2026-06-08T00:00:00Z)`
            selects the first week of June; `[2026-06-01T00:00:00Z,*)` is everything from then onward.
        filterstarted_at (None | str | Unset): Restrict to runs whose `started_at` falls in a
            half-open `[start,end)` interval. Bounds are ISO-8601 timestamps; `*` leaves a bound open.
            The leading bracket is `[` (inclusive) or `(` (exclusive) and the trailing bracket is `]`
            (inclusive) or `)` (exclusive). Example: `[2026-06-01T00:00:00Z,2026-06-08T00:00:00Z)`
            selects the first week of June; `[2026-06-01T00:00:00Z,*)` is everything from then onward.
        filterfinished_at (None | str | Unset): Restrict to runs whose `finished_at` falls in a
            half-open `[start,end)` interval. Bounds are ISO-8601 timestamps; `*` leaves a bound open.
            The leading bracket is `[` (inclusive) or `(` (exclusive) and the trailing bracket is `]`
            (inclusive) or `)` (exclusive). Example: `[2026-06-01T00:00:00Z,2026-06-08T00:00:00Z)`
            selects the first week of June; `[2026-06-01T00:00:00Z,*)` is everything from then onward.
        filterscheduled_for (None | str | Unset): Restrict to runs whose `scheduled_for` falls in
            a half-open `[start,end)` interval. Bounds are ISO-8601 timestamps; `*` leaves a bound
            open. The leading bracket is `[` (inclusive) or `(` (exclusive) and the trailing bracket
            is `]` (inclusive) or `)` (exclusive). Example:
            `[2026-06-01T00:00:00Z,2026-06-08T00:00:00Z)` selects the first week of June;
            `[2026-06-01T00:00:00Z,*)` is everything from then onward.
        last_run_only (bool | Unset): Return only the last completed run for each job-and-
            environment combination. "Completed" means a terminal state — succeeded, failed, or
            canceled; runs still in flight (pending or running) are not included, so a job that is
            currently running still shows its previous completed result. The other filters and date
            ranges apply first, then the results collapse, so each row is the most recent completed
            run in its group that also matches them. Defaults to `false`. Default: False.
        pagesize (int | None | Unset): Number of runs per page. Optional; defaults to `50` when
            omitted. Must be between `1` and `1000` inclusive — requests outside that range are
            rejected with a 400 error.
        pageafter (None | str | Unset):
        sort (ListRunsSort | Unset): Field to sort by. Prefix with `-` for descending order.
            Default: `-created_at`. Allowed values: `created_at`, `-created_at`, `finished_at`,
            `-finished_at`, `job`, `-job`, `scheduled_for`, `-scheduled_for`, `started_at`,
            `-started_at`, `status`, `-status`, `total_duration_ms`, `-total_duration_ms`. Default:
            '-created_at'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RunListResponse]
    """

    kwargs = _get_kwargs(
        filterjob=filterjob,
        filterstatus=filterstatus,
        filterenvironment=filterenvironment,
        filtertrigger=filtertrigger,
        filtercreated_at=filtercreated_at,
        filterstarted_at=filterstarted_at,
        filterfinished_at=filterfinished_at,
        filterscheduled_for=filterscheduled_for,
        last_run_only=last_run_only,
        pagesize=pagesize,
        pageafter=pageafter,
        sort=sort,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    filterjob: None | str | Unset = UNSET,
    filterstatus: None | str | Unset = UNSET,
    filterenvironment: None | str | Unset = UNSET,
    filtertrigger: None | str | Unset = UNSET,
    filtercreated_at: None | str | Unset = UNSET,
    filterstarted_at: None | str | Unset = UNSET,
    filterfinished_at: None | str | Unset = UNSET,
    filterscheduled_for: None | str | Unset = UNSET,
    last_run_only: bool | Unset = False,
    pagesize: int | None | Unset = UNSET,
    pageafter: None | str | Unset = UNSET,
    sort: ListRunsSort | Unset = "-created_at",
) -> RunListResponse | None:
    r"""List Runs

     List runs for this account (cursor paginated).

    Default sort is `-created_at` (newest first). Sort by `created_at`,
    `started_at`, `finished_at`, `scheduled_for`, `status`, `job`, or
    `total_duration_ms`, ascending or descending (prefix `-` for descending).
    Keep the same `sort` value across paginated requests so the cursor stays
    consistent. Runs that have not reached the relevant lifecycle point
    (`started_at`, `finished_at`, `scheduled_for`, `total_duration_ms` unset)
    sort to the end regardless of direction.

    Filters compose with AND:

    - `filter[job]={id}` — a single job's run history.
    - `filter[status]` — one state or a comma-separated list (any-of).
    - `filter[trigger]` — one trigger (`SCHEDULE`, `MANUAL`, `RERUN`, `RETRY`)
      or a comma-separated list of them (any-of).
    - `filter[environment]` — one environment key or a comma-separated list
      (any-of); omitted covers every environment you can access.
    - `filter[created_at]` / `filter[started_at]` / `filter[finished_at]` /
      `filter[scheduled_for]` — half-open `[start,end)` date ranges (see each
      parameter for the interval syntax).

    Set `last_run_only=true` to collapse the result to the last completed run
    for each job-and-environment combination. \"Completed\" means a terminal state
    — succeeded, failed, or canceled; in-flight runs (pending or running) are
    not included, so a job that is mid-run still surfaces its previous completed
    result and a combination with no completed run yet returns nothing. The
    filters above still apply, evaluated before the collapse, so each row is the
    most recent completed run in its group that also satisfies them.

    Args:
        filterjob (None | str | Unset):
        filterstatus (None | str | Unset): Restrict to runs in the given lifecycle state. One of
            `PENDING`, `RUNNING`, `SUCCEEDED`, `FAILED`, `CANCELED`, or a comma-separated list of them
            to match any (e.g. `SUCCEEDED,FAILED`).
        filterenvironment (None | str | Unset): Comma-separated list of environment keys to scope
            results to (e.g. `production,staging`). When omitted, results cover every environment you
            can access.
        filtertrigger (None | str | Unset): Restrict to runs with the given trigger. One of
            `SCHEDULE`, `MANUAL`, `RERUN`, `RETRY`, or a comma-separated list of them to match any
            (e.g. `SCHEDULE,RETRY` to see a job's automatic runs).
        filtercreated_at (None | str | Unset): Restrict to runs whose `created_at` falls in a
            half-open `[start,end)` interval. Bounds are ISO-8601 timestamps; `*` leaves a bound open.
            The leading bracket is `[` (inclusive) or `(` (exclusive) and the trailing bracket is `]`
            (inclusive) or `)` (exclusive). Example: `[2026-06-01T00:00:00Z,2026-06-08T00:00:00Z)`
            selects the first week of June; `[2026-06-01T00:00:00Z,*)` is everything from then onward.
        filterstarted_at (None | str | Unset): Restrict to runs whose `started_at` falls in a
            half-open `[start,end)` interval. Bounds are ISO-8601 timestamps; `*` leaves a bound open.
            The leading bracket is `[` (inclusive) or `(` (exclusive) and the trailing bracket is `]`
            (inclusive) or `)` (exclusive). Example: `[2026-06-01T00:00:00Z,2026-06-08T00:00:00Z)`
            selects the first week of June; `[2026-06-01T00:00:00Z,*)` is everything from then onward.
        filterfinished_at (None | str | Unset): Restrict to runs whose `finished_at` falls in a
            half-open `[start,end)` interval. Bounds are ISO-8601 timestamps; `*` leaves a bound open.
            The leading bracket is `[` (inclusive) or `(` (exclusive) and the trailing bracket is `]`
            (inclusive) or `)` (exclusive). Example: `[2026-06-01T00:00:00Z,2026-06-08T00:00:00Z)`
            selects the first week of June; `[2026-06-01T00:00:00Z,*)` is everything from then onward.
        filterscheduled_for (None | str | Unset): Restrict to runs whose `scheduled_for` falls in
            a half-open `[start,end)` interval. Bounds are ISO-8601 timestamps; `*` leaves a bound
            open. The leading bracket is `[` (inclusive) or `(` (exclusive) and the trailing bracket
            is `]` (inclusive) or `)` (exclusive). Example:
            `[2026-06-01T00:00:00Z,2026-06-08T00:00:00Z)` selects the first week of June;
            `[2026-06-01T00:00:00Z,*)` is everything from then onward.
        last_run_only (bool | Unset): Return only the last completed run for each job-and-
            environment combination. "Completed" means a terminal state — succeeded, failed, or
            canceled; runs still in flight (pending or running) are not included, so a job that is
            currently running still shows its previous completed result. The other filters and date
            ranges apply first, then the results collapse, so each row is the most recent completed
            run in its group that also matches them. Defaults to `false`. Default: False.
        pagesize (int | None | Unset): Number of runs per page. Optional; defaults to `50` when
            omitted. Must be between `1` and `1000` inclusive — requests outside that range are
            rejected with a 400 error.
        pageafter (None | str | Unset):
        sort (ListRunsSort | Unset): Field to sort by. Prefix with `-` for descending order.
            Default: `-created_at`. Allowed values: `created_at`, `-created_at`, `finished_at`,
            `-finished_at`, `job`, `-job`, `scheduled_for`, `-scheduled_for`, `started_at`,
            `-started_at`, `status`, `-status`, `total_duration_ms`, `-total_duration_ms`. Default:
            '-created_at'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RunListResponse
    """

    return sync_detailed(
        client=client,
        filterjob=filterjob,
        filterstatus=filterstatus,
        filterenvironment=filterenvironment,
        filtertrigger=filtertrigger,
        filtercreated_at=filtercreated_at,
        filterstarted_at=filterstarted_at,
        filterfinished_at=filterfinished_at,
        filterscheduled_for=filterscheduled_for,
        last_run_only=last_run_only,
        pagesize=pagesize,
        pageafter=pageafter,
        sort=sort,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    filterjob: None | str | Unset = UNSET,
    filterstatus: None | str | Unset = UNSET,
    filterenvironment: None | str | Unset = UNSET,
    filtertrigger: None | str | Unset = UNSET,
    filtercreated_at: None | str | Unset = UNSET,
    filterstarted_at: None | str | Unset = UNSET,
    filterfinished_at: None | str | Unset = UNSET,
    filterscheduled_for: None | str | Unset = UNSET,
    last_run_only: bool | Unset = False,
    pagesize: int | None | Unset = UNSET,
    pageafter: None | str | Unset = UNSET,
    sort: ListRunsSort | Unset = "-created_at",
) -> Response[RunListResponse]:
    r"""List Runs

     List runs for this account (cursor paginated).

    Default sort is `-created_at` (newest first). Sort by `created_at`,
    `started_at`, `finished_at`, `scheduled_for`, `status`, `job`, or
    `total_duration_ms`, ascending or descending (prefix `-` for descending).
    Keep the same `sort` value across paginated requests so the cursor stays
    consistent. Runs that have not reached the relevant lifecycle point
    (`started_at`, `finished_at`, `scheduled_for`, `total_duration_ms` unset)
    sort to the end regardless of direction.

    Filters compose with AND:

    - `filter[job]={id}` — a single job's run history.
    - `filter[status]` — one state or a comma-separated list (any-of).
    - `filter[trigger]` — one trigger (`SCHEDULE`, `MANUAL`, `RERUN`, `RETRY`)
      or a comma-separated list of them (any-of).
    - `filter[environment]` — one environment key or a comma-separated list
      (any-of); omitted covers every environment you can access.
    - `filter[created_at]` / `filter[started_at]` / `filter[finished_at]` /
      `filter[scheduled_for]` — half-open `[start,end)` date ranges (see each
      parameter for the interval syntax).

    Set `last_run_only=true` to collapse the result to the last completed run
    for each job-and-environment combination. \"Completed\" means a terminal state
    — succeeded, failed, or canceled; in-flight runs (pending or running) are
    not included, so a job that is mid-run still surfaces its previous completed
    result and a combination with no completed run yet returns nothing. The
    filters above still apply, evaluated before the collapse, so each row is the
    most recent completed run in its group that also satisfies them.

    Args:
        filterjob (None | str | Unset):
        filterstatus (None | str | Unset): Restrict to runs in the given lifecycle state. One of
            `PENDING`, `RUNNING`, `SUCCEEDED`, `FAILED`, `CANCELED`, or a comma-separated list of them
            to match any (e.g. `SUCCEEDED,FAILED`).
        filterenvironment (None | str | Unset): Comma-separated list of environment keys to scope
            results to (e.g. `production,staging`). When omitted, results cover every environment you
            can access.
        filtertrigger (None | str | Unset): Restrict to runs with the given trigger. One of
            `SCHEDULE`, `MANUAL`, `RERUN`, `RETRY`, or a comma-separated list of them to match any
            (e.g. `SCHEDULE,RETRY` to see a job's automatic runs).
        filtercreated_at (None | str | Unset): Restrict to runs whose `created_at` falls in a
            half-open `[start,end)` interval. Bounds are ISO-8601 timestamps; `*` leaves a bound open.
            The leading bracket is `[` (inclusive) or `(` (exclusive) and the trailing bracket is `]`
            (inclusive) or `)` (exclusive). Example: `[2026-06-01T00:00:00Z,2026-06-08T00:00:00Z)`
            selects the first week of June; `[2026-06-01T00:00:00Z,*)` is everything from then onward.
        filterstarted_at (None | str | Unset): Restrict to runs whose `started_at` falls in a
            half-open `[start,end)` interval. Bounds are ISO-8601 timestamps; `*` leaves a bound open.
            The leading bracket is `[` (inclusive) or `(` (exclusive) and the trailing bracket is `]`
            (inclusive) or `)` (exclusive). Example: `[2026-06-01T00:00:00Z,2026-06-08T00:00:00Z)`
            selects the first week of June; `[2026-06-01T00:00:00Z,*)` is everything from then onward.
        filterfinished_at (None | str | Unset): Restrict to runs whose `finished_at` falls in a
            half-open `[start,end)` interval. Bounds are ISO-8601 timestamps; `*` leaves a bound open.
            The leading bracket is `[` (inclusive) or `(` (exclusive) and the trailing bracket is `]`
            (inclusive) or `)` (exclusive). Example: `[2026-06-01T00:00:00Z,2026-06-08T00:00:00Z)`
            selects the first week of June; `[2026-06-01T00:00:00Z,*)` is everything from then onward.
        filterscheduled_for (None | str | Unset): Restrict to runs whose `scheduled_for` falls in
            a half-open `[start,end)` interval. Bounds are ISO-8601 timestamps; `*` leaves a bound
            open. The leading bracket is `[` (inclusive) or `(` (exclusive) and the trailing bracket
            is `]` (inclusive) or `)` (exclusive). Example:
            `[2026-06-01T00:00:00Z,2026-06-08T00:00:00Z)` selects the first week of June;
            `[2026-06-01T00:00:00Z,*)` is everything from then onward.
        last_run_only (bool | Unset): Return only the last completed run for each job-and-
            environment combination. "Completed" means a terminal state — succeeded, failed, or
            canceled; runs still in flight (pending or running) are not included, so a job that is
            currently running still shows its previous completed result. The other filters and date
            ranges apply first, then the results collapse, so each row is the most recent completed
            run in its group that also matches them. Defaults to `false`. Default: False.
        pagesize (int | None | Unset): Number of runs per page. Optional; defaults to `50` when
            omitted. Must be between `1` and `1000` inclusive — requests outside that range are
            rejected with a 400 error.
        pageafter (None | str | Unset):
        sort (ListRunsSort | Unset): Field to sort by. Prefix with `-` for descending order.
            Default: `-created_at`. Allowed values: `created_at`, `-created_at`, `finished_at`,
            `-finished_at`, `job`, `-job`, `scheduled_for`, `-scheduled_for`, `started_at`,
            `-started_at`, `status`, `-status`, `total_duration_ms`, `-total_duration_ms`. Default:
            '-created_at'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RunListResponse]
    """

    kwargs = _get_kwargs(
        filterjob=filterjob,
        filterstatus=filterstatus,
        filterenvironment=filterenvironment,
        filtertrigger=filtertrigger,
        filtercreated_at=filtercreated_at,
        filterstarted_at=filterstarted_at,
        filterfinished_at=filterfinished_at,
        filterscheduled_for=filterscheduled_for,
        last_run_only=last_run_only,
        pagesize=pagesize,
        pageafter=pageafter,
        sort=sort,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    filterjob: None | str | Unset = UNSET,
    filterstatus: None | str | Unset = UNSET,
    filterenvironment: None | str | Unset = UNSET,
    filtertrigger: None | str | Unset = UNSET,
    filtercreated_at: None | str | Unset = UNSET,
    filterstarted_at: None | str | Unset = UNSET,
    filterfinished_at: None | str | Unset = UNSET,
    filterscheduled_for: None | str | Unset = UNSET,
    last_run_only: bool | Unset = False,
    pagesize: int | None | Unset = UNSET,
    pageafter: None | str | Unset = UNSET,
    sort: ListRunsSort | Unset = "-created_at",
) -> RunListResponse | None:
    r"""List Runs

     List runs for this account (cursor paginated).

    Default sort is `-created_at` (newest first). Sort by `created_at`,
    `started_at`, `finished_at`, `scheduled_for`, `status`, `job`, or
    `total_duration_ms`, ascending or descending (prefix `-` for descending).
    Keep the same `sort` value across paginated requests so the cursor stays
    consistent. Runs that have not reached the relevant lifecycle point
    (`started_at`, `finished_at`, `scheduled_for`, `total_duration_ms` unset)
    sort to the end regardless of direction.

    Filters compose with AND:

    - `filter[job]={id}` — a single job's run history.
    - `filter[status]` — one state or a comma-separated list (any-of).
    - `filter[trigger]` — one trigger (`SCHEDULE`, `MANUAL`, `RERUN`, `RETRY`)
      or a comma-separated list of them (any-of).
    - `filter[environment]` — one environment key or a comma-separated list
      (any-of); omitted covers every environment you can access.
    - `filter[created_at]` / `filter[started_at]` / `filter[finished_at]` /
      `filter[scheduled_for]` — half-open `[start,end)` date ranges (see each
      parameter for the interval syntax).

    Set `last_run_only=true` to collapse the result to the last completed run
    for each job-and-environment combination. \"Completed\" means a terminal state
    — succeeded, failed, or canceled; in-flight runs (pending or running) are
    not included, so a job that is mid-run still surfaces its previous completed
    result and a combination with no completed run yet returns nothing. The
    filters above still apply, evaluated before the collapse, so each row is the
    most recent completed run in its group that also satisfies them.

    Args:
        filterjob (None | str | Unset):
        filterstatus (None | str | Unset): Restrict to runs in the given lifecycle state. One of
            `PENDING`, `RUNNING`, `SUCCEEDED`, `FAILED`, `CANCELED`, or a comma-separated list of them
            to match any (e.g. `SUCCEEDED,FAILED`).
        filterenvironment (None | str | Unset): Comma-separated list of environment keys to scope
            results to (e.g. `production,staging`). When omitted, results cover every environment you
            can access.
        filtertrigger (None | str | Unset): Restrict to runs with the given trigger. One of
            `SCHEDULE`, `MANUAL`, `RERUN`, `RETRY`, or a comma-separated list of them to match any
            (e.g. `SCHEDULE,RETRY` to see a job's automatic runs).
        filtercreated_at (None | str | Unset): Restrict to runs whose `created_at` falls in a
            half-open `[start,end)` interval. Bounds are ISO-8601 timestamps; `*` leaves a bound open.
            The leading bracket is `[` (inclusive) or `(` (exclusive) and the trailing bracket is `]`
            (inclusive) or `)` (exclusive). Example: `[2026-06-01T00:00:00Z,2026-06-08T00:00:00Z)`
            selects the first week of June; `[2026-06-01T00:00:00Z,*)` is everything from then onward.
        filterstarted_at (None | str | Unset): Restrict to runs whose `started_at` falls in a
            half-open `[start,end)` interval. Bounds are ISO-8601 timestamps; `*` leaves a bound open.
            The leading bracket is `[` (inclusive) or `(` (exclusive) and the trailing bracket is `]`
            (inclusive) or `)` (exclusive). Example: `[2026-06-01T00:00:00Z,2026-06-08T00:00:00Z)`
            selects the first week of June; `[2026-06-01T00:00:00Z,*)` is everything from then onward.
        filterfinished_at (None | str | Unset): Restrict to runs whose `finished_at` falls in a
            half-open `[start,end)` interval. Bounds are ISO-8601 timestamps; `*` leaves a bound open.
            The leading bracket is `[` (inclusive) or `(` (exclusive) and the trailing bracket is `]`
            (inclusive) or `)` (exclusive). Example: `[2026-06-01T00:00:00Z,2026-06-08T00:00:00Z)`
            selects the first week of June; `[2026-06-01T00:00:00Z,*)` is everything from then onward.
        filterscheduled_for (None | str | Unset): Restrict to runs whose `scheduled_for` falls in
            a half-open `[start,end)` interval. Bounds are ISO-8601 timestamps; `*` leaves a bound
            open. The leading bracket is `[` (inclusive) or `(` (exclusive) and the trailing bracket
            is `]` (inclusive) or `)` (exclusive). Example:
            `[2026-06-01T00:00:00Z,2026-06-08T00:00:00Z)` selects the first week of June;
            `[2026-06-01T00:00:00Z,*)` is everything from then onward.
        last_run_only (bool | Unset): Return only the last completed run for each job-and-
            environment combination. "Completed" means a terminal state — succeeded, failed, or
            canceled; runs still in flight (pending or running) are not included, so a job that is
            currently running still shows its previous completed result. The other filters and date
            ranges apply first, then the results collapse, so each row is the most recent completed
            run in its group that also matches them. Defaults to `false`. Default: False.
        pagesize (int | None | Unset): Number of runs per page. Optional; defaults to `50` when
            omitted. Must be between `1` and `1000` inclusive — requests outside that range are
            rejected with a 400 error.
        pageafter (None | str | Unset):
        sort (ListRunsSort | Unset): Field to sort by. Prefix with `-` for descending order.
            Default: `-created_at`. Allowed values: `created_at`, `-created_at`, `finished_at`,
            `-finished_at`, `job`, `-job`, `scheduled_for`, `-scheduled_for`, `started_at`,
            `-started_at`, `status`, `-status`, `total_duration_ms`, `-total_duration_ms`. Default:
            '-created_at'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RunListResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            filterjob=filterjob,
            filterstatus=filterstatus,
            filterenvironment=filterenvironment,
            filtertrigger=filtertrigger,
            filtercreated_at=filtercreated_at,
            filterstarted_at=filterstarted_at,
            filterfinished_at=filterfinished_at,
            filterscheduled_for=filterscheduled_for,
            last_run_only=last_run_only,
            pagesize=pagesize,
            pageafter=pageafter,
            sort=sort,
        )
    ).parsed
