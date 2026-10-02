from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.components_usage_stats import ComponentsUsageStats
from ...types import UNSET, Response, Unset


def _get_kwargs(
    uuid: UUID,
    *,
    for_current_month: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["for_current_month"] = for_current_month

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/openportal-unmanaged-projects/{uuid}/stats/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ComponentsUsageStats:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ComponentsUsageStats.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ComponentsUsageStats]:
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
    for_current_month: Union[Unset, bool] = UNSET,
) -> Response[ComponentsUsageStats]:
    """Get project resource usage statistics

     Provides statistics about the resource usage (e.g., CPU, RAM, storage) for all resources within a
    project. Can be filtered to show usage for the current month only.

    Args:
        uuid (UUID):
        for_current_month (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ComponentsUsageStats]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        for_current_month=for_current_month,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    for_current_month: Union[Unset, bool] = UNSET,
) -> ComponentsUsageStats:
    """Get project resource usage statistics

     Provides statistics about the resource usage (e.g., CPU, RAM, storage) for all resources within a
    project. Can be filtered to show usage for the current month only.

    Args:
        uuid (UUID):
        for_current_month (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ComponentsUsageStats
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        for_current_month=for_current_month,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    for_current_month: Union[Unset, bool] = UNSET,
) -> Response[ComponentsUsageStats]:
    """Get project resource usage statistics

     Provides statistics about the resource usage (e.g., CPU, RAM, storage) for all resources within a
    project. Can be filtered to show usage for the current month only.

    Args:
        uuid (UUID):
        for_current_month (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ComponentsUsageStats]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        for_current_month=for_current_month,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    for_current_month: Union[Unset, bool] = UNSET,
) -> ComponentsUsageStats:
    """Get project resource usage statistics

     Provides statistics about the resource usage (e.g., CPU, RAM, storage) for all resources within a
    project. Can be filtered to show usage for the current month only.

    Args:
        uuid (UUID):
        for_current_month (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ComponentsUsageStats
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            for_current_month=for_current_month,
        )
    ).parsed
