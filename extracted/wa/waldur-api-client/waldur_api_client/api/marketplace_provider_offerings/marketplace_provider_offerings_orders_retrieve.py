from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.order_details import OrderDetails
from ...types import Response


def _get_kwargs(
    uuid: str,
    order_uuid: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/marketplace-provider-offerings/{uuid}/orders/{order_uuid}/",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> OrderDetails:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = OrderDetails.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[OrderDetails]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: str,
    order_uuid: str,
    *,
    client: AuthenticatedClient,
) -> Response[OrderDetails]:
    """Retrieve a specific order for an offering

     Returns details of a specific order associated with an offering.

    Args:
        uuid (str):
        order_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OrderDetails]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        order_uuid=order_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: str,
    order_uuid: str,
    *,
    client: AuthenticatedClient,
) -> OrderDetails:
    """Retrieve a specific order for an offering

     Returns details of a specific order associated with an offering.

    Args:
        uuid (str):
        order_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OrderDetails
    """

    return sync_detailed(
        uuid=uuid,
        order_uuid=order_uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    uuid: str,
    order_uuid: str,
    *,
    client: AuthenticatedClient,
) -> Response[OrderDetails]:
    """Retrieve a specific order for an offering

     Returns details of a specific order associated with an offering.

    Args:
        uuid (str):
        order_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OrderDetails]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        order_uuid=order_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: str,
    order_uuid: str,
    *,
    client: AuthenticatedClient,
) -> OrderDetails:
    """Retrieve a specific order for an offering

     Returns details of a specific order associated with an offering.

    Args:
        uuid (str):
        order_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OrderDetails
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            order_uuid=order_uuid,
            client=client,
        )
    ).parsed
