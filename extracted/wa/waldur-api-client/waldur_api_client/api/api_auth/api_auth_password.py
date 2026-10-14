from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.auth_token_challenge import AuthTokenChallenge
from ...models.core_auth_token import CoreAuthToken
from ...models.obtain_auth_token_request import ObtainAuthTokenRequest
from ...types import Response


def _get_kwargs(
    *,
    body: ObtainAuthTokenRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api-auth/password/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[AuthTokenChallenge, CoreAuthToken]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = CoreAuthToken.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = AuthTokenChallenge.from_dict(response.json())

        return response_401
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[AuthTokenChallenge, CoreAuthToken]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ObtainAuthTokenRequest,
) -> Response[Union[AuthTokenChallenge, CoreAuthToken]]:
    """Obtain authentication token

     Authenticates a user with username and password and returns an authentication token.

    Args:
        body (ObtainAuthTokenRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AuthTokenChallenge, CoreAuthToken]]
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
    client: Union[AuthenticatedClient, Client],
    body: ObtainAuthTokenRequest,
) -> Union[AuthTokenChallenge, CoreAuthToken]:
    """Obtain authentication token

     Authenticates a user with username and password and returns an authentication token.

    Args:
        body (ObtainAuthTokenRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AuthTokenChallenge, CoreAuthToken]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ObtainAuthTokenRequest,
) -> Response[Union[AuthTokenChallenge, CoreAuthToken]]:
    """Obtain authentication token

     Authenticates a user with username and password and returns an authentication token.

    Args:
        body (ObtainAuthTokenRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AuthTokenChallenge, CoreAuthToken]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ObtainAuthTokenRequest,
) -> Union[AuthTokenChallenge, CoreAuthToken]:
    """Obtain authentication token

     Authenticates a user with username and password and returns an authentication token.

    Args:
        body (ObtainAuthTokenRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AuthTokenChallenge, CoreAuthToken]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
