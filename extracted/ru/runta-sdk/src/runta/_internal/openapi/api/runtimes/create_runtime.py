from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.checkpoint_runtime_restore_request import CheckpointRuntimeRestoreRequest
from ...models.error_envelope import ErrorEnvelope
from ...models.fresh_runtime_create_request import FreshRuntimeCreateRequest
from ...models.runtime_response import RuntimeResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: CheckpointRuntimeRestoreRequest | FreshRuntimeCreateRequest,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v2/runtimes",
    }

    if isinstance(body, FreshRuntimeCreateRequest):
        _kwargs["json"] = body.to_dict()
    else:
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorEnvelope | RuntimeResponse:
    if response.status_code == 201:
        response_201 = RuntimeResponse.from_dict(response.json())

        return response_201

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
) -> Response[ErrorEnvelope | RuntimeResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CheckpointRuntimeRestoreRequest | FreshRuntimeCreateRequest,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorEnvelope | RuntimeResponse]:
    """Create a runtime

    Args:
        idempotency_key (str | Unset):
        body (CheckpointRuntimeRestoreRequest | FreshRuntimeCreateRequest): Fresh runtime creation
            or checkpoint restoration request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | RuntimeResponse]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: CheckpointRuntimeRestoreRequest | FreshRuntimeCreateRequest,
    idempotency_key: str | Unset = UNSET,
) -> ErrorEnvelope | RuntimeResponse | None:
    """Create a runtime

    Args:
        idempotency_key (str | Unset):
        body (CheckpointRuntimeRestoreRequest | FreshRuntimeCreateRequest): Fresh runtime creation
            or checkpoint restoration request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | RuntimeResponse
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CheckpointRuntimeRestoreRequest | FreshRuntimeCreateRequest,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorEnvelope | RuntimeResponse]:
    """Create a runtime

    Args:
        idempotency_key (str | Unset):
        body (CheckpointRuntimeRestoreRequest | FreshRuntimeCreateRequest): Fresh runtime creation
            or checkpoint restoration request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | RuntimeResponse]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CheckpointRuntimeRestoreRequest | FreshRuntimeCreateRequest,
    idempotency_key: str | Unset = UNSET,
) -> ErrorEnvelope | RuntimeResponse | None:
    """Create a runtime

    Args:
        idempotency_key (str | Unset):
        body (CheckpointRuntimeRestoreRequest | FreshRuntimeCreateRequest): Fresh runtime creation
            or checkpoint restoration request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | RuntimeResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
