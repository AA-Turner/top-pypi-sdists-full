from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.rmq_purge_request_request import RmqPurgeRequestRequest
from ...models.rmq_purge_response import RmqPurgeResponse
from ...models.rmq_stats_error import RmqStatsError
from ...types import Response


def _get_kwargs(
    *,
    body: RmqPurgeRequestRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/rabbitmq-stats/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[RmqPurgeResponse, RmqStatsError]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = RmqPurgeResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = RmqStatsError.from_dict(response.json())

        return response_400
    if response.status_code == 404:
        response_404 = RmqStatsError.from_dict(response.json())

        return response_404
    if response.status_code == 503:
        response_503 = RmqStatsError.from_dict(response.json())

        return response_503
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[RmqPurgeResponse, RmqStatsError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: RmqPurgeRequestRequest,
) -> Response[Union[RmqPurgeResponse, RmqStatsError]]:
    """Purge or delete RabbitMQ subscription queues

     Purges messages from or deletes specified RabbitMQ subscription queues.

    **Purge operations** (remove messages, keep queue):
    - `vhost` and `queue_name`: Purge a specific queue
    - `vhost` and `queue_pattern`: Purge queues matching pattern (e.g., '*_resource')
    - `purge_all_subscription_queues`: Purge all subscription queues across all vhosts

    **Delete operations** (remove queue entirely):
    - `vhost`, `queue_name`, and `delete_queue=true`: Delete a specific queue
    - `vhost`, `queue_pattern`, and `delete_queue=true`: Delete queues matching pattern
    - `delete_all_subscription_queues`: Delete all subscription queues across all vhosts

    Requires staff permissions (more restrictive than viewing).

    Args:
        body (RmqPurgeRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[RmqPurgeResponse, RmqStatsError]]
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
    body: RmqPurgeRequestRequest,
) -> Union[RmqPurgeResponse, RmqStatsError]:
    """Purge or delete RabbitMQ subscription queues

     Purges messages from or deletes specified RabbitMQ subscription queues.

    **Purge operations** (remove messages, keep queue):
    - `vhost` and `queue_name`: Purge a specific queue
    - `vhost` and `queue_pattern`: Purge queues matching pattern (e.g., '*_resource')
    - `purge_all_subscription_queues`: Purge all subscription queues across all vhosts

    **Delete operations** (remove queue entirely):
    - `vhost`, `queue_name`, and `delete_queue=true`: Delete a specific queue
    - `vhost`, `queue_pattern`, and `delete_queue=true`: Delete queues matching pattern
    - `delete_all_subscription_queues`: Delete all subscription queues across all vhosts

    Requires staff permissions (more restrictive than viewing).

    Args:
        body (RmqPurgeRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[RmqPurgeResponse, RmqStatsError]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: RmqPurgeRequestRequest,
) -> Response[Union[RmqPurgeResponse, RmqStatsError]]:
    """Purge or delete RabbitMQ subscription queues

     Purges messages from or deletes specified RabbitMQ subscription queues.

    **Purge operations** (remove messages, keep queue):
    - `vhost` and `queue_name`: Purge a specific queue
    - `vhost` and `queue_pattern`: Purge queues matching pattern (e.g., '*_resource')
    - `purge_all_subscription_queues`: Purge all subscription queues across all vhosts

    **Delete operations** (remove queue entirely):
    - `vhost`, `queue_name`, and `delete_queue=true`: Delete a specific queue
    - `vhost`, `queue_pattern`, and `delete_queue=true`: Delete queues matching pattern
    - `delete_all_subscription_queues`: Delete all subscription queues across all vhosts

    Requires staff permissions (more restrictive than viewing).

    Args:
        body (RmqPurgeRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[RmqPurgeResponse, RmqStatsError]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: RmqPurgeRequestRequest,
) -> Union[RmqPurgeResponse, RmqStatsError]:
    """Purge or delete RabbitMQ subscription queues

     Purges messages from or deletes specified RabbitMQ subscription queues.

    **Purge operations** (remove messages, keep queue):
    - `vhost` and `queue_name`: Purge a specific queue
    - `vhost` and `queue_pattern`: Purge queues matching pattern (e.g., '*_resource')
    - `purge_all_subscription_queues`: Purge all subscription queues across all vhosts

    **Delete operations** (remove queue entirely):
    - `vhost`, `queue_name`, and `delete_queue=true`: Delete a specific queue
    - `vhost`, `queue_pattern`, and `delete_queue=true`: Delete queues matching pattern
    - `delete_all_subscription_queues`: Delete all subscription queues across all vhosts

    Requires staff permissions (more restrictive than viewing).

    Args:
        body (RmqPurgeRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[RmqPurgeResponse, RmqStatsError]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
