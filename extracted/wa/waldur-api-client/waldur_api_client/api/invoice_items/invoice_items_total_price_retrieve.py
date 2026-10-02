from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.invoice_item_total_price import InvoiceItemTotalPrice
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    credit_uuid: Union[Unset, UUID] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    month: Union[Unset, int] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    start_month: Union[Unset, float] = UNSET,
    start_year: Union[Unset, float] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_credit_uuid: Union[Unset, str] = UNSET
    if not isinstance(credit_uuid, Unset):
        json_credit_uuid = str(credit_uuid)
    params["credit_uuid"] = json_credit_uuid

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    params["month"] = month

    json_offering_uuid: Union[Unset, str] = UNSET
    if not isinstance(offering_uuid, Unset):
        json_offering_uuid = str(offering_uuid)
    params["offering_uuid"] = json_offering_uuid

    json_project_uuid: Union[Unset, str] = UNSET
    if not isinstance(project_uuid, Unset):
        json_project_uuid = str(project_uuid)
    params["project_uuid"] = json_project_uuid

    json_resource_uuid: Union[Unset, str] = UNSET
    if not isinstance(resource_uuid, Unset):
        json_resource_uuid = str(resource_uuid)
    params["resource_uuid"] = json_resource_uuid

    params["start_month"] = start_month

    params["start_year"] = start_year

    params["year"] = year

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/invoice-items/total_price/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> InvoiceItemTotalPrice:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = InvoiceItemTotalPrice.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[InvoiceItemTotalPrice]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    credit_uuid: Union[Unset, UUID] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    month: Union[Unset, int] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    start_month: Union[Unset, float] = UNSET,
    start_year: Union[Unset, float] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> Response[InvoiceItemTotalPrice]:
    """Calculate total price for filtered invoice items.

    Args:
        credit_uuid (Union[Unset, UUID]):
        customer_uuid (Union[Unset, UUID]):
        month (Union[Unset, int]):
        offering_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):
        resource_uuid (Union[Unset, UUID]):
        start_month (Union[Unset, float]):
        start_year (Union[Unset, float]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[InvoiceItemTotalPrice]
    """

    kwargs = _get_kwargs(
        credit_uuid=credit_uuid,
        customer_uuid=customer_uuid,
        month=month,
        offering_uuid=offering_uuid,
        project_uuid=project_uuid,
        resource_uuid=resource_uuid,
        start_month=start_month,
        start_year=start_year,
        year=year,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    credit_uuid: Union[Unset, UUID] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    month: Union[Unset, int] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    start_month: Union[Unset, float] = UNSET,
    start_year: Union[Unset, float] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> InvoiceItemTotalPrice:
    """Calculate total price for filtered invoice items.

    Args:
        credit_uuid (Union[Unset, UUID]):
        customer_uuid (Union[Unset, UUID]):
        month (Union[Unset, int]):
        offering_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):
        resource_uuid (Union[Unset, UUID]):
        start_month (Union[Unset, float]):
        start_year (Union[Unset, float]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        InvoiceItemTotalPrice
    """

    return sync_detailed(
        client=client,
        credit_uuid=credit_uuid,
        customer_uuid=customer_uuid,
        month=month,
        offering_uuid=offering_uuid,
        project_uuid=project_uuid,
        resource_uuid=resource_uuid,
        start_month=start_month,
        start_year=start_year,
        year=year,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    credit_uuid: Union[Unset, UUID] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    month: Union[Unset, int] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    start_month: Union[Unset, float] = UNSET,
    start_year: Union[Unset, float] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> Response[InvoiceItemTotalPrice]:
    """Calculate total price for filtered invoice items.

    Args:
        credit_uuid (Union[Unset, UUID]):
        customer_uuid (Union[Unset, UUID]):
        month (Union[Unset, int]):
        offering_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):
        resource_uuid (Union[Unset, UUID]):
        start_month (Union[Unset, float]):
        start_year (Union[Unset, float]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[InvoiceItemTotalPrice]
    """

    kwargs = _get_kwargs(
        credit_uuid=credit_uuid,
        customer_uuid=customer_uuid,
        month=month,
        offering_uuid=offering_uuid,
        project_uuid=project_uuid,
        resource_uuid=resource_uuid,
        start_month=start_month,
        start_year=start_year,
        year=year,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    credit_uuid: Union[Unset, UUID] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    month: Union[Unset, int] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    start_month: Union[Unset, float] = UNSET,
    start_year: Union[Unset, float] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> InvoiceItemTotalPrice:
    """Calculate total price for filtered invoice items.

    Args:
        credit_uuid (Union[Unset, UUID]):
        customer_uuid (Union[Unset, UUID]):
        month (Union[Unset, int]):
        offering_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):
        resource_uuid (Union[Unset, UUID]):
        start_month (Union[Unset, float]):
        start_year (Union[Unset, float]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        InvoiceItemTotalPrice
    """

    return (
        await asyncio_detailed(
            client=client,
            credit_uuid=credit_uuid,
            customer_uuid=customer_uuid,
            month=month,
            offering_uuid=offering_uuid,
            project_uuid=project_uuid,
            resource_uuid=resource_uuid,
            start_month=start_month,
            start_year=start_year,
            year=year,
        )
    ).parsed
