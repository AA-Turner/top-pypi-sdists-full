from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.context_list_response import ContextListResponse
from ...models.error_response import ErrorResponse
from ...models.list_contexts_sort import ListContextsSort
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    filtercontext_type: None | str | Unset = UNSET,
    filtersearch: None | str | Unset = UNSET,
    sort: ListContextsSort | Unset = "key",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_filtercontext_type: str | Unset | None
    if isinstance(filtercontext_type, Unset):
        json_filtercontext_type = UNSET
    else:
        json_filtercontext_type = filtercontext_type
    params["filter[context_type]"] = json_filtercontext_type

    json_filtersearch: str | Unset | None
    if isinstance(filtersearch, Unset):
        json_filtersearch = UNSET
    else:
        json_filtersearch = filtersearch
    params["filter[search]"] = json_filtersearch

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
        "url": "/api/v1/contexts",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ContextListResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = ContextListResponse.from_dict(response.json())

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
) -> Response[ContextListResponse | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    filtercontext_type: None | str | Unset = UNSET,
    filtersearch: None | str | Unset = UNSET,
    sort: ListContextsSort | Unset = "key",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> Response[ContextListResponse | ErrorResponse]:
    """List Contexts

     List context instances for the authenticated account. `filter[context_type]` narrows the result to
    one context type. `filter[search]` does a case-insensitive substring match against the context
    `key`, `name`, and every attribute value, returning any context where at least one of those fields
    contains the search term.

    Args:
        filtercontext_type (None | str | Unset): Limit results to context instances of this
            context type (e.g. `user`).
        filtersearch (None | str | Unset): Case-insensitive substring match against the `key`,
            `name`, and any attribute value. A context is returned if at least one of those fields
            contains the search term.
        sort (ListContextsSort | Unset): Field to sort by. Prefix with `-` for descending order.
            Default: `key`. Allowed values: `created_at`, `-created_at`, `key`, `-key`, `name`,
            `-name`, `updated_at`, `-updated_at`. Default: 'key'.
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
        Response[ContextListResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        filtercontext_type=filtercontext_type,
        filtersearch=filtersearch,
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
    filtercontext_type: None | str | Unset = UNSET,
    filtersearch: None | str | Unset = UNSET,
    sort: ListContextsSort | Unset = "key",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> ContextListResponse | ErrorResponse | None:
    """List Contexts

     List context instances for the authenticated account. `filter[context_type]` narrows the result to
    one context type. `filter[search]` does a case-insensitive substring match against the context
    `key`, `name`, and every attribute value, returning any context where at least one of those fields
    contains the search term.

    Args:
        filtercontext_type (None | str | Unset): Limit results to context instances of this
            context type (e.g. `user`).
        filtersearch (None | str | Unset): Case-insensitive substring match against the `key`,
            `name`, and any attribute value. A context is returned if at least one of those fields
            contains the search term.
        sort (ListContextsSort | Unset): Field to sort by. Prefix with `-` for descending order.
            Default: `key`. Allowed values: `created_at`, `-created_at`, `key`, `-key`, `name`,
            `-name`, `updated_at`, `-updated_at`. Default: 'key'.
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
        ContextListResponse | ErrorResponse
    """

    return sync_detailed(
        client=client,
        filtercontext_type=filtercontext_type,
        filtersearch=filtersearch,
        sort=sort,
        pagenumber=pagenumber,
        pagesize=pagesize,
        metatotal=metatotal,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    filtercontext_type: None | str | Unset = UNSET,
    filtersearch: None | str | Unset = UNSET,
    sort: ListContextsSort | Unset = "key",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> Response[ContextListResponse | ErrorResponse]:
    """List Contexts

     List context instances for the authenticated account. `filter[context_type]` narrows the result to
    one context type. `filter[search]` does a case-insensitive substring match against the context
    `key`, `name`, and every attribute value, returning any context where at least one of those fields
    contains the search term.

    Args:
        filtercontext_type (None | str | Unset): Limit results to context instances of this
            context type (e.g. `user`).
        filtersearch (None | str | Unset): Case-insensitive substring match against the `key`,
            `name`, and any attribute value. A context is returned if at least one of those fields
            contains the search term.
        sort (ListContextsSort | Unset): Field to sort by. Prefix with `-` for descending order.
            Default: `key`. Allowed values: `created_at`, `-created_at`, `key`, `-key`, `name`,
            `-name`, `updated_at`, `-updated_at`. Default: 'key'.
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
        Response[ContextListResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        filtercontext_type=filtercontext_type,
        filtersearch=filtersearch,
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
    filtercontext_type: None | str | Unset = UNSET,
    filtersearch: None | str | Unset = UNSET,
    sort: ListContextsSort | Unset = "key",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> ContextListResponse | ErrorResponse | None:
    """List Contexts

     List context instances for the authenticated account. `filter[context_type]` narrows the result to
    one context type. `filter[search]` does a case-insensitive substring match against the context
    `key`, `name`, and every attribute value, returning any context where at least one of those fields
    contains the search term.

    Args:
        filtercontext_type (None | str | Unset): Limit results to context instances of this
            context type (e.g. `user`).
        filtersearch (None | str | Unset): Case-insensitive substring match against the `key`,
            `name`, and any attribute value. A context is returned if at least one of those fields
            contains the search term.
        sort (ListContextsSort | Unset): Field to sort by. Prefix with `-` for descending order.
            Default: `key`. Allowed values: `created_at`, `-created_at`, `key`, `-key`, `name`,
            `-name`, `updated_at`, `-updated_at`. Default: 'key'.
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
        ContextListResponse | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            filtercontext_type=filtercontext_type,
            filtersearch=filtersearch,
            sort=sort,
            pagenumber=pagenumber,
            pagesize=pagesize,
            metatotal=metatotal,
        )
    ).parsed
