from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.database_stats_response import DatabaseStatsResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/database-stats/",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> DatabaseStatsResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = DatabaseStatsResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[DatabaseStatsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[DatabaseStatsResponse]:
    """Get comprehensive database statistics

     Retrieves comprehensive statistics about the PostgreSQL database including:
    - **Table statistics**: Top 10 largest tables by size
    - **Connection statistics**: Active, idle, and waiting connections with utilization
    - **Database size**: Total size, data size, and index size
    - **Cache performance**: Buffer cache and index hit ratios (should be >99%)
    - **Transaction statistics**: Commits, rollbacks, deadlocks
    - **Lock statistics**: Current locks and waiting queries
    - **Maintenance statistics**: Dead tuples, vacuum needs, oldest transaction age
    - **Active queries**: Currently running queries with duration
    - **Query performance**: Sequential vs index scan ratios
    - **Replication status**: WAL size and replication lag (if applicable)

    This information is useful for monitoring, debugging, and performance tuning.
    Requires support user permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatabaseStatsResponse]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> DatabaseStatsResponse:
    """Get comprehensive database statistics

     Retrieves comprehensive statistics about the PostgreSQL database including:
    - **Table statistics**: Top 10 largest tables by size
    - **Connection statistics**: Active, idle, and waiting connections with utilization
    - **Database size**: Total size, data size, and index size
    - **Cache performance**: Buffer cache and index hit ratios (should be >99%)
    - **Transaction statistics**: Commits, rollbacks, deadlocks
    - **Lock statistics**: Current locks and waiting queries
    - **Maintenance statistics**: Dead tuples, vacuum needs, oldest transaction age
    - **Active queries**: Currently running queries with duration
    - **Query performance**: Sequential vs index scan ratios
    - **Replication status**: WAL size and replication lag (if applicable)

    This information is useful for monitoring, debugging, and performance tuning.
    Requires support user permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatabaseStatsResponse
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[DatabaseStatsResponse]:
    """Get comprehensive database statistics

     Retrieves comprehensive statistics about the PostgreSQL database including:
    - **Table statistics**: Top 10 largest tables by size
    - **Connection statistics**: Active, idle, and waiting connections with utilization
    - **Database size**: Total size, data size, and index size
    - **Cache performance**: Buffer cache and index hit ratios (should be >99%)
    - **Transaction statistics**: Commits, rollbacks, deadlocks
    - **Lock statistics**: Current locks and waiting queries
    - **Maintenance statistics**: Dead tuples, vacuum needs, oldest transaction age
    - **Active queries**: Currently running queries with duration
    - **Query performance**: Sequential vs index scan ratios
    - **Replication status**: WAL size and replication lag (if applicable)

    This information is useful for monitoring, debugging, and performance tuning.
    Requires support user permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatabaseStatsResponse]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> DatabaseStatsResponse:
    """Get comprehensive database statistics

     Retrieves comprehensive statistics about the PostgreSQL database including:
    - **Table statistics**: Top 10 largest tables by size
    - **Connection statistics**: Active, idle, and waiting connections with utilization
    - **Database size**: Total size, data size, and index size
    - **Cache performance**: Buffer cache and index hit ratios (should be >99%)
    - **Transaction statistics**: Commits, rollbacks, deadlocks
    - **Lock statistics**: Current locks and waiting queries
    - **Maintenance statistics**: Dead tuples, vacuum needs, oldest transaction age
    - **Active queries**: Currently running queries with duration
    - **Query performance**: Sequential vs index scan ratios
    - **Replication status**: WAL size and replication lag (if applicable)

    This information is useful for monitoring, debugging, and performance tuning.
    Requires support user permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatabaseStatsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
