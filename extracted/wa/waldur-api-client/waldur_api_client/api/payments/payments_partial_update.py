from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.patched_payment_request import PatchedPaymentRequest
from ...models.patched_payment_request_form import PatchedPaymentRequestForm
from ...models.patched_payment_request_multipart import PatchedPaymentRequestMultipart
from ...models.payment import Payment
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: Union[
        PatchedPaymentRequest,
        PatchedPaymentRequestForm,
        PatchedPaymentRequestMultipart,
    ],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/api/payments/{uuid}/",
    }

    if isinstance(body, PatchedPaymentRequest):
        _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"
    if isinstance(body, PatchedPaymentRequestForm):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, PatchedPaymentRequestMultipart):
        _kwargs["files"] = body.to_multipart()

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Payment:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = Payment.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Payment]:
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
        PatchedPaymentRequest,
        PatchedPaymentRequestForm,
        PatchedPaymentRequestMultipart,
    ],
) -> Response[Payment]:
    """
    Args:
        uuid (UUID):
        body (PatchedPaymentRequest):
        body (PatchedPaymentRequestForm):
        body (PatchedPaymentRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Payment]
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
        PatchedPaymentRequest,
        PatchedPaymentRequestForm,
        PatchedPaymentRequestMultipart,
    ],
) -> Payment:
    """
    Args:
        uuid (UUID):
        body (PatchedPaymentRequest):
        body (PatchedPaymentRequestForm):
        body (PatchedPaymentRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Payment
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
        PatchedPaymentRequest,
        PatchedPaymentRequestForm,
        PatchedPaymentRequestMultipart,
    ],
) -> Response[Payment]:
    """
    Args:
        uuid (UUID):
        body (PatchedPaymentRequest):
        body (PatchedPaymentRequestForm):
        body (PatchedPaymentRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Payment]
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
        PatchedPaymentRequest,
        PatchedPaymentRequestForm,
        PatchedPaymentRequestMultipart,
    ],
) -> Payment:
    """
    Args:
        uuid (UUID):
        body (PatchedPaymentRequest):
        body (PatchedPaymentRequestForm):
        body (PatchedPaymentRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Payment
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
