from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.components_usage_stats_per_offering import ComponentsUsageStatsPerOffering
from ...types import Response


def _get_kwargs(
    uuid: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/customers/{uuid}/components-usage/",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> ComponentsUsageStatsPerOffering:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ComponentsUsageStatsPerOffering.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ComponentsUsageStatsPerOffering]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[ComponentsUsageStatsPerOffering]:
    """Get customer resource usage statistics broken down per offering

     Returns one row per (offering, component type, billing type) for all non-terminated resources within
    the customer. Each row's `usage` and `limit_usage` are aggregated using the offering's own
    `limit_period`, so quarterly offerings report quarter-to-date, yearly report year-to-date, total
    report lifetime, and monthly report current month. Each row also includes the resolved current
    period bounds (`current_period_label`, `current_period_start`, `current_period_end`).

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ComponentsUsageStatsPerOffering]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> ComponentsUsageStatsPerOffering:
    """Get customer resource usage statistics broken down per offering

     Returns one row per (offering, component type, billing type) for all non-terminated resources within
    the customer. Each row's `usage` and `limit_usage` are aggregated using the offering's own
    `limit_period`, so quarterly offerings report quarter-to-date, yearly report year-to-date, total
    report lifetime, and monthly report current month. Each row also includes the resolved current
    period bounds (`current_period_label`, `current_period_start`, `current_period_end`).

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ComponentsUsageStatsPerOffering
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[ComponentsUsageStatsPerOffering]:
    """Get customer resource usage statistics broken down per offering

     Returns one row per (offering, component type, billing type) for all non-terminated resources within
    the customer. Each row's `usage` and `limit_usage` are aggregated using the offering's own
    `limit_period`, so quarterly offerings report quarter-to-date, yearly report year-to-date, total
    report lifetime, and monthly report current month. Each row also includes the resolved current
    period bounds (`current_period_label`, `current_period_start`, `current_period_end`).

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ComponentsUsageStatsPerOffering]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> ComponentsUsageStatsPerOffering:
    """Get customer resource usage statistics broken down per offering

     Returns one row per (offering, component type, billing type) for all non-terminated resources within
    the customer. Each row's `usage` and `limit_usage` are aggregated using the offering's own
    `limit_period`, so quarterly offerings report quarter-to-date, yearly report year-to-date, total
    report lifetime, and monthly report current month. Each row also includes the resolved current
    period bounds (`current_period_label`, `current_period_start`, `current_period_end`).

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ComponentsUsageStatsPerOffering
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
        )
    ).parsed
