from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.dashboard_general_stats import DashboardGeneralStats
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/users/dashboard-general-stats/",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> DashboardGeneralStats:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = DashboardGeneralStats.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[DashboardGeneralStats]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[DashboardGeneralStats]:
    """Get general dashboard stats

     Returns counts shown on the general dashboard for the current user: pending permission requests they
    can act on, active invitations addressed to them, and their pending onboarding applications.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DashboardGeneralStats]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> DashboardGeneralStats:
    """Get general dashboard stats

     Returns counts shown on the general dashboard for the current user: pending permission requests they
    can act on, active invitations addressed to them, and their pending onboarding applications.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DashboardGeneralStats
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[DashboardGeneralStats]:
    """Get general dashboard stats

     Returns counts shown on the general dashboard for the current user: pending permission requests they
    can act on, active invitations addressed to them, and their pending onboarding applications.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DashboardGeneralStats]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> DashboardGeneralStats:
    """Get general dashboard stats

     Returns counts shown on the general dashboard for the current user: pending permission requests they
    can act on, active invitations addressed to them, and their pending onboarding applications.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DashboardGeneralStats
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
