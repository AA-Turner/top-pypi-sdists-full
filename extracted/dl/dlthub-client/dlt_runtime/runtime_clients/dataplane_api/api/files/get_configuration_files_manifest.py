from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response_400 import ErrorResponse400
from ...models.t_files_manifest import TFilesManifest
from ...types import Response


def _get_kwargs(
    workspace_id: UUID,
    configuration_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/workspaces/{workspace_id}/configurations/{configuration_id}/files".format(
            workspace_id=quote(str(workspace_id), safe=""),
            configuration_id=quote(str(configuration_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse400 | TFilesManifest | None:
    if response.status_code == 200:
        response_200 = TFilesManifest.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse400.from_dict(response.json())

        return response_400

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse400 | TFilesManifest]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: UUID,
    configuration_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse400 | TFilesManifest]:
    """GetConfigurationFilesManifest

     Return the ``TFilesManifest`` for a configuration. Auth: ``DataplaneUserJwt`` with a ``ws:read``
    grant on the URL ``workspace_id``.

    Args:
        workspace_id (UUID):
        configuration_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | TFilesManifest]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        configuration_id=configuration_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: UUID,
    configuration_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse400 | TFilesManifest | None:
    """GetConfigurationFilesManifest

     Return the ``TFilesManifest`` for a configuration. Auth: ``DataplaneUserJwt`` with a ``ws:read``
    grant on the URL ``workspace_id``.

    Args:
        workspace_id (UUID):
        configuration_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | TFilesManifest
    """

    return sync_detailed(
        workspace_id=workspace_id,
        configuration_id=configuration_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    configuration_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse400 | TFilesManifest]:
    """GetConfigurationFilesManifest

     Return the ``TFilesManifest`` for a configuration. Auth: ``DataplaneUserJwt`` with a ``ws:read``
    grant on the URL ``workspace_id``.

    Args:
        workspace_id (UUID):
        configuration_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | TFilesManifest]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        configuration_id=configuration_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    configuration_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse400 | TFilesManifest | None:
    """GetConfigurationFilesManifest

     Return the ``TFilesManifest`` for a configuration. Auth: ``DataplaneUserJwt`` with a ``ws:read``
    grant on the URL ``workspace_id``.

    Args:
        workspace_id (UUID):
        configuration_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | TFilesManifest
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            configuration_id=configuration_id,
            client=client,
        )
    ).parsed
