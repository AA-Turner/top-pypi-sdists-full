from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.dead_letter_queue import DeadLetterQueue
from ...models.rmq_stats_error import RmqStatsError
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/debug/pubsub/dead_letter_queue/",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[DeadLetterQueue, RmqStatsError]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = DeadLetterQueue.from_dict(response.json())

        return response_200
    if response.status_code == 503:
        response_503 = RmqStatsError.from_dict(response.json())

        return response_503
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[DeadLetterQueue, RmqStatsError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[DeadLetterQueue, RmqStatsError]]:
    """Get dead letter queue status

     Get dead letter queue (DLQ) statistics.

    The DLQ receives messages that failed to be delivered to their original
    destination. This endpoint shows the current DLQ status.

    Note: DLQ is configured per-vhost. This endpoint checks all vhosts
    for queues with 'dlq' in the name.

    Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeadLetterQueue, RmqStatsError]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Union[DeadLetterQueue, RmqStatsError]:
    """Get dead letter queue status

     Get dead letter queue (DLQ) statistics.

    The DLQ receives messages that failed to be delivered to their original
    destination. This endpoint shows the current DLQ status.

    Note: DLQ is configured per-vhost. This endpoint checks all vhosts
    for queues with 'dlq' in the name.

    Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeadLetterQueue, RmqStatsError]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[DeadLetterQueue, RmqStatsError]]:
    """Get dead letter queue status

     Get dead letter queue (DLQ) statistics.

    The DLQ receives messages that failed to be delivered to their original
    destination. This endpoint shows the current DLQ status.

    Note: DLQ is configured per-vhost. This endpoint checks all vhosts
    for queues with 'dlq' in the name.

    Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeadLetterQueue, RmqStatsError]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Union[DeadLetterQueue, RmqStatsError]:
    """Get dead letter queue status

     Get dead letter queue (DLQ) statistics.

    The DLQ receives messages that failed to be delivered to their original
    destination. This endpoint shows the current DLQ status.

    Note: DLQ is configured per-vhost. This endpoint checks all vhosts
    for queues with 'dlq' in the name.

    Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeadLetterQueue, RmqStatsError]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
