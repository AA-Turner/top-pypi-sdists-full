from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.reviewer_publication import ReviewerPublication
from ...models.reviewer_publication_request import ReviewerPublicationRequest
from ...types import Response


def _get_kwargs(
    reviewer_profile_uuid: str,
    *,
    body: ReviewerPublicationRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/reviewer-profiles/{reviewer_profile_uuid}/publications/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ReviewerPublication:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 201:
        response_201 = ReviewerPublication.from_dict(response.json())

        return response_201
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ReviewerPublication]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    reviewer_profile_uuid: str,
    *,
    client: AuthenticatedClient,
    body: ReviewerPublicationRequest,
) -> Response[ReviewerPublication]:
    """
    Args:
        reviewer_profile_uuid (str):
        body (ReviewerPublicationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ReviewerPublication]
    """

    kwargs = _get_kwargs(
        reviewer_profile_uuid=reviewer_profile_uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    reviewer_profile_uuid: str,
    *,
    client: AuthenticatedClient,
    body: ReviewerPublicationRequest,
) -> ReviewerPublication:
    """
    Args:
        reviewer_profile_uuid (str):
        body (ReviewerPublicationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ReviewerPublication
    """

    return sync_detailed(
        reviewer_profile_uuid=reviewer_profile_uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    reviewer_profile_uuid: str,
    *,
    client: AuthenticatedClient,
    body: ReviewerPublicationRequest,
) -> Response[ReviewerPublication]:
    """
    Args:
        reviewer_profile_uuid (str):
        body (ReviewerPublicationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ReviewerPublication]
    """

    kwargs = _get_kwargs(
        reviewer_profile_uuid=reviewer_profile_uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    reviewer_profile_uuid: str,
    *,
    client: AuthenticatedClient,
    body: ReviewerPublicationRequest,
) -> ReviewerPublication:
    """
    Args:
        reviewer_profile_uuid (str):
        body (ReviewerPublicationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ReviewerPublication
    """

    return (
        await asyncio_detailed(
            reviewer_profile_uuid=reviewer_profile_uuid,
            client=client,
            body=body,
        )
    ).parsed
