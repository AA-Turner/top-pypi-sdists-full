from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.maintenance_announcement import MaintenanceAnnouncement
from ...models.maintenance_announcement_request import MaintenanceAnnouncementRequest
from ...types import Response


def _get_kwargs(
    *,
    body: MaintenanceAnnouncementRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/maintenance-announcements/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> MaintenanceAnnouncement:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 201:
        response_201 = MaintenanceAnnouncement.from_dict(response.json())

        return response_201
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[MaintenanceAnnouncement]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: MaintenanceAnnouncementRequest,
) -> Response[MaintenanceAnnouncement]:
    """Create a maintenance announcement

     Creates a new maintenance announcement in the 'Draft' state.

    Args:
        body (MaintenanceAnnouncementRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MaintenanceAnnouncement]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: MaintenanceAnnouncementRequest,
) -> MaintenanceAnnouncement:
    """Create a maintenance announcement

     Creates a new maintenance announcement in the 'Draft' state.

    Args:
        body (MaintenanceAnnouncementRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MaintenanceAnnouncement
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: MaintenanceAnnouncementRequest,
) -> Response[MaintenanceAnnouncement]:
    """Create a maintenance announcement

     Creates a new maintenance announcement in the 'Draft' state.

    Args:
        body (MaintenanceAnnouncementRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MaintenanceAnnouncement]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: MaintenanceAnnouncementRequest,
) -> MaintenanceAnnouncement:
    """Create a maintenance announcement

     Creates a new maintenance announcement in the 'Draft' state.

    Args:
        body (MaintenanceAnnouncementRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MaintenanceAnnouncement
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
