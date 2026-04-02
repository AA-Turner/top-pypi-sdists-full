from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.invoice_growth import InvoiceGrowth
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    accounting_is_running: Union[Unset, bool] = UNSET,
    accounting_mode: Union[Unset, str] = UNSET,
    customers_count: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["accounting_is_running"] = accounting_is_running

    params["accounting_mode"] = accounting_mode

    params["customers_count"] = customers_count

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/invoices/growth/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> InvoiceGrowth:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = InvoiceGrowth.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[InvoiceGrowth]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    accounting_is_running: Union[Unset, bool] = UNSET,
    accounting_mode: Union[Unset, str] = UNSET,
    customers_count: Union[Unset, int] = UNSET,
) -> Response[InvoiceGrowth]:
    """Analyze invoice trends over time by comparing monthly totals for major customers versus others over
    the past year.

    Args:
        accounting_is_running (Union[Unset, bool]):
        accounting_mode (Union[Unset, str]):
        customers_count (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[InvoiceGrowth]
    """

    kwargs = _get_kwargs(
        accounting_is_running=accounting_is_running,
        accounting_mode=accounting_mode,
        customers_count=customers_count,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    accounting_is_running: Union[Unset, bool] = UNSET,
    accounting_mode: Union[Unset, str] = UNSET,
    customers_count: Union[Unset, int] = UNSET,
) -> InvoiceGrowth:
    """Analyze invoice trends over time by comparing monthly totals for major customers versus others over
    the past year.

    Args:
        accounting_is_running (Union[Unset, bool]):
        accounting_mode (Union[Unset, str]):
        customers_count (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        InvoiceGrowth
    """

    return sync_detailed(
        client=client,
        accounting_is_running=accounting_is_running,
        accounting_mode=accounting_mode,
        customers_count=customers_count,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    accounting_is_running: Union[Unset, bool] = UNSET,
    accounting_mode: Union[Unset, str] = UNSET,
    customers_count: Union[Unset, int] = UNSET,
) -> Response[InvoiceGrowth]:
    """Analyze invoice trends over time by comparing monthly totals for major customers versus others over
    the past year.

    Args:
        accounting_is_running (Union[Unset, bool]):
        accounting_mode (Union[Unset, str]):
        customers_count (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[InvoiceGrowth]
    """

    kwargs = _get_kwargs(
        accounting_is_running=accounting_is_running,
        accounting_mode=accounting_mode,
        customers_count=customers_count,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    accounting_is_running: Union[Unset, bool] = UNSET,
    accounting_mode: Union[Unset, str] = UNSET,
    customers_count: Union[Unset, int] = UNSET,
) -> InvoiceGrowth:
    """Analyze invoice trends over time by comparing monthly totals for major customers versus others over
    the past year.

    Args:
        accounting_is_running (Union[Unset, bool]):
        accounting_mode (Union[Unset, str]):
        customers_count (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        InvoiceGrowth
    """

    return (
        await asyncio_detailed(
            client=client,
            accounting_is_running=accounting_is_running,
            accounting_mode=accounting_mode,
            customers_count=customers_count,
        )
    ).parsed
