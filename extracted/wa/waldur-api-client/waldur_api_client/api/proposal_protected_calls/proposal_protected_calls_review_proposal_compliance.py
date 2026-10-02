from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.call_compliance_review_request import CallComplianceReviewRequest
from ...models.proposal_protected_calls_review_proposal_compliance_response_200 import (
    ProposalProtectedCallsReviewProposalComplianceResponse200,
)
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: CallComplianceReviewRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/proposal-protected-calls/{uuid}/review_proposal_compliance/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> ProposalProtectedCallsReviewProposalComplianceResponse200:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ProposalProtectedCallsReviewProposalComplianceResponse200.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ProposalProtectedCallsReviewProposalComplianceResponse200]:
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
    body: CallComplianceReviewRequest,
) -> Response[ProposalProtectedCallsReviewProposalComplianceResponse200]:
    """Mark proposal compliance as reviewed by call manager.

    Args:
        uuid (UUID):
        body (CallComplianceReviewRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProposalProtectedCallsReviewProposalComplianceResponse200]
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
    body: CallComplianceReviewRequest,
) -> ProposalProtectedCallsReviewProposalComplianceResponse200:
    """Mark proposal compliance as reviewed by call manager.

    Args:
        uuid (UUID):
        body (CallComplianceReviewRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProposalProtectedCallsReviewProposalComplianceResponse200
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
    body: CallComplianceReviewRequest,
) -> Response[ProposalProtectedCallsReviewProposalComplianceResponse200]:
    """Mark proposal compliance as reviewed by call manager.

    Args:
        uuid (UUID):
        body (CallComplianceReviewRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProposalProtectedCallsReviewProposalComplianceResponse200]
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
    body: CallComplianceReviewRequest,
) -> ProposalProtectedCallsReviewProposalComplianceResponse200:
    """Mark proposal compliance as reviewed by call manager.

    Args:
        uuid (UUID):
        body (CallComplianceReviewRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProposalProtectedCallsReviewProposalComplianceResponse200
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
