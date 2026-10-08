from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.issue_upload_configuration_response import (
    IssueUploadConfigurationResponse,
)
from ...types import Response


def _get_kwargs(
    workspace_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/workspaces/{workspace_id}/configurations/-issue-upload".format(
            workspace_id=quote(str(workspace_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | IssueUploadConfigurationResponse | None:
    if response.status_code == 200:
        response_200 = IssueUploadConfigurationResponse.from_dict(response.json())

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

    if response.status_code == 409:
        response_409 = ErrorResponse.from_dict(response.json())

        return response_409

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | IssueUploadConfigurationResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | IssueUploadConfigurationResponse]:
    """IssueUploadConfiguration

    Mint a short-lived ``DataplaneUserJwt`` (carrying a ``configuration:upload``
    grant, with the workspace taken from its signed binding) and return the
    absolute DP API URL where the
    tarball bytes are POSTed next. **No database row is created in this step**
    — the row is INSERTed by the DP API after vault store succeeds, via the
    ``dp-api → api CONFIGURATIONS_WRITE`` write-back edge.

    Requires WRITE permission on the workspace.

    Args:
        workspace_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | IssueUploadConfigurationResponse]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | IssueUploadConfigurationResponse | None:
    """IssueUploadConfiguration

    Mint a short-lived ``DataplaneUserJwt`` (carrying a ``configuration:upload``
    grant, with the workspace taken from its signed binding) and return the
    absolute DP API URL where the
    tarball bytes are POSTed next. **No database row is created in this step**
    — the row is INSERTed by the DP API after vault store succeeds, via the
    ``dp-api → api CONFIGURATIONS_WRITE`` write-back edge.

    Requires WRITE permission on the workspace.

    Args:
        workspace_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | IssueUploadConfigurationResponse
    """
    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | IssueUploadConfigurationResponse]:
    """IssueUploadConfiguration

    Mint a short-lived ``DataplaneUserJwt`` (carrying a ``configuration:upload``
    grant, with the workspace taken from its signed binding) and return the
    absolute DP API URL where the
    tarball bytes are POSTed next. **No database row is created in this step**
    — the row is INSERTed by the DP API after vault store succeeds, via the
    ``dp-api → api CONFIGURATIONS_WRITE`` write-back edge.

    Requires WRITE permission on the workspace.

    Args:
        workspace_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | IssueUploadConfigurationResponse]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | IssueUploadConfigurationResponse | None:
    """IssueUploadConfiguration

    Mint a short-lived ``DataplaneUserJwt`` (carrying a ``configuration:upload``
    grant, with the workspace taken from its signed binding) and return the
    absolute DP API URL where the
    tarball bytes are POSTed next. **No database row is created in this step**
    — the row is INSERTed by the DP API after vault store succeeds, via the
    ``dp-api → api CONFIGURATIONS_WRITE`` write-back edge.

    Requires WRITE permission on the workspace.

    Args:
        workspace_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | IssueUploadConfigurationResponse
    """
    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
        )
    ).parsed
