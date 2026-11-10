from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.user_invitation_accept_request import UserInvitationAcceptRequest
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: UserInvitationAcceptRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/user-invitations/{uuid}/accept/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Any:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        return None
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
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
    body: UserInvitationAcceptRequest,
) -> Response[Any]:
    """Accept an invitation

     Accepts an invitation for the currently authenticated user. This grants the user the specified role
    in the invitation's scope. Staff may pass `user` to accept it for that user instead, for example
    from a service account that registers users elsewhere; the user's email must match the invitation.

    Args:
        uuid (UUID):
        body (UserInvitationAcceptRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: UserInvitationAcceptRequest,
) -> Response[Any]:
    """Accept an invitation

     Accepts an invitation for the currently authenticated user. This grants the user the specified role
    in the invitation's scope. Staff may pass `user` to accept it for that user instead, for example
    from a service account that registers users elsewhere; the user's email must match the invitation.

    Args:
        uuid (UUID):
        body (UserInvitationAcceptRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
