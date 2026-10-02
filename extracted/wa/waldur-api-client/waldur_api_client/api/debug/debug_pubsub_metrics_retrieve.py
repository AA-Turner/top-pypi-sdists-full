from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.publishing_metrics import PublishingMetrics
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/debug/pubsub/metrics/",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> PublishingMetrics:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = PublishingMetrics.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[PublishingMetrics]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[PublishingMetrics]:
    """Get publishing metrics

     Get message publishing metrics and statistics.

    Returns:
    - messages_sent: Total messages successfully sent
    - messages_failed: Total failed message attempts
    - messages_retried: Messages that required retry
    - messages_skipped: Messages skipped due to circuit breaker
    - circuit_breaker_trips: Number of times circuit opened
    - rate_limiter_rejections: Messages rejected by rate limiter
    - avg_publish_time_ms: Average publish latency
    - last_publish_time: Timestamp of last publish attempt

    Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PublishingMetrics]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> PublishingMetrics:
    """Get publishing metrics

     Get message publishing metrics and statistics.

    Returns:
    - messages_sent: Total messages successfully sent
    - messages_failed: Total failed message attempts
    - messages_retried: Messages that required retry
    - messages_skipped: Messages skipped due to circuit breaker
    - circuit_breaker_trips: Number of times circuit opened
    - rate_limiter_rejections: Messages rejected by rate limiter
    - avg_publish_time_ms: Average publish latency
    - last_publish_time: Timestamp of last publish attempt

    Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PublishingMetrics
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[PublishingMetrics]:
    """Get publishing metrics

     Get message publishing metrics and statistics.

    Returns:
    - messages_sent: Total messages successfully sent
    - messages_failed: Total failed message attempts
    - messages_retried: Messages that required retry
    - messages_skipped: Messages skipped due to circuit breaker
    - circuit_breaker_trips: Number of times circuit opened
    - rate_limiter_rejections: Messages rejected by rate limiter
    - avg_publish_time_ms: Average publish latency
    - last_publish_time: Timestamp of last publish attempt

    Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PublishingMetrics]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> PublishingMetrics:
    """Get publishing metrics

     Get message publishing metrics and statistics.

    Returns:
    - messages_sent: Total messages successfully sent
    - messages_failed: Total failed message attempts
    - messages_retried: Messages that required retry
    - messages_skipped: Messages skipped due to circuit breaker
    - circuit_breaker_trips: Number of times circuit opened
    - rate_limiter_rejections: Messages rejected by rate limiter
    - avg_publish_time_ms: Average publish latency
    - last_publish_time: Timestamp of last publish attempt

    Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PublishingMetrics
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
