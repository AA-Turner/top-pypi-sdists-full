from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.reviewer_profile_request import ReviewerProfileRequest
from ...models.reviewer_profiles_publish_response_200 import ReviewerProfilesPublishResponse200
from ...types import Response


def _get_kwargs(
    *,
    body: ReviewerProfileRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/reviewer-profiles/publish/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> ReviewerProfilesPublishResponse200:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ReviewerProfilesPublishResponse200.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ReviewerProfilesPublishResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ReviewerProfileRequest,
) -> Response[ReviewerProfilesPublishResponse200]:
    """Publish reviewer profile for discovery by call managers. Warning: Publishing makes your full profile
    visible to call managers globally.

    Args:
        body (ReviewerProfileRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ReviewerProfilesPublishResponse200]
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
    body: ReviewerProfileRequest,
) -> ReviewerProfilesPublishResponse200:
    """Publish reviewer profile for discovery by call managers. Warning: Publishing makes your full profile
    visible to call managers globally.

    Args:
        body (ReviewerProfileRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ReviewerProfilesPublishResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ReviewerProfileRequest,
) -> Response[ReviewerProfilesPublishResponse200]:
    """Publish reviewer profile for discovery by call managers. Warning: Publishing makes your full profile
    visible to call managers globally.

    Args:
        body (ReviewerProfileRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ReviewerProfilesPublishResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ReviewerProfileRequest,
) -> ReviewerProfilesPublishResponse200:
    """Publish reviewer profile for discovery by call managers. Warning: Publishing makes your full profile
    visible to call managers globally.

    Args:
        body (ReviewerProfileRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ReviewerProfilesPublishResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
