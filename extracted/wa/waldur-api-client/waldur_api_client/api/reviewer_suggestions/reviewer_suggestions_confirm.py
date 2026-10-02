from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.reviewer_suggestion import ReviewerSuggestion
from ...models.reviewer_suggestion_request import ReviewerSuggestionRequest
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: ReviewerSuggestionRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/reviewer-suggestions/{uuid}/confirm/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ReviewerSuggestion:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ReviewerSuggestion.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ReviewerSuggestion]:
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
    body: ReviewerSuggestionRequest,
) -> Response[ReviewerSuggestion]:
    """Confirm a reviewer suggestion. The reviewer will be invited to the call.

    Args:
        uuid (UUID):
        body (ReviewerSuggestionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ReviewerSuggestion]
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
    body: ReviewerSuggestionRequest,
) -> ReviewerSuggestion:
    """Confirm a reviewer suggestion. The reviewer will be invited to the call.

    Args:
        uuid (UUID):
        body (ReviewerSuggestionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ReviewerSuggestion
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
    body: ReviewerSuggestionRequest,
) -> Response[ReviewerSuggestion]:
    """Confirm a reviewer suggestion. The reviewer will be invited to the call.

    Args:
        uuid (UUID):
        body (ReviewerSuggestionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ReviewerSuggestion]
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
    body: ReviewerSuggestionRequest,
) -> ReviewerSuggestion:
    """Confirm a reviewer suggestion. The reviewer will be invited to the call.

    Args:
        uuid (UUID):
        body (ReviewerSuggestionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ReviewerSuggestion
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
