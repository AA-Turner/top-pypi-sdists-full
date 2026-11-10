from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.event_consumer import EventConsumer
from ...models.event_consumer_webhook_update_request import EventConsumerWebhookUpdateRequest
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: EventConsumerWebhookUpdateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/event-consumers/{uuid}/update_webhook/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> EventConsumer:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = EventConsumer.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[EventConsumer]:
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
    body: EventConsumerWebhookUpdateRequest,
) -> Response[EventConsumer]:
    """Change a webhook consumer's destination URL, object types or payload filters. Staff only. Omitted
    fields are left unchanged.

    Args:
        uuid (UUID):
        body (EventConsumerWebhookUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EventConsumer]
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
    body: EventConsumerWebhookUpdateRequest,
) -> EventConsumer:
    """Change a webhook consumer's destination URL, object types or payload filters. Staff only. Omitted
    fields are left unchanged.

    Args:
        uuid (UUID):
        body (EventConsumerWebhookUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EventConsumer
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
    body: EventConsumerWebhookUpdateRequest,
) -> Response[EventConsumer]:
    """Change a webhook consumer's destination URL, object types or payload filters. Staff only. Omitted
    fields are left unchanged.

    Args:
        uuid (UUID):
        body (EventConsumerWebhookUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EventConsumer]
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
    body: EventConsumerWebhookUpdateRequest,
) -> EventConsumer:
    """Change a webhook consumer's destination URL, object types or payload filters. Staff only. Omitted
    fields are left unchanged.

    Args:
        uuid (UUID):
        body (EventConsumerWebhookUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EventConsumer
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
