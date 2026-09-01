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
from ...models.organization_workspace_response import OrganizationWorkspaceResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    organization_id: UUID,
    *,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    include_archived: bool | Unset = False,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    params["include_archived"] = include_archived

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/organizations/{organization_id}/workspaces".format(
            organization_id=quote(str(organization_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | list[OrganizationWorkspaceResponse]
    | None
):
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = OrganizationWorkspaceResponse.from_dict(
                response_200_item_data
            )

            response_200.append(response_200_item)

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
    | list[OrganizationWorkspaceResponse]
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
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    include_archived: bool | Unset = False,
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | list[OrganizationWorkspaceResponse]
]:
    """ListWorkspaces


    Lists the workspaces under an organization visible to the caller. Organization owners
    see every workspace; other members see workspaces they belong to or have access to via the default
    org-wide workspace role.

    Each workspace includes member stats: its owners and the count of active members.

    Playground workspaces of other members are not included; the caller only sees their own.

    Archived workspaces are excluded by default; pass include_archived=true to list them.
    No other route returns them.

    Requires READ permission on the organization level.

    Args:
        organization_id (UUID):
        limit (int | Unset): Maximum number of items to return. At most 1000. Default: 100.
        offset (int | Unset): Number of items to skip. At most 10000; a list reports its total up
            to 10001, so narrow with filters instead of paging deeper. Default: 0.
        include_archived (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | list[OrganizationWorkspaceResponse]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        limit=limit,
        offset=offset,
        include_archived=include_archived,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    organization_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    include_archived: bool | Unset = False,
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | list[OrganizationWorkspaceResponse]
    | None
):
    """ListWorkspaces


    Lists the workspaces under an organization visible to the caller. Organization owners
    see every workspace; other members see workspaces they belong to or have access to via the default
    org-wide workspace role.

    Each workspace includes member stats: its owners and the count of active members.

    Playground workspaces of other members are not included; the caller only sees their own.

    Archived workspaces are excluded by default; pass include_archived=true to list them.
    No other route returns them.

    Requires READ permission on the organization level.

    Args:
        organization_id (UUID):
        limit (int | Unset): Maximum number of items to return. At most 1000. Default: 100.
        offset (int | Unset): Number of items to skip. At most 10000; a list reports its total up
            to 10001, so narrow with filters instead of paging deeper. Default: 0.
        include_archived (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | list[OrganizationWorkspaceResponse]
    """

    return sync_detailed(
        organization_id=organization_id,
        client=client,
        limit=limit,
        offset=offset,
        include_archived=include_archived,
    ).parsed


async def asyncio_detailed(
    organization_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    include_archived: bool | Unset = False,
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | list[OrganizationWorkspaceResponse]
]:
    """ListWorkspaces


    Lists the workspaces under an organization visible to the caller. Organization owners
    see every workspace; other members see workspaces they belong to or have access to via the default
    org-wide workspace role.

    Each workspace includes member stats: its owners and the count of active members.

    Playground workspaces of other members are not included; the caller only sees their own.

    Archived workspaces are excluded by default; pass include_archived=true to list them.
    No other route returns them.

    Requires READ permission on the organization level.

    Args:
        organization_id (UUID):
        limit (int | Unset): Maximum number of items to return. At most 1000. Default: 100.
        offset (int | Unset): Number of items to skip. At most 10000; a list reports its total up
            to 10001, so narrow with filters instead of paging deeper. Default: 0.
        include_archived (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | list[OrganizationWorkspaceResponse]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        limit=limit,
        offset=offset,
        include_archived=include_archived,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    organization_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    include_archived: bool | Unset = False,
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | list[OrganizationWorkspaceResponse]
    | None
):
    """ListWorkspaces


    Lists the workspaces under an organization visible to the caller. Organization owners
    see every workspace; other members see workspaces they belong to or have access to via the default
    org-wide workspace role.

    Each workspace includes member stats: its owners and the count of active members.

    Playground workspaces of other members are not included; the caller only sees their own.

    Archived workspaces are excluded by default; pass include_archived=true to list them.
    No other route returns them.

    Requires READ permission on the organization level.

    Args:
        organization_id (UUID):
        limit (int | Unset): Maximum number of items to return. At most 1000. Default: 100.
        offset (int | Unset): Number of items to skip. At most 10000; a list reports its total up
            to 10001, so narrow with filters instead of paging deeper. Default: 0.
        include_archived (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | list[OrganizationWorkspaceResponse]
    """

    return (
        await asyncio_detailed(
            organization_id=organization_id,
            client=client,
            limit=limit,
            offset=offset,
            include_archived=include_archived,
        )
    ).parsed
