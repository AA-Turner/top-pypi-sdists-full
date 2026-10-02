from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.webhook_payload import WebhookPayload
from ...models.webhook_payload_request import WebhookPayloadRequest
from ...types import Response


def _get_kwargs(
    provider_uuid: str,
    backend_type: str,
    *,
    body: WebhookPayloadRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/support-provider-webhook/{provider_uuid}/{backend_type}/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> WebhookPayload:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = WebhookPayload.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[WebhookPayload]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    provider_uuid: str,
    backend_type: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: WebhookPayloadRequest,
) -> Response[WebhookPayload]:
    """
    Args:
        provider_uuid (str):
        backend_type (str):
        body (WebhookPayloadRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WebhookPayload]
    """

    kwargs = _get_kwargs(
        provider_uuid=provider_uuid,
        backend_type=backend_type,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    provider_uuid: str,
    backend_type: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: WebhookPayloadRequest,
) -> WebhookPayload:
    """
    Args:
        provider_uuid (str):
        backend_type (str):
        body (WebhookPayloadRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WebhookPayload
    """

    return sync_detailed(
        provider_uuid=provider_uuid,
        backend_type=backend_type,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    provider_uuid: str,
    backend_type: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: WebhookPayloadRequest,
) -> Response[WebhookPayload]:
    """
    Args:
        provider_uuid (str):
        backend_type (str):
        body (WebhookPayloadRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WebhookPayload]
    """

    kwargs = _get_kwargs(
        provider_uuid=provider_uuid,
        backend_type=backend_type,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    provider_uuid: str,
    backend_type: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: WebhookPayloadRequest,
) -> WebhookPayload:
    """
    Args:
        provider_uuid (str):
        backend_type (str):
        body (WebhookPayloadRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WebhookPayload
    """

    return (
        await asyncio_detailed(
            provider_uuid=provider_uuid,
            backend_type=backend_type,
            client=client,
            body=body,
        )
    ).parsed
