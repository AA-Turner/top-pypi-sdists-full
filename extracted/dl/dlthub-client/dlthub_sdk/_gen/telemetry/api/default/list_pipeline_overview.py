import datetime
from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response_400 import ErrorResponse400
from ...models.list_pipeline_overview_order_type_0_item import (
    ListPipelineOverviewOrderType0Item,
)
from ...models.list_pipeline_overview_response_200 import (
    ListPipelineOverviewResponse200,
)
from ...models.list_pipeline_overview_sort_type_0_item import (
    ListPipelineOverviewSortType0Item,
)
from ...models.pipeline_run_status import PipelineRunStatus
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace_id: UUID,
    *,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    start: datetime.datetime,
    end: datetime.datetime,
    tz: str | Unset = "UTC",
    q: None | str | Unset = UNSET,
    pipeline_name: list[str] | None | Unset = UNSET,
    latest_status: list[PipelineRunStatus] | None | Unset = UNSET,
    latest_destination_name: list[str] | None | Unset = UNSET,
    sort: list[ListPipelineOverviewSortType0Item] | None | Unset = UNSET,
    order: list[ListPipelineOverviewOrderType0Item] | None | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    json_start = start.isoformat()
    params["start"] = json_start

    json_end = end.isoformat()
    params["end"] = json_end

    params["tz"] = tz

    json_q: None | str | Unset
    if isinstance(q, Unset):
        json_q = UNSET
    else:
        json_q = q
    params["q"] = json_q

    json_pipeline_name: list[str] | None | Unset
    if isinstance(pipeline_name, Unset):
        json_pipeline_name = UNSET
    elif isinstance(pipeline_name, list):
        json_pipeline_name = pipeline_name

    else:
        json_pipeline_name = pipeline_name
    params["pipeline_name"] = json_pipeline_name

    json_latest_status: list[str] | None | Unset
    if isinstance(latest_status, Unset):
        json_latest_status = UNSET
    elif isinstance(latest_status, list):
        json_latest_status = []
        for latest_status_type_0_item_data in latest_status:
            latest_status_type_0_item = latest_status_type_0_item_data.value
            json_latest_status.append(latest_status_type_0_item)

    else:
        json_latest_status = latest_status
    params["latest_status"] = json_latest_status

    json_latest_destination_name: list[str] | None | Unset
    if isinstance(latest_destination_name, Unset):
        json_latest_destination_name = UNSET
    elif isinstance(latest_destination_name, list):
        json_latest_destination_name = latest_destination_name

    else:
        json_latest_destination_name = latest_destination_name
    params["latest_destination_name"] = json_latest_destination_name

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

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/telemetry/v1/workspaces/{workspace_id}/pipelines/stats".format(
            workspace_id=quote(str(workspace_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse400 | ListPipelineOverviewResponse200 | None:
    if response.status_code == 200:
        response_200 = ListPipelineOverviewResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse400.from_dict(response.json())

        return response_400

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse400 | ListPipelineOverviewResponse200]:
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
    start: datetime.datetime,
    end: datetime.datetime,
    tz: str | Unset = "UTC",
    q: None | str | Unset = UNSET,
    pipeline_name: list[str] | None | Unset = UNSET,
    latest_status: list[PipelineRunStatus] | None | Unset = UNSET,
    latest_destination_name: list[str] | None | Unset = UNSET,
    sort: list[ListPipelineOverviewSortType0Item] | None | Unset = UNSET,
    order: list[ListPipelineOverviewOrderType0Item] | None | Unset = UNSET,
) -> Response[ErrorResponse400 | ListPipelineOverviewResponse200]:
    """ListPipelineOverview

    One row per pipeline in the time range, with its aggregate metrics.

    Search with `q` over the pipeline name, filter on what a row displays, and sort
    with paired `sort` and `order` lists.

    Args:
        workspace_id (UUID):
        limit (int | Unset): Maximum number of items to return. At most 1000. Default: 100.
        offset (int | Unset): Number of items to skip. At most 10000; a list reports its total up
            to 10001, so narrow with filters instead of paging deeper. Default: 0.
        start (datetime.datetime): Start of period. Naive datetime (no offset), interpreted in
            `tz`. E.g. `2026-03-01T00:00:00`.
        end (datetime.datetime): End of period. Naive datetime (no offset), interpreted in `tz`.
            E.g. `2026-03-11T00:00:00`.
        tz (str | Unset): IANA timezone name (e.g. 'Europe/Berlin', 'America/New_York', 'UTC').
            Used for bucket alignment and interpreting `start`/`end`. Default: 'UTC'.
        q (None | str | Unset): Case-insensitive substring match on `pipeline_name`.
        pipeline_name (list[str] | None | Unset): Exact match on `pipeline_name`. Repeat the
            parameter to match any of several values.
        latest_status (list[PipelineRunStatus] | None | Unset): Exact match on `latest_status`.
            Repeat the parameter to match any of several values.
        latest_destination_name (list[str] | None | Unset): Exact match on
            `latest_destination_name`. Repeat the parameter to match any of several values.
        sort (list[ListPipelineOverviewSortType0Item] | None | Unset): Keys to sort by, applied in
            the order given. Pairs positionally with `order`, which must have the same number of
            entries.
        order (list[ListPipelineOverviewOrderType0Item] | None | Unset): Sort directions, one per
            `sort` key and in the same order. Required whenever `sort` is supplied.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | ListPipelineOverviewResponse200]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        limit=limit,
        offset=offset,
        start=start,
        end=end,
        tz=tz,
        q=q,
        pipeline_name=pipeline_name,
        latest_status=latest_status,
        latest_destination_name=latest_destination_name,
        sort=sort,
        order=order,
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
    start: datetime.datetime,
    end: datetime.datetime,
    tz: str | Unset = "UTC",
    q: None | str | Unset = UNSET,
    pipeline_name: list[str] | None | Unset = UNSET,
    latest_status: list[PipelineRunStatus] | None | Unset = UNSET,
    latest_destination_name: list[str] | None | Unset = UNSET,
    sort: list[ListPipelineOverviewSortType0Item] | None | Unset = UNSET,
    order: list[ListPipelineOverviewOrderType0Item] | None | Unset = UNSET,
) -> ErrorResponse400 | ListPipelineOverviewResponse200 | None:
    """ListPipelineOverview

    One row per pipeline in the time range, with its aggregate metrics.

    Search with `q` over the pipeline name, filter on what a row displays, and sort
    with paired `sort` and `order` lists.

    Args:
        workspace_id (UUID):
        limit (int | Unset): Maximum number of items to return. At most 1000. Default: 100.
        offset (int | Unset): Number of items to skip. At most 10000; a list reports its total up
            to 10001, so narrow with filters instead of paging deeper. Default: 0.
        start (datetime.datetime): Start of period. Naive datetime (no offset), interpreted in
            `tz`. E.g. `2026-03-01T00:00:00`.
        end (datetime.datetime): End of period. Naive datetime (no offset), interpreted in `tz`.
            E.g. `2026-03-11T00:00:00`.
        tz (str | Unset): IANA timezone name (e.g. 'Europe/Berlin', 'America/New_York', 'UTC').
            Used for bucket alignment and interpreting `start`/`end`. Default: 'UTC'.
        q (None | str | Unset): Case-insensitive substring match on `pipeline_name`.
        pipeline_name (list[str] | None | Unset): Exact match on `pipeline_name`. Repeat the
            parameter to match any of several values.
        latest_status (list[PipelineRunStatus] | None | Unset): Exact match on `latest_status`.
            Repeat the parameter to match any of several values.
        latest_destination_name (list[str] | None | Unset): Exact match on
            `latest_destination_name`. Repeat the parameter to match any of several values.
        sort (list[ListPipelineOverviewSortType0Item] | None | Unset): Keys to sort by, applied in
            the order given. Pairs positionally with `order`, which must have the same number of
            entries.
        order (list[ListPipelineOverviewOrderType0Item] | None | Unset): Sort directions, one per
            `sort` key and in the same order. Required whenever `sort` is supplied.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | ListPipelineOverviewResponse200
    """
    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
        limit=limit,
        offset=offset,
        start=start,
        end=end,
        tz=tz,
        q=q,
        pipeline_name=pipeline_name,
        latest_status=latest_status,
        latest_destination_name=latest_destination_name,
        sort=sort,
        order=order,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    start: datetime.datetime,
    end: datetime.datetime,
    tz: str | Unset = "UTC",
    q: None | str | Unset = UNSET,
    pipeline_name: list[str] | None | Unset = UNSET,
    latest_status: list[PipelineRunStatus] | None | Unset = UNSET,
    latest_destination_name: list[str] | None | Unset = UNSET,
    sort: list[ListPipelineOverviewSortType0Item] | None | Unset = UNSET,
    order: list[ListPipelineOverviewOrderType0Item] | None | Unset = UNSET,
) -> Response[ErrorResponse400 | ListPipelineOverviewResponse200]:
    """ListPipelineOverview

    One row per pipeline in the time range, with its aggregate metrics.

    Search with `q` over the pipeline name, filter on what a row displays, and sort
    with paired `sort` and `order` lists.

    Args:
        workspace_id (UUID):
        limit (int | Unset): Maximum number of items to return. At most 1000. Default: 100.
        offset (int | Unset): Number of items to skip. At most 10000; a list reports its total up
            to 10001, so narrow with filters instead of paging deeper. Default: 0.
        start (datetime.datetime): Start of period. Naive datetime (no offset), interpreted in
            `tz`. E.g. `2026-03-01T00:00:00`.
        end (datetime.datetime): End of period. Naive datetime (no offset), interpreted in `tz`.
            E.g. `2026-03-11T00:00:00`.
        tz (str | Unset): IANA timezone name (e.g. 'Europe/Berlin', 'America/New_York', 'UTC').
            Used for bucket alignment and interpreting `start`/`end`. Default: 'UTC'.
        q (None | str | Unset): Case-insensitive substring match on `pipeline_name`.
        pipeline_name (list[str] | None | Unset): Exact match on `pipeline_name`. Repeat the
            parameter to match any of several values.
        latest_status (list[PipelineRunStatus] | None | Unset): Exact match on `latest_status`.
            Repeat the parameter to match any of several values.
        latest_destination_name (list[str] | None | Unset): Exact match on
            `latest_destination_name`. Repeat the parameter to match any of several values.
        sort (list[ListPipelineOverviewSortType0Item] | None | Unset): Keys to sort by, applied in
            the order given. Pairs positionally with `order`, which must have the same number of
            entries.
        order (list[ListPipelineOverviewOrderType0Item] | None | Unset): Sort directions, one per
            `sort` key and in the same order. Required whenever `sort` is supplied.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | ListPipelineOverviewResponse200]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        limit=limit,
        offset=offset,
        start=start,
        end=end,
        tz=tz,
        q=q,
        pipeline_name=pipeline_name,
        latest_status=latest_status,
        latest_destination_name=latest_destination_name,
        sort=sort,
        order=order,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    start: datetime.datetime,
    end: datetime.datetime,
    tz: str | Unset = "UTC",
    q: None | str | Unset = UNSET,
    pipeline_name: list[str] | None | Unset = UNSET,
    latest_status: list[PipelineRunStatus] | None | Unset = UNSET,
    latest_destination_name: list[str] | None | Unset = UNSET,
    sort: list[ListPipelineOverviewSortType0Item] | None | Unset = UNSET,
    order: list[ListPipelineOverviewOrderType0Item] | None | Unset = UNSET,
) -> ErrorResponse400 | ListPipelineOverviewResponse200 | None:
    """ListPipelineOverview

    One row per pipeline in the time range, with its aggregate metrics.

    Search with `q` over the pipeline name, filter on what a row displays, and sort
    with paired `sort` and `order` lists.

    Args:
        workspace_id (UUID):
        limit (int | Unset): Maximum number of items to return. At most 1000. Default: 100.
        offset (int | Unset): Number of items to skip. At most 10000; a list reports its total up
            to 10001, so narrow with filters instead of paging deeper. Default: 0.
        start (datetime.datetime): Start of period. Naive datetime (no offset), interpreted in
            `tz`. E.g. `2026-03-01T00:00:00`.
        end (datetime.datetime): End of period. Naive datetime (no offset), interpreted in `tz`.
            E.g. `2026-03-11T00:00:00`.
        tz (str | Unset): IANA timezone name (e.g. 'Europe/Berlin', 'America/New_York', 'UTC').
            Used for bucket alignment and interpreting `start`/`end`. Default: 'UTC'.
        q (None | str | Unset): Case-insensitive substring match on `pipeline_name`.
        pipeline_name (list[str] | None | Unset): Exact match on `pipeline_name`. Repeat the
            parameter to match any of several values.
        latest_status (list[PipelineRunStatus] | None | Unset): Exact match on `latest_status`.
            Repeat the parameter to match any of several values.
        latest_destination_name (list[str] | None | Unset): Exact match on
            `latest_destination_name`. Repeat the parameter to match any of several values.
        sort (list[ListPipelineOverviewSortType0Item] | None | Unset): Keys to sort by, applied in
            the order given. Pairs positionally with `order`, which must have the same number of
            entries.
        order (list[ListPipelineOverviewOrderType0Item] | None | Unset): Sort directions, one per
            `sort` key and in the same order. Required whenever `sort` is supplied.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | ListPipelineOverviewResponse200
    """
    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            limit=limit,
            offset=offset,
            start=start,
            end=end,
            tz=tz,
            q=q,
            pipeline_name=pipeline_name,
            latest_status=latest_status,
            latest_destination_name=latest_destination_name,
            sort=sort,
            order=order,
        )
    ).parsed
