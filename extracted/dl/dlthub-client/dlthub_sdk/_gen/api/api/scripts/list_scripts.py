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
from ...models.job_category import JobCategory
from ...models.list_page_detailed_script_response import ListPageDetailedScriptResponse
from ...models.list_scripts_order_type_0_item import ListScriptsOrderType0Item
from ...models.list_scripts_sort_type_0_item import ListScriptsSortType0Item
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
    script_type: list[ScriptType] | None | Unset = UNSET,
    archived: bool | None | Unset = UNSET,
    paused: bool | None | Unset = UNSET,
    profile: list[str] | None | Unset = UNSET,
    pipeline_name: list[str] | None | Unset = UNSET,
    status: list[RunStatus] | None | Unset = UNSET,
    trigger_kind: list[TriggerKind] | None | Unset = UNSET,
    self_firing: bool | None | Unset = UNSET,
    category: list[JobCategory] | None | Unset = UNSET,
    exclude_category: list[JobCategory] | None | Unset = UNSET,
    tags: list[str] | None | Unset = UNSET,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    tz: str | Unset = "UTC",
    sort: list[ListScriptsSortType0Item] | None | Unset = UNSET,
    order: list[ListScriptsOrderType0Item] | None | Unset = UNSET,
    cursor: None | str | Unset = UNSET,
    recent_runs_limit: int | None | Unset = UNSET,
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

    json_archived: bool | None | Unset
    if isinstance(archived, Unset):
        json_archived = UNSET
    else:
        json_archived = archived
    params["archived"] = json_archived

    json_paused: bool | None | Unset
    if isinstance(paused, Unset):
        json_paused = UNSET
    else:
        json_paused = paused
    params["paused"] = json_paused

    json_profile: list[str] | None | Unset
    if isinstance(profile, Unset):
        json_profile = UNSET
    elif isinstance(profile, list):
        json_profile = profile

    else:
        json_profile = profile
    params["profile"] = json_profile

    json_pipeline_name: list[str] | None | Unset
    if isinstance(pipeline_name, Unset):
        json_pipeline_name = UNSET
    elif isinstance(pipeline_name, list):
        json_pipeline_name = pipeline_name

    else:
        json_pipeline_name = pipeline_name
    params["pipeline_name"] = json_pipeline_name

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

    json_self_firing: bool | None | Unset
    if isinstance(self_firing, Unset):
        json_self_firing = UNSET
    else:
        json_self_firing = self_firing
    params["self_firing"] = json_self_firing

    json_category: list[str] | None | Unset
    if isinstance(category, Unset):
        json_category = UNSET
    elif isinstance(category, list):
        json_category = []
        for category_type_0_item_data in category:
            category_type_0_item = category_type_0_item_data.value
            json_category.append(category_type_0_item)

    else:
        json_category = category
    params["category"] = json_category

    json_exclude_category: list[str] | None | Unset
    if isinstance(exclude_category, Unset):
        json_exclude_category = UNSET
    elif isinstance(exclude_category, list):
        json_exclude_category = []
        for exclude_category_type_0_item_data in exclude_category:
            exclude_category_type_0_item = exclude_category_type_0_item_data.value
            json_exclude_category.append(exclude_category_type_0_item)

    else:
        json_exclude_category = exclude_category
    params["exclude_category"] = json_exclude_category

    json_tags: list[str] | None | Unset
    if isinstance(tags, Unset):
        json_tags = UNSET
    elif isinstance(tags, list):
        json_tags = tags

    else:
        json_tags = tags
    params["tags"] = json_tags

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

    json_recent_runs_limit: int | None | Unset
    if isinstance(recent_runs_limit, Unset):
        json_recent_runs_limit = UNSET
    else:
        json_recent_runs_limit = recent_runs_limit
    params["recent_runs_limit"] = json_recent_runs_limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/workspaces/{workspace_id}/scripts".format(
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
    | ListPageDetailedScriptResponse
    | None
):
    if response.status_code == 200:
        response_200 = ListPageDetailedScriptResponse.from_dict(response.json())

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
    | ListPageDetailedScriptResponse
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
    script_type: list[ScriptType] | None | Unset = UNSET,
    archived: bool | None | Unset = UNSET,
    paused: bool | None | Unset = UNSET,
    profile: list[str] | None | Unset = UNSET,
    pipeline_name: list[str] | None | Unset = UNSET,
    status: list[RunStatus] | None | Unset = UNSET,
    trigger_kind: list[TriggerKind] | None | Unset = UNSET,
    self_firing: bool | None | Unset = UNSET,
    category: list[JobCategory] | None | Unset = UNSET,
    exclude_category: list[JobCategory] | None | Unset = UNSET,
    tags: list[str] | None | Unset = UNSET,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    tz: str | Unset = "UTC",
    sort: list[ListScriptsSortType0Item] | None | Unset = UNSET,
    order: list[ListScriptsOrderType0Item] | None | Unset = UNSET,
    cursor: None | str | Unset = UNSET,
    recent_runs_limit: int | None | Unset = UNSET,
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ListPageDetailedScriptResponse
]:
    """ListScripts

    Gets the jobs of a workspace as a paginated list, newest run first.

    Search with `q` over the job name; filter by type, archived state,
    paused state, profile, or pipeline; sort with paired `sort` and `order` lists.

    Archived and live jobs are both listed unless `archived` says which to keep.

    Requires READ permission on the organization level.

    Args:
        workspace_id (UUID):
        limit (int | Unset): Maximum number of items to return. At most 1000. Default: 100.
        offset (int | Unset): Number of items to skip. At most 10000; a list reports its total up
            to 10001, so narrow with filters instead of paging deeper. Default: 0.
        q (None | str | Unset): Case-insensitive substring match on `name`.
        script_type (list[ScriptType] | None | Unset): Exact match on `script_type`. Repeat the
            parameter to match any of several values.
        archived (bool | None | Unset): Match `archived`. Omit to list both.
        paused (bool | None | Unset): Match `paused`. Omit to list both.
        profile (list[str] | None | Unset): Exact match on `profile`. Repeat the parameter to
            match any of several values.
        pipeline_name (list[str] | None | Unset): Exact match on `pipeline_name`. Repeat the
            parameter to match any of several values.
        status (list[RunStatus] | None | Unset): Exact match on the status of the job's most
            recent run. Repeat the parameter to match any of several values.
        trigger_kind (list[TriggerKind] | None | Unset): Match jobs declaring a trigger of any
            given kind. A job may declare several kinds at once; `manual` reflects the job's
            `expose.manual` setting, which is on by default.
        self_firing (bool | None | Unset): Match jobs by whether they declare a trigger that
            starts them with no person involved: a schedule, an interval, a one-off time, a webhook,
            an HTTP endpoint, or another job's outcome.
        category (list[JobCategory] | None | Unset): Match jobs declaring any of the given
            `expose.category` values. Most jobs declare none and match nothing here.
        exclude_category (list[JobCategory] | None | Unset): Drop jobs declaring any of the given
            `expose.category` values. A job declaring none is kept.
        tags (list[str] | None | Unset): Match jobs carrying any of the given tags.
        start (datetime.datetime | None | Unset): Start of period. Naive datetime (no offset),
            interpreted in `tz`. E.g. `2026-03-01T00:00:00`.
        end (datetime.datetime | None | Unset): End of period. Naive datetime (no offset),
            interpreted in `tz`. E.g. `2026-03-11T00:00:00`.
        tz (str | Unset): IANA timezone name (e.g. 'Europe/Berlin', 'America/New_York', 'UTC').
            Used for bucket alignment and interpreting `start`/`end`. Default: 'UTC'.
        sort (list[ListScriptsSortType0Item] | None | Unset): Keys to sort by, applied in the
            order given. Pairs positionally with `order`, which must have the same number of entries.
        order (list[ListScriptsOrderType0Item] | None | Unset): Sort directions, one per `sort`
            key and in the same order. Required whenever `sort` is supplied.
        cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`;
            returns the rows after it under the same `sort` and `order`. Mutually exclusive with
            `offset`.
        recent_runs_limit (int | None | Unset): Attach this many of the job's most recent runs.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ListPageDetailedScriptResponse]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        limit=limit,
        offset=offset,
        q=q,
        script_type=script_type,
        archived=archived,
        paused=paused,
        profile=profile,
        pipeline_name=pipeline_name,
        status=status,
        trigger_kind=trigger_kind,
        self_firing=self_firing,
        category=category,
        exclude_category=exclude_category,
        tags=tags,
        start=start,
        end=end,
        tz=tz,
        sort=sort,
        order=order,
        cursor=cursor,
        recent_runs_limit=recent_runs_limit,
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
    script_type: list[ScriptType] | None | Unset = UNSET,
    archived: bool | None | Unset = UNSET,
    paused: bool | None | Unset = UNSET,
    profile: list[str] | None | Unset = UNSET,
    pipeline_name: list[str] | None | Unset = UNSET,
    status: list[RunStatus] | None | Unset = UNSET,
    trigger_kind: list[TriggerKind] | None | Unset = UNSET,
    self_firing: bool | None | Unset = UNSET,
    category: list[JobCategory] | None | Unset = UNSET,
    exclude_category: list[JobCategory] | None | Unset = UNSET,
    tags: list[str] | None | Unset = UNSET,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    tz: str | Unset = "UTC",
    sort: list[ListScriptsSortType0Item] | None | Unset = UNSET,
    order: list[ListScriptsOrderType0Item] | None | Unset = UNSET,
    cursor: None | str | Unset = UNSET,
    recent_runs_limit: int | None | Unset = UNSET,
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ListPageDetailedScriptResponse
    | None
):
    """ListScripts

    Gets the jobs of a workspace as a paginated list, newest run first.

    Search with `q` over the job name; filter by type, archived state,
    paused state, profile, or pipeline; sort with paired `sort` and `order` lists.

    Archived and live jobs are both listed unless `archived` says which to keep.

    Requires READ permission on the organization level.

    Args:
        workspace_id (UUID):
        limit (int | Unset): Maximum number of items to return. At most 1000. Default: 100.
        offset (int | Unset): Number of items to skip. At most 10000; a list reports its total up
            to 10001, so narrow with filters instead of paging deeper. Default: 0.
        q (None | str | Unset): Case-insensitive substring match on `name`.
        script_type (list[ScriptType] | None | Unset): Exact match on `script_type`. Repeat the
            parameter to match any of several values.
        archived (bool | None | Unset): Match `archived`. Omit to list both.
        paused (bool | None | Unset): Match `paused`. Omit to list both.
        profile (list[str] | None | Unset): Exact match on `profile`. Repeat the parameter to
            match any of several values.
        pipeline_name (list[str] | None | Unset): Exact match on `pipeline_name`. Repeat the
            parameter to match any of several values.
        status (list[RunStatus] | None | Unset): Exact match on the status of the job's most
            recent run. Repeat the parameter to match any of several values.
        trigger_kind (list[TriggerKind] | None | Unset): Match jobs declaring a trigger of any
            given kind. A job may declare several kinds at once; `manual` reflects the job's
            `expose.manual` setting, which is on by default.
        self_firing (bool | None | Unset): Match jobs by whether they declare a trigger that
            starts them with no person involved: a schedule, an interval, a one-off time, a webhook,
            an HTTP endpoint, or another job's outcome.
        category (list[JobCategory] | None | Unset): Match jobs declaring any of the given
            `expose.category` values. Most jobs declare none and match nothing here.
        exclude_category (list[JobCategory] | None | Unset): Drop jobs declaring any of the given
            `expose.category` values. A job declaring none is kept.
        tags (list[str] | None | Unset): Match jobs carrying any of the given tags.
        start (datetime.datetime | None | Unset): Start of period. Naive datetime (no offset),
            interpreted in `tz`. E.g. `2026-03-01T00:00:00`.
        end (datetime.datetime | None | Unset): End of period. Naive datetime (no offset),
            interpreted in `tz`. E.g. `2026-03-11T00:00:00`.
        tz (str | Unset): IANA timezone name (e.g. 'Europe/Berlin', 'America/New_York', 'UTC').
            Used for bucket alignment and interpreting `start`/`end`. Default: 'UTC'.
        sort (list[ListScriptsSortType0Item] | None | Unset): Keys to sort by, applied in the
            order given. Pairs positionally with `order`, which must have the same number of entries.
        order (list[ListScriptsOrderType0Item] | None | Unset): Sort directions, one per `sort`
            key and in the same order. Required whenever `sort` is supplied.
        cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`;
            returns the rows after it under the same `sort` and `order`. Mutually exclusive with
            `offset`.
        recent_runs_limit (int | None | Unset): Attach this many of the job's most recent runs.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ListPageDetailedScriptResponse
    """
    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
        limit=limit,
        offset=offset,
        q=q,
        script_type=script_type,
        archived=archived,
        paused=paused,
        profile=profile,
        pipeline_name=pipeline_name,
        status=status,
        trigger_kind=trigger_kind,
        self_firing=self_firing,
        category=category,
        exclude_category=exclude_category,
        tags=tags,
        start=start,
        end=end,
        tz=tz,
        sort=sort,
        order=order,
        cursor=cursor,
        recent_runs_limit=recent_runs_limit,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    q: None | str | Unset = UNSET,
    script_type: list[ScriptType] | None | Unset = UNSET,
    archived: bool | None | Unset = UNSET,
    paused: bool | None | Unset = UNSET,
    profile: list[str] | None | Unset = UNSET,
    pipeline_name: list[str] | None | Unset = UNSET,
    status: list[RunStatus] | None | Unset = UNSET,
    trigger_kind: list[TriggerKind] | None | Unset = UNSET,
    self_firing: bool | None | Unset = UNSET,
    category: list[JobCategory] | None | Unset = UNSET,
    exclude_category: list[JobCategory] | None | Unset = UNSET,
    tags: list[str] | None | Unset = UNSET,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    tz: str | Unset = "UTC",
    sort: list[ListScriptsSortType0Item] | None | Unset = UNSET,
    order: list[ListScriptsOrderType0Item] | None | Unset = UNSET,
    cursor: None | str | Unset = UNSET,
    recent_runs_limit: int | None | Unset = UNSET,
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ListPageDetailedScriptResponse
]:
    """ListScripts

    Gets the jobs of a workspace as a paginated list, newest run first.

    Search with `q` over the job name; filter by type, archived state,
    paused state, profile, or pipeline; sort with paired `sort` and `order` lists.

    Archived and live jobs are both listed unless `archived` says which to keep.

    Requires READ permission on the organization level.

    Args:
        workspace_id (UUID):
        limit (int | Unset): Maximum number of items to return. At most 1000. Default: 100.
        offset (int | Unset): Number of items to skip. At most 10000; a list reports its total up
            to 10001, so narrow with filters instead of paging deeper. Default: 0.
        q (None | str | Unset): Case-insensitive substring match on `name`.
        script_type (list[ScriptType] | None | Unset): Exact match on `script_type`. Repeat the
            parameter to match any of several values.
        archived (bool | None | Unset): Match `archived`. Omit to list both.
        paused (bool | None | Unset): Match `paused`. Omit to list both.
        profile (list[str] | None | Unset): Exact match on `profile`. Repeat the parameter to
            match any of several values.
        pipeline_name (list[str] | None | Unset): Exact match on `pipeline_name`. Repeat the
            parameter to match any of several values.
        status (list[RunStatus] | None | Unset): Exact match on the status of the job's most
            recent run. Repeat the parameter to match any of several values.
        trigger_kind (list[TriggerKind] | None | Unset): Match jobs declaring a trigger of any
            given kind. A job may declare several kinds at once; `manual` reflects the job's
            `expose.manual` setting, which is on by default.
        self_firing (bool | None | Unset): Match jobs by whether they declare a trigger that
            starts them with no person involved: a schedule, an interval, a one-off time, a webhook,
            an HTTP endpoint, or another job's outcome.
        category (list[JobCategory] | None | Unset): Match jobs declaring any of the given
            `expose.category` values. Most jobs declare none and match nothing here.
        exclude_category (list[JobCategory] | None | Unset): Drop jobs declaring any of the given
            `expose.category` values. A job declaring none is kept.
        tags (list[str] | None | Unset): Match jobs carrying any of the given tags.
        start (datetime.datetime | None | Unset): Start of period. Naive datetime (no offset),
            interpreted in `tz`. E.g. `2026-03-01T00:00:00`.
        end (datetime.datetime | None | Unset): End of period. Naive datetime (no offset),
            interpreted in `tz`. E.g. `2026-03-11T00:00:00`.
        tz (str | Unset): IANA timezone name (e.g. 'Europe/Berlin', 'America/New_York', 'UTC').
            Used for bucket alignment and interpreting `start`/`end`. Default: 'UTC'.
        sort (list[ListScriptsSortType0Item] | None | Unset): Keys to sort by, applied in the
            order given. Pairs positionally with `order`, which must have the same number of entries.
        order (list[ListScriptsOrderType0Item] | None | Unset): Sort directions, one per `sort`
            key and in the same order. Required whenever `sort` is supplied.
        cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`;
            returns the rows after it under the same `sort` and `order`. Mutually exclusive with
            `offset`.
        recent_runs_limit (int | None | Unset): Attach this many of the job's most recent runs.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ListPageDetailedScriptResponse]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        limit=limit,
        offset=offset,
        q=q,
        script_type=script_type,
        archived=archived,
        paused=paused,
        profile=profile,
        pipeline_name=pipeline_name,
        status=status,
        trigger_kind=trigger_kind,
        self_firing=self_firing,
        category=category,
        exclude_category=exclude_category,
        tags=tags,
        start=start,
        end=end,
        tz=tz,
        sort=sort,
        order=order,
        cursor=cursor,
        recent_runs_limit=recent_runs_limit,
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
    script_type: list[ScriptType] | None | Unset = UNSET,
    archived: bool | None | Unset = UNSET,
    paused: bool | None | Unset = UNSET,
    profile: list[str] | None | Unset = UNSET,
    pipeline_name: list[str] | None | Unset = UNSET,
    status: list[RunStatus] | None | Unset = UNSET,
    trigger_kind: list[TriggerKind] | None | Unset = UNSET,
    self_firing: bool | None | Unset = UNSET,
    category: list[JobCategory] | None | Unset = UNSET,
    exclude_category: list[JobCategory] | None | Unset = UNSET,
    tags: list[str] | None | Unset = UNSET,
    start: datetime.datetime | None | Unset = UNSET,
    end: datetime.datetime | None | Unset = UNSET,
    tz: str | Unset = "UTC",
    sort: list[ListScriptsSortType0Item] | None | Unset = UNSET,
    order: list[ListScriptsOrderType0Item] | None | Unset = UNSET,
    cursor: None | str | Unset = UNSET,
    recent_runs_limit: int | None | Unset = UNSET,
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ListPageDetailedScriptResponse
    | None
):
    """ListScripts

    Gets the jobs of a workspace as a paginated list, newest run first.

    Search with `q` over the job name; filter by type, archived state,
    paused state, profile, or pipeline; sort with paired `sort` and `order` lists.

    Archived and live jobs are both listed unless `archived` says which to keep.

    Requires READ permission on the organization level.

    Args:
        workspace_id (UUID):
        limit (int | Unset): Maximum number of items to return. At most 1000. Default: 100.
        offset (int | Unset): Number of items to skip. At most 10000; a list reports its total up
            to 10001, so narrow with filters instead of paging deeper. Default: 0.
        q (None | str | Unset): Case-insensitive substring match on `name`.
        script_type (list[ScriptType] | None | Unset): Exact match on `script_type`. Repeat the
            parameter to match any of several values.
        archived (bool | None | Unset): Match `archived`. Omit to list both.
        paused (bool | None | Unset): Match `paused`. Omit to list both.
        profile (list[str] | None | Unset): Exact match on `profile`. Repeat the parameter to
            match any of several values.
        pipeline_name (list[str] | None | Unset): Exact match on `pipeline_name`. Repeat the
            parameter to match any of several values.
        status (list[RunStatus] | None | Unset): Exact match on the status of the job's most
            recent run. Repeat the parameter to match any of several values.
        trigger_kind (list[TriggerKind] | None | Unset): Match jobs declaring a trigger of any
            given kind. A job may declare several kinds at once; `manual` reflects the job's
            `expose.manual` setting, which is on by default.
        self_firing (bool | None | Unset): Match jobs by whether they declare a trigger that
            starts them with no person involved: a schedule, an interval, a one-off time, a webhook,
            an HTTP endpoint, or another job's outcome.
        category (list[JobCategory] | None | Unset): Match jobs declaring any of the given
            `expose.category` values. Most jobs declare none and match nothing here.
        exclude_category (list[JobCategory] | None | Unset): Drop jobs declaring any of the given
            `expose.category` values. A job declaring none is kept.
        tags (list[str] | None | Unset): Match jobs carrying any of the given tags.
        start (datetime.datetime | None | Unset): Start of period. Naive datetime (no offset),
            interpreted in `tz`. E.g. `2026-03-01T00:00:00`.
        end (datetime.datetime | None | Unset): End of period. Naive datetime (no offset),
            interpreted in `tz`. E.g. `2026-03-11T00:00:00`.
        tz (str | Unset): IANA timezone name (e.g. 'Europe/Berlin', 'America/New_York', 'UTC').
            Used for bucket alignment and interpreting `start`/`end`. Default: 'UTC'.
        sort (list[ListScriptsSortType0Item] | None | Unset): Keys to sort by, applied in the
            order given. Pairs positionally with `order`, which must have the same number of entries.
        order (list[ListScriptsOrderType0Item] | None | Unset): Sort directions, one per `sort`
            key and in the same order. Required whenever `sort` is supplied.
        cursor (None | str | Unset): Opaque cursor from a previous response's `next_cursor`;
            returns the rows after it under the same `sort` and `order`. Mutually exclusive with
            `offset`.
        recent_runs_limit (int | None | Unset): Attach this many of the job's most recent runs.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ListPageDetailedScriptResponse
    """
    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            limit=limit,
            offset=offset,
            q=q,
            script_type=script_type,
            archived=archived,
            paused=paused,
            profile=profile,
            pipeline_name=pipeline_name,
            status=status,
            trigger_kind=trigger_kind,
            self_firing=self_firing,
            category=category,
            exclude_category=exclude_category,
            tags=tags,
            start=start,
            end=end,
            tz=tz,
            sort=sort,
            order=order,
            cursor=cursor,
            recent_runs_limit=recent_runs_limit,
        )
    ).parsed
