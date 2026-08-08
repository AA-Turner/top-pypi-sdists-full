from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response_400 import ErrorResponse400
from ...models.error_response_401 import ErrorResponse401
from ...models.error_response_403 import ErrorResponse403
from ...models.error_response_404 import ErrorResponse404
from ...models.upload_initiated_response import UploadInitiatedResponse
from ...types import Response


def _get_kwargs(
    workspace_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/workspaces/{workspace_id}/configurations".format(
            workspace_id=quote(str(workspace_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | UploadInitiatedResponse
    | None
):
    if response.status_code == 201:
        response_201 = UploadInitiatedResponse.from_dict(response.json())

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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | UploadInitiatedResponse
]:
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
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | UploadInitiatedResponse
]:
    """CreateConfiguration


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
        Response[ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | UploadInitiatedResponse]
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
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | UploadInitiatedResponse
    | None
):
    """CreateConfiguration


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
        ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | UploadInitiatedResponse
    """

    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | UploadInitiatedResponse
]:
    """CreateConfiguration


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
        Response[ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | UploadInitiatedResponse]
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
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | UploadInitiatedResponse
    | None
):
    """CreateConfiguration


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
        ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | UploadInitiatedResponse
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
        )
    ).parsed
