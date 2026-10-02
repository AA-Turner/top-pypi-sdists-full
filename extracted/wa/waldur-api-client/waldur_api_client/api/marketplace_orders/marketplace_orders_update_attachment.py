from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.order_attachment import OrderAttachment
from ...models.order_attachment_request import OrderAttachmentRequest
from ...models.order_attachment_request_form import OrderAttachmentRequestForm
from ...models.order_attachment_request_multipart import OrderAttachmentRequestMultipart
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: Union[
        OrderAttachmentRequest,
        OrderAttachmentRequestForm,
        OrderAttachmentRequestMultipart,
    ],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/marketplace-orders/{uuid}/update_attachment/",
    }

    if isinstance(body, OrderAttachmentRequest):
        _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"
    if isinstance(body, OrderAttachmentRequestForm):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, OrderAttachmentRequestMultipart):
        _kwargs["files"] = body.to_multipart()

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> OrderAttachment:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = OrderAttachment.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[OrderAttachment]:
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
        OrderAttachmentRequest,
        OrderAttachmentRequestForm,
        OrderAttachmentRequestMultipart,
    ],
) -> Response[OrderAttachment]:
    """Update order attachment

     Allows uploading or replacing a file attachment (e.g., a purchase order) for a pending order.

    Args:
        uuid (UUID):
        body (OrderAttachmentRequest):
        body (OrderAttachmentRequestForm):
        body (OrderAttachmentRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OrderAttachment]
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
        OrderAttachmentRequest,
        OrderAttachmentRequestForm,
        OrderAttachmentRequestMultipart,
    ],
) -> OrderAttachment:
    """Update order attachment

     Allows uploading or replacing a file attachment (e.g., a purchase order) for a pending order.

    Args:
        uuid (UUID):
        body (OrderAttachmentRequest):
        body (OrderAttachmentRequestForm):
        body (OrderAttachmentRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OrderAttachment
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
        OrderAttachmentRequest,
        OrderAttachmentRequestForm,
        OrderAttachmentRequestMultipart,
    ],
) -> Response[OrderAttachment]:
    """Update order attachment

     Allows uploading or replacing a file attachment (e.g., a purchase order) for a pending order.

    Args:
        uuid (UUID):
        body (OrderAttachmentRequest):
        body (OrderAttachmentRequestForm):
        body (OrderAttachmentRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OrderAttachment]
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
        OrderAttachmentRequest,
        OrderAttachmentRequestForm,
        OrderAttachmentRequestMultipart,
    ],
) -> OrderAttachment:
    """Update order attachment

     Allows uploading or replacing a file attachment (e.g., a purchase order) for a pending order.

    Args:
        uuid (UUID):
        body (OrderAttachmentRequest):
        body (OrderAttachmentRequestForm):
        body (OrderAttachmentRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OrderAttachment
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
