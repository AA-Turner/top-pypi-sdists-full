from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.maintenance_reservation_import_request import MaintenanceReservationImportRequest
from ...models.maintenance_reservation_import_result import MaintenanceReservationImportResult
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: MaintenanceReservationImportRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/marketplace-provider-offerings/{uuid}/import_maintenance_reservations/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> MaintenanceReservationImportResult:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = MaintenanceReservationImportResult.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[MaintenanceReservationImportResult]:
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
    body: MaintenanceReservationImportRequest,
) -> Response[MaintenanceReservationImportResult]:
    """Import the cluster's maintenance reservations as drafts

     Site agents report the MAINT reservations made on the cluster; each becomes a draft maintenance
    announcement for the provider to review and publish. Reservations named with the Waldur prefix are
    ignored. Only when maintenance sync is enabled on the offering.

    Args:
        uuid (UUID):
        body (MaintenanceReservationImportRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MaintenanceReservationImportResult]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: MaintenanceReservationImportRequest,
) -> MaintenanceReservationImportResult:
    """Import the cluster's maintenance reservations as drafts

     Site agents report the MAINT reservations made on the cluster; each becomes a draft maintenance
    announcement for the provider to review and publish. Reservations named with the Waldur prefix are
    ignored. Only when maintenance sync is enabled on the offering.

    Args:
        uuid (UUID):
        body (MaintenanceReservationImportRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MaintenanceReservationImportResult
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: MaintenanceReservationImportRequest,
) -> Response[MaintenanceReservationImportResult]:
    """Import the cluster's maintenance reservations as drafts

     Site agents report the MAINT reservations made on the cluster; each becomes a draft maintenance
    announcement for the provider to review and publish. Reservations named with the Waldur prefix are
    ignored. Only when maintenance sync is enabled on the offering.

    Args:
        uuid (UUID):
        body (MaintenanceReservationImportRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MaintenanceReservationImportResult]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: MaintenanceReservationImportRequest,
) -> MaintenanceReservationImportResult:
    """Import the cluster's maintenance reservations as drafts

     Site agents report the MAINT reservations made on the cluster; each becomes a draft maintenance
    announcement for the provider to review and publish. Reservations named with the Waldur prefix are
    ignored. Only when maintenance sync is enabled on the offering.

    Args:
        uuid (UUID):
        body (MaintenanceReservationImportRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MaintenanceReservationImportResult
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
