from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.flag_list_response import FlagListResponse
from ...models.list_flags_sort import ListFlagsSort
from ...types import Unset


def _get_kwargs(
    *,
    filtertype: None | str | Unset = UNSET,
    filtermanaged: bool | None | Unset = UNSET,
    filterreferences_context: None | str | Unset = UNSET,
    filterreferences_context_type: None | str | Unset = UNSET,
    filtersearch: None | str | Unset = UNSET,
    sort: ListFlagsSort | Unset = "key",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_filtertype: None | str | Unset
    if isinstance(filtertype, Unset):
        json_filtertype = UNSET
    else:
        json_filtertype = filtertype
    params["filter[type]"] = json_filtertype

    json_filtermanaged: bool | None | Unset
    if isinstance(filtermanaged, Unset):
        json_filtermanaged = UNSET
    else:
        json_filtermanaged = filtermanaged
    params["filter[managed]"] = json_filtermanaged

    json_filterreferences_context: None | str | Unset
    if isinstance(filterreferences_context, Unset):
        json_filterreferences_context = UNSET
    else:
        json_filterreferences_context = filterreferences_context
    params["filter[references_context]"] = json_filterreferences_context

    json_filterreferences_context_type: None | str | Unset
    if isinstance(filterreferences_context_type, Unset):
        json_filterreferences_context_type = UNSET
    else:
        json_filterreferences_context_type = filterreferences_context_type
    params["filter[references_context_type]"] = json_filterreferences_context_type

    json_filtersearch: None | str | Unset
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
        "url": "/api/v1/flags",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> FlagListResponse | None:
    if response.status_code == 200:
        response_200 = FlagListResponse.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[FlagListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    filtertype: None | str | Unset = UNSET,
    filtermanaged: bool | None | Unset = UNSET,
    filterreferences_context: None | str | Unset = UNSET,
    filterreferences_context_type: None | str | Unset = UNSET,
    filtersearch: None | str | Unset = UNSET,
    sort: ListFlagsSort | Unset = "key",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> Response[FlagListResponse]:
    """List Flags

     List feature flags for this account.

    Default sort is `key` ascending. ``filter[references_context]`` and
    ``filter[references_context_type]`` walk the rules JSON in Python after
    the SQL fetch, so pagination for those calls is applied in memory after
    the filter; for the common case (no rules-traversal filter) pagination
    is applied at the SQL level.

    Args:
        filtertype (None | str | Unset):
        filtermanaged (bool | None | Unset):
        filterreferences_context (None | str | Unset): Return flags whose rules reference this
            context instance. Format: {type}:{key}
        filterreferences_context_type (None | str | Unset): Return flags whose rules reference any
            attribute of the given context type.
        filtersearch (None | str | Unset): Case-insensitive substring match against the flag `key`
            and `name`. A flag is returned if either field contains the search term.
        sort (ListFlagsSort | Unset): Field to sort by. Prefix with `-` for descending order.
            Default: `key`. Allowed values: `created_at`, `-created_at`, `key`, `-key`, `name`,
            `-name`, `type`, `-type`, `updated_at`, `-updated_at`. Default: 'key'.
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
        Response[FlagListResponse]
    """

    kwargs = _get_kwargs(
        filtertype=filtertype,
        filtermanaged=filtermanaged,
        filterreferences_context=filterreferences_context,
        filterreferences_context_type=filterreferences_context_type,
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
    filtertype: None | str | Unset = UNSET,
    filtermanaged: bool | None | Unset = UNSET,
    filterreferences_context: None | str | Unset = UNSET,
    filterreferences_context_type: None | str | Unset = UNSET,
    filtersearch: None | str | Unset = UNSET,
    sort: ListFlagsSort | Unset = "key",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> FlagListResponse | None:
    """List Flags

     List feature flags for this account.

    Default sort is `key` ascending. ``filter[references_context]`` and
    ``filter[references_context_type]`` walk the rules JSON in Python after
    the SQL fetch, so pagination for those calls is applied in memory after
    the filter; for the common case (no rules-traversal filter) pagination
    is applied at the SQL level.

    Args:
        filtertype (None | str | Unset):
        filtermanaged (bool | None | Unset):
        filterreferences_context (None | str | Unset): Return flags whose rules reference this
            context instance. Format: {type}:{key}
        filterreferences_context_type (None | str | Unset): Return flags whose rules reference any
            attribute of the given context type.
        filtersearch (None | str | Unset): Case-insensitive substring match against the flag `key`
            and `name`. A flag is returned if either field contains the search term.
        sort (ListFlagsSort | Unset): Field to sort by. Prefix with `-` for descending order.
            Default: `key`. Allowed values: `created_at`, `-created_at`, `key`, `-key`, `name`,
            `-name`, `type`, `-type`, `updated_at`, `-updated_at`. Default: 'key'.
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
        FlagListResponse
    """

    return sync_detailed(
        client=client,
        filtertype=filtertype,
        filtermanaged=filtermanaged,
        filterreferences_context=filterreferences_context,
        filterreferences_context_type=filterreferences_context_type,
        filtersearch=filtersearch,
        sort=sort,
        pagenumber=pagenumber,
        pagesize=pagesize,
        metatotal=metatotal,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    filtertype: None | str | Unset = UNSET,
    filtermanaged: bool | None | Unset = UNSET,
    filterreferences_context: None | str | Unset = UNSET,
    filterreferences_context_type: None | str | Unset = UNSET,
    filtersearch: None | str | Unset = UNSET,
    sort: ListFlagsSort | Unset = "key",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> Response[FlagListResponse]:
    """List Flags

     List feature flags for this account.

    Default sort is `key` ascending. ``filter[references_context]`` and
    ``filter[references_context_type]`` walk the rules JSON in Python after
    the SQL fetch, so pagination for those calls is applied in memory after
    the filter; for the common case (no rules-traversal filter) pagination
    is applied at the SQL level.

    Args:
        filtertype (None | str | Unset):
        filtermanaged (bool | None | Unset):
        filterreferences_context (None | str | Unset): Return flags whose rules reference this
            context instance. Format: {type}:{key}
        filterreferences_context_type (None | str | Unset): Return flags whose rules reference any
            attribute of the given context type.
        filtersearch (None | str | Unset): Case-insensitive substring match against the flag `key`
            and `name`. A flag is returned if either field contains the search term.
        sort (ListFlagsSort | Unset): Field to sort by. Prefix with `-` for descending order.
            Default: `key`. Allowed values: `created_at`, `-created_at`, `key`, `-key`, `name`,
            `-name`, `type`, `-type`, `updated_at`, `-updated_at`. Default: 'key'.
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
        Response[FlagListResponse]
    """

    kwargs = _get_kwargs(
        filtertype=filtertype,
        filtermanaged=filtermanaged,
        filterreferences_context=filterreferences_context,
        filterreferences_context_type=filterreferences_context_type,
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
    filtertype: None | str | Unset = UNSET,
    filtermanaged: bool | None | Unset = UNSET,
    filterreferences_context: None | str | Unset = UNSET,
    filterreferences_context_type: None | str | Unset = UNSET,
    filtersearch: None | str | Unset = UNSET,
    sort: ListFlagsSort | Unset = "key",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> FlagListResponse | None:
    """List Flags

     List feature flags for this account.

    Default sort is `key` ascending. ``filter[references_context]`` and
    ``filter[references_context_type]`` walk the rules JSON in Python after
    the SQL fetch, so pagination for those calls is applied in memory after
    the filter; for the common case (no rules-traversal filter) pagination
    is applied at the SQL level.

    Args:
        filtertype (None | str | Unset):
        filtermanaged (bool | None | Unset):
        filterreferences_context (None | str | Unset): Return flags whose rules reference this
            context instance. Format: {type}:{key}
        filterreferences_context_type (None | str | Unset): Return flags whose rules reference any
            attribute of the given context type.
        filtersearch (None | str | Unset): Case-insensitive substring match against the flag `key`
            and `name`. A flag is returned if either field contains the search term.
        sort (ListFlagsSort | Unset): Field to sort by. Prefix with `-` for descending order.
            Default: `key`. Allowed values: `created_at`, `-created_at`, `key`, `-key`, `name`,
            `-name`, `type`, `-type`, `updated_at`, `-updated_at`. Default: 'key'.
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
        FlagListResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            filtertype=filtertype,
            filtermanaged=filtermanaged,
            filterreferences_context=filterreferences_context,
            filterreferences_context_type=filterreferences_context_type,
            filtersearch=filtersearch,
            sort=sort,
            pagenumber=pagenumber,
            pagesize=pagesize,
            metatotal=metatotal,
        )
    ).parsed
