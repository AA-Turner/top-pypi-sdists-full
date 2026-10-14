from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.call_reviewer_pool import CallReviewerPool
from ...types import Response


def _get_kwargs(
    uuid: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/call-reviewer-pools/{uuid}/resend-invitation/",
    }

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
) -> Response[CallReviewerPool]:
    """Send a pending or expired pool invitation again. The invitation returns to pending with a new expiry
    date from the call's assignment configuration, and the invitee is emailed the link again.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CallReviewerPool]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> CallReviewerPool:
    """Send a pending or expired pool invitation again. The invitation returns to pending with a new expiry
    date from the call's assignment configuration, and the invitee is emailed the link again.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CallReviewerPool
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[CallReviewerPool]:
    """Send a pending or expired pool invitation again. The invitation returns to pending with a new expiry
    date from the call's assignment configuration, and the invitee is emailed the link again.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CallReviewerPool]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> CallReviewerPool:
    """Send a pending or expired pool invitation again. The invitation returns to pending with a new expiry
    date from the call's assignment configuration, and the invitee is emailed the link again.

    Args:
        uuid (UUID):

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
        )
    ).parsed
