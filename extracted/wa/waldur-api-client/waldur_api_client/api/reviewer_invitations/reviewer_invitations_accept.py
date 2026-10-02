from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.invitation_accept_error import InvitationAcceptError
from ...models.invitation_accept_request import InvitationAcceptRequest
from ...models.invitation_accept_response import InvitationAcceptResponse
from ...models.invitation_auth_error import InvitationAuthError
from ...types import Response


def _get_kwargs(
    token: str,
    *,
    body: InvitationAcceptRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/reviewer-invitations/{token}/accept/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[InvitationAcceptError, InvitationAcceptResponse, InvitationAuthError]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = InvitationAcceptResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = InvitationAcceptError.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = InvitationAuthError.from_dict(response.json())

        return response_401
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[InvitationAcceptError, InvitationAcceptResponse, InvitationAuthError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    token: str,
    *,
    client: AuthenticatedClient,
    body: InvitationAcceptRequest,
) -> Response[Union[InvitationAcceptError, InvitationAcceptResponse, InvitationAuthError]]:
    """Accept a reviewer invitation.

    Args:
        token (str):
        body (InvitationAcceptRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[InvitationAcceptError, InvitationAcceptResponse, InvitationAuthError]]
    """

    kwargs = _get_kwargs(
        token=token,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    token: str,
    *,
    client: AuthenticatedClient,
    body: InvitationAcceptRequest,
) -> Union[InvitationAcceptError, InvitationAcceptResponse, InvitationAuthError]:
    """Accept a reviewer invitation.

    Args:
        token (str):
        body (InvitationAcceptRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[InvitationAcceptError, InvitationAcceptResponse, InvitationAuthError]
    """

    return sync_detailed(
        token=token,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    token: str,
    *,
    client: AuthenticatedClient,
    body: InvitationAcceptRequest,
) -> Response[Union[InvitationAcceptError, InvitationAcceptResponse, InvitationAuthError]]:
    """Accept a reviewer invitation.

    Args:
        token (str):
        body (InvitationAcceptRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[InvitationAcceptError, InvitationAcceptResponse, InvitationAuthError]]
    """

    kwargs = _get_kwargs(
        token=token,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    token: str,
    *,
    client: AuthenticatedClient,
    body: InvitationAcceptRequest,
) -> Union[InvitationAcceptError, InvitationAcceptResponse, InvitationAuthError]:
    """Accept a reviewer invitation.

    Args:
        token (str):
        body (InvitationAcceptRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[InvitationAcceptError, InvitationAcceptResponse, InvitationAuthError]
    """

    return (
        await asyncio_detailed(
            token=token,
            client=client,
            body=body,
        )
    ).parsed
