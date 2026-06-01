from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.error_response import ErrorResponse
from ...models.invitation_accept_request import InvitationAcceptRequest
from ...models.invitation_response import InvitationResponse


def _get_kwargs(
    *,
    body: InvitationAcceptRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/invitations/accept",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/vnd.api+json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | InvitationResponse | None:
    if response.status_code == 200:
        response_200 = InvitationResponse.from_dict(response.json())

        return response_200

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
) -> Response[ErrorResponse | InvitationResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: InvitationAcceptRequest,
) -> Response[ErrorResponse | InvitationResponse]:
    """Accept Invitation

     Accept an invitation using a token from the invitation email.

    Args:
        body (InvitationAcceptRequest): Body for the invitation-accept endpoint. Example:
            {'token': 'eyJhbGciOiJIUzI1NiJ9...'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | InvitationResponse]
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
    body: InvitationAcceptRequest,
) -> ErrorResponse | InvitationResponse | None:
    """Accept Invitation

     Accept an invitation using a token from the invitation email.

    Args:
        body (InvitationAcceptRequest): Body for the invitation-accept endpoint. Example:
            {'token': 'eyJhbGciOiJIUzI1NiJ9...'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | InvitationResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: InvitationAcceptRequest,
) -> Response[ErrorResponse | InvitationResponse]:
    """Accept Invitation

     Accept an invitation using a token from the invitation email.

    Args:
        body (InvitationAcceptRequest): Body for the invitation-accept endpoint. Example:
            {'token': 'eyJhbGciOiJIUzI1NiJ9...'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | InvitationResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: InvitationAcceptRequest,
) -> ErrorResponse | InvitationResponse | None:
    """Accept Invitation

     Accept an invitation using a token from the invitation email.

    Args:
        body (InvitationAcceptRequest): Body for the invitation-accept endpoint. Example:
            {'token': 'eyJhbGciOiJIUzI1NiJ9...'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | InvitationResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
