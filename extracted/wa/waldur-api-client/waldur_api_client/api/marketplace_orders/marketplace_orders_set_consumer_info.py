from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.order_consumer_info_request import OrderConsumerInfoRequest
from ...models.order_consumer_info_request_form import OrderConsumerInfoRequestForm
from ...models.order_consumer_info_request_multipart import OrderConsumerInfoRequestMultipart
from ...models.order_info_response import OrderInfoResponse
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: Union[
        OrderConsumerInfoRequest,
        OrderConsumerInfoRequestForm,
        OrderConsumerInfoRequestMultipart,
    ],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/marketplace-orders/{uuid}/set_consumer_info/",
    }

    if isinstance(body, OrderConsumerInfoRequest):
        _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"
    if isinstance(body, OrderConsumerInfoRequestForm):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, OrderConsumerInfoRequestMultipart):
        _kwargs["files"] = body.to_multipart()

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> OrderInfoResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = OrderInfoResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[OrderInfoResponse]:
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
    body: Union[
        OrderConsumerInfoRequest,
        OrderConsumerInfoRequestForm,
        OrderConsumerInfoRequestMultipart,
    ],
) -> Response[OrderInfoResponse]:
    """Set consumer info on order

     Allows a consumer to respond to a provider's message with an optional message and file attachment on
    a pending order.

    Args:
        uuid (UUID):
        body (OrderConsumerInfoRequest):
        body (OrderConsumerInfoRequestForm):
        body (OrderConsumerInfoRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OrderInfoResponse]
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
    body: Union[
        OrderConsumerInfoRequest,
        OrderConsumerInfoRequestForm,
        OrderConsumerInfoRequestMultipart,
    ],
) -> OrderInfoResponse:
    """Set consumer info on order

     Allows a consumer to respond to a provider's message with an optional message and file attachment on
    a pending order.

    Args:
        uuid (UUID):
        body (OrderConsumerInfoRequest):
        body (OrderConsumerInfoRequestForm):
        body (OrderConsumerInfoRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OrderInfoResponse
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
    body: Union[
        OrderConsumerInfoRequest,
        OrderConsumerInfoRequestForm,
        OrderConsumerInfoRequestMultipart,
    ],
) -> Response[OrderInfoResponse]:
    """Set consumer info on order

     Allows a consumer to respond to a provider's message with an optional message and file attachment on
    a pending order.

    Args:
        uuid (UUID):
        body (OrderConsumerInfoRequest):
        body (OrderConsumerInfoRequestForm):
        body (OrderConsumerInfoRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OrderInfoResponse]
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
    body: Union[
        OrderConsumerInfoRequest,
        OrderConsumerInfoRequestForm,
        OrderConsumerInfoRequestMultipart,
    ],
) -> OrderInfoResponse:
    """Set consumer info on order

     Allows a consumer to respond to a provider's message with an optional message and file attachment on
    a pending order.

    Args:
        uuid (UUID):
        body (OrderConsumerInfoRequest):
        body (OrderConsumerInfoRequestForm):
        body (OrderConsumerInfoRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OrderInfoResponse
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
