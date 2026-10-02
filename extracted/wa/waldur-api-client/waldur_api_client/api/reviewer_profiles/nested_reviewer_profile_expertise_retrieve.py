from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.reviewer_expertise import ReviewerExpertise
from ...types import Response


def _get_kwargs(
    reviewer_profile_uuid: str,
    uuid: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/reviewer-profiles/{reviewer_profile_uuid}/expertise/{uuid}/",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ReviewerExpertise:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ReviewerExpertise.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ReviewerExpertise]:
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
) -> Response[ReviewerExpertise]:
    """
    Args:
        reviewer_profile_uuid (str):
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ReviewerExpertise]
    """

    kwargs = _get_kwargs(
        reviewer_profile_uuid=reviewer_profile_uuid,
        uuid=uuid,
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
) -> ReviewerExpertise:
    """
    Args:
        reviewer_profile_uuid (str):
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ReviewerExpertise
    """

    return sync_detailed(
        reviewer_profile_uuid=reviewer_profile_uuid,
        uuid=uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    reviewer_profile_uuid: str,
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[ReviewerExpertise]:
    """
    Args:
        reviewer_profile_uuid (str):
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ReviewerExpertise]
    """

    kwargs = _get_kwargs(
        reviewer_profile_uuid=reviewer_profile_uuid,
        uuid=uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    reviewer_profile_uuid: str,
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> ReviewerExpertise:
    """
    Args:
        reviewer_profile_uuid (str):
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ReviewerExpertise
    """

    return (
        await asyncio_detailed(
            reviewer_profile_uuid=reviewer_profile_uuid,
            uuid=uuid,
            client=client,
        )
    ).parsed
