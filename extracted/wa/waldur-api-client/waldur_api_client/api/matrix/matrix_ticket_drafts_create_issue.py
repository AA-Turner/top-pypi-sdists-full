from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.matrix_ticket_draft_create_issue_request import MatrixTicketDraftCreateIssueRequest
from ...models.matrix_ticket_draft_issue import MatrixTicketDraftIssue
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: MatrixTicketDraftCreateIssueRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/matrix/ticket-drafts/{uuid}/create_issue/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> MatrixTicketDraftIssue:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 201:
        response_201 = MatrixTicketDraftIssue.from_dict(response.json())

        return response_201
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[MatrixTicketDraftIssue]:
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
    body: MatrixTicketDraftCreateIssueRequest,
) -> Response[MatrixTicketDraftIssue]:
    """Create the draft's support ticket

     Create the pending draft's ticket as its requester, through the support API, and post its key in the
    room's thread. The draft is then sent: a second call, or one for a canceled or expired draft, gets
    404.

    Args:
        uuid (UUID):
        body (MatrixTicketDraftCreateIssueRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MatrixTicketDraftIssue]
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
    body: MatrixTicketDraftCreateIssueRequest,
) -> MatrixTicketDraftIssue:
    """Create the draft's support ticket

     Create the pending draft's ticket as its requester, through the support API, and post its key in the
    room's thread. The draft is then sent: a second call, or one for a canceled or expired draft, gets
    404.

    Args:
        uuid (UUID):
        body (MatrixTicketDraftCreateIssueRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MatrixTicketDraftIssue
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
    body: MatrixTicketDraftCreateIssueRequest,
) -> Response[MatrixTicketDraftIssue]:
    """Create the draft's support ticket

     Create the pending draft's ticket as its requester, through the support API, and post its key in the
    room's thread. The draft is then sent: a second call, or one for a canceled or expired draft, gets
    404.

    Args:
        uuid (UUID):
        body (MatrixTicketDraftCreateIssueRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MatrixTicketDraftIssue]
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
    body: MatrixTicketDraftCreateIssueRequest,
) -> MatrixTicketDraftIssue:
    """Create the draft's support ticket

     Create the pending draft's ticket as its requester, through the support API, and post its key in the
    room's thread. The draft is then sent: a second call, or one for a canceled or expired draft, gets
    404.

    Args:
        uuid (UUID):
        body (MatrixTicketDraftCreateIssueRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MatrixTicketDraftIssue
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
