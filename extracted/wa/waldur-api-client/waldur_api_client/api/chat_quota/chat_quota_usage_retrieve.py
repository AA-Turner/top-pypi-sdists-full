from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.token_quota_usage_response import TokenQuotaUsageResponse
from ...types import UNSET, Response


def _get_kwargs(
    *,
    user_uuid: UUID,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_user_uuid = str(user_uuid)
    params["user_uuid"] = json_user_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/chat-quota/usage/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> TokenQuotaUsageResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = TokenQuotaUsageResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[TokenQuotaUsageResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    user_uuid: UUID,
) -> Response[TokenQuotaUsageResponse]:
    """
            Get current token quota and usage for the requesting user.

            Returns token quota for all periods (daily, weekly, monthly):
            - limit: User's custom limit (null = use system default, -1 = unlimited, or positive
    integer)
            - usage: Tokens used in current period
            - remaining: Tokens remaining (null if unlimited)
            - reset_at: When the period resets
            - system_default: System-wide default limit from configuration (for transparency when limit
    is null)


    Args:
        user_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TokenQuotaUsageResponse]
    """

    kwargs = _get_kwargs(
        user_uuid=user_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    user_uuid: UUID,
) -> TokenQuotaUsageResponse:
    """
            Get current token quota and usage for the requesting user.

            Returns token quota for all periods (daily, weekly, monthly):
            - limit: User's custom limit (null = use system default, -1 = unlimited, or positive
    integer)
            - usage: Tokens used in current period
            - remaining: Tokens remaining (null if unlimited)
            - reset_at: When the period resets
            - system_default: System-wide default limit from configuration (for transparency when limit
    is null)


    Args:
        user_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TokenQuotaUsageResponse
    """

    return sync_detailed(
        client=client,
        user_uuid=user_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    user_uuid: UUID,
) -> Response[TokenQuotaUsageResponse]:
    """
            Get current token quota and usage for the requesting user.

            Returns token quota for all periods (daily, weekly, monthly):
            - limit: User's custom limit (null = use system default, -1 = unlimited, or positive
    integer)
            - usage: Tokens used in current period
            - remaining: Tokens remaining (null if unlimited)
            - reset_at: When the period resets
            - system_default: System-wide default limit from configuration (for transparency when limit
    is null)


    Args:
        user_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TokenQuotaUsageResponse]
    """

    kwargs = _get_kwargs(
        user_uuid=user_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    user_uuid: UUID,
) -> TokenQuotaUsageResponse:
    """
            Get current token quota and usage for the requesting user.

            Returns token quota for all periods (daily, weekly, monthly):
            - limit: User's custom limit (null = use system default, -1 = unlimited, or positive
    integer)
            - usage: Tokens used in current period
            - remaining: Tokens remaining (null if unlimited)
            - reset_at: When the period resets
            - system_default: System-wide default limit from configuration (for transparency when limit
    is null)


    Args:
        user_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TokenQuotaUsageResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            user_uuid=user_uuid,
        )
    ).parsed
