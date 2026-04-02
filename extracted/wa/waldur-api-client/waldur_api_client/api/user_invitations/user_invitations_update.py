from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.invitation_update import InvitationUpdate
from ...models.invitation_update_request import InvitationUpdateRequest
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: InvitationUpdateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/api/user-invitations/{uuid}/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> InvitationUpdate:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = InvitationUpdate.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[InvitationUpdate]:
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
    body: InvitationUpdateRequest,
) -> Response[InvitationUpdate]:
    """Update user invitation

     Update an existing user invitation. Only pending invitations can be edited. Allows changing email
    and role within the same scope.

    Args:
        uuid (UUID):
        body (InvitationUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[InvitationUpdate]
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
    body: InvitationUpdateRequest,
) -> InvitationUpdate:
    """Update user invitation

     Update an existing user invitation. Only pending invitations can be edited. Allows changing email
    and role within the same scope.

    Args:
        uuid (UUID):
        body (InvitationUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        InvitationUpdate
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
    body: InvitationUpdateRequest,
) -> Response[InvitationUpdate]:
    """Update user invitation

     Update an existing user invitation. Only pending invitations can be edited. Allows changing email
    and role within the same scope.

    Args:
        uuid (UUID):
        body (InvitationUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[InvitationUpdate]
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
    body: InvitationUpdateRequest,
) -> InvitationUpdate:
    """Update user invitation

     Update an existing user invitation. Only pending invitations can be edited. Allows changing email
    and role within the same scope.

    Args:
        uuid (UUID):
        body (InvitationUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        InvitationUpdate
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
