from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.group_invitation_update import GroupInvitationUpdate
from ...models.patched_group_invitation_update_request import PatchedGroupInvitationUpdateRequest
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: PatchedGroupInvitationUpdateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/api/user-group-invitations/{uuid}/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> GroupInvitationUpdate:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = GroupInvitationUpdate.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GroupInvitationUpdate]:
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
    body: PatchedGroupInvitationUpdateRequest,
) -> Response[GroupInvitationUpdate]:
    """Partially update a group invitation

     Partially update an active group invitation. Only active invitations can be edited.

    Args:
        uuid (UUID):
        body (PatchedGroupInvitationUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GroupInvitationUpdate]
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
    body: PatchedGroupInvitationUpdateRequest,
) -> GroupInvitationUpdate:
    """Partially update a group invitation

     Partially update an active group invitation. Only active invitations can be edited.

    Args:
        uuid (UUID):
        body (PatchedGroupInvitationUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GroupInvitationUpdate
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
    body: PatchedGroupInvitationUpdateRequest,
) -> Response[GroupInvitationUpdate]:
    """Partially update a group invitation

     Partially update an active group invitation. Only active invitations can be edited.

    Args:
        uuid (UUID):
        body (PatchedGroupInvitationUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GroupInvitationUpdate]
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
    body: PatchedGroupInvitationUpdateRequest,
) -> GroupInvitationUpdate:
    """Partially update a group invitation

     Partially update an active group invitation. Only active invitations can be edited.

    Args:
        uuid (UUID):
        body (PatchedGroupInvitationUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GroupInvitationUpdate
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
