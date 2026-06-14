from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.event_response import EventResponse
from uuid import UUID


def _get_kwargs(
    event_id: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/events/{event_id}".format(
            event_id=quote(str(event_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> EventResponse | None:
    if response.status_code == 200:
        response_200 = EventResponse.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[EventResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    event_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[EventResponse]:
    """Get Event

     Retrieve a single audit event by id.

    Authorized against the caller's permitted environment set: the event
    is returned only if its environment is one the caller may access,
    otherwise `404` (the same response as a non-existent id, so existence
    never leaks across environments). A single-object lookup names the
    object by id; it does not resolve a target environment.

    Args:
        event_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EventResponse]
    """

    kwargs = _get_kwargs(
        event_id=event_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    event_id: UUID,
    *,
    client: AuthenticatedClient,
) -> EventResponse | None:
    """Get Event

     Retrieve a single audit event by id.

    Authorized against the caller's permitted environment set: the event
    is returned only if its environment is one the caller may access,
    otherwise `404` (the same response as a non-existent id, so existence
    never leaks across environments). A single-object lookup names the
    object by id; it does not resolve a target environment.

    Args:
        event_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EventResponse
    """

    return sync_detailed(
        event_id=event_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    event_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[EventResponse]:
    """Get Event

     Retrieve a single audit event by id.

    Authorized against the caller's permitted environment set: the event
    is returned only if its environment is one the caller may access,
    otherwise `404` (the same response as a non-existent id, so existence
    never leaks across environments). A single-object lookup names the
    object by id; it does not resolve a target environment.

    Args:
        event_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EventResponse]
    """

    kwargs = _get_kwargs(
        event_id=event_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    event_id: UUID,
    *,
    client: AuthenticatedClient,
) -> EventResponse | None:
    """Get Event

     Retrieve a single audit event by id.

    Authorized against the caller's permitted environment set: the event
    is returned only if its environment is one the caller may access,
    otherwise `404` (the same response as a non-existent id, so existence
    never leaks across environments). A single-object lookup names the
    object by id; it does not resolve a target environment.

    Args:
        event_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EventResponse
    """

    return (
        await asyncio_detailed(
            event_id=event_id,
            client=client,
        )
    ).parsed
