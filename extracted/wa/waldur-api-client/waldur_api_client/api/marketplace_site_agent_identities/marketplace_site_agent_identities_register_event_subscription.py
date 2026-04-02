from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agent_event_subscription_create_request import AgentEventSubscriptionCreateRequest
from ...models.event_subscription import EventSubscription
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: AgentEventSubscriptionCreateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/marketplace-site-agent-identities/{uuid}/register_event_subscription/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> EventSubscription:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = EventSubscription.from_dict(response.json())

        return response_200
    if response.status_code == 201:
        response_201 = EventSubscription.from_dict(response.json())

        return response_201
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[EventSubscription]:
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
    body: AgentEventSubscriptionCreateRequest,
) -> Response[EventSubscription]:
    """Register an event subscription for the specified agent identity and observable object type. Returns
    existing subscription if already exists.

    Args:
        uuid (UUID):
        body (AgentEventSubscriptionCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EventSubscription]
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
    body: AgentEventSubscriptionCreateRequest,
) -> EventSubscription:
    """Register an event subscription for the specified agent identity and observable object type. Returns
    existing subscription if already exists.

    Args:
        uuid (UUID):
        body (AgentEventSubscriptionCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EventSubscription
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
    body: AgentEventSubscriptionCreateRequest,
) -> Response[EventSubscription]:
    """Register an event subscription for the specified agent identity and observable object type. Returns
    existing subscription if already exists.

    Args:
        uuid (UUID):
        body (AgentEventSubscriptionCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EventSubscription]
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
    body: AgentEventSubscriptionCreateRequest,
) -> EventSubscription:
    """Register an event subscription for the specified agent identity and observable object type. Returns
    existing subscription if already exists.

    Args:
        uuid (UUID):
        body (AgentEventSubscriptionCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EventSubscription
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
