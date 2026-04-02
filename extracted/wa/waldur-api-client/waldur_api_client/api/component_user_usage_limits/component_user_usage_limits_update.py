from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.component_user_usage_limit import ComponentUserUsageLimit
from ...models.component_user_usage_limit_request import ComponentUserUsageLimitRequest
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: ComponentUserUsageLimitRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/api/component-user-usage-limits/{uuid}/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ComponentUserUsageLimit:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ComponentUserUsageLimit.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ComponentUserUsageLimit]:
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
    body: ComponentUserUsageLimitRequest,
) -> Response[ComponentUserUsageLimit]:
    """Update a component usage limit

     Updates an existing usage limit for a user on a component.

    Args:
        uuid (UUID):
        body (ComponentUserUsageLimitRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ComponentUserUsageLimit]
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
    body: ComponentUserUsageLimitRequest,
) -> ComponentUserUsageLimit:
    """Update a component usage limit

     Updates an existing usage limit for a user on a component.

    Args:
        uuid (UUID):
        body (ComponentUserUsageLimitRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ComponentUserUsageLimit
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
    body: ComponentUserUsageLimitRequest,
) -> Response[ComponentUserUsageLimit]:
    """Update a component usage limit

     Updates an existing usage limit for a user on a component.

    Args:
        uuid (UUID):
        body (ComponentUserUsageLimitRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ComponentUserUsageLimit]
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
    body: ComponentUserUsageLimitRequest,
) -> ComponentUserUsageLimit:
    """Update a component usage limit

     Updates an existing usage limit for a user on a component.

    Args:
        uuid (UUID):
        body (ComponentUserUsageLimitRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ComponentUserUsageLimit
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
