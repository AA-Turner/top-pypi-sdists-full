from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.invitation_accept_error import InvitationAcceptError
from ...models.invitation_accept_response import InvitationAcceptResponse
from ...models.self_declared_conflict_request import SelfDeclaredConflictRequest
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: list["SelfDeclaredConflictRequest"],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/call-reviewer-pools/{uuid}/accept/",
    }

    _kwargs["json"] = []
    for body_item_data in body:
        body_item = body_item_data.to_dict()
        _kwargs["json"].append(body_item)

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[InvitationAcceptError, InvitationAcceptResponse]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = InvitationAcceptResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = InvitationAcceptError.from_dict(response.json())

        return response_400
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[InvitationAcceptError, InvitationAcceptResponse]]:
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
    body: list["SelfDeclaredConflictRequest"],
) -> Response[Union[InvitationAcceptError, InvitationAcceptResponse]]:
    """Accept a pool invitation (authenticated users only).

    Args:
        uuid (UUID):
        body (list['SelfDeclaredConflictRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[InvitationAcceptError, InvitationAcceptResponse]]
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
    body: list["SelfDeclaredConflictRequest"],
) -> Union[InvitationAcceptError, InvitationAcceptResponse]:
    """Accept a pool invitation (authenticated users only).

    Args:
        uuid (UUID):
        body (list['SelfDeclaredConflictRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[InvitationAcceptError, InvitationAcceptResponse]
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
    body: list["SelfDeclaredConflictRequest"],
) -> Response[Union[InvitationAcceptError, InvitationAcceptResponse]]:
    """Accept a pool invitation (authenticated users only).

    Args:
        uuid (UUID):
        body (list['SelfDeclaredConflictRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[InvitationAcceptError, InvitationAcceptResponse]]
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
    body: list["SelfDeclaredConflictRequest"],
) -> Union[InvitationAcceptError, InvitationAcceptResponse]:
    """Accept a pool invitation (authenticated users only).

    Args:
        uuid (UUID):
        body (list['SelfDeclaredConflictRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[InvitationAcceptError, InvitationAcceptResponse]
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
