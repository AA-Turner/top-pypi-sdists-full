from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.settings_metadata_response import SettingsMetadataResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/metadata/settings/",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> SettingsMetadataResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = SettingsMetadataResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SettingsMetadataResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[SettingsMetadataResponse]:
    """Get overridable settings metadata

     Retrieves metadata for all settings that can be configured via the Constance backend. This includes
    setting keys, human-readable descriptions, default values, and types. This endpoint is publicly
    accessible.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SettingsMetadataResponse]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> SettingsMetadataResponse:
    """Get overridable settings metadata

     Retrieves metadata for all settings that can be configured via the Constance backend. This includes
    setting keys, human-readable descriptions, default values, and types. This endpoint is publicly
    accessible.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SettingsMetadataResponse
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[SettingsMetadataResponse]:
    """Get overridable settings metadata

     Retrieves metadata for all settings that can be configured via the Constance backend. This includes
    setting keys, human-readable descriptions, default values, and types. This endpoint is publicly
    accessible.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SettingsMetadataResponse]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> SettingsMetadataResponse:
    """Get overridable settings metadata

     Retrieves metadata for all settings that can be configured via the Constance backend. This includes
    setting keys, human-readable descriptions, default values, and types. This endpoint is publicly
    accessible.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SettingsMetadataResponse
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
