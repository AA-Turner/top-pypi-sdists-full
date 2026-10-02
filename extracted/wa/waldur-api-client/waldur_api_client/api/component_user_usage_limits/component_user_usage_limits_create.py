from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.component_user_usage_limit import ComponentUserUsageLimit
from ...models.component_user_usage_limit_request import ComponentUserUsageLimitRequest
from ...types import Response


def _get_kwargs(
    *,
    body: ComponentUserUsageLimitRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/component-user-usage-limits/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ComponentUserUsageLimit:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 201:
        response_201 = ComponentUserUsageLimit.from_dict(response.json())

        return response_201
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
    *,
    client: AuthenticatedClient,
    body: ComponentUserUsageLimitRequest,
) -> Response[ComponentUserUsageLimit]:
    """Create a component usage limit for a user

     Sets a usage limit for a specific user on a resource's component. This is only applicable for
    offerings that support per-user consumption limitation.

    Args:
        body (ComponentUserUsageLimitRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ComponentUserUsageLimit]
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
    body: ComponentUserUsageLimitRequest,
) -> ComponentUserUsageLimit:
    """Create a component usage limit for a user

     Sets a usage limit for a specific user on a resource's component. This is only applicable for
    offerings that support per-user consumption limitation.

    Args:
        body (ComponentUserUsageLimitRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ComponentUserUsageLimit
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ComponentUserUsageLimitRequest,
) -> Response[ComponentUserUsageLimit]:
    """Create a component usage limit for a user

     Sets a usage limit for a specific user on a resource's component. This is only applicable for
    offerings that support per-user consumption limitation.

    Args:
        body (ComponentUserUsageLimitRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ComponentUserUsageLimit]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ComponentUserUsageLimitRequest,
) -> ComponentUserUsageLimit:
    """Create a component usage limit for a user

     Sets a usage limit for a specific user on a resource's component. This is only applicable for
    offerings that support per-user consumption limitation.

    Args:
        body (ComponentUserUsageLimitRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ComponentUserUsageLimit
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
