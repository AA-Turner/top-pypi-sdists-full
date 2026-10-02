from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_auth_token_exchange_response_400 import ApiAuthTokenExchangeResponse400
from ...models.core_auth_token import CoreAuthToken
from ...models.token_exchange_request import TokenExchangeRequest
from ...types import Response


def _get_kwargs(
    *,
    body: TokenExchangeRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api-auth/token-exchange/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[ApiAuthTokenExchangeResponse400, CoreAuthToken]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = CoreAuthToken.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ApiAuthTokenExchangeResponse400.from_dict(response.json())

        return response_400
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ApiAuthTokenExchangeResponse400, CoreAuthToken]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: TokenExchangeRequest,
) -> Response[Union[ApiAuthTokenExchangeResponse400, CoreAuthToken]]:
    """Exchange code for token

     Exchanges a short-lived one-time code for an authentication token.

    Args:
        body (TokenExchangeRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiAuthTokenExchangeResponse400, CoreAuthToken]]
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
    body: TokenExchangeRequest,
) -> Union[ApiAuthTokenExchangeResponse400, CoreAuthToken]:
    """Exchange code for token

     Exchanges a short-lived one-time code for an authentication token.

    Args:
        body (TokenExchangeRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiAuthTokenExchangeResponse400, CoreAuthToken]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: TokenExchangeRequest,
) -> Response[Union[ApiAuthTokenExchangeResponse400, CoreAuthToken]]:
    """Exchange code for token

     Exchanges a short-lived one-time code for an authentication token.

    Args:
        body (TokenExchangeRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApiAuthTokenExchangeResponse400, CoreAuthToken]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: TokenExchangeRequest,
) -> Union[ApiAuthTokenExchangeResponse400, CoreAuthToken]:
    """Exchange code for token

     Exchanges a short-lived one-time code for an authentication token.

    Args:
        body (TokenExchangeRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApiAuthTokenExchangeResponse400, CoreAuthToken]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
