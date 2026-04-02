from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.arrow_billing_sync_item_detail import ArrowBillingSyncItemDetail
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    arrow_line_reference: Union[Unset, str] = UNSET,
    billing_sync: Union[Unset, str] = UNSET,
    billing_sync_uuid: Union[Unset, UUID] = UNSET,
    classification: Union[Unset, str] = UNSET,
    has_compensation: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    report_period: Union[Unset, str] = UNSET,
    subscription_reference: Union[Unset, str] = UNSET,
    vendor_name: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["arrow_line_reference"] = arrow_line_reference

    params["billing_sync"] = billing_sync

    json_billing_sync_uuid: Union[Unset, str] = UNSET
    if not isinstance(billing_sync_uuid, Unset):
        json_billing_sync_uuid = str(billing_sync_uuid)
    params["billing_sync_uuid"] = json_billing_sync_uuid

    params["classification"] = classification

    params["has_compensation"] = has_compensation

    params["page"] = page

    params["page_size"] = page_size

    params["report_period"] = report_period

    params["subscription_reference"] = subscription_reference

    params["vendor_name"] = vendor_name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/admin/arrow/billing-sync-items/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["ArrowBillingSyncItemDetail"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ArrowBillingSyncItemDetail.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["ArrowBillingSyncItemDetail"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    arrow_line_reference: Union[Unset, str] = UNSET,
    billing_sync: Union[Unset, str] = UNSET,
    billing_sync_uuid: Union[Unset, UUID] = UNSET,
    classification: Union[Unset, str] = UNSET,
    has_compensation: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    report_period: Union[Unset, str] = UNSET,
    subscription_reference: Union[Unset, str] = UNSET,
    vendor_name: Union[Unset, str] = UNSET,
) -> Response[list["ArrowBillingSyncItemDetail"]]:
    """
    Args:
        arrow_line_reference (Union[Unset, str]):
        billing_sync (Union[Unset, str]):
        billing_sync_uuid (Union[Unset, UUID]):
        classification (Union[Unset, str]):
        has_compensation (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        report_period (Union[Unset, str]):
        subscription_reference (Union[Unset, str]):
        vendor_name (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ArrowBillingSyncItemDetail']]
    """

    kwargs = _get_kwargs(
        arrow_line_reference=arrow_line_reference,
        billing_sync=billing_sync,
        billing_sync_uuid=billing_sync_uuid,
        classification=classification,
        has_compensation=has_compensation,
        page=page,
        page_size=page_size,
        report_period=report_period,
        subscription_reference=subscription_reference,
        vendor_name=vendor_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    arrow_line_reference: Union[Unset, str] = UNSET,
    billing_sync: Union[Unset, str] = UNSET,
    billing_sync_uuid: Union[Unset, UUID] = UNSET,
    classification: Union[Unset, str] = UNSET,
    has_compensation: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    report_period: Union[Unset, str] = UNSET,
    subscription_reference: Union[Unset, str] = UNSET,
    vendor_name: Union[Unset, str] = UNSET,
) -> list["ArrowBillingSyncItemDetail"]:
    """
    Args:
        arrow_line_reference (Union[Unset, str]):
        billing_sync (Union[Unset, str]):
        billing_sync_uuid (Union[Unset, UUID]):
        classification (Union[Unset, str]):
        has_compensation (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        report_period (Union[Unset, str]):
        subscription_reference (Union[Unset, str]):
        vendor_name (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ArrowBillingSyncItemDetail']
    """

    return sync_detailed(
        client=client,
        arrow_line_reference=arrow_line_reference,
        billing_sync=billing_sync,
        billing_sync_uuid=billing_sync_uuid,
        classification=classification,
        has_compensation=has_compensation,
        page=page,
        page_size=page_size,
        report_period=report_period,
        subscription_reference=subscription_reference,
        vendor_name=vendor_name,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    arrow_line_reference: Union[Unset, str] = UNSET,
    billing_sync: Union[Unset, str] = UNSET,
    billing_sync_uuid: Union[Unset, UUID] = UNSET,
    classification: Union[Unset, str] = UNSET,
    has_compensation: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    report_period: Union[Unset, str] = UNSET,
    subscription_reference: Union[Unset, str] = UNSET,
    vendor_name: Union[Unset, str] = UNSET,
) -> Response[list["ArrowBillingSyncItemDetail"]]:
    """
    Args:
        arrow_line_reference (Union[Unset, str]):
        billing_sync (Union[Unset, str]):
        billing_sync_uuid (Union[Unset, UUID]):
        classification (Union[Unset, str]):
        has_compensation (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        report_period (Union[Unset, str]):
        subscription_reference (Union[Unset, str]):
        vendor_name (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ArrowBillingSyncItemDetail']]
    """

    kwargs = _get_kwargs(
        arrow_line_reference=arrow_line_reference,
        billing_sync=billing_sync,
        billing_sync_uuid=billing_sync_uuid,
        classification=classification,
        has_compensation=has_compensation,
        page=page,
        page_size=page_size,
        report_period=report_period,
        subscription_reference=subscription_reference,
        vendor_name=vendor_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    arrow_line_reference: Union[Unset, str] = UNSET,
    billing_sync: Union[Unset, str] = UNSET,
    billing_sync_uuid: Union[Unset, UUID] = UNSET,
    classification: Union[Unset, str] = UNSET,
    has_compensation: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    report_period: Union[Unset, str] = UNSET,
    subscription_reference: Union[Unset, str] = UNSET,
    vendor_name: Union[Unset, str] = UNSET,
) -> list["ArrowBillingSyncItemDetail"]:
    """
    Args:
        arrow_line_reference (Union[Unset, str]):
        billing_sync (Union[Unset, str]):
        billing_sync_uuid (Union[Unset, UUID]):
        classification (Union[Unset, str]):
        has_compensation (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        report_period (Union[Unset, str]):
        subscription_reference (Union[Unset, str]):
        vendor_name (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ArrowBillingSyncItemDetail']
    """

    return (
        await asyncio_detailed(
            client=client,
            arrow_line_reference=arrow_line_reference,
            billing_sync=billing_sync,
            billing_sync_uuid=billing_sync_uuid,
            classification=classification,
            has_compensation=has_compensation,
            page=page,
            page_size=page_size,
            report_period=report_period,
            subscription_reference=subscription_reference,
            vendor_name=vendor_name,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    arrow_line_reference: Union[Unset, str] = UNSET,
    billing_sync: Union[Unset, str] = UNSET,
    billing_sync_uuid: Union[Unset, UUID] = UNSET,
    classification: Union[Unset, str] = UNSET,
    has_compensation: Union[Unset, bool] = UNSET,
    report_period: Union[Unset, str] = UNSET,
    subscription_reference: Union[Unset, str] = UNSET,
    vendor_name: Union[Unset, str] = UNSET,
) -> list["ArrowBillingSyncItemDetail"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        arrow_line_reference (Union[Unset, str]):
        billing_sync (Union[Unset, str]):
        billing_sync_uuid (Union[Unset, UUID]):
        classification (Union[Unset, str]):
        has_compensation (Union[Unset, bool]):
        report_period (Union[Unset, str]):
        subscription_reference (Union[Unset, str]):
        vendor_name (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ArrowBillingSyncItemDetail']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[ArrowBillingSyncItemDetail] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        arrow_line_reference=arrow_line_reference,
        billing_sync=billing_sync,
        billing_sync_uuid=billing_sync_uuid,
        classification=classification,
        has_compensation=has_compensation,
        report_period=report_period,
        subscription_reference=subscription_reference,
        vendor_name=vendor_name,
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
    arrow_line_reference: Union[Unset, str] = UNSET,
    billing_sync: Union[Unset, str] = UNSET,
    billing_sync_uuid: Union[Unset, UUID] = UNSET,
    classification: Union[Unset, str] = UNSET,
    has_compensation: Union[Unset, bool] = UNSET,
    report_period: Union[Unset, str] = UNSET,
    subscription_reference: Union[Unset, str] = UNSET,
    vendor_name: Union[Unset, str] = UNSET,
) -> list["ArrowBillingSyncItemDetail"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        arrow_line_reference (Union[Unset, str]):
        billing_sync (Union[Unset, str]):
        billing_sync_uuid (Union[Unset, UUID]):
        classification (Union[Unset, str]):
        has_compensation (Union[Unset, bool]):
        report_period (Union[Unset, str]):
        subscription_reference (Union[Unset, str]):
        vendor_name (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ArrowBillingSyncItemDetail']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[ArrowBillingSyncItemDetail] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        arrow_line_reference=arrow_line_reference,
        billing_sync=billing_sync,
        billing_sync_uuid=billing_sync_uuid,
        classification=classification,
        has_compensation=has_compensation,
        report_period=report_period,
        subscription_reference=subscription_reference,
        vendor_name=vendor_name,
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
