from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.proposal_workflow_step_instance import ProposalWorkflowStepInstance
from ...models.reopen_decision_request import ReopenDecisionRequest
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: ReopenDecisionRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/proposal-proposals/{uuid}/reopen_decision/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> ProposalWorkflowStepInstance:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ProposalWorkflowStepInstance.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ProposalWorkflowStepInstance]:
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
    body: ReopenDecisionRequest,
) -> Response[ProposalWorkflowStepInstance]:
    """Reopen an allocation decision held for the round's publication: the decision step becomes active
    again with its outcome cleared, and the proposal counts as undecided until it is decided anew. Only
    before the round's results are published. Nothing is sent to the applicant. The reopen is logged on
    the proposal's event feed, which the applicant team reads, so the event carries neither the reason
    nor the outcome taken back.

    Args:
        uuid (UUID):
        body (ReopenDecisionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProposalWorkflowStepInstance]
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
    body: ReopenDecisionRequest,
) -> ProposalWorkflowStepInstance:
    """Reopen an allocation decision held for the round's publication: the decision step becomes active
    again with its outcome cleared, and the proposal counts as undecided until it is decided anew. Only
    before the round's results are published. Nothing is sent to the applicant. The reopen is logged on
    the proposal's event feed, which the applicant team reads, so the event carries neither the reason
    nor the outcome taken back.

    Args:
        uuid (UUID):
        body (ReopenDecisionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProposalWorkflowStepInstance
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
    body: ReopenDecisionRequest,
) -> Response[ProposalWorkflowStepInstance]:
    """Reopen an allocation decision held for the round's publication: the decision step becomes active
    again with its outcome cleared, and the proposal counts as undecided until it is decided anew. Only
    before the round's results are published. Nothing is sent to the applicant. The reopen is logged on
    the proposal's event feed, which the applicant team reads, so the event carries neither the reason
    nor the outcome taken back.

    Args:
        uuid (UUID):
        body (ReopenDecisionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProposalWorkflowStepInstance]
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
    body: ReopenDecisionRequest,
) -> ProposalWorkflowStepInstance:
    """Reopen an allocation decision held for the round's publication: the decision step becomes active
    again with its outcome cleared, and the proposal counts as undecided until it is decided anew. Only
    before the round's results are published. Nothing is sent to the applicant. The reopen is logged on
    the proposal's event feed, which the applicant team reads, so the event carries neither the reason
    nor the outcome taken back.

    Args:
        uuid (UUID):
        body (ReopenDecisionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProposalWorkflowStepInstance
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
