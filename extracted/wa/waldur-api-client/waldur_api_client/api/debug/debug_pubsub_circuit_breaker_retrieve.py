from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.circuit_breaker_status import CircuitBreakerStatus
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/debug/pubsub/circuit_breaker/",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> CircuitBreakerStatus:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = CircuitBreakerStatus.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CircuitBreakerStatus]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[CircuitBreakerStatus]:
    """Get circuit breaker state

     Get current STOMP circuit breaker state and statistics.

    Returns:
    - state: Current state (closed/open/half_open)
    - failure_count: Number of consecutive failures
    - success_count: Successes since last state change
    - last_failure_time: Timestamp of last failure
    - last_state_change: When state last changed
    - config: Circuit breaker configuration
    - state_history: Recent state transitions

    Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CircuitBreakerStatus]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> CircuitBreakerStatus:
    """Get circuit breaker state

     Get current STOMP circuit breaker state and statistics.

    Returns:
    - state: Current state (closed/open/half_open)
    - failure_count: Number of consecutive failures
    - success_count: Successes since last state change
    - last_failure_time: Timestamp of last failure
    - last_state_change: When state last changed
    - config: Circuit breaker configuration
    - state_history: Recent state transitions

    Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CircuitBreakerStatus
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[CircuitBreakerStatus]:
    """Get circuit breaker state

     Get current STOMP circuit breaker state and statistics.

    Returns:
    - state: Current state (closed/open/half_open)
    - failure_count: Number of consecutive failures
    - success_count: Successes since last state change
    - last_failure_time: Timestamp of last failure
    - last_state_change: When state last changed
    - config: Circuit breaker configuration
    - state_history: Recent state transitions

    Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CircuitBreakerStatus]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> CircuitBreakerStatus:
    """Get circuit breaker state

     Get current STOMP circuit breaker state and statistics.

    Returns:
    - state: Current state (closed/open/half_open)
    - failure_count: Number of consecutive failures
    - success_count: Successes since last state change
    - last_failure_time: Timestamp of last failure
    - last_state_change: When state last changed
    - config: Circuit breaker configuration
    - state_history: Recent state transitions

    Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CircuitBreakerStatus
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
