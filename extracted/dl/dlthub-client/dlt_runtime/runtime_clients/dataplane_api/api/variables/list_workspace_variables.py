from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response_400 import ErrorResponse400
from ...models.workspace_variables_response import WorkspaceVariablesResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace_id: UUID,
    *,
    profile: None | str | Unset = UNSET,
    workspace: bool | None | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_profile: None | str | Unset
    if isinstance(profile, Unset):
        json_profile = UNSET
    else:
        json_profile = profile
    params["profile"] = json_profile

    json_workspace: bool | None | Unset
    if isinstance(workspace, Unset):
        json_workspace = UNSET
    else:
        json_workspace = workspace
    params["workspace"] = json_workspace

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/workspaces/{workspace_id}/variables".format(
            workspace_id=quote(str(workspace_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse400 | WorkspaceVariablesResponse | None:
    if response.status_code == 200:
        response_200 = WorkspaceVariablesResponse.from_dict(response.json())

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
) -> Response[ErrorResponse400 | WorkspaceVariablesResponse]:
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
    profile: None | str | Unset = UNSET,
    workspace: bool | None | Unset = UNSET,
) -> Response[ErrorResponse400 | WorkspaceVariablesResponse]:
    """ListWorkspaceVariables

     Every scope in one response, or a single scope with `profile` or `workspace=true`. Secret values
    always come back `null`, and a scope holding nothing reads as an empty list rather than a 404.
    Requires a workspace variables token, which only a workspace owner can obtain.

    Args:
        workspace_id (UUID):
        profile (None | str | Unset):
        workspace (bool | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | WorkspaceVariablesResponse]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        profile=profile,
        workspace=workspace,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    profile: None | str | Unset = UNSET,
    workspace: bool | None | Unset = UNSET,
) -> ErrorResponse400 | WorkspaceVariablesResponse | None:
    """ListWorkspaceVariables

     Every scope in one response, or a single scope with `profile` or `workspace=true`. Secret values
    always come back `null`, and a scope holding nothing reads as an empty list rather than a 404.
    Requires a workspace variables token, which only a workspace owner can obtain.

    Args:
        workspace_id (UUID):
        profile (None | str | Unset):
        workspace (bool | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | WorkspaceVariablesResponse
    """

    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
        profile=profile,
        workspace=workspace,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    profile: None | str | Unset = UNSET,
    workspace: bool | None | Unset = UNSET,
) -> Response[ErrorResponse400 | WorkspaceVariablesResponse]:
    """ListWorkspaceVariables

     Every scope in one response, or a single scope with `profile` or `workspace=true`. Secret values
    always come back `null`, and a scope holding nothing reads as an empty list rather than a 404.
    Requires a workspace variables token, which only a workspace owner can obtain.

    Args:
        workspace_id (UUID):
        profile (None | str | Unset):
        workspace (bool | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | WorkspaceVariablesResponse]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        profile=profile,
        workspace=workspace,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    profile: None | str | Unset = UNSET,
    workspace: bool | None | Unset = UNSET,
) -> ErrorResponse400 | WorkspaceVariablesResponse | None:
    """ListWorkspaceVariables

     Every scope in one response, or a single scope with `profile` or `workspace=true`. Secret values
    always come back `null`, and a scope holding nothing reads as an empty list rather than a 404.
    Requires a workspace variables token, which only a workspace owner can obtain.

    Args:
        workspace_id (UUID):
        profile (None | str | Unset):
        workspace (bool | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | WorkspaceVariablesResponse
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            profile=profile,
            workspace=workspace,
        )
    ).parsed
