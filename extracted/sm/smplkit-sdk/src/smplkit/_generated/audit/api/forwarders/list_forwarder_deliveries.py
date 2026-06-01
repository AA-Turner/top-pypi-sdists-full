from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.forwarder_delivery_list_response import ForwarderDeliveryListResponse
from ...models.list_forwarder_deliveries_sort import ListForwarderDeliveriesSort
from ...types import Unset


def _get_kwargs(
    forwarder_id: str,
    *,
    filterstatus: None | str | Unset = UNSET,
    filtercreated_at: None | str | Unset = UNSET,
    filterevent_id: None | str | Unset = UNSET,
    pagesize: int | None | Unset = UNSET,
    pageafter: None | str | Unset = UNSET,
    sort: ListForwarderDeliveriesSort | Unset = "-created_at",
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_filterstatus: None | str | Unset
    if isinstance(filterstatus, Unset):
        json_filterstatus = UNSET
    else:
        json_filterstatus = filterstatus
    params["filter[status]"] = json_filterstatus

    json_filtercreated_at: None | str | Unset
    if isinstance(filtercreated_at, Unset):
        json_filtercreated_at = UNSET
    else:
        json_filtercreated_at = filtercreated_at
    params["filter[created_at]"] = json_filtercreated_at

    json_filterevent_id: None | str | Unset
    if isinstance(filterevent_id, Unset):
        json_filterevent_id = UNSET
    else:
        json_filterevent_id = filterevent_id
    params["filter[event_id]"] = json_filterevent_id

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

    json_sort: str | Unset = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort

    params["sort"] = json_sort

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/forwarders/{forwarder_id}/deliveries".format(
            forwarder_id=quote(str(forwarder_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ForwarderDeliveryListResponse | None:
    if response.status_code == 200:
        response_200 = ForwarderDeliveryListResponse.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ForwarderDeliveryListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    forwarder_id: str,
    *,
    client: AuthenticatedClient,
    filterstatus: None | str | Unset = UNSET,
    filtercreated_at: None | str | Unset = UNSET,
    filterevent_id: None | str | Unset = UNSET,
    pagesize: int | None | Unset = UNSET,
    pageafter: None | str | Unset = UNSET,
    sort: ListForwarderDeliveriesSort | Unset = "-created_at",
) -> Response[ForwarderDeliveryListResponse]:
    """List Forwarder Deliveries

     List delivery log entries for a forwarder.

    Default sort is `-created_at` (newest first). Filter by `status` (one of
    `SUCCEEDED`, `FAILED`, `FILTERED_OUT`, `SKIPPED_DO_NOT_FORWARD` —
    case-insensitive), by `event_id`, or by a `created_at` range using
    interval notation (e.g. `[2026-01-01T00:00:00Z,*)`).

    Args:
        forwarder_id (str):
        filterstatus (None | str | Unset):
        filtercreated_at (None | str | Unset):
        filterevent_id (None | str | Unset):
        pagesize (int | None | Unset):
        pageafter (None | str | Unset):
        sort (ListForwarderDeliveriesSort | Unset): Field to sort by. Prefix with `-` for
            descending order. Default: `-created_at`. Allowed values: `created_at`, `-created_at`.
            Default: '-created_at'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ForwarderDeliveryListResponse]
    """

    kwargs = _get_kwargs(
        forwarder_id=forwarder_id,
        filterstatus=filterstatus,
        filtercreated_at=filtercreated_at,
        filterevent_id=filterevent_id,
        pagesize=pagesize,
        pageafter=pageafter,
        sort=sort,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    forwarder_id: str,
    *,
    client: AuthenticatedClient,
    filterstatus: None | str | Unset = UNSET,
    filtercreated_at: None | str | Unset = UNSET,
    filterevent_id: None | str | Unset = UNSET,
    pagesize: int | None | Unset = UNSET,
    pageafter: None | str | Unset = UNSET,
    sort: ListForwarderDeliveriesSort | Unset = "-created_at",
) -> ForwarderDeliveryListResponse | None:
    """List Forwarder Deliveries

     List delivery log entries for a forwarder.

    Default sort is `-created_at` (newest first). Filter by `status` (one of
    `SUCCEEDED`, `FAILED`, `FILTERED_OUT`, `SKIPPED_DO_NOT_FORWARD` —
    case-insensitive), by `event_id`, or by a `created_at` range using
    interval notation (e.g. `[2026-01-01T00:00:00Z,*)`).

    Args:
        forwarder_id (str):
        filterstatus (None | str | Unset):
        filtercreated_at (None | str | Unset):
        filterevent_id (None | str | Unset):
        pagesize (int | None | Unset):
        pageafter (None | str | Unset):
        sort (ListForwarderDeliveriesSort | Unset): Field to sort by. Prefix with `-` for
            descending order. Default: `-created_at`. Allowed values: `created_at`, `-created_at`.
            Default: '-created_at'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ForwarderDeliveryListResponse
    """

    return sync_detailed(
        forwarder_id=forwarder_id,
        client=client,
        filterstatus=filterstatus,
        filtercreated_at=filtercreated_at,
        filterevent_id=filterevent_id,
        pagesize=pagesize,
        pageafter=pageafter,
        sort=sort,
    ).parsed


async def asyncio_detailed(
    forwarder_id: str,
    *,
    client: AuthenticatedClient,
    filterstatus: None | str | Unset = UNSET,
    filtercreated_at: None | str | Unset = UNSET,
    filterevent_id: None | str | Unset = UNSET,
    pagesize: int | None | Unset = UNSET,
    pageafter: None | str | Unset = UNSET,
    sort: ListForwarderDeliveriesSort | Unset = "-created_at",
) -> Response[ForwarderDeliveryListResponse]:
    """List Forwarder Deliveries

     List delivery log entries for a forwarder.

    Default sort is `-created_at` (newest first). Filter by `status` (one of
    `SUCCEEDED`, `FAILED`, `FILTERED_OUT`, `SKIPPED_DO_NOT_FORWARD` —
    case-insensitive), by `event_id`, or by a `created_at` range using
    interval notation (e.g. `[2026-01-01T00:00:00Z,*)`).

    Args:
        forwarder_id (str):
        filterstatus (None | str | Unset):
        filtercreated_at (None | str | Unset):
        filterevent_id (None | str | Unset):
        pagesize (int | None | Unset):
        pageafter (None | str | Unset):
        sort (ListForwarderDeliveriesSort | Unset): Field to sort by. Prefix with `-` for
            descending order. Default: `-created_at`. Allowed values: `created_at`, `-created_at`.
            Default: '-created_at'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ForwarderDeliveryListResponse]
    """

    kwargs = _get_kwargs(
        forwarder_id=forwarder_id,
        filterstatus=filterstatus,
        filtercreated_at=filtercreated_at,
        filterevent_id=filterevent_id,
        pagesize=pagesize,
        pageafter=pageafter,
        sort=sort,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    forwarder_id: str,
    *,
    client: AuthenticatedClient,
    filterstatus: None | str | Unset = UNSET,
    filtercreated_at: None | str | Unset = UNSET,
    filterevent_id: None | str | Unset = UNSET,
    pagesize: int | None | Unset = UNSET,
    pageafter: None | str | Unset = UNSET,
    sort: ListForwarderDeliveriesSort | Unset = "-created_at",
) -> ForwarderDeliveryListResponse | None:
    """List Forwarder Deliveries

     List delivery log entries for a forwarder.

    Default sort is `-created_at` (newest first). Filter by `status` (one of
    `SUCCEEDED`, `FAILED`, `FILTERED_OUT`, `SKIPPED_DO_NOT_FORWARD` —
    case-insensitive), by `event_id`, or by a `created_at` range using
    interval notation (e.g. `[2026-01-01T00:00:00Z,*)`).

    Args:
        forwarder_id (str):
        filterstatus (None | str | Unset):
        filtercreated_at (None | str | Unset):
        filterevent_id (None | str | Unset):
        pagesize (int | None | Unset):
        pageafter (None | str | Unset):
        sort (ListForwarderDeliveriesSort | Unset): Field to sort by. Prefix with `-` for
            descending order. Default: `-created_at`. Allowed values: `created_at`, `-created_at`.
            Default: '-created_at'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ForwarderDeliveryListResponse
    """

    return (
        await asyncio_detailed(
            forwarder_id=forwarder_id,
            client=client,
            filterstatus=filterstatus,
            filtercreated_at=filtercreated_at,
            filterevent_id=filterevent_id,
            pagesize=pagesize,
            pageafter=pageafter,
            sort=sort,
        )
    ).parsed
