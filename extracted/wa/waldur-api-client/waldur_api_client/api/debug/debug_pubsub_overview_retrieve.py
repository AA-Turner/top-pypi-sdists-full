from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.pubsub_overview import PubsubOverview
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/debug/pubsub/overview/",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> PubsubOverview:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = PubsubOverview.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[PubsubOverview]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[PubsubOverview]:
    """Get pubsub system health overview

     Dashboard overview of pubsub system health.

    Combines circuit breaker state, publishing metrics, and health indicators
    into a single response suitable for monitoring dashboards.

    Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PubsubOverview]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> PubsubOverview:
    """Get pubsub system health overview

     Dashboard overview of pubsub system health.

    Combines circuit breaker state, publishing metrics, and health indicators
    into a single response suitable for monitoring dashboards.

    Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PubsubOverview
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[PubsubOverview]:
    """Get pubsub system health overview

     Dashboard overview of pubsub system health.

    Combines circuit breaker state, publishing metrics, and health indicators
    into a single response suitable for monitoring dashboards.

    Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PubsubOverview]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> PubsubOverview:
    """Get pubsub system health overview

     Dashboard overview of pubsub system health.

    Combines circuit breaker state, publishing metrics, and health indicators
    into a single response suitable for monitoring dashboards.

    Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PubsubOverview
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
