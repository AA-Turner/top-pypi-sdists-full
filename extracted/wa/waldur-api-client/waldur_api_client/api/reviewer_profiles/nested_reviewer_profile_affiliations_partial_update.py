from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.patched_reviewer_affiliation_request import PatchedReviewerAffiliationRequest
from ...models.reviewer_affiliation import ReviewerAffiliation
from ...types import Response


def _get_kwargs(
    reviewer_profile_uuid: str,
    uuid: UUID,
    *,
    body: PatchedReviewerAffiliationRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/api/reviewer-profiles/{reviewer_profile_uuid}/affiliations/{uuid}/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ReviewerAffiliation:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ReviewerAffiliation.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ReviewerAffiliation]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    reviewer_profile_uuid: str,
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: PatchedReviewerAffiliationRequest,
) -> Response[ReviewerAffiliation]:
    """
    Args:
        reviewer_profile_uuid (str):
        uuid (UUID):
        body (PatchedReviewerAffiliationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ReviewerAffiliation]
    """

    kwargs = _get_kwargs(
        reviewer_profile_uuid=reviewer_profile_uuid,
        uuid=uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    reviewer_profile_uuid: str,
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: PatchedReviewerAffiliationRequest,
) -> ReviewerAffiliation:
    """
    Args:
        reviewer_profile_uuid (str):
        uuid (UUID):
        body (PatchedReviewerAffiliationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ReviewerAffiliation
    """

    return sync_detailed(
        reviewer_profile_uuid=reviewer_profile_uuid,
        uuid=uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    reviewer_profile_uuid: str,
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: PatchedReviewerAffiliationRequest,
) -> Response[ReviewerAffiliation]:
    """
    Args:
        reviewer_profile_uuid (str):
        uuid (UUID):
        body (PatchedReviewerAffiliationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ReviewerAffiliation]
    """

    kwargs = _get_kwargs(
        reviewer_profile_uuid=reviewer_profile_uuid,
        uuid=uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    reviewer_profile_uuid: str,
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: PatchedReviewerAffiliationRequest,
) -> ReviewerAffiliation:
    """
    Args:
        reviewer_profile_uuid (str):
        uuid (UUID):
        body (PatchedReviewerAffiliationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ReviewerAffiliation
    """

    return (
        await asyncio_detailed(
            reviewer_profile_uuid=reviewer_profile_uuid,
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
