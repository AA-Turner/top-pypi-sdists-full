from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.job_list_response import JobListResponse
from ...models.list_jobs_sort import ListJobsSort
from ...types import Unset


def _get_kwargs(
    *,
    filterenabled: bool | None | Unset = UNSET,
    filterrecurring: bool | None | Unset = UNSET,
    filtername: None | str | Unset = UNSET,
    sort: ListJobsSort | Unset = "name",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_filterenabled: bool | None | Unset
    if isinstance(filterenabled, Unset):
        json_filterenabled = UNSET
    else:
        json_filterenabled = filterenabled
    params["filter[enabled]"] = json_filterenabled

    json_filterrecurring: bool | None | Unset
    if isinstance(filterrecurring, Unset):
        json_filterrecurring = UNSET
    else:
        json_filterrecurring = filterrecurring
    params["filter[recurring]"] = json_filterrecurring

    json_filtername: None | str | Unset
    if isinstance(filtername, Unset):
        json_filtername = UNSET
    else:
        json_filtername = filtername
    params["filter[name]"] = json_filtername

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
        "url": "/api/v1/jobs",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> JobListResponse | None:
    if response.status_code == 200:
        response_200 = JobListResponse.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[JobListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    filterenabled: bool | None | Unset = UNSET,
    filterrecurring: bool | None | Unset = UNSET,
    filtername: None | str | Unset = UNSET,
    sort: ListJobsSort | Unset = "name",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> Response[JobListResponse]:
    """List Jobs

     List this account's jobs.

    Default sort is `name` ascending. Sort by `name`, `created_at`,
    `updated_at`, `next_run_at`, or `enabled`, ascending or descending (prefix
    `-` for descending). Filter with `filter[enabled]`, `filter[recurring]`,
    and `filter[name]` (case-insensitive substring match on the name); filters
    compose with AND.

    Args:
        filterenabled (bool | None | Unset):
        filterrecurring (bool | None | Unset):
        filtername (None | str | Unset): Case-insensitive substring match on the job `name`
            (matches when the name contains the given text).
        sort (ListJobsSort | Unset): Field to sort by. Prefix with `-` for descending order.
            Default: `name`. Allowed values: `created_at`, `-created_at`, `enabled`, `-enabled`,
            `name`, `-name`, `next_run_at`, `-next_run_at`, `updated_at`, `-updated_at`. Default:
            'name'.
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
        Response[JobListResponse]
    """

    kwargs = _get_kwargs(
        filterenabled=filterenabled,
        filterrecurring=filterrecurring,
        filtername=filtername,
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
    filterenabled: bool | None | Unset = UNSET,
    filterrecurring: bool | None | Unset = UNSET,
    filtername: None | str | Unset = UNSET,
    sort: ListJobsSort | Unset = "name",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> JobListResponse | None:
    """List Jobs

     List this account's jobs.

    Default sort is `name` ascending. Sort by `name`, `created_at`,
    `updated_at`, `next_run_at`, or `enabled`, ascending or descending (prefix
    `-` for descending). Filter with `filter[enabled]`, `filter[recurring]`,
    and `filter[name]` (case-insensitive substring match on the name); filters
    compose with AND.

    Args:
        filterenabled (bool | None | Unset):
        filterrecurring (bool | None | Unset):
        filtername (None | str | Unset): Case-insensitive substring match on the job `name`
            (matches when the name contains the given text).
        sort (ListJobsSort | Unset): Field to sort by. Prefix with `-` for descending order.
            Default: `name`. Allowed values: `created_at`, `-created_at`, `enabled`, `-enabled`,
            `name`, `-name`, `next_run_at`, `-next_run_at`, `updated_at`, `-updated_at`. Default:
            'name'.
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
        JobListResponse
    """

    return sync_detailed(
        client=client,
        filterenabled=filterenabled,
        filterrecurring=filterrecurring,
        filtername=filtername,
        sort=sort,
        pagenumber=pagenumber,
        pagesize=pagesize,
        metatotal=metatotal,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    filterenabled: bool | None | Unset = UNSET,
    filterrecurring: bool | None | Unset = UNSET,
    filtername: None | str | Unset = UNSET,
    sort: ListJobsSort | Unset = "name",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> Response[JobListResponse]:
    """List Jobs

     List this account's jobs.

    Default sort is `name` ascending. Sort by `name`, `created_at`,
    `updated_at`, `next_run_at`, or `enabled`, ascending or descending (prefix
    `-` for descending). Filter with `filter[enabled]`, `filter[recurring]`,
    and `filter[name]` (case-insensitive substring match on the name); filters
    compose with AND.

    Args:
        filterenabled (bool | None | Unset):
        filterrecurring (bool | None | Unset):
        filtername (None | str | Unset): Case-insensitive substring match on the job `name`
            (matches when the name contains the given text).
        sort (ListJobsSort | Unset): Field to sort by. Prefix with `-` for descending order.
            Default: `name`. Allowed values: `created_at`, `-created_at`, `enabled`, `-enabled`,
            `name`, `-name`, `next_run_at`, `-next_run_at`, `updated_at`, `-updated_at`. Default:
            'name'.
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
        Response[JobListResponse]
    """

    kwargs = _get_kwargs(
        filterenabled=filterenabled,
        filterrecurring=filterrecurring,
        filtername=filtername,
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
    filterenabled: bool | None | Unset = UNSET,
    filterrecurring: bool | None | Unset = UNSET,
    filtername: None | str | Unset = UNSET,
    sort: ListJobsSort | Unset = "name",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> JobListResponse | None:
    """List Jobs

     List this account's jobs.

    Default sort is `name` ascending. Sort by `name`, `created_at`,
    `updated_at`, `next_run_at`, or `enabled`, ascending or descending (prefix
    `-` for descending). Filter with `filter[enabled]`, `filter[recurring]`,
    and `filter[name]` (case-insensitive substring match on the name); filters
    compose with AND.

    Args:
        filterenabled (bool | None | Unset):
        filterrecurring (bool | None | Unset):
        filtername (None | str | Unset): Case-insensitive substring match on the job `name`
            (matches when the name contains the given text).
        sort (ListJobsSort | Unset): Field to sort by. Prefix with `-` for descending order.
            Default: `name`. Allowed values: `created_at`, `-created_at`, `enabled`, `-enabled`,
            `name`, `-name`, `next_run_at`, `-next_run_at`, `updated_at`, `-updated_at`. Default:
            'name'.
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
        JobListResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            filterenabled=filterenabled,
            filterrecurring=filterrecurring,
            filtername=filtername,
            sort=sort,
            pagenumber=pagenumber,
            pagesize=pagesize,
            metatotal=metatotal,
        )
    ).parsed
