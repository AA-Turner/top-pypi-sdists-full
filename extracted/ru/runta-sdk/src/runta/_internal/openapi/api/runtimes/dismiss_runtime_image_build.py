from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ...client import AuthenticatedClient, Client
from ...models.empty_response import EmptyResponse
from ...models.error_envelope import ErrorEnvelope
from ...types import Response


def _get_kwargs(
    build_id: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/v2/images/builds/{build_id}/history".format(
            build_id=quote(str(build_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> EmptyResponse | ErrorEnvelope:
    if response.status_code == 200:
        response_200 = EmptyResponse.from_dict(response.json())

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
) -> Response[EmptyResponse | ErrorEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    build_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[EmptyResponse | ErrorEnvelope]:
    """Dismiss a terminal Runtime Image build from recent history

    Args:
        build_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EmptyResponse | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        build_id=build_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    build_id: UUID,
    *,
    client: AuthenticatedClient,
) -> EmptyResponse | ErrorEnvelope | None:
    """Dismiss a terminal Runtime Image build from recent history

    Args:
        build_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EmptyResponse | ErrorEnvelope
    """

    return sync_detailed(
        build_id=build_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    build_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[EmptyResponse | ErrorEnvelope]:
    """Dismiss a terminal Runtime Image build from recent history

    Args:
        build_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EmptyResponse | ErrorEnvelope]
    """

    kwargs = _get_kwargs(
        build_id=build_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    build_id: UUID,
    *,
    client: AuthenticatedClient,
) -> EmptyResponse | ErrorEnvelope | None:
    """Dismiss a terminal Runtime Image build from recent history

    Args:
        build_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EmptyResponse | ErrorEnvelope
    """

    return (
        await asyncio_detailed(
            build_id=build_id,
            client=client,
        )
    ).parsed
