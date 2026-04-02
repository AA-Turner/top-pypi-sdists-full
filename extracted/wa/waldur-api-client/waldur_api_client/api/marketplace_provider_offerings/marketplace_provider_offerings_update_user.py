from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.user_role_expiration_time import UserRoleExpirationTime
from ...models.user_role_update_request import UserRoleUpdateRequest
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: UserRoleUpdateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/marketplace-provider-offerings/{uuid}/update_user/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> UserRoleExpirationTime:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = UserRoleExpirationTime.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[UserRoleExpirationTime]:
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
    body: UserRoleUpdateRequest,
) -> Response[UserRoleExpirationTime]:
    """Update a user's role expiration

     Updates the expiration time for a user's existing role in the current scope. This is useful for
    extending or shortening the duration of a permission. To make a role permanent, set expiration_time
    to null.

    Args:
        uuid (UUID):
        body (UserRoleUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UserRoleExpirationTime]
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
    body: UserRoleUpdateRequest,
) -> UserRoleExpirationTime:
    """Update a user's role expiration

     Updates the expiration time for a user's existing role in the current scope. This is useful for
    extending or shortening the duration of a permission. To make a role permanent, set expiration_time
    to null.

    Args:
        uuid (UUID):
        body (UserRoleUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UserRoleExpirationTime
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
    body: UserRoleUpdateRequest,
) -> Response[UserRoleExpirationTime]:
    """Update a user's role expiration

     Updates the expiration time for a user's existing role in the current scope. This is useful for
    extending or shortening the duration of a permission. To make a role permanent, set expiration_time
    to null.

    Args:
        uuid (UUID):
        body (UserRoleUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UserRoleExpirationTime]
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
    body: UserRoleUpdateRequest,
) -> UserRoleExpirationTime:
    """Update a user's role expiration

     Updates the expiration time for a user's existing role in the current scope. This is useful for
    extending or shortening the duration of a permission. To make a role permanent, set expiration_time
    to null.

    Args:
        uuid (UUID):
        body (UserRoleUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UserRoleExpirationTime
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
