from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.event_consumer_registration_request import EventConsumerRegistrationRequest
from ...models.event_consumer_registration_response import EventConsumerRegistrationResponse
from ...types import Response


def _get_kwargs(
    *,
    body: EventConsumerRegistrationRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/event-consumers/register/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> EventConsumerRegistrationResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = EventConsumerRegistrationResponse.from_dict(response.json())

        return response_200
    if response.status_code == 201:
        response_201 = EventConsumerRegistrationResponse.from_dict(response.json())

        return response_201
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[EventConsumerRegistrationResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: EventConsumerRegistrationRequest,
) -> Response[EventConsumerRegistrationResponse]:
    """Register (or refresh) an event-consumer queue for the calling user. Pass `scopes` to bind the queue
    to entities you hold a role on; an EMPTY `scopes` list requests a GLOBAL queue (all events,
    including all-user PII) and requires staff/support. Idempotent per binding set.

    Args:
        body (EventConsumerRegistrationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EventConsumerRegistrationResponse]
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
    body: EventConsumerRegistrationRequest,
) -> EventConsumerRegistrationResponse:
    """Register (or refresh) an event-consumer queue for the calling user. Pass `scopes` to bind the queue
    to entities you hold a role on; an EMPTY `scopes` list requests a GLOBAL queue (all events,
    including all-user PII) and requires staff/support. Idempotent per binding set.

    Args:
        body (EventConsumerRegistrationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EventConsumerRegistrationResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: EventConsumerRegistrationRequest,
) -> Response[EventConsumerRegistrationResponse]:
    """Register (or refresh) an event-consumer queue for the calling user. Pass `scopes` to bind the queue
    to entities you hold a role on; an EMPTY `scopes` list requests a GLOBAL queue (all events,
    including all-user PII) and requires staff/support. Idempotent per binding set.

    Args:
        body (EventConsumerRegistrationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EventConsumerRegistrationResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: EventConsumerRegistrationRequest,
) -> EventConsumerRegistrationResponse:
    """Register (or refresh) an event-consumer queue for the calling user. Pass `scopes` to bind the queue
    to entities you hold a role on; an EMPTY `scopes` list requests a GLOBAL queue (all events,
    including all-user PII) and requires staff/support. Idempotent per binding set.

    Args:
        body (EventConsumerRegistrationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EventConsumerRegistrationResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
