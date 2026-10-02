from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.hypervisor_summary import HypervisorSummary
from ...types import UNSET, Response


def _get_kwargs(
    *,
    settings_uuid: UUID,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_settings_uuid = str(settings_uuid)
    params["settings_uuid"] = json_settings_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/openstack-hypervisors/summary/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> HypervisorSummary:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = HypervisorSummary.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[HypervisorSummary]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    settings_uuid: UUID,
) -> Response[HypervisorSummary]:
    """Get hypervisor summary statistics

     Return aggregated vCPU, RAM and disk totals across all hypervisors matching the current filter (e.g.
    settings_uuid).

    Args:
        settings_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HypervisorSummary]
    """

    kwargs = _get_kwargs(
        settings_uuid=settings_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    settings_uuid: UUID,
) -> HypervisorSummary:
    """Get hypervisor summary statistics

     Return aggregated vCPU, RAM and disk totals across all hypervisors matching the current filter (e.g.
    settings_uuid).

    Args:
        settings_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HypervisorSummary
    """

    return sync_detailed(
        client=client,
        settings_uuid=settings_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    settings_uuid: UUID,
) -> Response[HypervisorSummary]:
    """Get hypervisor summary statistics

     Return aggregated vCPU, RAM and disk totals across all hypervisors matching the current filter (e.g.
    settings_uuid).

    Args:
        settings_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HypervisorSummary]
    """

    kwargs = _get_kwargs(
        settings_uuid=settings_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    settings_uuid: UUID,
) -> HypervisorSummary:
    """Get hypervisor summary statistics

     Return aggregated vCPU, RAM and disk totals across all hypervisors matching the current filter (e.g.
    settings_uuid).

    Args:
        settings_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HypervisorSummary
    """

    return (
        await asyncio_detailed(
            client=client,
            settings_uuid=settings_uuid,
        )
    ).parsed
