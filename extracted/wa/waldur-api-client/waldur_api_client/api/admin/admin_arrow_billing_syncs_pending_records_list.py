from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.pending_record import PendingRecord
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    arrow_state: Union[Unset, str] = UNSET,
    customer_mapping: Union[Unset, str] = UNSET,
    customer_mapping_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    report_period: Union[Unset, str] = UNSET,
    report_period_from: Union[Unset, str] = UNSET,
    report_period_to: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, int] = UNSET,
    statement_reference: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["arrow_state"] = arrow_state

    params["customer_mapping"] = customer_mapping

    json_customer_mapping_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_mapping_uuid, Unset):
        json_customer_mapping_uuid = str(customer_mapping_uuid)
    params["customer_mapping_uuid"] = json_customer_mapping_uuid

    params["page"] = page

    params["page_size"] = page_size

    params["report_period"] = report_period

    params["report_period_from"] = report_period_from

    params["report_period_to"] = report_period_to

    json_settings_uuid: Union[Unset, str] = UNSET
    if not isinstance(settings_uuid, Unset):
        json_settings_uuid = str(settings_uuid)
    params["settings_uuid"] = json_settings_uuid

    params["state"] = state

    params["statement_reference"] = statement_reference

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/admin/arrow/billing-syncs/pending_records/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["PendingRecord"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = PendingRecord.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["PendingRecord"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    arrow_state: Union[Unset, str] = UNSET,
    customer_mapping: Union[Unset, str] = UNSET,
    customer_mapping_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    report_period: Union[Unset, str] = UNSET,
    report_period_from: Union[Unset, str] = UNSET,
    report_period_to: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, int] = UNSET,
    statement_reference: Union[Unset, str] = UNSET,
) -> Response[list["PendingRecord"]]:
    """List pending consumption records (not yet finalized).

    Args:
        arrow_state (Union[Unset, str]):
        customer_mapping (Union[Unset, str]):
        customer_mapping_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        report_period (Union[Unset, str]):
        report_period_from (Union[Unset, str]):
        report_period_to (Union[Unset, str]):
        settings_uuid (Union[Unset, UUID]):
        state (Union[Unset, int]):
        statement_reference (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['PendingRecord']]
    """

    kwargs = _get_kwargs(
        arrow_state=arrow_state,
        customer_mapping=customer_mapping,
        customer_mapping_uuid=customer_mapping_uuid,
        page=page,
        page_size=page_size,
        report_period=report_period,
        report_period_from=report_period_from,
        report_period_to=report_period_to,
        settings_uuid=settings_uuid,
        state=state,
        statement_reference=statement_reference,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    arrow_state: Union[Unset, str] = UNSET,
    customer_mapping: Union[Unset, str] = UNSET,
    customer_mapping_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    report_period: Union[Unset, str] = UNSET,
    report_period_from: Union[Unset, str] = UNSET,
    report_period_to: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, int] = UNSET,
    statement_reference: Union[Unset, str] = UNSET,
) -> list["PendingRecord"]:
    """List pending consumption records (not yet finalized).

    Args:
        arrow_state (Union[Unset, str]):
        customer_mapping (Union[Unset, str]):
        customer_mapping_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        report_period (Union[Unset, str]):
        report_period_from (Union[Unset, str]):
        report_period_to (Union[Unset, str]):
        settings_uuid (Union[Unset, UUID]):
        state (Union[Unset, int]):
        statement_reference (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PendingRecord']
    """

    return sync_detailed(
        client=client,
        arrow_state=arrow_state,
        customer_mapping=customer_mapping,
        customer_mapping_uuid=customer_mapping_uuid,
        page=page,
        page_size=page_size,
        report_period=report_period,
        report_period_from=report_period_from,
        report_period_to=report_period_to,
        settings_uuid=settings_uuid,
        state=state,
        statement_reference=statement_reference,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    arrow_state: Union[Unset, str] = UNSET,
    customer_mapping: Union[Unset, str] = UNSET,
    customer_mapping_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    report_period: Union[Unset, str] = UNSET,
    report_period_from: Union[Unset, str] = UNSET,
    report_period_to: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, int] = UNSET,
    statement_reference: Union[Unset, str] = UNSET,
) -> Response[list["PendingRecord"]]:
    """List pending consumption records (not yet finalized).

    Args:
        arrow_state (Union[Unset, str]):
        customer_mapping (Union[Unset, str]):
        customer_mapping_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        report_period (Union[Unset, str]):
        report_period_from (Union[Unset, str]):
        report_period_to (Union[Unset, str]):
        settings_uuid (Union[Unset, UUID]):
        state (Union[Unset, int]):
        statement_reference (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['PendingRecord']]
    """

    kwargs = _get_kwargs(
        arrow_state=arrow_state,
        customer_mapping=customer_mapping,
        customer_mapping_uuid=customer_mapping_uuid,
        page=page,
        page_size=page_size,
        report_period=report_period,
        report_period_from=report_period_from,
        report_period_to=report_period_to,
        settings_uuid=settings_uuid,
        state=state,
        statement_reference=statement_reference,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    arrow_state: Union[Unset, str] = UNSET,
    customer_mapping: Union[Unset, str] = UNSET,
    customer_mapping_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    report_period: Union[Unset, str] = UNSET,
    report_period_from: Union[Unset, str] = UNSET,
    report_period_to: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, int] = UNSET,
    statement_reference: Union[Unset, str] = UNSET,
) -> list["PendingRecord"]:
    """List pending consumption records (not yet finalized).

    Args:
        arrow_state (Union[Unset, str]):
        customer_mapping (Union[Unset, str]):
        customer_mapping_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        report_period (Union[Unset, str]):
        report_period_from (Union[Unset, str]):
        report_period_to (Union[Unset, str]):
        settings_uuid (Union[Unset, UUID]):
        state (Union[Unset, int]):
        statement_reference (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PendingRecord']
    """

    return (
        await asyncio_detailed(
            client=client,
            arrow_state=arrow_state,
            customer_mapping=customer_mapping,
            customer_mapping_uuid=customer_mapping_uuid,
            page=page,
            page_size=page_size,
            report_period=report_period,
            report_period_from=report_period_from,
            report_period_to=report_period_to,
            settings_uuid=settings_uuid,
            state=state,
            statement_reference=statement_reference,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    arrow_state: Union[Unset, str] = UNSET,
    customer_mapping: Union[Unset, str] = UNSET,
    customer_mapping_uuid: Union[Unset, UUID] = UNSET,
    report_period: Union[Unset, str] = UNSET,
    report_period_from: Union[Unset, str] = UNSET,
    report_period_to: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, int] = UNSET,
    statement_reference: Union[Unset, str] = UNSET,
) -> list["PendingRecord"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        arrow_state (Union[Unset, str]):
        customer_mapping (Union[Unset, str]):
        customer_mapping_uuid (Union[Unset, UUID]):
        report_period (Union[Unset, str]):
        report_period_from (Union[Unset, str]):
        report_period_to (Union[Unset, str]):
        settings_uuid (Union[Unset, UUID]):
        state (Union[Unset, int]):
        statement_reference (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PendingRecord']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[PendingRecord] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        arrow_state=arrow_state,
        customer_mapping=customer_mapping,
        customer_mapping_uuid=customer_mapping_uuid,
        report_period=report_period,
        report_period_from=report_period_from,
        report_period_to=report_period_to,
        settings_uuid=settings_uuid,
        state=state,
        statement_reference=statement_reference,
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
    *,
    client: AuthenticatedClient,
    arrow_state: Union[Unset, str] = UNSET,
    customer_mapping: Union[Unset, str] = UNSET,
    customer_mapping_uuid: Union[Unset, UUID] = UNSET,
    report_period: Union[Unset, str] = UNSET,
    report_period_from: Union[Unset, str] = UNSET,
    report_period_to: Union[Unset, str] = UNSET,
    settings_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, int] = UNSET,
    statement_reference: Union[Unset, str] = UNSET,
) -> list["PendingRecord"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        arrow_state (Union[Unset, str]):
        customer_mapping (Union[Unset, str]):
        customer_mapping_uuid (Union[Unset, UUID]):
        report_period (Union[Unset, str]):
        report_period_from (Union[Unset, str]):
        report_period_to (Union[Unset, str]):
        settings_uuid (Union[Unset, UUID]):
        state (Union[Unset, int]):
        statement_reference (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PendingRecord']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[PendingRecord] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        arrow_state=arrow_state,
        customer_mapping=customer_mapping,
        customer_mapping_uuid=customer_mapping_uuid,
        report_period=report_period,
        report_period_from=report_period_from,
        report_period_to=report_period_to,
        settings_uuid=settings_uuid,
        state=state,
        statement_reference=statement_reference,
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
