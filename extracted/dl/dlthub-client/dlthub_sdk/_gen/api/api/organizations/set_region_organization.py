from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.organization_response import OrganizationResponse
from ...models.set_region_organization_request import SetRegionOrganizationRequest
from ...types import Response


def _get_kwargs(
    organization_id: UUID,
    *,
    body: SetRegionOrganizationRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/organizations/{organization_id}/-set-region".format(
            organization_id=quote(str(organization_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | OrganizationResponse | None:
    if response.status_code == 200:
        response_200 = OrganizationResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ErrorResponse.from_dict(response.json())

        return response_409

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | OrganizationResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    organization_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: SetRegionOrganizationRequest,
) -> Response[ErrorResponse | OrganizationResponse]:
    """SetOrganizationRegion

    Sets the organization's region, its data plane. This is one-time and
    irreversible: a second attempt returns 409. An unknown dataplane_id returns 400.

    Requires MANAGE_ORG permission on the organization level.

    Args:
        organization_id (UUID):
        body (SetRegionOrganizationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | OrganizationResponse]
    """
    kwargs = _get_kwargs(
        organization_id=organization_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    organization_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: SetRegionOrganizationRequest,
) -> ErrorResponse | OrganizationResponse | None:
    """SetOrganizationRegion

    Sets the organization's region, its data plane. This is one-time and
    irreversible: a second attempt returns 409. An unknown dataplane_id returns 400.

    Requires MANAGE_ORG permission on the organization level.

    Args:
        organization_id (UUID):
        body (SetRegionOrganizationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | OrganizationResponse
    """
    return sync_detailed(
        organization_id=organization_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    organization_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: SetRegionOrganizationRequest,
) -> Response[ErrorResponse | OrganizationResponse]:
    """SetOrganizationRegion

    Sets the organization's region, its data plane. This is one-time and
    irreversible: a second attempt returns 409. An unknown dataplane_id returns 400.

    Requires MANAGE_ORG permission on the organization level.

    Args:
        organization_id (UUID):
        body (SetRegionOrganizationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | OrganizationResponse]
    """
    kwargs = _get_kwargs(
        organization_id=organization_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    organization_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: SetRegionOrganizationRequest,
) -> ErrorResponse | OrganizationResponse | None:
    """SetOrganizationRegion

    Sets the organization's region, its data plane. This is one-time and
    irreversible: a second attempt returns 409. An unknown dataplane_id returns 400.

    Requires MANAGE_ORG permission on the organization level.

    Args:
        organization_id (UUID):
        body (SetRegionOrganizationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | OrganizationResponse
    """
    return (
        await asyncio_detailed(
            organization_id=organization_id,
            client=client,
            body=body,
        )
    ).parsed
