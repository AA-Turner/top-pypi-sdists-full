from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.anonymous_chat_feedback import AnonymousChatFeedback
from ...types import Response


def _get_kwargs(
    interaction_uuid: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/anonymous-chat-feedbacks/{interaction_uuid}/",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> AnonymousChatFeedback:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = AnonymousChatFeedback.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[AnonymousChatFeedback]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    interaction_uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[AnonymousChatFeedback]:
    """
    Args:
        interaction_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AnonymousChatFeedback]
    """

    kwargs = _get_kwargs(
        interaction_uuid=interaction_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    interaction_uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> AnonymousChatFeedback:
    """
    Args:
        interaction_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AnonymousChatFeedback
    """

    return sync_detailed(
        interaction_uuid=interaction_uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    interaction_uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[AnonymousChatFeedback]:
    """
    Args:
        interaction_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AnonymousChatFeedback]
    """

    kwargs = _get_kwargs(
        interaction_uuid=interaction_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    interaction_uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> AnonymousChatFeedback:
    """
    Args:
        interaction_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AnonymousChatFeedback
    """

    return (
        await asyncio_detailed(
            interaction_uuid=interaction_uuid,
            client=client,
        )
    ).parsed
