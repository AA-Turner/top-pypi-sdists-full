import datetime
from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response_400 import ErrorResponse400
from ...models.error_response_401 import ErrorResponse401
from ...models.error_response_403 import ErrorResponse403
from ...models.error_response_404 import ErrorResponse404
from ...models.list_page_detailed_run_response import ListPageDetailedRunResponse
from ...models.list_runs_order_type_0_item import ListRunsOrderType0Item
from ...models.list_runs_sort_type_0_item import ListRunsSortType0Item
from ...models.run_status import RunStatus
from ...models.script_type import ScriptType
from ...models.trigger_kind import TriggerKind
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace_id: UUID,
    *,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    q: None | str | Unset = UNSET,
    status: list[RunStatus] | None | Unset = UNSET,
    script_id: None | Unset | UUID = UNSET,
    prev_run_id: None | Unset | UUID = UNSET,
    script_type: list[ScriptType] | None | Unset = UNSET,
    trigger: list[str] | None | Unset = UNSET,
    trigger_kind: list[TriggerKind] | None | Unset = UNSET,
    triggered_by: list[str] | None | Unset = UNSET,
    profile: list[str] | None | Unset = UNSET,
    duration_min: float | None | Unset = UNSET,
    duration_max: float | None | Unset = UNSET,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    tz: str | Unset = "UTC",
    sort: list[ListRunsSortType0Item] | None | Unset = UNSET,
    order: list[ListRunsOrderType0Item] | None | Unset = UNSET,
    cursor: None | str | Unset = UNSET,
    include_system_runs: bool | Unset = False,
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

    json_script_id: None | str | Unset
    if isinstance(script_id, Unset):
        json_script_id = UNSET
    elif isinstance(script_id, UUID):
        json_script_id = str(script_id)
    else:
        json_script_id = script_id
    params["script_id"] = json_script_id

    json_prev_run_id: None | str | Unset
    if isinstance(prev_run_id, Unset):
        json_prev_run_id = UNSET
    elif isinstance(prev_run_id, UUID):
        json_prev_run_id = str(prev_run_id)
    else:
        json_prev_run_id = prev_run_id
    params["prev_run_id"] = json_prev_run_id

    json_script_type: list[str] | None | Unset
    if isinstance(script_type, Unset):
        json_script_type = UNSET
    elif isinstance(script_type, list):
        json_script_type = []
        for script_type_type_0_item_data in script_type:
            script_type_type_0_item = script_type_type_0_item_data.value
            json_script_type.append(script_type_type_0_item)

    else:
        json_script_type = script_type
    params["script_type"] = json_script_type

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
        json_triggered_by = triggered_by

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

    json_duration_min: float | None | Unset
    if isinstance(duration_min, Unset):
        json_duration_min = UNSET
    else:
        json_duration_min = duration_min
    params["duration_min"] = json_duration_min

    json_duration_max: float | None | Unset
    if isinstance(duration_max, Unset):
        json_duration_max = UNSET
    else:
        json_duration_max = duration_max
    params["duration_max"] = json_duration_max

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

    params["tz"] = tz

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

    params["include_system_runs"] = include_system_runs

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/workspaces/{workspace_id}/runs".format(
            workspace_id=quote(str(workspace_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ListPageDetailedRunResponse
    | None
):
    if response.status_code == 200:
        response_200 = ListPageDetailedRunResponse.from_dict(response.json())

        return response_200

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
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ListPageDetailedRunResponse
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
    client: AuthenticatedClient | Client,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    q: None | str | Unset = UNSET,
    status: list[RunStatus] | None | Unset = UNSET,
    script_id: None | Unset | UUID = UNSET,
    prev_run_id: None | Unset | UUID = UNSET,
    script_type: list[ScriptType] | None | Unset = UNSET,
    trigger: list[str] | None | Unset = UNSET,
    trigger_kind: list[TriggerKind] | None | Unset = UNSET,
    triggered_by: list[str] | None | Unset = UNSET,
    profile: list[str] | None | Unset = UNSET,
    duration_min: float | None | Unset = UNSET,
    duration_max: float | None | Unset = UNSET,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    tz: str | Unset = "UTC",
    sort: list[ListRunsSortType0Item] | None | Unset = UNSET,
    order: list[ListRunsOrderType0Item] | None | Unset = UNSET,
    cursor: None | str | Unset = UNSET,
    include_system_runs: bool | Unset = False,
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ListPageDetailedRunResponse
]:
    """ListRuns

    Gets the job runs of a workspace as a paginated list, newest first.

    Search with `q` over the job name; filter by status, job, job type, trigger,
    profile, upstream run (`prev_run_id`, giving the runs one run triggered), or a
    time window; sort with paired `sort` and `order` lists.

    System runs, such as the dashboard job, are excluded unless `script_id` or
    `prev_run_id` names one, or `include_system_runs` is set.

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
        script_id (None | Unset | UUID): Exact match on `script_id`.
        prev_run_id (None | Unset | UUID): Exact match on `prev_run_id`.
        script_type (list[ScriptType] | None | Unset): Exact match on `script_type`. Repeat the
            parameter to match any of several values.
        trigger (list[str] | None | Unset): Exact match on `trigger`. Repeat the parameter to
            match any of several values.
        trigger_kind (list[TriggerKind] | None | Unset): Match runs by the kind of trigger that
            fired them, whatever its expression. `manual` means a person started the run.
        triggered_by (list[str] | None | Unset): Exact match on `triggered_by`. Repeat the
            parameter to match any of several values.
        profile (list[str] | None | Unset): Exact match on `profile`. Repeat the parameter to
            match any of several values.
        duration_min (float | None | Unset): Inclusive range over `duration`, given as
            `duration_min` and `duration_max`. Either bound may stand alone.
        duration_max (float | None | Unset): Inclusive range over `duration`, given as
            `duration_min` and `duration_max`. Either bound may stand alone.
        start (datetime.datetime | None | Unset): Start of period. Naive datetime (no offset),
            interpreted in `tz`. E.g. `2026-03-01T00:00:00`.
        end (datetime.datetime | None | Unset): End of period. Naive datetime (no offset),
            interpreted in `tz`. E.g. `2026-03-11T00:00:00`.
        tz (str | Unset): IANA timezone name (e.g. 'Europe/Berlin', 'America/New_York', 'UTC').
            Used for bucket alignment and interpreting `start`/`end`. Default: 'UTC'.
        sort (list[ListRunsSortType0Item] | None | Unset): Keys to sort by, applied in the order
            given. Pairs positionally with `order`, which must have the same number of entries.
        order (list[ListRunsOrderType0Item] | None | Unset): Sort directions, one per `sort` key
            and in the same order. Required whenever `sort` is supplied.
        cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`;
            returns the rows after it under the same `sort` and `order`. Mutually exclusive with
            `offset`.
        include_system_runs (bool | Unset): Include runs of system jobs such as the dashboard.
            Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ListPageDetailedRunResponse]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        limit=limit,
        offset=offset,
        q=q,
        status=status,
        script_id=script_id,
        prev_run_id=prev_run_id,
        script_type=script_type,
        trigger=trigger,
        trigger_kind=trigger_kind,
        triggered_by=triggered_by,
        profile=profile,
        duration_min=duration_min,
        duration_max=duration_max,
        start=start,
        end=end,
        tz=tz,
        sort=sort,
        order=order,
        cursor=cursor,
        include_system_runs=include_system_runs,
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
    script_id: None | Unset | UUID = UNSET,
    prev_run_id: None | Unset | UUID = UNSET,
    script_type: list[ScriptType] | None | Unset = UNSET,
    trigger: list[str] | None | Unset = UNSET,
    trigger_kind: list[TriggerKind] | None | Unset = UNSET,
    triggered_by: list[str] | None | Unset = UNSET,
    profile: list[str] | None | Unset = UNSET,
    duration_min: float | None | Unset = UNSET,
    duration_max: float | None | Unset = UNSET,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    tz: str | Unset = "UTC",
    sort: list[ListRunsSortType0Item] | None | Unset = UNSET,
    order: list[ListRunsOrderType0Item] | None | Unset = UNSET,
    cursor: None | str | Unset = UNSET,
    include_system_runs: bool | Unset = False,
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ListPageDetailedRunResponse
    | None
):
    """ListRuns

    Gets the job runs of a workspace as a paginated list, newest first.

    Search with `q` over the job name; filter by status, job, job type, trigger,
    profile, upstream run (`prev_run_id`, giving the runs one run triggered), or a
    time window; sort with paired `sort` and `order` lists.

    System runs, such as the dashboard job, are excluded unless `script_id` or
    `prev_run_id` names one, or `include_system_runs` is set.

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
        script_id (None | Unset | UUID): Exact match on `script_id`.
        prev_run_id (None | Unset | UUID): Exact match on `prev_run_id`.
        script_type (list[ScriptType] | None | Unset): Exact match on `script_type`. Repeat the
            parameter to match any of several values.
        trigger (list[str] | None | Unset): Exact match on `trigger`. Repeat the parameter to
            match any of several values.
        trigger_kind (list[TriggerKind] | None | Unset): Match runs by the kind of trigger that
            fired them, whatever its expression. `manual` means a person started the run.
        triggered_by (list[str] | None | Unset): Exact match on `triggered_by`. Repeat the
            parameter to match any of several values.
        profile (list[str] | None | Unset): Exact match on `profile`. Repeat the parameter to
            match any of several values.
        duration_min (float | None | Unset): Inclusive range over `duration`, given as
            `duration_min` and `duration_max`. Either bound may stand alone.
        duration_max (float | None | Unset): Inclusive range over `duration`, given as
            `duration_min` and `duration_max`. Either bound may stand alone.
        start (datetime.datetime | None | Unset): Start of period. Naive datetime (no offset),
            interpreted in `tz`. E.g. `2026-03-01T00:00:00`.
        end (datetime.datetime | None | Unset): End of period. Naive datetime (no offset),
            interpreted in `tz`. E.g. `2026-03-11T00:00:00`.
        tz (str | Unset): IANA timezone name (e.g. 'Europe/Berlin', 'America/New_York', 'UTC').
            Used for bucket alignment and interpreting `start`/`end`. Default: 'UTC'.
        sort (list[ListRunsSortType0Item] | None | Unset): Keys to sort by, applied in the order
            given. Pairs positionally with `order`, which must have the same number of entries.
        order (list[ListRunsOrderType0Item] | None | Unset): Sort directions, one per `sort` key
            and in the same order. Required whenever `sort` is supplied.
        cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`;
            returns the rows after it under the same `sort` and `order`. Mutually exclusive with
            `offset`.
        include_system_runs (bool | Unset): Include runs of system jobs such as the dashboard.
            Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ListPageDetailedRunResponse
    """
    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
        limit=limit,
        offset=offset,
        q=q,
        status=status,
        script_id=script_id,
        prev_run_id=prev_run_id,
        script_type=script_type,
        trigger=trigger,
        trigger_kind=trigger_kind,
        triggered_by=triggered_by,
        profile=profile,
        duration_min=duration_min,
        duration_max=duration_max,
        start=start,
        end=end,
        tz=tz,
        sort=sort,
        order=order,
        cursor=cursor,
        include_system_runs=include_system_runs,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    q: None | str | Unset = UNSET,
    status: list[RunStatus] | None | Unset = UNSET,
    script_id: None | Unset | UUID = UNSET,
    prev_run_id: None | Unset | UUID = UNSET,
    script_type: list[ScriptType] | None | Unset = UNSET,
    trigger: list[str] | None | Unset = UNSET,
    trigger_kind: list[TriggerKind] | None | Unset = UNSET,
    triggered_by: list[str] | None | Unset = UNSET,
    profile: list[str] | None | Unset = UNSET,
    duration_min: float | None | Unset = UNSET,
    duration_max: float | None | Unset = UNSET,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    tz: str | Unset = "UTC",
    sort: list[ListRunsSortType0Item] | None | Unset = UNSET,
    order: list[ListRunsOrderType0Item] | None | Unset = UNSET,
    cursor: None | str | Unset = UNSET,
    include_system_runs: bool | Unset = False,
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ListPageDetailedRunResponse
]:
    """ListRuns

    Gets the job runs of a workspace as a paginated list, newest first.

    Search with `q` over the job name; filter by status, job, job type, trigger,
    profile, upstream run (`prev_run_id`, giving the runs one run triggered), or a
    time window; sort with paired `sort` and `order` lists.

    System runs, such as the dashboard job, are excluded unless `script_id` or
    `prev_run_id` names one, or `include_system_runs` is set.

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
        script_id (None | Unset | UUID): Exact match on `script_id`.
        prev_run_id (None | Unset | UUID): Exact match on `prev_run_id`.
        script_type (list[ScriptType] | None | Unset): Exact match on `script_type`. Repeat the
            parameter to match any of several values.
        trigger (list[str] | None | Unset): Exact match on `trigger`. Repeat the parameter to
            match any of several values.
        trigger_kind (list[TriggerKind] | None | Unset): Match runs by the kind of trigger that
            fired them, whatever its expression. `manual` means a person started the run.
        triggered_by (list[str] | None | Unset): Exact match on `triggered_by`. Repeat the
            parameter to match any of several values.
        profile (list[str] | None | Unset): Exact match on `profile`. Repeat the parameter to
            match any of several values.
        duration_min (float | None | Unset): Inclusive range over `duration`, given as
            `duration_min` and `duration_max`. Either bound may stand alone.
        duration_max (float | None | Unset): Inclusive range over `duration`, given as
            `duration_min` and `duration_max`. Either bound may stand alone.
        start (datetime.datetime | None | Unset): Start of period. Naive datetime (no offset),
            interpreted in `tz`. E.g. `2026-03-01T00:00:00`.
        end (datetime.datetime | None | Unset): End of period. Naive datetime (no offset),
            interpreted in `tz`. E.g. `2026-03-11T00:00:00`.
        tz (str | Unset): IANA timezone name (e.g. 'Europe/Berlin', 'America/New_York', 'UTC').
            Used for bucket alignment and interpreting `start`/`end`. Default: 'UTC'.
        sort (list[ListRunsSortType0Item] | None | Unset): Keys to sort by, applied in the order
            given. Pairs positionally with `order`, which must have the same number of entries.
        order (list[ListRunsOrderType0Item] | None | Unset): Sort directions, one per `sort` key
            and in the same order. Required whenever `sort` is supplied.
        cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`;
            returns the rows after it under the same `sort` and `order`. Mutually exclusive with
            `offset`.
        include_system_runs (bool | Unset): Include runs of system jobs such as the dashboard.
            Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ListPageDetailedRunResponse]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        limit=limit,
        offset=offset,
        q=q,
        status=status,
        script_id=script_id,
        prev_run_id=prev_run_id,
        script_type=script_type,
        trigger=trigger,
        trigger_kind=trigger_kind,
        triggered_by=triggered_by,
        profile=profile,
        duration_min=duration_min,
        duration_max=duration_max,
        start=start,
        end=end,
        tz=tz,
        sort=sort,
        order=order,
        cursor=cursor,
        include_system_runs=include_system_runs,
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
    script_id: None | Unset | UUID = UNSET,
    prev_run_id: None | Unset | UUID = UNSET,
    script_type: list[ScriptType] | None | Unset = UNSET,
    trigger: list[str] | None | Unset = UNSET,
    trigger_kind: list[TriggerKind] | None | Unset = UNSET,
    triggered_by: list[str] | None | Unset = UNSET,
    profile: list[str] | None | Unset = UNSET,
    duration_min: float | None | Unset = UNSET,
    duration_max: float | None | Unset = UNSET,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    tz: str | Unset = "UTC",
    sort: list[ListRunsSortType0Item] | None | Unset = UNSET,
    order: list[ListRunsOrderType0Item] | None | Unset = UNSET,
    cursor: None | str | Unset = UNSET,
    include_system_runs: bool | Unset = False,
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ListPageDetailedRunResponse
    | None
):
    """ListRuns

    Gets the job runs of a workspace as a paginated list, newest first.

    Search with `q` over the job name; filter by status, job, job type, trigger,
    profile, upstream run (`prev_run_id`, giving the runs one run triggered), or a
    time window; sort with paired `sort` and `order` lists.

    System runs, such as the dashboard job, are excluded unless `script_id` or
    `prev_run_id` names one, or `include_system_runs` is set.

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
        script_id (None | Unset | UUID): Exact match on `script_id`.
        prev_run_id (None | Unset | UUID): Exact match on `prev_run_id`.
        script_type (list[ScriptType] | None | Unset): Exact match on `script_type`. Repeat the
            parameter to match any of several values.
        trigger (list[str] | None | Unset): Exact match on `trigger`. Repeat the parameter to
            match any of several values.
        trigger_kind (list[TriggerKind] | None | Unset): Match runs by the kind of trigger that
            fired them, whatever its expression. `manual` means a person started the run.
        triggered_by (list[str] | None | Unset): Exact match on `triggered_by`. Repeat the
            parameter to match any of several values.
        profile (list[str] | None | Unset): Exact match on `profile`. Repeat the parameter to
            match any of several values.
        duration_min (float | None | Unset): Inclusive range over `duration`, given as
            `duration_min` and `duration_max`. Either bound may stand alone.
        duration_max (float | None | Unset): Inclusive range over `duration`, given as
            `duration_min` and `duration_max`. Either bound may stand alone.
        start (datetime.datetime | None | Unset): Start of period. Naive datetime (no offset),
            interpreted in `tz`. E.g. `2026-03-01T00:00:00`.
        end (datetime.datetime | None | Unset): End of period. Naive datetime (no offset),
            interpreted in `tz`. E.g. `2026-03-11T00:00:00`.
        tz (str | Unset): IANA timezone name (e.g. 'Europe/Berlin', 'America/New_York', 'UTC').
            Used for bucket alignment and interpreting `start`/`end`. Default: 'UTC'.
        sort (list[ListRunsSortType0Item] | None | Unset): Keys to sort by, applied in the order
            given. Pairs positionally with `order`, which must have the same number of entries.
        order (list[ListRunsOrderType0Item] | None | Unset): Sort directions, one per `sort` key
            and in the same order. Required whenever `sort` is supplied.
        cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`;
            returns the rows after it under the same `sort` and `order`. Mutually exclusive with
            `offset`.
        include_system_runs (bool | Unset): Include runs of system jobs such as the dashboard.
            Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ListPageDetailedRunResponse
    """
    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            limit=limit,
            offset=offset,
            q=q,
            status=status,
            script_id=script_id,
            prev_run_id=prev_run_id,
            script_type=script_type,
            trigger=trigger,
            trigger_kind=trigger_kind,
            triggered_by=triggered_by,
            profile=profile,
            duration_min=duration_min,
            duration_max=duration_max,
            start=start,
            end=end,
            tz=tz,
            sort=sort,
            order=order,
            cursor=cursor,
            include_system_runs=include_system_runs,
        )
    ).parsed
