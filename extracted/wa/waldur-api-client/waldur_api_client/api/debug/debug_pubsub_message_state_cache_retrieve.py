from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.message_state_cache import MessageStateCache
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/debug/pubsub/message_state_cache/",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> MessageStateCache:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = MessageStateCache.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[MessageStateCache]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[MessageStateCache]:
    """Get message state cache statistics

     Get message state tracker cache statistics for idempotency.

    The message state tracker prevents duplicate message sends by caching
    the hash of message content. This endpoint provides cache statistics.

    Query params:
    - resource_uuid: Filter by specific resource
    - message_type: Filter by message type

    Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MessageStateCache]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> MessageStateCache:
    """Get message state cache statistics

     Get message state tracker cache statistics for idempotency.

    The message state tracker prevents duplicate message sends by caching
    the hash of message content. This endpoint provides cache statistics.

    Query params:
    - resource_uuid: Filter by specific resource
    - message_type: Filter by message type

    Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MessageStateCache
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[MessageStateCache]:
    """Get message state cache statistics

     Get message state tracker cache statistics for idempotency.

    The message state tracker prevents duplicate message sends by caching
    the hash of message content. This endpoint provides cache statistics.

    Query params:
    - resource_uuid: Filter by specific resource
    - message_type: Filter by message type

    Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MessageStateCache]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> MessageStateCache:
    """Get message state cache statistics

     Get message state tracker cache statistics for idempotency.

    The message state tracker prevents duplicate message sends by caching
    the hash of message content. This endpoint provides cache statistics.

    Query params:
    - resource_uuid: Filter by specific resource
    - message_type: Filter by message type

    Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MessageStateCache
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
