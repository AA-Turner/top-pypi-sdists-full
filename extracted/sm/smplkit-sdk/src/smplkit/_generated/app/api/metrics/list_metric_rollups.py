from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_response import ErrorResponse
from ...models.list_metric_rollups_sort import ListMetricRollupsSort
from ...models.metric_rollup_list_response import MetricRollupListResponse
from ...types import Unset


def _get_kwargs(
    *,
    filtername: str,
    filterrollup: str,
    filterrecorded_at: None | str | Unset = UNSET,
    sort: ListMetricRollupsSort | Unset = "bucket",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["filter[name]"] = filtername

    params["filter[rollup]"] = filterrollup

    json_filterrecorded_at: None | str | Unset
    if isinstance(filterrecorded_at, Unset):
        json_filterrecorded_at = UNSET
    else:
        json_filterrecorded_at = filterrecorded_at
    params["filter[recorded_at]"] = json_filterrecorded_at

    json_sort: str | Unset = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort

    params["sort"] = json_sort

    params["page[number]"] = pagenumber

    params["page[size]"] = pagesize

    params["meta[total]"] = metatotal

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/metric_rollups",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | MetricRollupListResponse | None:
    if response.status_code == 200:
        response_200 = MetricRollupListResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = ErrorResponse.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | MetricRollupListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    filtername: str,
    filterrollup: str,
    filterrecorded_at: None | str | Unset = UNSET,
    sort: ListMetricRollupsSort | Unset = "bucket",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> Response[ErrorResponse | MetricRollupListResponse]:
    """List Metric Rollups

     Query aggregated metric rollups. Requires filter[rollup] for the aggregation interval.

    Args:
        filtername (str):
        filterrollup (str):
        filterrecorded_at (None | str | Unset):
        sort (ListMetricRollupsSort | Unset): Field to sort by. Prefix with `-` for descending
            order. Default: `bucket`. Allowed values: `bucket`, `-bucket`. Default: 'bucket'.
        pagenumber (int | Unset): 1-based page number to return. Optional; defaults to `1` when
            omitted. Must be `>= 1` — requests with a smaller value are rejected with a 400 error.
            Default: 1.
        pagesize (int | Unset): Number of items per page. Optional; defaults to `1000` when
            omitted. Must be between `1` and `1000` inclusive — requests outside that range are
            rejected with a 400 error. Default: 1000.
        metatotal (bool | Unset): When `true`, the response's `meta.pagination` block includes
            `total` (the total number of matching items across all pages) and `total_pages`. Computing
            these requires an extra `COUNT` query, so omit (or pass `false`) when the totals are not
            needed. Defaults to `false`. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | MetricRollupListResponse]
    """

    kwargs = _get_kwargs(
        filtername=filtername,
        filterrollup=filterrollup,
        filterrecorded_at=filterrecorded_at,
        sort=sort,
        pagenumber=pagenumber,
        pagesize=pagesize,
        metatotal=metatotal,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    filtername: str,
    filterrollup: str,
    filterrecorded_at: None | str | Unset = UNSET,
    sort: ListMetricRollupsSort | Unset = "bucket",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> ErrorResponse | MetricRollupListResponse | None:
    """List Metric Rollups

     Query aggregated metric rollups. Requires filter[rollup] for the aggregation interval.

    Args:
        filtername (str):
        filterrollup (str):
        filterrecorded_at (None | str | Unset):
        sort (ListMetricRollupsSort | Unset): Field to sort by. Prefix with `-` for descending
            order. Default: `bucket`. Allowed values: `bucket`, `-bucket`. Default: 'bucket'.
        pagenumber (int | Unset): 1-based page number to return. Optional; defaults to `1` when
            omitted. Must be `>= 1` — requests with a smaller value are rejected with a 400 error.
            Default: 1.
        pagesize (int | Unset): Number of items per page. Optional; defaults to `1000` when
            omitted. Must be between `1` and `1000` inclusive — requests outside that range are
            rejected with a 400 error. Default: 1000.
        metatotal (bool | Unset): When `true`, the response's `meta.pagination` block includes
            `total` (the total number of matching items across all pages) and `total_pages`. Computing
            these requires an extra `COUNT` query, so omit (or pass `false`) when the totals are not
            needed. Defaults to `false`. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | MetricRollupListResponse
    """

    return sync_detailed(
        client=client,
        filtername=filtername,
        filterrollup=filterrollup,
        filterrecorded_at=filterrecorded_at,
        sort=sort,
        pagenumber=pagenumber,
        pagesize=pagesize,
        metatotal=metatotal,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    filtername: str,
    filterrollup: str,
    filterrecorded_at: None | str | Unset = UNSET,
    sort: ListMetricRollupsSort | Unset = "bucket",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> Response[ErrorResponse | MetricRollupListResponse]:
    """List Metric Rollups

     Query aggregated metric rollups. Requires filter[rollup] for the aggregation interval.

    Args:
        filtername (str):
        filterrollup (str):
        filterrecorded_at (None | str | Unset):
        sort (ListMetricRollupsSort | Unset): Field to sort by. Prefix with `-` for descending
            order. Default: `bucket`. Allowed values: `bucket`, `-bucket`. Default: 'bucket'.
        pagenumber (int | Unset): 1-based page number to return. Optional; defaults to `1` when
            omitted. Must be `>= 1` — requests with a smaller value are rejected with a 400 error.
            Default: 1.
        pagesize (int | Unset): Number of items per page. Optional; defaults to `1000` when
            omitted. Must be between `1` and `1000` inclusive — requests outside that range are
            rejected with a 400 error. Default: 1000.
        metatotal (bool | Unset): When `true`, the response's `meta.pagination` block includes
            `total` (the total number of matching items across all pages) and `total_pages`. Computing
            these requires an extra `COUNT` query, so omit (or pass `false`) when the totals are not
            needed. Defaults to `false`. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | MetricRollupListResponse]
    """

    kwargs = _get_kwargs(
        filtername=filtername,
        filterrollup=filterrollup,
        filterrecorded_at=filterrecorded_at,
        sort=sort,
        pagenumber=pagenumber,
        pagesize=pagesize,
        metatotal=metatotal,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    filtername: str,
    filterrollup: str,
    filterrecorded_at: None | str | Unset = UNSET,
    sort: ListMetricRollupsSort | Unset = "bucket",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> ErrorResponse | MetricRollupListResponse | None:
    """List Metric Rollups

     Query aggregated metric rollups. Requires filter[rollup] for the aggregation interval.

    Args:
        filtername (str):
        filterrollup (str):
        filterrecorded_at (None | str | Unset):
        sort (ListMetricRollupsSort | Unset): Field to sort by. Prefix with `-` for descending
            order. Default: `bucket`. Allowed values: `bucket`, `-bucket`. Default: 'bucket'.
        pagenumber (int | Unset): 1-based page number to return. Optional; defaults to `1` when
            omitted. Must be `>= 1` — requests with a smaller value are rejected with a 400 error.
            Default: 1.
        pagesize (int | Unset): Number of items per page. Optional; defaults to `1000` when
            omitted. Must be between `1` and `1000` inclusive — requests outside that range are
            rejected with a 400 error. Default: 1000.
        metatotal (bool | Unset): When `true`, the response's `meta.pagination` block includes
            `total` (the total number of matching items across all pages) and `total_pages`. Computing
            these requires an extra `COUNT` query, so omit (or pass `false`) when the totals are not
            needed. Defaults to `false`. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | MetricRollupListResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            filtername=filtername,
            filterrollup=filterrollup,
            filterrecorded_at=filterrecorded_at,
            sort=sort,
            pagenumber=pagenumber,
            pagesize=pagesize,
            metatotal=metatotal,
        )
    ).parsed
