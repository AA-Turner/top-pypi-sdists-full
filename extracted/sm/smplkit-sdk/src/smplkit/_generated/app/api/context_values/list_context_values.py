from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.context_value_list_response import ContextValueListResponse
from ...models.error_response import ErrorResponse
from ...types import Unset


def _get_kwargs(
    *,
    filtercontext_type: None | str | Unset = UNSET,
    filterattribute: None | str | Unset = UNSET,
    filtersearch: None | str | Unset = UNSET,
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_filtercontext_type: None | str | Unset
    if isinstance(filtercontext_type, Unset):
        json_filtercontext_type = UNSET
    else:
        json_filtercontext_type = filtercontext_type
    params["filter[context_type]"] = json_filtercontext_type

    json_filterattribute: None | str | Unset
    if isinstance(filterattribute, Unset):
        json_filterattribute = UNSET
    else:
        json_filterattribute = filterattribute
    params["filter[attribute]"] = json_filterattribute

    json_filtersearch: None | str | Unset
    if isinstance(filtersearch, Unset):
        json_filtersearch = UNSET
    else:
        json_filtersearch = filtersearch
    params["filter[search]"] = json_filtersearch

    params["page[number]"] = pagenumber

    params["page[size]"] = pagesize

    params["meta[total]"] = metatotal

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/context_values",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ContextValueListResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = ContextValueListResponse.from_dict(response.json())

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
) -> Response[ContextValueListResponse | ErrorResponse]:
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
    filterattribute: None | str | Unset = UNSET,
    filtersearch: None | str | Unset = UNSET,
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> Response[ContextValueListResponse | ErrorResponse]:
    """List Context Values

     Return distinct values observed for a single attribute across context instances of one context type.
    The intended use case is a typeahead picker in a rule-building UI: the customer chooses a context
    type and an attribute name, then this endpoint streams back the distinct values matching what
    they've typed so far.

    `filter[context_type]` and `filter[attribute]` are required. `filter[attribute]` accepts any
    attribute name — including the two first-class columns `key` and `name` — and is treated uniformly
    from the customer's perspective; the server adjusts the underlying query accordingly.

    `filter[search]` does a case-insensitive starts-with match. The returned set excludes empty strings
    and NULL values.

    Args:
        filtercontext_type (None | str | Unset): Context type key whose instances should be
            searched (e.g. `user`).
        filterattribute (None | str | Unset): Attribute name whose distinct values should be
            returned (e.g. `first_name`). Accepts `key` and `name` as well as any attribute key stored
            on the context instance.
        filtersearch (None | str | Unset): Optional case-insensitive starts-with match against the
            projected attribute value. When omitted, all distinct values are returned in the page.
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
        Response[ContextValueListResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        filtercontext_type=filtercontext_type,
        filterattribute=filterattribute,
        filtersearch=filtersearch,
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
    filterattribute: None | str | Unset = UNSET,
    filtersearch: None | str | Unset = UNSET,
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> ContextValueListResponse | ErrorResponse | None:
    """List Context Values

     Return distinct values observed for a single attribute across context instances of one context type.
    The intended use case is a typeahead picker in a rule-building UI: the customer chooses a context
    type and an attribute name, then this endpoint streams back the distinct values matching what
    they've typed so far.

    `filter[context_type]` and `filter[attribute]` are required. `filter[attribute]` accepts any
    attribute name — including the two first-class columns `key` and `name` — and is treated uniformly
    from the customer's perspective; the server adjusts the underlying query accordingly.

    `filter[search]` does a case-insensitive starts-with match. The returned set excludes empty strings
    and NULL values.

    Args:
        filtercontext_type (None | str | Unset): Context type key whose instances should be
            searched (e.g. `user`).
        filterattribute (None | str | Unset): Attribute name whose distinct values should be
            returned (e.g. `first_name`). Accepts `key` and `name` as well as any attribute key stored
            on the context instance.
        filtersearch (None | str | Unset): Optional case-insensitive starts-with match against the
            projected attribute value. When omitted, all distinct values are returned in the page.
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
        ContextValueListResponse | ErrorResponse
    """

    return sync_detailed(
        client=client,
        filtercontext_type=filtercontext_type,
        filterattribute=filterattribute,
        filtersearch=filtersearch,
        pagenumber=pagenumber,
        pagesize=pagesize,
        metatotal=metatotal,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    filtercontext_type: None | str | Unset = UNSET,
    filterattribute: None | str | Unset = UNSET,
    filtersearch: None | str | Unset = UNSET,
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> Response[ContextValueListResponse | ErrorResponse]:
    """List Context Values

     Return distinct values observed for a single attribute across context instances of one context type.
    The intended use case is a typeahead picker in a rule-building UI: the customer chooses a context
    type and an attribute name, then this endpoint streams back the distinct values matching what
    they've typed so far.

    `filter[context_type]` and `filter[attribute]` are required. `filter[attribute]` accepts any
    attribute name — including the two first-class columns `key` and `name` — and is treated uniformly
    from the customer's perspective; the server adjusts the underlying query accordingly.

    `filter[search]` does a case-insensitive starts-with match. The returned set excludes empty strings
    and NULL values.

    Args:
        filtercontext_type (None | str | Unset): Context type key whose instances should be
            searched (e.g. `user`).
        filterattribute (None | str | Unset): Attribute name whose distinct values should be
            returned (e.g. `first_name`). Accepts `key` and `name` as well as any attribute key stored
            on the context instance.
        filtersearch (None | str | Unset): Optional case-insensitive starts-with match against the
            projected attribute value. When omitted, all distinct values are returned in the page.
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
        Response[ContextValueListResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        filtercontext_type=filtercontext_type,
        filterattribute=filterattribute,
        filtersearch=filtersearch,
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
    filterattribute: None | str | Unset = UNSET,
    filtersearch: None | str | Unset = UNSET,
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> ContextValueListResponse | ErrorResponse | None:
    """List Context Values

     Return distinct values observed for a single attribute across context instances of one context type.
    The intended use case is a typeahead picker in a rule-building UI: the customer chooses a context
    type and an attribute name, then this endpoint streams back the distinct values matching what
    they've typed so far.

    `filter[context_type]` and `filter[attribute]` are required. `filter[attribute]` accepts any
    attribute name — including the two first-class columns `key` and `name` — and is treated uniformly
    from the customer's perspective; the server adjusts the underlying query accordingly.

    `filter[search]` does a case-insensitive starts-with match. The returned set excludes empty strings
    and NULL values.

    Args:
        filtercontext_type (None | str | Unset): Context type key whose instances should be
            searched (e.g. `user`).
        filterattribute (None | str | Unset): Attribute name whose distinct values should be
            returned (e.g. `first_name`). Accepts `key` and `name` as well as any attribute key stored
            on the context instance.
        filtersearch (None | str | Unset): Optional case-insensitive starts-with match against the
            projected attribute value. When omitted, all distinct values are returned in the page.
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
        ContextValueListResponse | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            filtercontext_type=filtercontext_type,
            filterattribute=filterattribute,
            filtersearch=filtersearch,
            pagenumber=pagenumber,
            pagesize=pagesize,
            metatotal=metatotal,
        )
    ).parsed
