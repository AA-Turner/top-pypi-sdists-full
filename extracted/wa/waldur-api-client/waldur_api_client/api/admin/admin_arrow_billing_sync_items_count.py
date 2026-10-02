from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


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
        "method": "head",
        "url": "/api/admin/arrow/billing-sync-items/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> int:
    if response.status_code == HTTPStatus.OK:
        try:
            return int(response.headers["x-result-count"])
        except KeyError:
            raise errors.UnexpectedStatus(
                response.status_code,
                b"Expected 'X-Result-Count' header for HEAD request, but it was not found.",
                response.url,
            )
        except ValueError:
            count_val = response.headers.get("x-result-count")
            msg = f"Expected 'X-Result-Count' header to be an integer, but got '{count_val}'."
            raise errors.UnexpectedStatus(response.status_code, msg.encode(), response.url)
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[int]:
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
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

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
        Response[int]
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
) -> int:
    """Get number of items in the collection matching the request parameters.

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
        int
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
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

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
        Response[int]
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
) -> int:
    """Get number of items in the collection matching the request parameters.

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
        int
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
