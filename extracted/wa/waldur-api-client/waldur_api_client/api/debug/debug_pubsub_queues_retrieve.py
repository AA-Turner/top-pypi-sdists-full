from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.event_subscription_queues_overview import EventSubscriptionQueuesOverview
from ...models.rmq_stats_error import RmqStatsError
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/debug/pubsub/queues/",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[EventSubscriptionQueuesOverview, RmqStatsError]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = EventSubscriptionQueuesOverview.from_dict(response.json())

        return response_200
    if response.status_code == 503:
        response_503 = RmqStatsError.from_dict(response.json())

        return response_503
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[EventSubscriptionQueuesOverview, RmqStatsError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[EventSubscriptionQueuesOverview, RmqStatsError]]:
    """Get subscription queues overview

     Get overview of subscription queues from RabbitMQ.

    Returns summary of subscription queues across all vhosts including
    message counts and queue statistics.

    Note: For detailed queue management, use /api/rabbitmq-stats/ endpoint.

    Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[EventSubscriptionQueuesOverview, RmqStatsError]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Union[EventSubscriptionQueuesOverview, RmqStatsError]:
    """Get subscription queues overview

     Get overview of subscription queues from RabbitMQ.

    Returns summary of subscription queues across all vhosts including
    message counts and queue statistics.

    Note: For detailed queue management, use /api/rabbitmq-stats/ endpoint.

    Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[EventSubscriptionQueuesOverview, RmqStatsError]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[EventSubscriptionQueuesOverview, RmqStatsError]]:
    """Get subscription queues overview

     Get overview of subscription queues from RabbitMQ.

    Returns summary of subscription queues across all vhosts including
    message counts and queue statistics.

    Note: For detailed queue management, use /api/rabbitmq-stats/ endpoint.

    Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[EventSubscriptionQueuesOverview, RmqStatsError]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Union[EventSubscriptionQueuesOverview, RmqStatsError]:
    """Get subscription queues overview

     Get overview of subscription queues from RabbitMQ.

    Returns summary of subscription queues across all vhosts including
    message counts and queue statistics.

    Note: For detailed queue management, use /api/rabbitmq-stats/ endpoint.

    Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[EventSubscriptionQueuesOverview, RmqStatsError]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
