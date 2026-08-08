from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response_400 import ErrorResponse400
from ...models.variables_change import VariablesChange
from ...models.variables_change_response import VariablesChangeResponse
from ...types import Response


def _get_kwargs(
    workspace_id: UUID,
    *,
    body: VariablesChange,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/api/v1/workspaces/{workspace_id}/variables".format(
            workspace_id=quote(str(workspace_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse400 | VariablesChangeResponse | None:
    if response.status_code == 200:
        response_200 = VariablesChangeResponse.from_dict(response.json())

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
) -> Response[ErrorResponse400 | VariablesChangeResponse]:
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
    body: VariablesChange,
) -> Response[ErrorResponse400 | VariablesChangeResponse]:
    """ChangeWorkspaceVariables

     Create, update and delete variables in one scope, applied atomically. `profile` null targets the
    workspace-wide scope. Deleting a name that was not set is reported as `not_found` rather than
    failing the request.

    Args:
        workspace_id (UUID):
        body (VariablesChange):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | VariablesChangeResponse]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: VariablesChange,
) -> ErrorResponse400 | VariablesChangeResponse | None:
    """ChangeWorkspaceVariables

     Create, update and delete variables in one scope, applied atomically. `profile` null targets the
    workspace-wide scope. Deleting a name that was not set is reported as `not_found` rather than
    failing the request.

    Args:
        workspace_id (UUID):
        body (VariablesChange):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | VariablesChangeResponse
    """

    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: VariablesChange,
) -> Response[ErrorResponse400 | VariablesChangeResponse]:
    """ChangeWorkspaceVariables

     Create, update and delete variables in one scope, applied atomically. `profile` null targets the
    workspace-wide scope. Deleting a name that was not set is reported as `not_found` rather than
    failing the request.

    Args:
        workspace_id (UUID):
        body (VariablesChange):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | VariablesChangeResponse]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: VariablesChange,
) -> ErrorResponse400 | VariablesChangeResponse | None:
    """ChangeWorkspaceVariables

     Create, update and delete variables in one scope, applied atomically. `profile` null targets the
    workspace-wide scope. Deleting a name that was not set is reported as `not_found` rather than
    failing the request.

    Args:
        workspace_id (UUID):
        body (VariablesChange):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | VariablesChangeResponse
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            body=body,
        )
    ).parsed
