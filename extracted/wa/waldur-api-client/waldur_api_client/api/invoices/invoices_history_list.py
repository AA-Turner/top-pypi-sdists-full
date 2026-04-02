import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.invoice_o_enum import InvoiceOEnum
from ...models.invoice_state_enum import InvoiceStateEnum
from ...models.version_history import VersionHistory
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    uuid: UUID,
    *,
    accounting_is_running: Union[Unset, bool] = UNSET,
    created: Union[Unset, datetime.date] = UNSET,
    created_after: Union[Unset, str] = UNSET,
    created_before: Union[Unset, str] = UNSET,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    month: Union[Unset, int] = UNSET,
    o: Union[Unset, list[InvoiceOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    state: Union[Unset, list[InvoiceStateEnum]] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["accounting_is_running"] = accounting_is_running

    json_created: Union[Unset, str] = UNSET
    if not isinstance(created, Unset):
        json_created = created.isoformat()
    params["created"] = json_created

    params["created_after"] = created_after

    params["created_before"] = created_before

    params["customer"] = customer

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    json_end_date: Union[Unset, str] = UNSET
    if not isinstance(end_date, Unset):
        json_end_date = end_date.isoformat()
    params["end_date"] = json_end_date

    params["month"] = month

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["page"] = page

    params["page_size"] = page_size

    json_start_date: Union[Unset, str] = UNSET
    if not isinstance(start_date, Unset):
        json_start_date = start_date.isoformat()
    params["start_date"] = json_start_date

    json_state: Union[Unset, list[str]] = UNSET
    if not isinstance(state, Unset):
        json_state = []
        for state_item_data in state:
            state_item = state_item_data.value
            json_state.append(state_item)

    params["state"] = json_state

    params["year"] = year

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/invoices/{uuid}/history/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["VersionHistory"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = VersionHistory.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["VersionHistory"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    accounting_is_running: Union[Unset, bool] = UNSET,
    created: Union[Unset, datetime.date] = UNSET,
    created_after: Union[Unset, str] = UNSET,
    created_before: Union[Unset, str] = UNSET,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    month: Union[Unset, int] = UNSET,
    o: Union[Unset, list[InvoiceOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    state: Union[Unset, list[InvoiceStateEnum]] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> Response[list["VersionHistory"]]:
    """Get version history

     Returns the version history for this object. Only accessible by staff and support users.

    Args:
        uuid (UUID):
        accounting_is_running (Union[Unset, bool]):
        created (Union[Unset, datetime.date]):
        created_after (Union[Unset, str]):
        created_before (Union[Unset, str]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        end_date (Union[Unset, datetime.date]):
        month (Union[Unset, int]):
        o (Union[Unset, list[InvoiceOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        start_date (Union[Unset, datetime.date]):
        state (Union[Unset, list[InvoiceStateEnum]]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VersionHistory']]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        accounting_is_running=accounting_is_running,
        created=created,
        created_after=created_after,
        created_before=created_before,
        customer=customer,
        customer_uuid=customer_uuid,
        end_date=end_date,
        month=month,
        o=o,
        page=page,
        page_size=page_size,
        start_date=start_date,
        state=state,
        year=year,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    accounting_is_running: Union[Unset, bool] = UNSET,
    created: Union[Unset, datetime.date] = UNSET,
    created_after: Union[Unset, str] = UNSET,
    created_before: Union[Unset, str] = UNSET,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    month: Union[Unset, int] = UNSET,
    o: Union[Unset, list[InvoiceOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    state: Union[Unset, list[InvoiceStateEnum]] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> list["VersionHistory"]:
    """Get version history

     Returns the version history for this object. Only accessible by staff and support users.

    Args:
        uuid (UUID):
        accounting_is_running (Union[Unset, bool]):
        created (Union[Unset, datetime.date]):
        created_after (Union[Unset, str]):
        created_before (Union[Unset, str]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        end_date (Union[Unset, datetime.date]):
        month (Union[Unset, int]):
        o (Union[Unset, list[InvoiceOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        start_date (Union[Unset, datetime.date]):
        state (Union[Unset, list[InvoiceStateEnum]]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VersionHistory']
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        accounting_is_running=accounting_is_running,
        created=created,
        created_after=created_after,
        created_before=created_before,
        customer=customer,
        customer_uuid=customer_uuid,
        end_date=end_date,
        month=month,
        o=o,
        page=page,
        page_size=page_size,
        start_date=start_date,
        state=state,
        year=year,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    accounting_is_running: Union[Unset, bool] = UNSET,
    created: Union[Unset, datetime.date] = UNSET,
    created_after: Union[Unset, str] = UNSET,
    created_before: Union[Unset, str] = UNSET,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    month: Union[Unset, int] = UNSET,
    o: Union[Unset, list[InvoiceOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    state: Union[Unset, list[InvoiceStateEnum]] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> Response[list["VersionHistory"]]:
    """Get version history

     Returns the version history for this object. Only accessible by staff and support users.

    Args:
        uuid (UUID):
        accounting_is_running (Union[Unset, bool]):
        created (Union[Unset, datetime.date]):
        created_after (Union[Unset, str]):
        created_before (Union[Unset, str]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        end_date (Union[Unset, datetime.date]):
        month (Union[Unset, int]):
        o (Union[Unset, list[InvoiceOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        start_date (Union[Unset, datetime.date]):
        state (Union[Unset, list[InvoiceStateEnum]]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VersionHistory']]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        accounting_is_running=accounting_is_running,
        created=created,
        created_after=created_after,
        created_before=created_before,
        customer=customer,
        customer_uuid=customer_uuid,
        end_date=end_date,
        month=month,
        o=o,
        page=page,
        page_size=page_size,
        start_date=start_date,
        state=state,
        year=year,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    accounting_is_running: Union[Unset, bool] = UNSET,
    created: Union[Unset, datetime.date] = UNSET,
    created_after: Union[Unset, str] = UNSET,
    created_before: Union[Unset, str] = UNSET,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    month: Union[Unset, int] = UNSET,
    o: Union[Unset, list[InvoiceOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    state: Union[Unset, list[InvoiceStateEnum]] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> list["VersionHistory"]:
    """Get version history

     Returns the version history for this object. Only accessible by staff and support users.

    Args:
        uuid (UUID):
        accounting_is_running (Union[Unset, bool]):
        created (Union[Unset, datetime.date]):
        created_after (Union[Unset, str]):
        created_before (Union[Unset, str]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        end_date (Union[Unset, datetime.date]):
        month (Union[Unset, int]):
        o (Union[Unset, list[InvoiceOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        start_date (Union[Unset, datetime.date]):
        state (Union[Unset, list[InvoiceStateEnum]]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VersionHistory']
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            accounting_is_running=accounting_is_running,
            created=created,
            created_after=created_after,
            created_before=created_before,
            customer=customer,
            customer_uuid=customer_uuid,
            end_date=end_date,
            month=month,
            o=o,
            page=page,
            page_size=page_size,
            start_date=start_date,
            state=state,
            year=year,
        )
    ).parsed


def sync_all(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    accounting_is_running: Union[Unset, bool] = UNSET,
    created: Union[Unset, datetime.date] = UNSET,
    created_after: Union[Unset, str] = UNSET,
    created_before: Union[Unset, str] = UNSET,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    month: Union[Unset, int] = UNSET,
    o: Union[Unset, list[InvoiceOEnum]] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    state: Union[Unset, list[InvoiceStateEnum]] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> list["VersionHistory"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        uuid (UUID):
        accounting_is_running (Union[Unset, bool]):
        created (Union[Unset, datetime.date]):
        created_after (Union[Unset, str]):
        created_before (Union[Unset, str]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        end_date (Union[Unset, datetime.date]):
        month (Union[Unset, int]):
        o (Union[Unset, list[InvoiceOEnum]]):
        start_date (Union[Unset, datetime.date]):
        state (Union[Unset, list[InvoiceStateEnum]]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VersionHistory']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[VersionHistory] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        uuid=uuid,
        accounting_is_running=accounting_is_running,
        created=created,
        created_after=created_after,
        created_before=created_before,
        customer=customer,
        customer_uuid=customer_uuid,
        end_date=end_date,
        month=month,
        o=o,
        start_date=start_date,
        state=state,
        year=year,
    )

    # Set page_size to maximum
    if "params" not in kwargs:
        kwargs["params"] = {}
    kwargs["params"]["page_size"] = 100

    # Make initial request
    response = client.get_httpx_client().request(**kwargs)
    parsed_response = _parse_response(client=client, response=response)

    if parsed_response:
        all_results.extend(parsed_response)

    # Follow pagination links
    while True:
        link_header = response.headers.get("Link", "")
        links = parse_link_header(link_header)

        if "next" not in links:
            break

        # Extract page number from next URL
        next_url = links["next"]
        parsed_url = urlparse(next_url)
        next_params = parse_qs(parsed_url.query)

        if "page" not in next_params:
            break

        # Update only the page parameter, keep all other params
        page_number = next_params["page"][0]
        kwargs["params"]["page"] = page_number

        # Fetch next page
        response = client.get_httpx_client().request(**kwargs)
        parsed_response = _parse_response(client=client, response=response)

        if parsed_response:
            all_results.extend(parsed_response)

    return all_results


async def asyncio_all(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    accounting_is_running: Union[Unset, bool] = UNSET,
    created: Union[Unset, datetime.date] = UNSET,
    created_after: Union[Unset, str] = UNSET,
    created_before: Union[Unset, str] = UNSET,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    month: Union[Unset, int] = UNSET,
    o: Union[Unset, list[InvoiceOEnum]] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    state: Union[Unset, list[InvoiceStateEnum]] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> list["VersionHistory"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        uuid (UUID):
        accounting_is_running (Union[Unset, bool]):
        created (Union[Unset, datetime.date]):
        created_after (Union[Unset, str]):
        created_before (Union[Unset, str]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        end_date (Union[Unset, datetime.date]):
        month (Union[Unset, int]):
        o (Union[Unset, list[InvoiceOEnum]]):
        start_date (Union[Unset, datetime.date]):
        state (Union[Unset, list[InvoiceStateEnum]]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VersionHistory']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[VersionHistory] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        uuid=uuid,
        accounting_is_running=accounting_is_running,
        created=created,
        created_after=created_after,
        created_before=created_before,
        customer=customer,
        customer_uuid=customer_uuid,
        end_date=end_date,
        month=month,
        o=o,
        start_date=start_date,
        state=state,
        year=year,
    )

    # Set page_size to maximum
    if "params" not in kwargs:
        kwargs["params"] = {}
    kwargs["params"]["page_size"] = 100

    # Make initial request
    response = await client.get_async_httpx_client().request(**kwargs)
    parsed_response = _parse_response(client=client, response=response)

    if parsed_response:
        all_results.extend(parsed_response)

    # Follow pagination links
    while True:
        link_header = response.headers.get("Link", "")
        links = parse_link_header(link_header)

        if "next" not in links:
            break

        # Extract page number from next URL
        next_url = links["next"]
        parsed_url = urlparse(next_url)
        next_params = parse_qs(parsed_url.query)

        if "page" not in next_params:
            break

        # Update only the page parameter, keep all other params
        page_number = next_params["page"][0]
        kwargs["params"]["page"] = page_number

        # Fetch next page
        response = await client.get_async_httpx_client().request(**kwargs)
        parsed_response = _parse_response(client=client, response=response)

        if parsed_response:
            all_results.extend(parsed_response)

    return all_results
