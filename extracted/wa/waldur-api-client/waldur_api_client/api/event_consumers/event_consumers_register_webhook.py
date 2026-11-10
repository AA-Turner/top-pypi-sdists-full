from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.event_consumer import EventConsumer
from ...models.event_consumer_webhook_request import EventConsumerWebhookRequest
from ...types import Response


def _get_kwargs(
    *,
    body: EventConsumerWebhookRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/event-consumers/register_webhook/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> EventConsumer:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 201:
        response_201 = EventConsumer.from_dict(response.json())

        return response_201
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[EventConsumer]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: EventConsumerWebhookRequest,
) -> Response[EventConsumer]:
    """Create a webhook event consumer: the same messages a queue consumer receives are POSTed as JSON to
    `webhook_url` instead. Staff only. An EMPTY `scopes` list makes it global (all events, including
    all-user PII). Use `payload_filters` to narrow delivery, e.g. to one role, and `resync` to send the
    current state once.

    Args:
        body (EventConsumerWebhookRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EventConsumer]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: EventConsumerWebhookRequest,
) -> EventConsumer:
    """Create a webhook event consumer: the same messages a queue consumer receives are POSTed as JSON to
    `webhook_url` instead. Staff only. An EMPTY `scopes` list makes it global (all events, including
    all-user PII). Use `payload_filters` to narrow delivery, e.g. to one role, and `resync` to send the
    current state once.

    Args:
        body (EventConsumerWebhookRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EventConsumer
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: EventConsumerWebhookRequest,
) -> Response[EventConsumer]:
    """Create a webhook event consumer: the same messages a queue consumer receives are POSTed as JSON to
    `webhook_url` instead. Staff only. An EMPTY `scopes` list makes it global (all events, including
    all-user PII). Use `payload_filters` to narrow delivery, e.g. to one role, and `resync` to send the
    current state once.

    Args:
        body (EventConsumerWebhookRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EventConsumer]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: EventConsumerWebhookRequest,
) -> EventConsumer:
    """Create a webhook event consumer: the same messages a queue consumer receives are POSTed as JSON to
    `webhook_url` instead. Staff only. An EMPTY `scopes` list makes it global (all events, including
    all-user PII). Use `payload_filters` to narrow delivery, e.g. to one role, and `resync` to send the
    current state once.

    Args:
        body (EventConsumerWebhookRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EventConsumer
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
