from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.total_customer_cost import TotalCustomerCost
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    accounting_is_running: Union[Unset, bool] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    month: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["accounting_is_running"] = accounting_is_running

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    params["month"] = month

    params["name"] = name

    params["year"] = year

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/billing-total-cost/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> TotalCustomerCost:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = TotalCustomerCost.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[TotalCustomerCost]:
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
    customer_uuid: Union[Unset, UUID] = UNSET,
    month: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> Response[TotalCustomerCost]:
    """
    Args:
        accounting_is_running (Union[Unset, bool]):
        customer_uuid (Union[Unset, UUID]):
        month (Union[Unset, int]):
        name (Union[Unset, str]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TotalCustomerCost]
    """

    kwargs = _get_kwargs(
        accounting_is_running=accounting_is_running,
        customer_uuid=customer_uuid,
        month=month,
        name=name,
        year=year,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    accounting_is_running: Union[Unset, bool] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    month: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> TotalCustomerCost:
    """
    Args:
        accounting_is_running (Union[Unset, bool]):
        customer_uuid (Union[Unset, UUID]):
        month (Union[Unset, int]):
        name (Union[Unset, str]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TotalCustomerCost
    """

    return sync_detailed(
        client=client,
        accounting_is_running=accounting_is_running,
        customer_uuid=customer_uuid,
        month=month,
        name=name,
        year=year,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    accounting_is_running: Union[Unset, bool] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    month: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> Response[TotalCustomerCost]:
    """
    Args:
        accounting_is_running (Union[Unset, bool]):
        customer_uuid (Union[Unset, UUID]):
        month (Union[Unset, int]):
        name (Union[Unset, str]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TotalCustomerCost]
    """

    kwargs = _get_kwargs(
        accounting_is_running=accounting_is_running,
        customer_uuid=customer_uuid,
        month=month,
        name=name,
        year=year,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    accounting_is_running: Union[Unset, bool] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    month: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> TotalCustomerCost:
    """
    Args:
        accounting_is_running (Union[Unset, bool]):
        customer_uuid (Union[Unset, UUID]):
        month (Union[Unset, int]):
        name (Union[Unset, str]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TotalCustomerCost
    """

    return (
        await asyncio_detailed(
            client=client,
            accounting_is_running=accounting_is_running,
            customer_uuid=customer_uuid,
            month=month,
            name=name,
            year=year,
        )
    ).parsed
