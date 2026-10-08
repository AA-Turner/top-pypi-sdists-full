from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.deployment_response import DeploymentResponse
from ...models.error_response import ErrorResponse
from ...models.upload_deployment_request import UploadDeploymentRequest
from ...types import Response


def _get_kwargs(
    workspace_id: UUID,
    deployment_id: UUID,
    *,
    body: UploadDeploymentRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/workspaces/{workspace_id}/deployments/{deployment_id}/-upload".format(
            workspace_id=quote(str(workspace_id), safe=""),
            deployment_id=quote(str(deployment_id), safe=""),
        ),
    }

    _kwargs["files"] = body.to_multipart()

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DeploymentResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = DeploymentResponse.from_dict(response.json())

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

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[DeploymentResponse | ErrorResponse]:
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
    body: UploadDeploymentRequest,
) -> Response[DeploymentResponse | ErrorResponse]:
    """UploadDeploymentBytes

     Upload deployment tarball bytes. Auth: ``DataplaneUserJwt`` with ``deployment:upload`` grant on the
    URL ``deployment_id``. Server parses the tarball, stores it + the requirements + the files manifest
    in vault, then writes the row back to the CP API. Returns the freshly-created
    ``DeploymentResponse``.

    Args:
        workspace_id (UUID):
        deployment_id (UUID):
        body (UploadDeploymentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeploymentResponse | ErrorResponse]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        deployment_id=deployment_id,
        body=body,
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
    body: UploadDeploymentRequest,
) -> DeploymentResponse | ErrorResponse | None:
    """UploadDeploymentBytes

     Upload deployment tarball bytes. Auth: ``DataplaneUserJwt`` with ``deployment:upload`` grant on the
    URL ``deployment_id``. Server parses the tarball, stores it + the requirements + the files manifest
    in vault, then writes the row back to the CP API. Returns the freshly-created
    ``DeploymentResponse``.

    Args:
        workspace_id (UUID):
        deployment_id (UUID):
        body (UploadDeploymentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeploymentResponse | ErrorResponse
    """
    return sync_detailed(
        workspace_id=workspace_id,
        deployment_id=deployment_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    deployment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UploadDeploymentRequest,
) -> Response[DeploymentResponse | ErrorResponse]:
    """UploadDeploymentBytes

     Upload deployment tarball bytes. Auth: ``DataplaneUserJwt`` with ``deployment:upload`` grant on the
    URL ``deployment_id``. Server parses the tarball, stores it + the requirements + the files manifest
    in vault, then writes the row back to the CP API. Returns the freshly-created
    ``DeploymentResponse``.

    Args:
        workspace_id (UUID):
        deployment_id (UUID):
        body (UploadDeploymentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeploymentResponse | ErrorResponse]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        deployment_id=deployment_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    deployment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UploadDeploymentRequest,
) -> DeploymentResponse | ErrorResponse | None:
    """UploadDeploymentBytes

     Upload deployment tarball bytes. Auth: ``DataplaneUserJwt`` with ``deployment:upload`` grant on the
    URL ``deployment_id``. Server parses the tarball, stores it + the requirements + the files manifest
    in vault, then writes the row back to the CP API. Returns the freshly-created
    ``DeploymentResponse``.

    Args:
        workspace_id (UUID):
        deployment_id (UUID):
        body (UploadDeploymentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeploymentResponse | ErrorResponse
    """
    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            deployment_id=deployment_id,
            client=client,
            body=body,
        )
    ).parsed
