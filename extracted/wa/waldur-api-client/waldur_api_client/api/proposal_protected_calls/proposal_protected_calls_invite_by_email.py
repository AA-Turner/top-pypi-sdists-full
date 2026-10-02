from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.call_reviewer_pool import CallReviewerPool
from ...models.email_invitation_request import EmailInvitationRequest
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: EmailInvitationRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/proposal-protected-calls/{uuid}/invite-by-email/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> CallReviewerPool:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = CallReviewerPool.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CallReviewerPool]:
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
    body: EmailInvitationRequest,
) -> Response[CallReviewerPool]:
    """Invite a reviewer by email address. Creates an invitation that requires the reviewer to create and
    publish a profile before accepting.

    Args:
        uuid (UUID):
        body (EmailInvitationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CallReviewerPool]
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
    body: EmailInvitationRequest,
) -> CallReviewerPool:
    """Invite a reviewer by email address. Creates an invitation that requires the reviewer to create and
    publish a profile before accepting.

    Args:
        uuid (UUID):
        body (EmailInvitationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CallReviewerPool
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
    body: EmailInvitationRequest,
) -> Response[CallReviewerPool]:
    """Invite a reviewer by email address. Creates an invitation that requires the reviewer to create and
    publish a profile before accepting.

    Args:
        uuid (UUID):
        body (EmailInvitationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CallReviewerPool]
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
    body: EmailInvitationRequest,
) -> CallReviewerPool:
    """Invite a reviewer by email address. Creates an invitation that requires the reviewer to create and
    publish a profile before accepting.

    Args:
        uuid (UUID):
        body (EmailInvitationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CallReviewerPool
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
