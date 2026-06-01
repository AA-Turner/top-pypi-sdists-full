from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.error_response import ErrorResponse
from ...models.put_user_settings_key_body import PutUserSettingsKeyBody
from ...models.put_user_settings_key_response_put_user_settings_key import PutUserSettingsKeyResponsePutUserSettingsKey


def _get_kwargs(
    key: str,
    *,
    body: PutUserSettingsKeyBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/v1/users/current/settings/{key}".format(
            key=quote(str(key), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/vnd.api+json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | PutUserSettingsKeyResponsePutUserSettingsKey | None:
    if response.status_code == 200:
        response_200 = PutUserSettingsKeyResponsePutUserSettingsKey.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = ErrorResponse.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | PutUserSettingsKeyResponsePutUserSettingsKey]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    key: str,
    *,
    client: AuthenticatedClient,
    body: PutUserSettingsKeyBody,
) -> Response[ErrorResponse | PutUserSettingsKeyResponsePutUserSettingsKey]:
    """Update User Setting by Key

     Set a single key in the current user's settings. The key is stored as a flat literal key (dot-
    notation is NOT expanded to nested paths). Returns the full updated settings object.

    Args:
        key (str):
        body (PutUserSettingsKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | PutUserSettingsKeyResponsePutUserSettingsKey]
    """

    kwargs = _get_kwargs(
        key=key,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    key: str,
    *,
    client: AuthenticatedClient,
    body: PutUserSettingsKeyBody,
) -> ErrorResponse | PutUserSettingsKeyResponsePutUserSettingsKey | None:
    """Update User Setting by Key

     Set a single key in the current user's settings. The key is stored as a flat literal key (dot-
    notation is NOT expanded to nested paths). Returns the full updated settings object.

    Args:
        key (str):
        body (PutUserSettingsKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | PutUserSettingsKeyResponsePutUserSettingsKey
    """

    return sync_detailed(
        key=key,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    key: str,
    *,
    client: AuthenticatedClient,
    body: PutUserSettingsKeyBody,
) -> Response[ErrorResponse | PutUserSettingsKeyResponsePutUserSettingsKey]:
    """Update User Setting by Key

     Set a single key in the current user's settings. The key is stored as a flat literal key (dot-
    notation is NOT expanded to nested paths). Returns the full updated settings object.

    Args:
        key (str):
        body (PutUserSettingsKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | PutUserSettingsKeyResponsePutUserSettingsKey]
    """

    kwargs = _get_kwargs(
        key=key,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    key: str,
    *,
    client: AuthenticatedClient,
    body: PutUserSettingsKeyBody,
) -> ErrorResponse | PutUserSettingsKeyResponsePutUserSettingsKey | None:
    """Update User Setting by Key

     Set a single key in the current user's settings. The key is stored as a flat literal key (dot-
    notation is NOT expanded to nested paths). Returns the full updated settings object.

    Args:
        key (str):
        body (PutUserSettingsKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | PutUserSettingsKeyResponsePutUserSettingsKey
    """

    return (
        await asyncio_detailed(
            key=key,
            client=client,
            body=body,
        )
    ).parsed
