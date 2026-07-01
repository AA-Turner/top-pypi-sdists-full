from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response_400 import ErrorResponse400
from ...models.error_response_401 import ErrorResponse401
from ...models.error_response_403 import ErrorResponse403
from ...models.error_response_404 import ErrorResponse404
from ...models.organization_member_response import OrganizationMemberResponse
from ...models.update_organization_member_request import UpdateOrganizationMemberRequest
from ...types import Response


def _get_kwargs(
    organization_id: UUID,
    user_id: str,
    *,
    body: UpdateOrganizationMemberRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/api/v1/organizations/{organization_id}/members/{user_id}".format(
            organization_id=quote(str(organization_id), safe=""),
            user_id=quote(str(user_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | OrganizationMemberResponse
    | None
):
    if response.status_code == 200:
        response_200 = OrganizationMemberResponse.from_dict(response.json())

        return response_200

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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | OrganizationMemberResponse
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    organization_id: UUID,
    user_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateOrganizationMemberRequest,
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | OrganizationMemberResponse
]:
    """UpdateOrganizationMember


    Changes a member's role in an organization (including promotion to owner).

    You cannot change your own membership. The last owner cannot be demoted.

    Requires MANAGE_ORG permission on the organization level.

    Args:
        organization_id (UUID):
        user_id (str):
        body (UpdateOrganizationMemberRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | OrganizationMemberResponse]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        user_id=user_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    organization_id: UUID,
    user_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateOrganizationMemberRequest,
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | OrganizationMemberResponse
    | None
):
    """UpdateOrganizationMember


    Changes a member's role in an organization (including promotion to owner).

    You cannot change your own membership. The last owner cannot be demoted.

    Requires MANAGE_ORG permission on the organization level.

    Args:
        organization_id (UUID):
        user_id (str):
        body (UpdateOrganizationMemberRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | OrganizationMemberResponse
    """

    return sync_detailed(
        organization_id=organization_id,
        user_id=user_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    organization_id: UUID,
    user_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateOrganizationMemberRequest,
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | OrganizationMemberResponse
]:
    """UpdateOrganizationMember


    Changes a member's role in an organization (including promotion to owner).

    You cannot change your own membership. The last owner cannot be demoted.

    Requires MANAGE_ORG permission on the organization level.

    Args:
        organization_id (UUID):
        user_id (str):
        body (UpdateOrganizationMemberRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | OrganizationMemberResponse]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        user_id=user_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    organization_id: UUID,
    user_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateOrganizationMemberRequest,
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | OrganizationMemberResponse
    | None
):
    """UpdateOrganizationMember


    Changes a member's role in an organization (including promotion to owner).

    You cannot change your own membership. The last owner cannot be demoted.

    Requires MANAGE_ORG permission on the organization level.

    Args:
        organization_id (UUID):
        user_id (str):
        body (UpdateOrganizationMemberRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | OrganizationMemberResponse
    """

    return (
        await asyncio_detailed(
            organization_id=organization_id,
            user_id=user_id,
            client=client,
            body=body,
        )
    ).parsed
