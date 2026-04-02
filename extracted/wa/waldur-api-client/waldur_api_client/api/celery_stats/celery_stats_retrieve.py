from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.celery_stats_response import CeleryStatsResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/celery-stats/",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> CeleryStatsResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = CeleryStatsResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CeleryStatsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[CeleryStatsResponse]:
    """Get Celery worker statistics

     Provides a comprehensive snapshot of all Celery workers' status.

    This endpoint returns detailed information about:
    - **active**: Tasks currently being executed by workers
    - **scheduled**: Tasks scheduled for future execution (with ETA)
    - **reserved**: Tasks received by workers but not yet started
    - **revoked**: Task IDs that have been cancelled/revoked
    - **query_task**: Results of task queries (if any)
    - **stats**: Detailed worker statistics including uptime, pool info, and broker connection

    Each field is a dictionary where keys are worker names (e.g., 'celery@hostname').
    If no workers are available, fields will be `null`.

    Requires support user permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CeleryStatsResponse]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> CeleryStatsResponse:
    """Get Celery worker statistics

     Provides a comprehensive snapshot of all Celery workers' status.

    This endpoint returns detailed information about:
    - **active**: Tasks currently being executed by workers
    - **scheduled**: Tasks scheduled for future execution (with ETA)
    - **reserved**: Tasks received by workers but not yet started
    - **revoked**: Task IDs that have been cancelled/revoked
    - **query_task**: Results of task queries (if any)
    - **stats**: Detailed worker statistics including uptime, pool info, and broker connection

    Each field is a dictionary where keys are worker names (e.g., 'celery@hostname').
    If no workers are available, fields will be `null`.

    Requires support user permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CeleryStatsResponse
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[CeleryStatsResponse]:
    """Get Celery worker statistics

     Provides a comprehensive snapshot of all Celery workers' status.

    This endpoint returns detailed information about:
    - **active**: Tasks currently being executed by workers
    - **scheduled**: Tasks scheduled for future execution (with ETA)
    - **reserved**: Tasks received by workers but not yet started
    - **revoked**: Task IDs that have been cancelled/revoked
    - **query_task**: Results of task queries (if any)
    - **stats**: Detailed worker statistics including uptime, pool info, and broker connection

    Each field is a dictionary where keys are worker names (e.g., 'celery@hostname').
    If no workers are available, fields will be `null`.

    Requires support user permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CeleryStatsResponse]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> CeleryStatsResponse:
    """Get Celery worker statistics

     Provides a comprehensive snapshot of all Celery workers' status.

    This endpoint returns detailed information about:
    - **active**: Tasks currently being executed by workers
    - **scheduled**: Tasks scheduled for future execution (with ETA)
    - **reserved**: Tasks received by workers but not yet started
    - **revoked**: Task IDs that have been cancelled/revoked
    - **query_task**: Results of task queries (if any)
    - **stats**: Detailed worker statistics including uptime, pool info, and broker connection

    Each field is a dictionary where keys are worker names (e.g., 'celery@hostname').
    If no workers are available, fields will be `null`.

    Requires support user permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CeleryStatsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
