from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_organization_invite_request import CreateOrganizationInviteRequest
from ...models.create_organization_invite_response_409 import (
    CreateOrganizationInviteResponse409,
)
from ...models.error_response_400 import ErrorResponse400
from ...models.error_response_401 import ErrorResponse401
from ...models.error_response_403 import ErrorResponse403
from ...models.error_response_404 import ErrorResponse404
from ...models.invite_response import InviteResponse
from ...types import Response


def _get_kwargs(
    organization_id: UUID,
    *,
    body: CreateOrganizationInviteRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/organizations/{organization_id}/invites".format(
            organization_id=quote(str(organization_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    CreateOrganizationInviteResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | InviteResponse
    | None
):
    if response.status_code == 201:
        response_201 = InviteResponse.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = ErrorResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = CreateOrganizationInviteResponse409.from_dict(response.json())

        return response_409

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    CreateOrganizationInviteResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | InviteResponse
]:
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
    body: CreateOrganizationInviteRequest,
) -> Response[
    CreateOrganizationInviteResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | InviteResponse
]:
    """CreateOrganizationInvite


    Invites a user to an organization by email, granting the owner or member role on accept.

    Re-inviting reopens a revoked invite; inviting someone who is already a member returns 409.

    Returns 409 while the organization's region is not set.

    Requires MANAGE_ORG permission on the organization level.

    Args:
        organization_id (UUID):
        body (CreateOrganizationInviteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateOrganizationInviteResponse409 | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | InviteResponse]
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
    body: CreateOrganizationInviteRequest,
) -> (
    CreateOrganizationInviteResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | InviteResponse
    | None
):
    """CreateOrganizationInvite


    Invites a user to an organization by email, granting the owner or member role on accept.

    Re-inviting reopens a revoked invite; inviting someone who is already a member returns 409.

    Returns 409 while the organization's region is not set.

    Requires MANAGE_ORG permission on the organization level.

    Args:
        organization_id (UUID):
        body (CreateOrganizationInviteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateOrganizationInviteResponse409 | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | InviteResponse
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
    body: CreateOrganizationInviteRequest,
) -> Response[
    CreateOrganizationInviteResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | InviteResponse
]:
    """CreateOrganizationInvite


    Invites a user to an organization by email, granting the owner or member role on accept.

    Re-inviting reopens a revoked invite; inviting someone who is already a member returns 409.

    Returns 409 while the organization's region is not set.

    Requires MANAGE_ORG permission on the organization level.

    Args:
        organization_id (UUID):
        body (CreateOrganizationInviteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateOrganizationInviteResponse409 | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | InviteResponse]
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
    body: CreateOrganizationInviteRequest,
) -> (
    CreateOrganizationInviteResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | InviteResponse
    | None
):
    """CreateOrganizationInvite


    Invites a user to an organization by email, granting the owner or member role on accept.

    Re-inviting reopens a revoked invite; inviting someone who is already a member returns 409.

    Returns 409 while the organization's region is not set.

    Requires MANAGE_ORG permission on the organization level.

    Args:
        organization_id (UUID):
        body (CreateOrganizationInviteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateOrganizationInviteResponse409 | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | InviteResponse
    """

    return (
        await asyncio_detailed(
            organization_id=organization_id,
            client=client,
            body=body,
        )
    ).parsed
