from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.event_list_response import EventListResponse
from ...models.list_events_format_type_0 import ListEventsFormatType0
from ...models.list_events_sort import ListEventsSort
from ...types import Unset


def _get_kwargs(
    *,
    filteroccurred_at: None | str | Unset = UNSET,
    filteractor_type: None | str | Unset = UNSET,
    filteractor_id: None | str | Unset = UNSET,
    filterevent_type: None | str | Unset = UNSET,
    filterresource_type: None | str | Unset = UNSET,
    filterresource_id: None | str | Unset = UNSET,
    filterseverity: None | str | Unset = UNSET,
    filtercategory: None | str | Unset = UNSET,
    filtersearch: None | str | Unset = UNSET,
    filterdo_not_forward: bool | None | Unset = UNSET,
    pagesize: int | None | Unset = UNSET,
    pageafter: None | str | Unset = UNSET,
    format_: ListEventsFormatType0 | None | Unset = UNSET,
    sort: ListEventsSort | Unset = "-occurred_at",
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_filteroccurred_at: None | str | Unset
    if isinstance(filteroccurred_at, Unset):
        json_filteroccurred_at = UNSET
    else:
        json_filteroccurred_at = filteroccurred_at
    params["filter[occurred_at]"] = json_filteroccurred_at

    json_filteractor_type: None | str | Unset
    if isinstance(filteractor_type, Unset):
        json_filteractor_type = UNSET
    else:
        json_filteractor_type = filteractor_type
    params["filter[actor_type]"] = json_filteractor_type

    json_filteractor_id: None | str | Unset
    if isinstance(filteractor_id, Unset):
        json_filteractor_id = UNSET
    else:
        json_filteractor_id = filteractor_id
    params["filter[actor_id]"] = json_filteractor_id

    json_filterevent_type: None | str | Unset
    if isinstance(filterevent_type, Unset):
        json_filterevent_type = UNSET
    else:
        json_filterevent_type = filterevent_type
    params["filter[event_type]"] = json_filterevent_type

    json_filterresource_type: None | str | Unset
    if isinstance(filterresource_type, Unset):
        json_filterresource_type = UNSET
    else:
        json_filterresource_type = filterresource_type
    params["filter[resource_type]"] = json_filterresource_type

    json_filterresource_id: None | str | Unset
    if isinstance(filterresource_id, Unset):
        json_filterresource_id = UNSET
    else:
        json_filterresource_id = filterresource_id
    params["filter[resource_id]"] = json_filterresource_id

    json_filterseverity: None | str | Unset
    if isinstance(filterseverity, Unset):
        json_filterseverity = UNSET
    else:
        json_filterseverity = filterseverity
    params["filter[severity]"] = json_filterseverity

    json_filtercategory: None | str | Unset
    if isinstance(filtercategory, Unset):
        json_filtercategory = UNSET
    else:
        json_filtercategory = filtercategory
    params["filter[category]"] = json_filtercategory

    json_filtersearch: None | str | Unset
    if isinstance(filtersearch, Unset):
        json_filtersearch = UNSET
    else:
        json_filtersearch = filtersearch
    params["filter[search]"] = json_filtersearch

    json_filterdo_not_forward: bool | None | Unset
    if isinstance(filterdo_not_forward, Unset):
        json_filterdo_not_forward = UNSET
    else:
        json_filterdo_not_forward = filterdo_not_forward
    params["filter[do_not_forward]"] = json_filterdo_not_forward

    json_pagesize: int | None | Unset
    if isinstance(pagesize, Unset):
        json_pagesize = UNSET
    else:
        json_pagesize = pagesize
    params["page[size]"] = json_pagesize

    json_pageafter: None | str | Unset
    if isinstance(pageafter, Unset):
        json_pageafter = UNSET
    else:
        json_pageafter = pageafter
    params["page[after]"] = json_pageafter

    json_format_: None | str | Unset
    if isinstance(format_, Unset):
        json_format_ = UNSET
    elif isinstance(format_, str):
        json_format_ = format_
    else:
        json_format_ = format_
    params["format"] = json_format_

    json_sort: str | Unset = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort

    params["sort"] = json_sort

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/events",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> EventListResponse | None:
    if response.status_code == 200:
        response_200 = EventListResponse.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[EventListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    filteroccurred_at: None | str | Unset = UNSET,
    filteractor_type: None | str | Unset = UNSET,
    filteractor_id: None | str | Unset = UNSET,
    filterevent_type: None | str | Unset = UNSET,
    filterresource_type: None | str | Unset = UNSET,
    filterresource_id: None | str | Unset = UNSET,
    filterseverity: None | str | Unset = UNSET,
    filtercategory: None | str | Unset = UNSET,
    filtersearch: None | str | Unset = UNSET,
    filterdo_not_forward: bool | None | Unset = UNSET,
    pagesize: int | None | Unset = UNSET,
    pageafter: None | str | Unset = UNSET,
    format_: ListEventsFormatType0 | None | Unset = UNSET,
    sort: ListEventsSort | Unset = "-occurred_at",
) -> Response[EventListResponse]:
    """List Events

     List audit events for this account.

    Default sort is `-occurred_at` (newest occurrence first). Sort by
    `occurred_at` or `created_at`, ascending or descending — keep the same
    `sort` value across paginated requests so the cursor stays consistent.
    Filters are exact-match except `filter[occurred_at]`, which uses
    interval notation (e.g.
    `[2026-01-01T00:00:00Z,2026-01-31T00:00:00Z)`), and `filter[search]`,
    which is a case-insensitive substring match against `resource_id` or
    `description`.

    Two filter-combination rules:

    - `filter[resource_id]` must be accompanied by `filter[resource_type]`
      (the index is keyed on the pair).
    - `filter[search]` must be accompanied by either `filter[occurred_at]`
      or `filter[resource_type]` + `filter[resource_id]` (substring
      matching has no index, so an unbounded substring scan is rejected).

    No other filter combinations are required — calling the endpoint with
    no query parameters returns the latest events for the account,
    paginated.

    `page[size]` defaults to 1000 and must not exceed 1000.

    Pass `format=CSV` or `format=JSONL` to stream a download of the full
    filtered result set instead of a paginated JSON:API response. The
    download honors every supplied filter and ignores `page[size]` and
    `page[after]`.

    Args:
        filteroccurred_at (None | str | Unset):
        filteractor_type (None | str | Unset):
        filteractor_id (None | str | Unset):
        filterevent_type (None | str | Unset):
        filterresource_type (None | str | Unset):
        filterresource_id (None | str | Unset):
        filterseverity (None | str | Unset): Exact match on the event's `severity` field. One of
            `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`, `FATAL`.
        filtercategory (None | str | Unset): Exact match on the event's `category` field.
        filtersearch (None | str | Unset): Case-insensitive substring match against `resource_id`
            or `description`. Use `filter[resource_id]` for an exact match on `resource_id`.
        filterdo_not_forward (bool | None | Unset): When set, restrict to events whose
            `do_not_forward` flag matches the given boolean. Forwarder previews typically pass `false`
            to match live-pipeline semantics (events flagged `do_not_forward=true` are skipped by the
            forwarder pipeline).
        pagesize (int | None | Unset):
        pageafter (None | str | Unset):
        format_ (ListEventsFormatType0 | None | Unset): When set, stream a download of the full
            filtered result set in the chosen format instead of returning a paginated JSON:API
            response. `page[size]` and `page[after]` are ignored in this mode; every event matching
            the supplied filters is emitted. `CSV` writes one row per event with the event payload
            (`data`) serialized as a single JSON-encoded cell. `JSONL` writes one JSON object per line
            with the event payload nested as a JSON object. Omit this parameter to receive the
            paginated JSON:API response.
        sort (ListEventsSort | Unset): Field to sort by. Prefix with `-` for descending order.
            Default: `-occurred_at`. Allowed values: `created_at`, `-created_at`, `occurred_at`,
            `-occurred_at`. Default: '-occurred_at'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EventListResponse]
    """

    kwargs = _get_kwargs(
        filteroccurred_at=filteroccurred_at,
        filteractor_type=filteractor_type,
        filteractor_id=filteractor_id,
        filterevent_type=filterevent_type,
        filterresource_type=filterresource_type,
        filterresource_id=filterresource_id,
        filterseverity=filterseverity,
        filtercategory=filtercategory,
        filtersearch=filtersearch,
        filterdo_not_forward=filterdo_not_forward,
        pagesize=pagesize,
        pageafter=pageafter,
        format_=format_,
        sort=sort,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    filteroccurred_at: None | str | Unset = UNSET,
    filteractor_type: None | str | Unset = UNSET,
    filteractor_id: None | str | Unset = UNSET,
    filterevent_type: None | str | Unset = UNSET,
    filterresource_type: None | str | Unset = UNSET,
    filterresource_id: None | str | Unset = UNSET,
    filterseverity: None | str | Unset = UNSET,
    filtercategory: None | str | Unset = UNSET,
    filtersearch: None | str | Unset = UNSET,
    filterdo_not_forward: bool | None | Unset = UNSET,
    pagesize: int | None | Unset = UNSET,
    pageafter: None | str | Unset = UNSET,
    format_: ListEventsFormatType0 | None | Unset = UNSET,
    sort: ListEventsSort | Unset = "-occurred_at",
) -> EventListResponse | None:
    """List Events

     List audit events for this account.

    Default sort is `-occurred_at` (newest occurrence first). Sort by
    `occurred_at` or `created_at`, ascending or descending — keep the same
    `sort` value across paginated requests so the cursor stays consistent.
    Filters are exact-match except `filter[occurred_at]`, which uses
    interval notation (e.g.
    `[2026-01-01T00:00:00Z,2026-01-31T00:00:00Z)`), and `filter[search]`,
    which is a case-insensitive substring match against `resource_id` or
    `description`.

    Two filter-combination rules:

    - `filter[resource_id]` must be accompanied by `filter[resource_type]`
      (the index is keyed on the pair).
    - `filter[search]` must be accompanied by either `filter[occurred_at]`
      or `filter[resource_type]` + `filter[resource_id]` (substring
      matching has no index, so an unbounded substring scan is rejected).

    No other filter combinations are required — calling the endpoint with
    no query parameters returns the latest events for the account,
    paginated.

    `page[size]` defaults to 1000 and must not exceed 1000.

    Pass `format=CSV` or `format=JSONL` to stream a download of the full
    filtered result set instead of a paginated JSON:API response. The
    download honors every supplied filter and ignores `page[size]` and
    `page[after]`.

    Args:
        filteroccurred_at (None | str | Unset):
        filteractor_type (None | str | Unset):
        filteractor_id (None | str | Unset):
        filterevent_type (None | str | Unset):
        filterresource_type (None | str | Unset):
        filterresource_id (None | str | Unset):
        filterseverity (None | str | Unset): Exact match on the event's `severity` field. One of
            `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`, `FATAL`.
        filtercategory (None | str | Unset): Exact match on the event's `category` field.
        filtersearch (None | str | Unset): Case-insensitive substring match against `resource_id`
            or `description`. Use `filter[resource_id]` for an exact match on `resource_id`.
        filterdo_not_forward (bool | None | Unset): When set, restrict to events whose
            `do_not_forward` flag matches the given boolean. Forwarder previews typically pass `false`
            to match live-pipeline semantics (events flagged `do_not_forward=true` are skipped by the
            forwarder pipeline).
        pagesize (int | None | Unset):
        pageafter (None | str | Unset):
        format_ (ListEventsFormatType0 | None | Unset): When set, stream a download of the full
            filtered result set in the chosen format instead of returning a paginated JSON:API
            response. `page[size]` and `page[after]` are ignored in this mode; every event matching
            the supplied filters is emitted. `CSV` writes one row per event with the event payload
            (`data`) serialized as a single JSON-encoded cell. `JSONL` writes one JSON object per line
            with the event payload nested as a JSON object. Omit this parameter to receive the
            paginated JSON:API response.
        sort (ListEventsSort | Unset): Field to sort by. Prefix with `-` for descending order.
            Default: `-occurred_at`. Allowed values: `created_at`, `-created_at`, `occurred_at`,
            `-occurred_at`. Default: '-occurred_at'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EventListResponse
    """

    return sync_detailed(
        client=client,
        filteroccurred_at=filteroccurred_at,
        filteractor_type=filteractor_type,
        filteractor_id=filteractor_id,
        filterevent_type=filterevent_type,
        filterresource_type=filterresource_type,
        filterresource_id=filterresource_id,
        filterseverity=filterseverity,
        filtercategory=filtercategory,
        filtersearch=filtersearch,
        filterdo_not_forward=filterdo_not_forward,
        pagesize=pagesize,
        pageafter=pageafter,
        format_=format_,
        sort=sort,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    filteroccurred_at: None | str | Unset = UNSET,
    filteractor_type: None | str | Unset = UNSET,
    filteractor_id: None | str | Unset = UNSET,
    filterevent_type: None | str | Unset = UNSET,
    filterresource_type: None | str | Unset = UNSET,
    filterresource_id: None | str | Unset = UNSET,
    filterseverity: None | str | Unset = UNSET,
    filtercategory: None | str | Unset = UNSET,
    filtersearch: None | str | Unset = UNSET,
    filterdo_not_forward: bool | None | Unset = UNSET,
    pagesize: int | None | Unset = UNSET,
    pageafter: None | str | Unset = UNSET,
    format_: ListEventsFormatType0 | None | Unset = UNSET,
    sort: ListEventsSort | Unset = "-occurred_at",
) -> Response[EventListResponse]:
    """List Events

     List audit events for this account.

    Default sort is `-occurred_at` (newest occurrence first). Sort by
    `occurred_at` or `created_at`, ascending or descending — keep the same
    `sort` value across paginated requests so the cursor stays consistent.
    Filters are exact-match except `filter[occurred_at]`, which uses
    interval notation (e.g.
    `[2026-01-01T00:00:00Z,2026-01-31T00:00:00Z)`), and `filter[search]`,
    which is a case-insensitive substring match against `resource_id` or
    `description`.

    Two filter-combination rules:

    - `filter[resource_id]` must be accompanied by `filter[resource_type]`
      (the index is keyed on the pair).
    - `filter[search]` must be accompanied by either `filter[occurred_at]`
      or `filter[resource_type]` + `filter[resource_id]` (substring
      matching has no index, so an unbounded substring scan is rejected).

    No other filter combinations are required — calling the endpoint with
    no query parameters returns the latest events for the account,
    paginated.

    `page[size]` defaults to 1000 and must not exceed 1000.

    Pass `format=CSV` or `format=JSONL` to stream a download of the full
    filtered result set instead of a paginated JSON:API response. The
    download honors every supplied filter and ignores `page[size]` and
    `page[after]`.

    Args:
        filteroccurred_at (None | str | Unset):
        filteractor_type (None | str | Unset):
        filteractor_id (None | str | Unset):
        filterevent_type (None | str | Unset):
        filterresource_type (None | str | Unset):
        filterresource_id (None | str | Unset):
        filterseverity (None | str | Unset): Exact match on the event's `severity` field. One of
            `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`, `FATAL`.
        filtercategory (None | str | Unset): Exact match on the event's `category` field.
        filtersearch (None | str | Unset): Case-insensitive substring match against `resource_id`
            or `description`. Use `filter[resource_id]` for an exact match on `resource_id`.
        filterdo_not_forward (bool | None | Unset): When set, restrict to events whose
            `do_not_forward` flag matches the given boolean. Forwarder previews typically pass `false`
            to match live-pipeline semantics (events flagged `do_not_forward=true` are skipped by the
            forwarder pipeline).
        pagesize (int | None | Unset):
        pageafter (None | str | Unset):
        format_ (ListEventsFormatType0 | None | Unset): When set, stream a download of the full
            filtered result set in the chosen format instead of returning a paginated JSON:API
            response. `page[size]` and `page[after]` are ignored in this mode; every event matching
            the supplied filters is emitted. `CSV` writes one row per event with the event payload
            (`data`) serialized as a single JSON-encoded cell. `JSONL` writes one JSON object per line
            with the event payload nested as a JSON object. Omit this parameter to receive the
            paginated JSON:API response.
        sort (ListEventsSort | Unset): Field to sort by. Prefix with `-` for descending order.
            Default: `-occurred_at`. Allowed values: `created_at`, `-created_at`, `occurred_at`,
            `-occurred_at`. Default: '-occurred_at'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EventListResponse]
    """

    kwargs = _get_kwargs(
        filteroccurred_at=filteroccurred_at,
        filteractor_type=filteractor_type,
        filteractor_id=filteractor_id,
        filterevent_type=filterevent_type,
        filterresource_type=filterresource_type,
        filterresource_id=filterresource_id,
        filterseverity=filterseverity,
        filtercategory=filtercategory,
        filtersearch=filtersearch,
        filterdo_not_forward=filterdo_not_forward,
        pagesize=pagesize,
        pageafter=pageafter,
        format_=format_,
        sort=sort,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    filteroccurred_at: None | str | Unset = UNSET,
    filteractor_type: None | str | Unset = UNSET,
    filteractor_id: None | str | Unset = UNSET,
    filterevent_type: None | str | Unset = UNSET,
    filterresource_type: None | str | Unset = UNSET,
    filterresource_id: None | str | Unset = UNSET,
    filterseverity: None | str | Unset = UNSET,
    filtercategory: None | str | Unset = UNSET,
    filtersearch: None | str | Unset = UNSET,
    filterdo_not_forward: bool | None | Unset = UNSET,
    pagesize: int | None | Unset = UNSET,
    pageafter: None | str | Unset = UNSET,
    format_: ListEventsFormatType0 | None | Unset = UNSET,
    sort: ListEventsSort | Unset = "-occurred_at",
) -> EventListResponse | None:
    """List Events

     List audit events for this account.

    Default sort is `-occurred_at` (newest occurrence first). Sort by
    `occurred_at` or `created_at`, ascending or descending — keep the same
    `sort` value across paginated requests so the cursor stays consistent.
    Filters are exact-match except `filter[occurred_at]`, which uses
    interval notation (e.g.
    `[2026-01-01T00:00:00Z,2026-01-31T00:00:00Z)`), and `filter[search]`,
    which is a case-insensitive substring match against `resource_id` or
    `description`.

    Two filter-combination rules:

    - `filter[resource_id]` must be accompanied by `filter[resource_type]`
      (the index is keyed on the pair).
    - `filter[search]` must be accompanied by either `filter[occurred_at]`
      or `filter[resource_type]` + `filter[resource_id]` (substring
      matching has no index, so an unbounded substring scan is rejected).

    No other filter combinations are required — calling the endpoint with
    no query parameters returns the latest events for the account,
    paginated.

    `page[size]` defaults to 1000 and must not exceed 1000.

    Pass `format=CSV` or `format=JSONL` to stream a download of the full
    filtered result set instead of a paginated JSON:API response. The
    download honors every supplied filter and ignores `page[size]` and
    `page[after]`.

    Args:
        filteroccurred_at (None | str | Unset):
        filteractor_type (None | str | Unset):
        filteractor_id (None | str | Unset):
        filterevent_type (None | str | Unset):
        filterresource_type (None | str | Unset):
        filterresource_id (None | str | Unset):
        filterseverity (None | str | Unset): Exact match on the event's `severity` field. One of
            `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`, `FATAL`.
        filtercategory (None | str | Unset): Exact match on the event's `category` field.
        filtersearch (None | str | Unset): Case-insensitive substring match against `resource_id`
            or `description`. Use `filter[resource_id]` for an exact match on `resource_id`.
        filterdo_not_forward (bool | None | Unset): When set, restrict to events whose
            `do_not_forward` flag matches the given boolean. Forwarder previews typically pass `false`
            to match live-pipeline semantics (events flagged `do_not_forward=true` are skipped by the
            forwarder pipeline).
        pagesize (int | None | Unset):
        pageafter (None | str | Unset):
        format_ (ListEventsFormatType0 | None | Unset): When set, stream a download of the full
            filtered result set in the chosen format instead of returning a paginated JSON:API
            response. `page[size]` and `page[after]` are ignored in this mode; every event matching
            the supplied filters is emitted. `CSV` writes one row per event with the event payload
            (`data`) serialized as a single JSON-encoded cell. `JSONL` writes one JSON object per line
            with the event payload nested as a JSON object. Omit this parameter to receive the
            paginated JSON:API response.
        sort (ListEventsSort | Unset): Field to sort by. Prefix with `-` for descending order.
            Default: `-occurred_at`. Allowed values: `created_at`, `-created_at`, `occurred_at`,
            `-occurred_at`. Default: '-occurred_at'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EventListResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            filteroccurred_at=filteroccurred_at,
            filteractor_type=filteractor_type,
            filteractor_id=filteractor_id,
            filterevent_type=filterevent_type,
            filterresource_type=filterresource_type,
            filterresource_id=filterresource_id,
            filterseverity=filterseverity,
            filtercategory=filtercategory,
            filtersearch=filtersearch,
            filterdo_not_forward=filterdo_not_forward,
            pagesize=pagesize,
            pageafter=pageafter,
            format_=format_,
            sort=sort,
        )
    ).parsed
