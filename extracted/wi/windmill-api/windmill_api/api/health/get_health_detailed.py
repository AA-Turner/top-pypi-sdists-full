from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_health_detailed_response_200 import GetHealthDetailedResponse200
from ...models.get_health_detailed_response_503 import GetHealthDetailedResponse503
from ...types import Response


def _get_kwargs() -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/health/detailed",
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetHealthDetailedResponse200, GetHealthDetailedResponse503]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetHealthDetailedResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
        response_503 = GetHealthDetailedResponse503.from_dict(response.json())

        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[GetHealthDetailedResponse200, GetHealthDetailedResponse503]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[GetHealthDetailedResponse200, GetHealthDetailedResponse503]]:
    """detailed health status

     Returns detailed health information including database pool stats, worker details, and queue status.
    Requires authentication. Use for monitoring dashboards and debugging.
    This endpoint always returns fresh data (no caching).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetHealthDetailedResponse200, GetHealthDetailedResponse503]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[GetHealthDetailedResponse200, GetHealthDetailedResponse503]]:
    """detailed health status

     Returns detailed health information including database pool stats, worker details, and queue status.
    Requires authentication. Use for monitoring dashboards and debugging.
    This endpoint always returns fresh data (no caching).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetHealthDetailedResponse200, GetHealthDetailedResponse503]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[GetHealthDetailedResponse200, GetHealthDetailedResponse503]]:
    """detailed health status

     Returns detailed health information including database pool stats, worker details, and queue status.
    Requires authentication. Use for monitoring dashboards and debugging.
    This endpoint always returns fresh data (no caching).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetHealthDetailedResponse200, GetHealthDetailedResponse503]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[GetHealthDetailedResponse200, GetHealthDetailedResponse503]]:
    """detailed health status

     Returns detailed health information including database pool stats, worker details, and queue status.
    Requires authentication. Use for monitoring dashboards and debugging.
    This endpoint always returns fresh data (no caching).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetHealthDetailedResponse200, GetHealthDetailedResponse503]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
