from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.error_response import ErrorResponse
from ...models.group_membership_request import GroupMembershipRequest
from ...models.group_membership_response import GroupMembershipResponse


def _get_kwargs(
    *,
    body: GroupMembershipRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/group_memberships",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/vnd.api+json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | GroupMembershipResponse | None:
    if response.status_code == 201:
        response_201 = GroupMembershipResponse.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = ErrorResponse.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | GroupMembershipResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: GroupMembershipRequest,
) -> Response[ErrorResponse | GroupMembershipResponse]:
    """Create Group Membership

     Add a user to a group. The body references the user (UUID) and the group (key) in the resource
    attributes. Returns `409` if this user is already a member of this group, or `422` if either the
    user is not a member of the account or the group does not exist.

    Args:
        body (GroupMembershipRequest): JSON:API request envelope for creating a group membership.

            Memberships have no mutable attributes, so this envelope is used
            only on POST. There is no PUT/PATCH on the membership resource.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GroupMembershipResponse]
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
    body: GroupMembershipRequest,
) -> ErrorResponse | GroupMembershipResponse | None:
    """Create Group Membership

     Add a user to a group. The body references the user (UUID) and the group (key) in the resource
    attributes. Returns `409` if this user is already a member of this group, or `422` if either the
    user is not a member of the account or the group does not exist.

    Args:
        body (GroupMembershipRequest): JSON:API request envelope for creating a group membership.

            Memberships have no mutable attributes, so this envelope is used
            only on POST. There is no PUT/PATCH on the membership resource.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GroupMembershipResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: GroupMembershipRequest,
) -> Response[ErrorResponse | GroupMembershipResponse]:
    """Create Group Membership

     Add a user to a group. The body references the user (UUID) and the group (key) in the resource
    attributes. Returns `409` if this user is already a member of this group, or `422` if either the
    user is not a member of the account or the group does not exist.

    Args:
        body (GroupMembershipRequest): JSON:API request envelope for creating a group membership.

            Memberships have no mutable attributes, so this envelope is used
            only on POST. There is no PUT/PATCH on the membership resource.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GroupMembershipResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: GroupMembershipRequest,
) -> ErrorResponse | GroupMembershipResponse | None:
    """Create Group Membership

     Add a user to a group. The body references the user (UUID) and the group (key) in the resource
    attributes. Returns `409` if this user is already a member of this group, or `422` if either the
    user is not a member of the account or the group does not exist.

    Args:
        body (GroupMembershipRequest): JSON:API request envelope for creating a group membership.

            Memberships have no mutable attributes, so this envelope is used
            only on POST. There is no PUT/PATCH on the membership resource.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GroupMembershipResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
