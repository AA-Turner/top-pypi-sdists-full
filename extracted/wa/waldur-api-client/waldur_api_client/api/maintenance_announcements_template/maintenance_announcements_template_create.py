from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.maintenance_announcement_template import MaintenanceAnnouncementTemplate
from ...models.maintenance_announcement_template_request import MaintenanceAnnouncementTemplateRequest
from ...types import Response


def _get_kwargs(
    *,
    body: MaintenanceAnnouncementTemplateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/maintenance-announcements-template/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> MaintenanceAnnouncementTemplate:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 201:
        response_201 = MaintenanceAnnouncementTemplate.from_dict(response.json())

        return response_201
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[MaintenanceAnnouncementTemplate]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: MaintenanceAnnouncementTemplateRequest,
) -> Response[MaintenanceAnnouncementTemplate]:
    """Create a maintenance announcement template

     Creates a new reusable template for maintenance announcements, including a default message and type.

    Args:
        body (MaintenanceAnnouncementTemplateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MaintenanceAnnouncementTemplate]
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
    body: MaintenanceAnnouncementTemplateRequest,
) -> MaintenanceAnnouncementTemplate:
    """Create a maintenance announcement template

     Creates a new reusable template for maintenance announcements, including a default message and type.

    Args:
        body (MaintenanceAnnouncementTemplateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MaintenanceAnnouncementTemplate
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: MaintenanceAnnouncementTemplateRequest,
) -> Response[MaintenanceAnnouncementTemplate]:
    """Create a maintenance announcement template

     Creates a new reusable template for maintenance announcements, including a default message and type.

    Args:
        body (MaintenanceAnnouncementTemplateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MaintenanceAnnouncementTemplate]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: MaintenanceAnnouncementTemplateRequest,
) -> MaintenanceAnnouncementTemplate:
    """Create a maintenance announcement template

     Creates a new reusable template for maintenance announcements, including a default message and type.

    Args:
        body (MaintenanceAnnouncementTemplateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MaintenanceAnnouncementTemplate
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
