from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.manifest_files_response import ManifestFilesResponse
from ...types import Response


def _get_kwargs(
    workspace_id: UUID,
    deployment_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/workspaces/{workspace_id}/deployments/{deployment_id}/files".format(
            workspace_id=quote(str(workspace_id), safe=""),
            deployment_id=quote(str(deployment_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | ManifestFilesResponse | None:
    if response.status_code == 200:
        response_200 = ManifestFilesResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | ManifestFilesResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: UUID,
    deployment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | ManifestFilesResponse]:
    """GetDeploymentFilesManifest

     Return the files manifest for a deployment. Auth: ``DataplaneUserJwt`` with a ``ws:read`` grant on
    the URL ``workspace_id``.

    Args:
        workspace_id (UUID):
        deployment_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ManifestFilesResponse]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        deployment_id=deployment_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: UUID,
    deployment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | ManifestFilesResponse | None:
    """GetDeploymentFilesManifest

     Return the files manifest for a deployment. Auth: ``DataplaneUserJwt`` with a ``ws:read`` grant on
    the URL ``workspace_id``.

    Args:
        workspace_id (UUID):
        deployment_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ManifestFilesResponse
    """
    return sync_detailed(
        workspace_id=workspace_id,
        deployment_id=deployment_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    deployment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | ManifestFilesResponse]:
    """GetDeploymentFilesManifest

     Return the files manifest for a deployment. Auth: ``DataplaneUserJwt`` with a ``ws:read`` grant on
    the URL ``workspace_id``.

    Args:
        workspace_id (UUID):
        deployment_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ManifestFilesResponse]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        deployment_id=deployment_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    deployment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | ManifestFilesResponse | None:
    """GetDeploymentFilesManifest

     Return the files manifest for a deployment. Auth: ``DataplaneUserJwt`` with a ``ws:read`` grant on
    the URL ``workspace_id``.

    Args:
        workspace_id (UUID):
        deployment_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ManifestFilesResponse
    """
    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            deployment_id=deployment_id,
            client=client,
        )
    ).parsed
