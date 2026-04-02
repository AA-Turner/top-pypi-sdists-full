from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.marketplace_orders_set_backend_id_response_200 import MarketplaceOrdersSetBackendIdResponse200
from ...models.order_backend_id_request import OrderBackendIDRequest
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: OrderBackendIDRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/marketplace-orders/{uuid}/set_backend_id/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> MarketplaceOrdersSetBackendIdResponse200:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = MarketplaceOrdersSetBackendIdResponse200.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[MarketplaceOrdersSetBackendIdResponse200]:
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
    body: OrderBackendIDRequest,
) -> Response[MarketplaceOrdersSetBackendIdResponse200]:
    """Set order backend ID

     Allows a service provider or staff to set or update the backend ID associated with an order. This is
    useful for linking the order to an external system's identifier.

    Args:
        uuid (UUID):
        body (OrderBackendIDRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MarketplaceOrdersSetBackendIdResponse200]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: OrderBackendIDRequest,
) -> MarketplaceOrdersSetBackendIdResponse200:
    """Set order backend ID

     Allows a service provider or staff to set or update the backend ID associated with an order. This is
    useful for linking the order to an external system's identifier.

    Args:
        uuid (UUID):
        body (OrderBackendIDRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MarketplaceOrdersSetBackendIdResponse200
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: OrderBackendIDRequest,
) -> Response[MarketplaceOrdersSetBackendIdResponse200]:
    """Set order backend ID

     Allows a service provider or staff to set or update the backend ID associated with an order. This is
    useful for linking the order to an external system's identifier.

    Args:
        uuid (UUID):
        body (OrderBackendIDRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MarketplaceOrdersSetBackendIdResponse200]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: OrderBackendIDRequest,
) -> MarketplaceOrdersSetBackendIdResponse200:
    """Set order backend ID

     Allows a service provider or staff to set or update the backend ID associated with an order. This is
    useful for linking the order to an external system's identifier.

    Args:
        uuid (UUID):
        body (OrderBackendIDRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MarketplaceOrdersSetBackendIdResponse200
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
