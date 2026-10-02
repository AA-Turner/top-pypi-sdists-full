from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.invitation_duplicate_check_request import InvitationDuplicateCheckRequest
from ...models.invitation_duplicate_check_response import InvitationDuplicateCheckResponse
from ...types import Response


def _get_kwargs(
    *,
    body: InvitationDuplicateCheckRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/user-invitations/check-duplicates/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> InvitationDuplicateCheckResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = InvitationDuplicateCheckResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[InvitationDuplicateCheckResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: InvitationDuplicateCheckRequest,
) -> Response[InvitationDuplicateCheckResponse]:
    """Check for duplicate invitations

     Returns pending invitations that already exist for the same email and role within the given scope.

    Args:
        body (InvitationDuplicateCheckRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[InvitationDuplicateCheckResponse]
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
    body: InvitationDuplicateCheckRequest,
) -> InvitationDuplicateCheckResponse:
    """Check for duplicate invitations

     Returns pending invitations that already exist for the same email and role within the given scope.

    Args:
        body (InvitationDuplicateCheckRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        InvitationDuplicateCheckResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: InvitationDuplicateCheckRequest,
) -> Response[InvitationDuplicateCheckResponse]:
    """Check for duplicate invitations

     Returns pending invitations that already exist for the same email and role within the given scope.

    Args:
        body (InvitationDuplicateCheckRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[InvitationDuplicateCheckResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: InvitationDuplicateCheckRequest,
) -> InvitationDuplicateCheckResponse:
    """Check for duplicate invitations

     Returns pending invitations that already exist for the same email and role within the given scope.

    Args:
        body (InvitationDuplicateCheckRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        InvitationDuplicateCheckResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
