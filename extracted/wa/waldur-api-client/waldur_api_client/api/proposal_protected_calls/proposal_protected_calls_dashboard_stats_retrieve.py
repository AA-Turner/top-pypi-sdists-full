from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.dashboard_call_manager_stats import DashboardCallManagerStats
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/proposal-protected-calls/dashboard-stats/",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> DashboardCallManagerStats:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = DashboardCallManagerStats.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[DashboardCallManagerStats]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[DashboardCallManagerStats]:
    """Get call manager dashboard stats

     Returns counts for the call manager dashboard: pending assessments, active calls managed by the
    user, and reviews on calls they manage that are due within the next few days.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DashboardCallManagerStats]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> DashboardCallManagerStats:
    """Get call manager dashboard stats

     Returns counts for the call manager dashboard: pending assessments, active calls managed by the
    user, and reviews on calls they manage that are due within the next few days.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DashboardCallManagerStats
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[DashboardCallManagerStats]:
    """Get call manager dashboard stats

     Returns counts for the call manager dashboard: pending assessments, active calls managed by the
    user, and reviews on calls they manage that are due within the next few days.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DashboardCallManagerStats]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> DashboardCallManagerStats:
    """Get call manager dashboard stats

     Returns counts for the call manager dashboard: pending assessments, active calls managed by the
    user, and reviews on calls they manage that are due within the next few days.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DashboardCallManagerStats
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
