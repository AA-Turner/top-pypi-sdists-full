from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.api_key_list_response import ApiKeyListResponse
from ...models.error_response import ErrorResponse
from ...models.list_api_keys_sort import ListApiKeysSort
from ...types import Unset


def _get_kwargs(
    *,
    filterstatus: None | str | Unset = UNSET,
    filtersearch: None | str | Unset = UNSET,
    sort: ListApiKeysSort | Unset = "name",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_filterstatus: None | str | Unset
    if isinstance(filterstatus, Unset):
        json_filterstatus = UNSET
    else:
        json_filterstatus = filterstatus
    params["filter[status]"] = json_filterstatus

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
        "url": "/api/v1/api_keys",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ApiKeyListResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = ApiKeyListResponse.from_dict(response.json())

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
) -> Response[ApiKeyListResponse | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    filterstatus: None | str | Unset = UNSET,
    filtersearch: None | str | Unset = UNSET,
    sort: ListApiKeysSort | Unset = "name",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> Response[ApiKeyListResponse | ErrorResponse]:
    """List API Keys

     List all API keys for the authenticated account. `filter[search]` does a case-insensitive substring
    match against the API key `name`.

    Args:
        filterstatus (None | str | Unset):
        filtersearch (None | str | Unset): Case-insensitive substring match against the API key
            `name`.
        sort (ListApiKeysSort | Unset): Field to sort by. Prefix with `-` for descending order.
            Default: `name`. Allowed values: `created_at`, `-created_at`, `expires_at`, `-expires_at`,
            `last_used_at`, `-last_used_at`, `name`, `-name`, `status`, `-status`. Default: 'name'.
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
        Response[ApiKeyListResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        filterstatus=filterstatus,
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
    filterstatus: None | str | Unset = UNSET,
    filtersearch: None | str | Unset = UNSET,
    sort: ListApiKeysSort | Unset = "name",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> ApiKeyListResponse | ErrorResponse | None:
    """List API Keys

     List all API keys for the authenticated account. `filter[search]` does a case-insensitive substring
    match against the API key `name`.

    Args:
        filterstatus (None | str | Unset):
        filtersearch (None | str | Unset): Case-insensitive substring match against the API key
            `name`.
        sort (ListApiKeysSort | Unset): Field to sort by. Prefix with `-` for descending order.
            Default: `name`. Allowed values: `created_at`, `-created_at`, `expires_at`, `-expires_at`,
            `last_used_at`, `-last_used_at`, `name`, `-name`, `status`, `-status`. Default: 'name'.
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
        ApiKeyListResponse | ErrorResponse
    """

    return sync_detailed(
        client=client,
        filterstatus=filterstatus,
        filtersearch=filtersearch,
        sort=sort,
        pagenumber=pagenumber,
        pagesize=pagesize,
        metatotal=metatotal,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    filterstatus: None | str | Unset = UNSET,
    filtersearch: None | str | Unset = UNSET,
    sort: ListApiKeysSort | Unset = "name",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> Response[ApiKeyListResponse | ErrorResponse]:
    """List API Keys

     List all API keys for the authenticated account. `filter[search]` does a case-insensitive substring
    match against the API key `name`.

    Args:
        filterstatus (None | str | Unset):
        filtersearch (None | str | Unset): Case-insensitive substring match against the API key
            `name`.
        sort (ListApiKeysSort | Unset): Field to sort by. Prefix with `-` for descending order.
            Default: `name`. Allowed values: `created_at`, `-created_at`, `expires_at`, `-expires_at`,
            `last_used_at`, `-last_used_at`, `name`, `-name`, `status`, `-status`. Default: 'name'.
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
        Response[ApiKeyListResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        filterstatus=filterstatus,
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
    filterstatus: None | str | Unset = UNSET,
    filtersearch: None | str | Unset = UNSET,
    sort: ListApiKeysSort | Unset = "name",
    pagenumber: int | Unset = 1,
    pagesize: int | Unset = 1000,
    metatotal: bool | Unset = False,
) -> ApiKeyListResponse | ErrorResponse | None:
    """List API Keys

     List all API keys for the authenticated account. `filter[search]` does a case-insensitive substring
    match against the API key `name`.

    Args:
        filterstatus (None | str | Unset):
        filtersearch (None | str | Unset): Case-insensitive substring match against the API key
            `name`.
        sort (ListApiKeysSort | Unset): Field to sort by. Prefix with `-` for descending order.
            Default: `name`. Allowed values: `created_at`, `-created_at`, `expires_at`, `-expires_at`,
            `last_used_at`, `-last_used_at`, `name`, `-name`, `status`, `-status`. Default: 'name'.
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
        ApiKeyListResponse | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            filterstatus=filterstatus,
            filtersearch=filtersearch,
            sort=sort,
            pagenumber=pagenumber,
            pagesize=pagesize,
            metatotal=metatotal,
        )
    ).parsed
