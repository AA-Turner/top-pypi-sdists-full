from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_user_api_key_request import CreateUserApiKeyRequest
from ...models.create_user_api_key_response import CreateUserApiKeyResponse
from ...models.create_user_api_key_response_409 import CreateUserApiKeyResponse409
from ...models.error_response_400 import ErrorResponse400
from ...models.error_response_401 import ErrorResponse401
from ...models.error_response_403 import ErrorResponse403
from ...models.error_response_404 import ErrorResponse404
from ...types import Response


def _get_kwargs(
    *,
    body: CreateUserApiKeyRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/api-keys",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    CreateUserApiKeyResponse
    | CreateUserApiKeyResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | None
):
    if response.status_code == 201:
        response_201 = CreateUserApiKeyResponse.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = ErrorResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorResponse404.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = CreateUserApiKeyResponse409.from_dict(response.json())

        return response_409

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    CreateUserApiKeyResponse
    | CreateUserApiKeyResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
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
    body: CreateUserApiKeyRequest,
) -> Response[
    CreateUserApiKeyResponse
    | CreateUserApiKeyResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
]:
    """CreateUserApiKey

     Create a new user API key. The plaintext key is returned once and never stored.

    Args:
        body (CreateUserApiKeyRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateUserApiKeyResponse | CreateUserApiKeyResponse409 | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404]
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
    client: AuthenticatedClient | Client,
    body: CreateUserApiKeyRequest,
) -> (
    CreateUserApiKeyResponse
    | CreateUserApiKeyResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | None
):
    """CreateUserApiKey

     Create a new user API key. The plaintext key is returned once and never stored.

    Args:
        body (CreateUserApiKeyRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateUserApiKeyResponse | CreateUserApiKeyResponse409 | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: CreateUserApiKeyRequest,
) -> Response[
    CreateUserApiKeyResponse
    | CreateUserApiKeyResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
]:
    """CreateUserApiKey

     Create a new user API key. The plaintext key is returned once and never stored.

    Args:
        body (CreateUserApiKeyRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateUserApiKeyResponse | CreateUserApiKeyResponse409 | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: CreateUserApiKeyRequest,
) -> (
    CreateUserApiKeyResponse
    | CreateUserApiKeyResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | None
):
    """CreateUserApiKey

     Create a new user API key. The plaintext key is returned once and never stored.

    Args:
        body (CreateUserApiKeyRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateUserApiKeyResponse | CreateUserApiKeyResponse409 | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
