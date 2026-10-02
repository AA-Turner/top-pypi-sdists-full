import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.invoice_o_enum import InvoiceOEnum
from ...models.invoice_state_enum import InvoiceStateEnum
from ...models.invoice_stats_offering import InvoiceStatsOffering
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    uuid: UUID,
    *,
    accounting_is_running: Union[Unset, bool] = UNSET,
    created: Union[Unset, datetime.date] = UNSET,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    month: Union[Unset, int] = UNSET,
    o: Union[Unset, list[InvoiceOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
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

    json_provider_uuid: Union[Unset, str] = UNSET
    if not isinstance(provider_uuid, Unset):
        json_provider_uuid = str(provider_uuid)
    params["provider_uuid"] = json_provider_uuid

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
        "url": f"/api/invoices/{uuid}/stats/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["InvoiceStatsOffering"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = InvoiceStatsOffering.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["InvoiceStatsOffering"]]:
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
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    month: Union[Unset, int] = UNSET,
    o: Union[Unset, list[InvoiceOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    state: Union[Unset, list[InvoiceStateEnum]] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> Response[list["InvoiceStatsOffering"]]:
    """Spendings grouped by offerings and filtered by provider.

    Args:
        uuid (UUID):
        accounting_is_running (Union[Unset, bool]):
        created (Union[Unset, datetime.date]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        end_date (Union[Unset, datetime.date]):
        month (Union[Unset, int]):
        o (Union[Unset, list[InvoiceOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        provider_uuid (Union[Unset, UUID]):
        start_date (Union[Unset, datetime.date]):
        state (Union[Unset, list[InvoiceStateEnum]]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['InvoiceStatsOffering']]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        accounting_is_running=accounting_is_running,
        created=created,
        customer=customer,
        customer_uuid=customer_uuid,
        end_date=end_date,
        month=month,
        o=o,
        page=page,
        page_size=page_size,
        provider_uuid=provider_uuid,
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
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    month: Union[Unset, int] = UNSET,
    o: Union[Unset, list[InvoiceOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    state: Union[Unset, list[InvoiceStateEnum]] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> list["InvoiceStatsOffering"]:
    """Spendings grouped by offerings and filtered by provider.

    Args:
        uuid (UUID):
        accounting_is_running (Union[Unset, bool]):
        created (Union[Unset, datetime.date]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        end_date (Union[Unset, datetime.date]):
        month (Union[Unset, int]):
        o (Union[Unset, list[InvoiceOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        provider_uuid (Union[Unset, UUID]):
        start_date (Union[Unset, datetime.date]):
        state (Union[Unset, list[InvoiceStateEnum]]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['InvoiceStatsOffering']
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        accounting_is_running=accounting_is_running,
        created=created,
        customer=customer,
        customer_uuid=customer_uuid,
        end_date=end_date,
        month=month,
        o=o,
        page=page,
        page_size=page_size,
        provider_uuid=provider_uuid,
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
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    month: Union[Unset, int] = UNSET,
    o: Union[Unset, list[InvoiceOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    state: Union[Unset, list[InvoiceStateEnum]] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> Response[list["InvoiceStatsOffering"]]:
    """Spendings grouped by offerings and filtered by provider.

    Args:
        uuid (UUID):
        accounting_is_running (Union[Unset, bool]):
        created (Union[Unset, datetime.date]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        end_date (Union[Unset, datetime.date]):
        month (Union[Unset, int]):
        o (Union[Unset, list[InvoiceOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        provider_uuid (Union[Unset, UUID]):
        start_date (Union[Unset, datetime.date]):
        state (Union[Unset, list[InvoiceStateEnum]]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['InvoiceStatsOffering']]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        accounting_is_running=accounting_is_running,
        created=created,
        customer=customer,
        customer_uuid=customer_uuid,
        end_date=end_date,
        month=month,
        o=o,
        page=page,
        page_size=page_size,
        provider_uuid=provider_uuid,
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
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    month: Union[Unset, int] = UNSET,
    o: Union[Unset, list[InvoiceOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    state: Union[Unset, list[InvoiceStateEnum]] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> list["InvoiceStatsOffering"]:
    """Spendings grouped by offerings and filtered by provider.

    Args:
        uuid (UUID):
        accounting_is_running (Union[Unset, bool]):
        created (Union[Unset, datetime.date]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        end_date (Union[Unset, datetime.date]):
        month (Union[Unset, int]):
        o (Union[Unset, list[InvoiceOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        provider_uuid (Union[Unset, UUID]):
        start_date (Union[Unset, datetime.date]):
        state (Union[Unset, list[InvoiceStateEnum]]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['InvoiceStatsOffering']
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            accounting_is_running=accounting_is_running,
            created=created,
            customer=customer,
            customer_uuid=customer_uuid,
            end_date=end_date,
            month=month,
            o=o,
            page=page,
            page_size=page_size,
            provider_uuid=provider_uuid,
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
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    month: Union[Unset, int] = UNSET,
    o: Union[Unset, list[InvoiceOEnum]] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    state: Union[Unset, list[InvoiceStateEnum]] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> list["InvoiceStatsOffering"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        uuid (UUID):
        accounting_is_running (Union[Unset, bool]):
        created (Union[Unset, datetime.date]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        end_date (Union[Unset, datetime.date]):
        month (Union[Unset, int]):
        o (Union[Unset, list[InvoiceOEnum]]):
        provider_uuid (Union[Unset, UUID]):
        start_date (Union[Unset, datetime.date]):
        state (Union[Unset, list[InvoiceStateEnum]]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['InvoiceStatsOffering']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[InvoiceStatsOffering] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        uuid=uuid,
        accounting_is_running=accounting_is_running,
        created=created,
        customer=customer,
        customer_uuid=customer_uuid,
        end_date=end_date,
        month=month,
        o=o,
        provider_uuid=provider_uuid,
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
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    month: Union[Unset, int] = UNSET,
    o: Union[Unset, list[InvoiceOEnum]] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    state: Union[Unset, list[InvoiceStateEnum]] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> list["InvoiceStatsOffering"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        uuid (UUID):
        accounting_is_running (Union[Unset, bool]):
        created (Union[Unset, datetime.date]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        end_date (Union[Unset, datetime.date]):
        month (Union[Unset, int]):
        o (Union[Unset, list[InvoiceOEnum]]):
        provider_uuid (Union[Unset, UUID]):
        start_date (Union[Unset, datetime.date]):
        state (Union[Unset, list[InvoiceStateEnum]]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['InvoiceStatsOffering']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[InvoiceStatsOffering] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        uuid=uuid,
        accounting_is_running=accounting_is_running,
        created=created,
        customer=customer,
        customer_uuid=customer_uuid,
        end_date=end_date,
        month=month,
        o=o,
        provider_uuid=provider_uuid,
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
