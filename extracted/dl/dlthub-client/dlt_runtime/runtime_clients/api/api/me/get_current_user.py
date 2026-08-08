from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.current_user_response import CurrentUserResponse
from ...models.error_response_401 import ErrorResponse401
from ...models.error_response_403 import ErrorResponse403
from ...models.error_response_404 import ErrorResponse404
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/user",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    CurrentUserResponse | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | None
):
    if response.status_code == 200:
        response_200 = CurrentUserResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ErrorResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorResponse404.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    CurrentUserResponse | ErrorResponse401 | ErrorResponse403 | ErrorResponse404
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[
    CurrentUserResponse | ErrorResponse401 | ErrorResponse403 | ErrorResponse404
]:
    """GetCurrentUser


    Get the current user's identity and organization memberships.

    Like /me but without the cross-org workspace listing, so it stays cheap on the
    frontend hot path (fetch per-org workspaces via /organizations/{id}/me).

    On the first call for a user who has no organization yet, bootstraps a personal
    organization and a playground workspace, so a freshly authenticated user always
    gets a 200.

    Requires Authorization Header.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CurrentUserResponse | ErrorResponse401 | ErrorResponse403 | ErrorResponse404]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> (
    CurrentUserResponse | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | None
):
    """GetCurrentUser


    Get the current user's identity and organization memberships.

    Like /me but without the cross-org workspace listing, so it stays cheap on the
    frontend hot path (fetch per-org workspaces via /organizations/{id}/me).

    On the first call for a user who has no organization yet, bootstraps a personal
    organization and a playground workspace, so a freshly authenticated user always
    gets a 200.

    Requires Authorization Header.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CurrentUserResponse | ErrorResponse401 | ErrorResponse403 | ErrorResponse404
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[
    CurrentUserResponse | ErrorResponse401 | ErrorResponse403 | ErrorResponse404
]:
    """GetCurrentUser


    Get the current user's identity and organization memberships.

    Like /me but without the cross-org workspace listing, so it stays cheap on the
    frontend hot path (fetch per-org workspaces via /organizations/{id}/me).

    On the first call for a user who has no organization yet, bootstraps a personal
    organization and a playground workspace, so a freshly authenticated user always
    gets a 200.

    Requires Authorization Header.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CurrentUserResponse | ErrorResponse401 | ErrorResponse403 | ErrorResponse404]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> (
    CurrentUserResponse | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | None
):
    """GetCurrentUser


    Get the current user's identity and organization memberships.

    Like /me but without the cross-org workspace listing, so it stays cheap on the
    frontend hot path (fetch per-org workspaces via /organizations/{id}/me).

    On the first call for a user who has no organization yet, bootstraps a personal
    organization and a playground workspace, so a freshly authenticated user always
    gets a 200.

    Requires Authorization Header.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CurrentUserResponse | ErrorResponse401 | ErrorResponse403 | ErrorResponse404
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
