from http import HTTPStatus
from io import BytesIO
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.proposal_review_state_enum import ProposalReviewStateEnum
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    uuid: UUID,
    *,
    proposal_name: Union[Unset, str] = UNSET,
    proposal_uuid: Union[Unset, UUID] = UNSET,
    review_state: Union[Unset, list[ProposalReviewStateEnum]] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    round_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["proposal_name"] = proposal_name

    json_proposal_uuid: Union[Unset, str] = UNSET
    if not isinstance(proposal_uuid, Unset):
        json_proposal_uuid = str(proposal_uuid)
    params["proposal_uuid"] = json_proposal_uuid

    json_review_state: Union[Unset, list[str]] = UNSET
    if not isinstance(review_state, Unset):
        json_review_state = []
        for review_state_item_data in review_state:
            review_state_item = review_state_item_data.value
            json_review_state.append(review_state_item)

    params["review_state"] = json_review_state

    json_reviewer_uuid: Union[Unset, str] = UNSET
    if not isinstance(reviewer_uuid, Unset):
        json_reviewer_uuid = str(reviewer_uuid)
    params["reviewer_uuid"] = json_reviewer_uuid

    json_round_uuid: Union[Unset, str] = UNSET
    if not isinstance(round_uuid, Unset):
        json_round_uuid = str(round_uuid)
    params["round_uuid"] = json_round_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/proposal-protected-calls/{uuid}/export-reviews/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> File:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = File(payload=BytesIO(response.text))

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[File]:
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
    proposal_name: Union[Unset, str] = UNSET,
    proposal_uuid: Union[Unset, UUID] = UNSET,
    review_state: Union[Unset, list[ProposalReviewStateEnum]] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    round_uuid: Union[Unset, UUID] = UNSET,
) -> Response[File]:
    """Download the call's reviews as CSV, one row per review. The reviewer's private comment is never
    included: the export is open to call managers, and the review API keeps that field from them.

    Args:
        uuid (UUID):
        proposal_name (Union[Unset, str]):
        proposal_uuid (Union[Unset, UUID]):
        review_state (Union[Unset, list[ProposalReviewStateEnum]]):
        reviewer_uuid (Union[Unset, UUID]):
        round_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[File]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        proposal_name=proposal_name,
        proposal_uuid=proposal_uuid,
        review_state=review_state,
        reviewer_uuid=reviewer_uuid,
        round_uuid=round_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    proposal_name: Union[Unset, str] = UNSET,
    proposal_uuid: Union[Unset, UUID] = UNSET,
    review_state: Union[Unset, list[ProposalReviewStateEnum]] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    round_uuid: Union[Unset, UUID] = UNSET,
) -> File:
    """Download the call's reviews as CSV, one row per review. The reviewer's private comment is never
    included: the export is open to call managers, and the review API keeps that field from them.

    Args:
        uuid (UUID):
        proposal_name (Union[Unset, str]):
        proposal_uuid (Union[Unset, UUID]):
        review_state (Union[Unset, list[ProposalReviewStateEnum]]):
        reviewer_uuid (Union[Unset, UUID]):
        round_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        File
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        proposal_name=proposal_name,
        proposal_uuid=proposal_uuid,
        review_state=review_state,
        reviewer_uuid=reviewer_uuid,
        round_uuid=round_uuid,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    proposal_name: Union[Unset, str] = UNSET,
    proposal_uuid: Union[Unset, UUID] = UNSET,
    review_state: Union[Unset, list[ProposalReviewStateEnum]] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    round_uuid: Union[Unset, UUID] = UNSET,
) -> Response[File]:
    """Download the call's reviews as CSV, one row per review. The reviewer's private comment is never
    included: the export is open to call managers, and the review API keeps that field from them.

    Args:
        uuid (UUID):
        proposal_name (Union[Unset, str]):
        proposal_uuid (Union[Unset, UUID]):
        review_state (Union[Unset, list[ProposalReviewStateEnum]]):
        reviewer_uuid (Union[Unset, UUID]):
        round_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[File]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        proposal_name=proposal_name,
        proposal_uuid=proposal_uuid,
        review_state=review_state,
        reviewer_uuid=reviewer_uuid,
        round_uuid=round_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    proposal_name: Union[Unset, str] = UNSET,
    proposal_uuid: Union[Unset, UUID] = UNSET,
    review_state: Union[Unset, list[ProposalReviewStateEnum]] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    round_uuid: Union[Unset, UUID] = UNSET,
) -> File:
    """Download the call's reviews as CSV, one row per review. The reviewer's private comment is never
    included: the export is open to call managers, and the review API keeps that field from them.

    Args:
        uuid (UUID):
        proposal_name (Union[Unset, str]):
        proposal_uuid (Union[Unset, UUID]):
        review_state (Union[Unset, list[ProposalReviewStateEnum]]):
        reviewer_uuid (Union[Unset, UUID]):
        round_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        File
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            proposal_name=proposal_name,
            proposal_uuid=proposal_uuid,
            review_state=review_state,
            reviewer_uuid=reviewer_uuid,
            round_uuid=round_uuid,
        )
    ).parsed
