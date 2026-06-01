from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.flag_source_list_response import FlagSourceListResponse
from ...models.list_all_flag_sources_sort import ListAllFlagSourcesSort
from ...types import Unset


def _get_kwargs(
    *,
    filterenvironment: None | str | Unset = UNSET,
    filterservice: None | str | Unset = UNSET,
    sort: ListAllFlagSourcesSort | Unset = "-last_seen",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_filterenvironment: None | str | Unset
    if isinstance(filterenvironment, Unset):
        json_filterenvironment = UNSET
    else:
        json_filterenvironment = filterenvironment
    params["filter[environment]"] = json_filterenvironment

    json_filterservice: None | str | Unset
    if isinstance(filterservice, Unset):
        json_filterservice = UNSET
    else:
        json_filterservice = filterservice
    params["filter[service]"] = json_filterservice

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
        "url": "/api/v1/flag_sources",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> FlagSourceListResponse | None:
    if response.status_code == 200:
        response_200 = FlagSourceListResponse.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[FlagSourceListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    filterenvironment: None | str | Unset = UNSET,
    filterservice: None | str | Unset = UNSET,
    sort: ListAllFlagSourcesSort | Unset = "-last_seen",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> Response[FlagSourceListResponse]:
    """List All Flag Sources

     List service/environment observations across all flags for this account.

    Default sort is `-last_seen` (most recently seen first). Filter by
    `environment` or `service` (or both) to narrow the result.

    Args:
        filterenvironment (None | str | Unset):
        filterservice (None | str | Unset):
        sort (ListAllFlagSourcesSort | Unset): Field to sort by. Prefix with `-` for descending
            order. Default: `-last_seen`. Allowed values: `created_at`, `-created_at`, `environment`,
            `-environment`, `last_seen`, `-last_seen`, `service`, `-service`. Default: '-last_seen'.
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
        Response[FlagSourceListResponse]
    """

    kwargs = _get_kwargs(
        filterenvironment=filterenvironment,
        filterservice=filterservice,
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
    filterenvironment: None | str | Unset = UNSET,
    filterservice: None | str | Unset = UNSET,
    sort: ListAllFlagSourcesSort | Unset = "-last_seen",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> FlagSourceListResponse | None:
    """List All Flag Sources

     List service/environment observations across all flags for this account.

    Default sort is `-last_seen` (most recently seen first). Filter by
    `environment` or `service` (or both) to narrow the result.

    Args:
        filterenvironment (None | str | Unset):
        filterservice (None | str | Unset):
        sort (ListAllFlagSourcesSort | Unset): Field to sort by. Prefix with `-` for descending
            order. Default: `-last_seen`. Allowed values: `created_at`, `-created_at`, `environment`,
            `-environment`, `last_seen`, `-last_seen`, `service`, `-service`. Default: '-last_seen'.
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
        FlagSourceListResponse
    """

    return sync_detailed(
        client=client,
        filterenvironment=filterenvironment,
        filterservice=filterservice,
        sort=sort,
        pagenumber=pagenumber,
        pagesize=pagesize,
        metatotal=metatotal,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    filterenvironment: None | str | Unset = UNSET,
    filterservice: None | str | Unset = UNSET,
    sort: ListAllFlagSourcesSort | Unset = "-last_seen",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> Response[FlagSourceListResponse]:
    """List All Flag Sources

     List service/environment observations across all flags for this account.

    Default sort is `-last_seen` (most recently seen first). Filter by
    `environment` or `service` (or both) to narrow the result.

    Args:
        filterenvironment (None | str | Unset):
        filterservice (None | str | Unset):
        sort (ListAllFlagSourcesSort | Unset): Field to sort by. Prefix with `-` for descending
            order. Default: `-last_seen`. Allowed values: `created_at`, `-created_at`, `environment`,
            `-environment`, `last_seen`, `-last_seen`, `service`, `-service`. Default: '-last_seen'.
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
        Response[FlagSourceListResponse]
    """

    kwargs = _get_kwargs(
        filterenvironment=filterenvironment,
        filterservice=filterservice,
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
    filterenvironment: None | str | Unset = UNSET,
    filterservice: None | str | Unset = UNSET,
    sort: ListAllFlagSourcesSort | Unset = "-last_seen",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> FlagSourceListResponse | None:
    """List All Flag Sources

     List service/environment observations across all flags for this account.

    Default sort is `-last_seen` (most recently seen first). Filter by
    `environment` or `service` (or both) to narrow the result.

    Args:
        filterenvironment (None | str | Unset):
        filterservice (None | str | Unset):
        sort (ListAllFlagSourcesSort | Unset): Field to sort by. Prefix with `-` for descending
            order. Default: `-last_seen`. Allowed values: `created_at`, `-created_at`, `environment`,
            `-environment`, `last_seen`, `-last_seen`, `service`, `-service`. Default: '-last_seen'.
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
        FlagSourceListResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            filterenvironment=filterenvironment,
            filterservice=filterservice,
            sort=sort,
            pagenumber=pagenumber,
            pagesize=pagesize,
            metatotal=metatotal,
        )
    ).parsed
