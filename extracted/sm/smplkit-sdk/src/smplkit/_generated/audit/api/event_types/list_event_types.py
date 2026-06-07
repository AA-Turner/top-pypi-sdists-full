from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.event_type_list_response import EventTypeListResponse
from ...models.list_event_types_sort import ListEventTypesSort
from ...types import Unset


def _get_kwargs(
    *,
    filterresource_type: None | str | Unset = UNSET,
    sort: ListEventTypesSort | Unset = "key",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_filterresource_type: None | str | Unset
    if isinstance(filterresource_type, Unset):
        json_filterresource_type = UNSET
    else:
        json_filterresource_type = filterresource_type
    params["filter[resource_type]"] = json_filterresource_type

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
        "url": "/api/v1/event_types",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> EventTypeListResponse | None:
    if response.status_code == 200:
        response_200 = EventTypeListResponse.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[EventTypeListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    filterresource_type: None | str | Unset = UNSET,
    sort: ListEventTypesSort | Unset = "key",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> Response[EventTypeListResponse]:
    """List Event Types

     List the distinct `event_type` slugs recorded for this account.

    Default sort is `key` ascending; pass `sort=-key` for descending.
    Scoped to the resolved environment. Without `filter[resource_type]`,
    returns one row per distinct event_type. With `filter[resource_type]`,
    returns the event_types recorded for that specific resource type.

    Args:
        filterresource_type (None | str | Unset):
        sort (ListEventTypesSort | Unset): Field to sort by. Prefix with `-` for descending order.
            Default: `key`. Allowed values: `key`, `-key`. Default: 'key'.
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
        Response[EventTypeListResponse]
    """

    kwargs = _get_kwargs(
        filterresource_type=filterresource_type,
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
    filterresource_type: None | str | Unset = UNSET,
    sort: ListEventTypesSort | Unset = "key",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> EventTypeListResponse | None:
    """List Event Types

     List the distinct `event_type` slugs recorded for this account.

    Default sort is `key` ascending; pass `sort=-key` for descending.
    Scoped to the resolved environment. Without `filter[resource_type]`,
    returns one row per distinct event_type. With `filter[resource_type]`,
    returns the event_types recorded for that specific resource type.

    Args:
        filterresource_type (None | str | Unset):
        sort (ListEventTypesSort | Unset): Field to sort by. Prefix with `-` for descending order.
            Default: `key`. Allowed values: `key`, `-key`. Default: 'key'.
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
        EventTypeListResponse
    """

    return sync_detailed(
        client=client,
        filterresource_type=filterresource_type,
        sort=sort,
        pagenumber=pagenumber,
        pagesize=pagesize,
        metatotal=metatotal,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    filterresource_type: None | str | Unset = UNSET,
    sort: ListEventTypesSort | Unset = "key",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> Response[EventTypeListResponse]:
    """List Event Types

     List the distinct `event_type` slugs recorded for this account.

    Default sort is `key` ascending; pass `sort=-key` for descending.
    Scoped to the resolved environment. Without `filter[resource_type]`,
    returns one row per distinct event_type. With `filter[resource_type]`,
    returns the event_types recorded for that specific resource type.

    Args:
        filterresource_type (None | str | Unset):
        sort (ListEventTypesSort | Unset): Field to sort by. Prefix with `-` for descending order.
            Default: `key`. Allowed values: `key`, `-key`. Default: 'key'.
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
        Response[EventTypeListResponse]
    """

    kwargs = _get_kwargs(
        filterresource_type=filterresource_type,
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
    filterresource_type: None | str | Unset = UNSET,
    sort: ListEventTypesSort | Unset = "key",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> EventTypeListResponse | None:
    """List Event Types

     List the distinct `event_type` slugs recorded for this account.

    Default sort is `key` ascending; pass `sort=-key` for descending.
    Scoped to the resolved environment. Without `filter[resource_type]`,
    returns one row per distinct event_type. With `filter[resource_type]`,
    returns the event_types recorded for that specific resource type.

    Args:
        filterresource_type (None | str | Unset):
        sort (ListEventTypesSort | Unset): Field to sort by. Prefix with `-` for descending order.
            Default: `key`. Allowed values: `key`, `-key`. Default: 'key'.
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
        EventTypeListResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            filterresource_type=filterresource_type,
            sort=sort,
            pagenumber=pagenumber,
            pagesize=pagesize,
            metatotal=metatotal,
        )
    ).parsed
