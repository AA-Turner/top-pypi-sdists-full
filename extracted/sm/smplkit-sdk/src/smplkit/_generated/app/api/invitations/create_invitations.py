from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.error_response import ErrorResponse
from ...models.invitation_bulk_create_request import InvitationBulkCreateRequest
from ...models.invitation_list_response import InvitationListResponse


def _get_kwargs(
    *,
    body: InvitationBulkCreateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/invitations",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/vnd.api+json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | InvitationListResponse | None:
    if response.status_code == 201:
        response_201 = InvitationListResponse.from_dict(response.json())

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
) -> Response[ErrorResponse | InvitationListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: InvitationBulkCreateRequest,
) -> Response[ErrorResponse | InvitationListResponse]:
    """Bulk Create Invitations

     Send one or more invitations to join the account.

    Args:
        body (InvitationBulkCreateRequest): Bulk-create request body for the invitations endpoint.
            Example: {'invitations': [{'email': 'alice@example.com', 'role': 'MEMBER'}, {'email':
            'bob@example.com', 'role': 'MEMBER'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | InvitationListResponse]
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
    body: InvitationBulkCreateRequest,
) -> ErrorResponse | InvitationListResponse | None:
    """Bulk Create Invitations

     Send one or more invitations to join the account.

    Args:
        body (InvitationBulkCreateRequest): Bulk-create request body for the invitations endpoint.
            Example: {'invitations': [{'email': 'alice@example.com', 'role': 'MEMBER'}, {'email':
            'bob@example.com', 'role': 'MEMBER'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | InvitationListResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: InvitationBulkCreateRequest,
) -> Response[ErrorResponse | InvitationListResponse]:
    """Bulk Create Invitations

     Send one or more invitations to join the account.

    Args:
        body (InvitationBulkCreateRequest): Bulk-create request body for the invitations endpoint.
            Example: {'invitations': [{'email': 'alice@example.com', 'role': 'MEMBER'}, {'email':
            'bob@example.com', 'role': 'MEMBER'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | InvitationListResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: InvitationBulkCreateRequest,
) -> ErrorResponse | InvitationListResponse | None:
    """Bulk Create Invitations

     Send one or more invitations to join the account.

    Args:
        body (InvitationBulkCreateRequest): Bulk-create request body for the invitations endpoint.
            Example: {'invitations': [{'email': 'alice@example.com', 'role': 'MEMBER'}, {'email':
            'bob@example.com', 'role': 'MEMBER'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | InvitationListResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
