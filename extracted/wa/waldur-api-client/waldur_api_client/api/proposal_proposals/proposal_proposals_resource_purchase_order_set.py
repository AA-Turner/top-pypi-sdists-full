from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.requested_resource_purchase_order import RequestedResourcePurchaseOrder
from ...models.requested_resource_purchase_order_request import RequestedResourcePurchaseOrderRequest
from ...models.requested_resource_purchase_order_request_form import RequestedResourcePurchaseOrderRequestForm
from ...models.requested_resource_purchase_order_request_multipart import RequestedResourcePurchaseOrderRequestMultipart
from ...types import Response


def _get_kwargs(
    uuid: str,
    obj_uuid: str,
    *,
    body: Union[
        RequestedResourcePurchaseOrderRequest,
        RequestedResourcePurchaseOrderRequestForm,
        RequestedResourcePurchaseOrderRequestMultipart,
    ],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/proposal-proposals/{uuid}/resources/{obj_uuid}/purchase_order/",
    }

    if isinstance(body, RequestedResourcePurchaseOrderRequest):
        _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"
    if isinstance(body, RequestedResourcePurchaseOrderRequestForm):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, RequestedResourcePurchaseOrderRequestMultipart):
        _kwargs["files"] = body.to_multipart()

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> RequestedResourcePurchaseOrder:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = RequestedResourcePurchaseOrder.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[RequestedResourcePurchaseOrder]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: str,
    obj_uuid: str,
    *,
    client: AuthenticatedClient,
    body: Union[
        RequestedResourcePurchaseOrderRequest,
        RequestedResourcePurchaseOrderRequestForm,
        RequestedResourcePurchaseOrderRequestMultipart,
    ],
) -> Response[RequestedResourcePurchaseOrder]:
    """Upload or replace the purchase order of a requested resource.

    Args:
        uuid (str):
        obj_uuid (str):
        body (RequestedResourcePurchaseOrderRequest):
        body (RequestedResourcePurchaseOrderRequestForm):
        body (RequestedResourcePurchaseOrderRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RequestedResourcePurchaseOrder]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        obj_uuid=obj_uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: str,
    obj_uuid: str,
    *,
    client: AuthenticatedClient,
    body: Union[
        RequestedResourcePurchaseOrderRequest,
        RequestedResourcePurchaseOrderRequestForm,
        RequestedResourcePurchaseOrderRequestMultipart,
    ],
) -> RequestedResourcePurchaseOrder:
    """Upload or replace the purchase order of a requested resource.

    Args:
        uuid (str):
        obj_uuid (str):
        body (RequestedResourcePurchaseOrderRequest):
        body (RequestedResourcePurchaseOrderRequestForm):
        body (RequestedResourcePurchaseOrderRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RequestedResourcePurchaseOrder
    """

    return sync_detailed(
        uuid=uuid,
        obj_uuid=obj_uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    uuid: str,
    obj_uuid: str,
    *,
    client: AuthenticatedClient,
    body: Union[
        RequestedResourcePurchaseOrderRequest,
        RequestedResourcePurchaseOrderRequestForm,
        RequestedResourcePurchaseOrderRequestMultipart,
    ],
) -> Response[RequestedResourcePurchaseOrder]:
    """Upload or replace the purchase order of a requested resource.

    Args:
        uuid (str):
        obj_uuid (str):
        body (RequestedResourcePurchaseOrderRequest):
        body (RequestedResourcePurchaseOrderRequestForm):
        body (RequestedResourcePurchaseOrderRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RequestedResourcePurchaseOrder]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        obj_uuid=obj_uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: str,
    obj_uuid: str,
    *,
    client: AuthenticatedClient,
    body: Union[
        RequestedResourcePurchaseOrderRequest,
        RequestedResourcePurchaseOrderRequestForm,
        RequestedResourcePurchaseOrderRequestMultipart,
    ],
) -> RequestedResourcePurchaseOrder:
    """Upload or replace the purchase order of a requested resource.

    Args:
        uuid (str):
        obj_uuid (str):
        body (RequestedResourcePurchaseOrderRequest):
        body (RequestedResourcePurchaseOrderRequestForm):
        body (RequestedResourcePurchaseOrderRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RequestedResourcePurchaseOrder
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            obj_uuid=obj_uuid,
            client=client,
            body=body,
        )
    ).parsed
