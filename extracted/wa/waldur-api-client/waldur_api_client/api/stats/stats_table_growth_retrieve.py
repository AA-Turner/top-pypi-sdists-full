from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.table_growth_stats_response import TableGrowthStatsResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/stats/table-growth/",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> TableGrowthStatsResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = TableGrowthStatsResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[TableGrowthStatsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[TableGrowthStatsResponse]:
    """Get table growth statistics

     Retrieves historical table growth statistics for detecting abnormal patterns.

    This endpoint returns:
    - **date**: Current date of the statistics
    - **weekly_threshold_percent**: Configured alert threshold for weekly growth
    - **monthly_threshold_percent**: Configured alert threshold for monthly growth
    - **tables**: List of tables with their growth statistics, sorted by growth rate

    Each table entry includes:
    - Current size and row estimates
    - Size and row estimates from 7 days ago
    - Size and row estimates from 30 days ago
    - Weekly and monthly growth percentages

    Use this data to identify tables that may be experiencing abnormal growth,
    which could indicate bugs like the version-based get_or_create issue.

    Query parameters:
    - **table_name** (optional): Filter to a specific table name
    - **days** (optional, default 30): Number of days of history to include

    Requires support user permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TableGrowthStatsResponse]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> TableGrowthStatsResponse:
    """Get table growth statistics

     Retrieves historical table growth statistics for detecting abnormal patterns.

    This endpoint returns:
    - **date**: Current date of the statistics
    - **weekly_threshold_percent**: Configured alert threshold for weekly growth
    - **monthly_threshold_percent**: Configured alert threshold for monthly growth
    - **tables**: List of tables with their growth statistics, sorted by growth rate

    Each table entry includes:
    - Current size and row estimates
    - Size and row estimates from 7 days ago
    - Size and row estimates from 30 days ago
    - Weekly and monthly growth percentages

    Use this data to identify tables that may be experiencing abnormal growth,
    which could indicate bugs like the version-based get_or_create issue.

    Query parameters:
    - **table_name** (optional): Filter to a specific table name
    - **days** (optional, default 30): Number of days of history to include

    Requires support user permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TableGrowthStatsResponse
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[TableGrowthStatsResponse]:
    """Get table growth statistics

     Retrieves historical table growth statistics for detecting abnormal patterns.

    This endpoint returns:
    - **date**: Current date of the statistics
    - **weekly_threshold_percent**: Configured alert threshold for weekly growth
    - **monthly_threshold_percent**: Configured alert threshold for monthly growth
    - **tables**: List of tables with their growth statistics, sorted by growth rate

    Each table entry includes:
    - Current size and row estimates
    - Size and row estimates from 7 days ago
    - Size and row estimates from 30 days ago
    - Weekly and monthly growth percentages

    Use this data to identify tables that may be experiencing abnormal growth,
    which could indicate bugs like the version-based get_or_create issue.

    Query parameters:
    - **table_name** (optional): Filter to a specific table name
    - **days** (optional, default 30): Number of days of history to include

    Requires support user permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TableGrowthStatsResponse]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> TableGrowthStatsResponse:
    """Get table growth statistics

     Retrieves historical table growth statistics for detecting abnormal patterns.

    This endpoint returns:
    - **date**: Current date of the statistics
    - **weekly_threshold_percent**: Configured alert threshold for weekly growth
    - **monthly_threshold_percent**: Configured alert threshold for monthly growth
    - **tables**: List of tables with their growth statistics, sorted by growth rate

    Each table entry includes:
    - Current size and row estimates
    - Size and row estimates from 7 days ago
    - Size and row estimates from 30 days ago
    - Weekly and monthly growth percentages

    Use this data to identify tables that may be experiencing abnormal growth,
    which could indicate bugs like the version-based get_or_create issue.

    Query parameters:
    - **table_name** (optional): Filter to a specific table name
    - **days** (optional, default 30): Number of days of history to include

    Requires support user permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TableGrowthStatsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
