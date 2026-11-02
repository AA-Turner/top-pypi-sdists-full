from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_envelope import ErrorEnvelope
from ...models.secret_response import SecretResponse
from ...models.set_secret_request import SetSecretRequest
from ...types import Response


def _get_kwargs(
    secret_id: str,
    *,
    body: SetSecretRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/v2/secrets/{secret_id}".format(
            secret_id=quote(str(secret_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorEnvelope | SecretResponse:
    if response.status_code == 200:
        response_200 = SecretResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ErrorEnvelope.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorEnvelope.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorEnvelope.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ErrorEnvelope.from_dict(response.json())

        return response_409

    if response.status_code == 422:
        response_422 = ErrorEnvelope.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = ErrorEnvelope.from_dict(response.json())

        return response_429

    if response.status_code == 501:
        response_501 = ErrorEnvelope.from_dict(response.json())

        return response_501

    if response.status_code == 503:
        response_503 = ErrorEnvelope.from_dict(response.json())

        return response_503

    if response.status_code == 504:
        response_504 = ErrorEnvelope.from_dict(response.json())

        return response_504

    response_default = ErrorEnvelope.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorEnvelope | SecretResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    secret_id: str,
    *,
    client: AuthenticatedClient,
    body: SetSecretRequest,
) -> Response[ErrorEnvelope | SecretResponse]:
    """Store or replace an egress secret

    Args:
        secret_id (str): Secret UUID or display name.
        body (SetSecretRequest): Secret set request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | SecretResponse]
    """

    kwargs = _get_kwargs(
        secret_id=secret_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    secret_id: str,
    *,
    client: AuthenticatedClient,
    body: SetSecretRequest,
) -> ErrorEnvelope | SecretResponse | None:
    """Store or replace an egress secret

    Args:
        secret_id (str): Secret UUID or display name.
        body (SetSecretRequest): Secret set request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | SecretResponse
    """

    return sync_detailed(
        secret_id=secret_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    secret_id: str,
    *,
    client: AuthenticatedClient,
    body: SetSecretRequest,
) -> Response[ErrorEnvelope | SecretResponse]:
    """Store or replace an egress secret

    Args:
        secret_id (str): Secret UUID or display name.
        body (SetSecretRequest): Secret set request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | SecretResponse]
    """

    kwargs = _get_kwargs(
        secret_id=secret_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    secret_id: str,
    *,
    client: AuthenticatedClient,
    body: SetSecretRequest,
) -> ErrorEnvelope | SecretResponse | None:
    """Store or replace an egress secret

    Args:
        secret_id (str): Secret UUID or display name.
        body (SetSecretRequest): Secret set request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | SecretResponse
    """

    return (
        await asyncio_detailed(
            secret_id=secret_id,
            client=client,
            body=body,
        )
    ).parsed
