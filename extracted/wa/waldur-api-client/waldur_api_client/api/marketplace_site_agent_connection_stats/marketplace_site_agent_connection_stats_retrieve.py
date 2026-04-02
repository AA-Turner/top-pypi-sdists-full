from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agent_connection_stats_response import AgentConnectionStatsResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/marketplace-site-agent-connection-stats/",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[AgentConnectionStatsResponse, Any]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = AgentConnectionStatsResponse.from_dict(response.json())

        return response_200
    if response.status_code == 503:
        response_503 = response.json()
        return response_503
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[AgentConnectionStatsResponse, Any]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[AgentConnectionStatsResponse, Any]]:
    """Get agent connection statistics

     Returns connection status for all registered agents.

    For each agent identity, provides:
    - Agent metadata (name, version, offering)
    - Services and their states
    - Event subscriptions with RabbitMQ connection status
    - RabbitMQ queues associated with the agent's offering

    The RMQ connection data includes:
    - Whether the agent is currently connected
    - Connection source IP, timestamp, and state
    - Traffic statistics (bytes sent/received)

    Requires support user permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AgentConnectionStatsResponse, Any]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Union[AgentConnectionStatsResponse, Any]:
    """Get agent connection statistics

     Returns connection status for all registered agents.

    For each agent identity, provides:
    - Agent metadata (name, version, offering)
    - Services and their states
    - Event subscriptions with RabbitMQ connection status
    - RabbitMQ queues associated with the agent's offering

    The RMQ connection data includes:
    - Whether the agent is currently connected
    - Connection source IP, timestamp, and state
    - Traffic statistics (bytes sent/received)

    Requires support user permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AgentConnectionStatsResponse, Any]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[AgentConnectionStatsResponse, Any]]:
    """Get agent connection statistics

     Returns connection status for all registered agents.

    For each agent identity, provides:
    - Agent metadata (name, version, offering)
    - Services and their states
    - Event subscriptions with RabbitMQ connection status
    - RabbitMQ queues associated with the agent's offering

    The RMQ connection data includes:
    - Whether the agent is currently connected
    - Connection source IP, timestamp, and state
    - Traffic statistics (bytes sent/received)

    Requires support user permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AgentConnectionStatsResponse, Any]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Union[AgentConnectionStatsResponse, Any]:
    """Get agent connection statistics

     Returns connection status for all registered agents.

    For each agent identity, provides:
    - Agent metadata (name, version, offering)
    - Services and their states
    - Event subscriptions with RabbitMQ connection status
    - RabbitMQ queues associated with the agent's offering

    The RMQ connection data includes:
    - Whether the agent is currently connected
    - Connection source IP, timestamp, and state
    - Traffic statistics (bytes sent/received)

    Requires support user permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AgentConnectionStatsResponse, Any]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
