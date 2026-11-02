from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_health_status_response_200 import GetHealthStatusResponse200
from ...models.get_health_status_response_503 import GetHealthStatusResponse503
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    force: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["force"] = force

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/health/status",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetHealthStatusResponse200, GetHealthStatusResponse503]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetHealthStatusResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
        response_503 = GetHealthStatusResponse503.from_dict(response.json())

        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[GetHealthStatusResponse200, GetHealthStatusResponse503]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    force: Union[Unset, None, bool] = False,
) -> Response[Union[GetHealthStatusResponse200, GetHealthStatusResponse503]]:
    """health status

     Health status endpoint. Returns cached health status (database connectivity, worker count).
    Cache TTL is fixed at 5 seconds. Use force=true query parameter to bypass cache.
    Note: This endpoint is intentionally different from Kubernetes probes to avoid confusion.
    For k8s liveness/readiness probes, use /version endpoint.

    Args:
        force (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetHealthStatusResponse200, GetHealthStatusResponse503]]
    """

    kwargs = _get_kwargs(
        force=force,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    force: Union[Unset, None, bool] = False,
) -> Optional[Union[GetHealthStatusResponse200, GetHealthStatusResponse503]]:
    """health status

     Health status endpoint. Returns cached health status (database connectivity, worker count).
    Cache TTL is fixed at 5 seconds. Use force=true query parameter to bypass cache.
    Note: This endpoint is intentionally different from Kubernetes probes to avoid confusion.
    For k8s liveness/readiness probes, use /version endpoint.

    Args:
        force (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetHealthStatusResponse200, GetHealthStatusResponse503]
    """

    return sync_detailed(
        client=client,
        force=force,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    force: Union[Unset, None, bool] = False,
) -> Response[Union[GetHealthStatusResponse200, GetHealthStatusResponse503]]:
    """health status

     Health status endpoint. Returns cached health status (database connectivity, worker count).
    Cache TTL is fixed at 5 seconds. Use force=true query parameter to bypass cache.
    Note: This endpoint is intentionally different from Kubernetes probes to avoid confusion.
    For k8s liveness/readiness probes, use /version endpoint.

    Args:
        force (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetHealthStatusResponse200, GetHealthStatusResponse503]]
    """

    kwargs = _get_kwargs(
        force=force,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    force: Union[Unset, None, bool] = False,
) -> Optional[Union[GetHealthStatusResponse200, GetHealthStatusResponse503]]:
    """health status

     Health status endpoint. Returns cached health status (database connectivity, worker count).
    Cache TTL is fixed at 5 seconds. Use force=true query parameter to bypass cache.
    Note: This endpoint is intentionally different from Kubernetes probes to avoid confusion.
    For k8s liveness/readiness probes, use /version endpoint.

    Args:
        force (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetHealthStatusResponse200, GetHealthStatusResponse503]
    """

    return (
        await asyncio_detailed(
            client=client,
            force=force,
        )
    ).parsed
