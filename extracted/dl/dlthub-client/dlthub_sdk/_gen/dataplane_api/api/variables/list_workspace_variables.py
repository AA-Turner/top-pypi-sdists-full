from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.workspace_variables_response import WorkspaceVariablesResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace_id: UUID,
    *,
    scope_profile: None | str | Unset = UNSET,
    is_workspace_scope: bool | None | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_scope_profile: None | str | Unset
    if isinstance(scope_profile, Unset):
        json_scope_profile = UNSET
    else:
        json_scope_profile = scope_profile
    params["scope_profile"] = json_scope_profile

    json_is_workspace_scope: bool | None | Unset
    if isinstance(is_workspace_scope, Unset):
        json_is_workspace_scope = UNSET
    else:
        json_is_workspace_scope = is_workspace_scope
    params["is_workspace_scope"] = json_is_workspace_scope

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
) -> ErrorResponse | WorkspaceVariablesResponse | None:
    if response.status_code == 200:
        response_200 = WorkspaceVariablesResponse.from_dict(response.json())

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
) -> Response[ErrorResponse | WorkspaceVariablesResponse]:
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
    scope_profile: None | str | Unset = UNSET,
    is_workspace_scope: bool | None | Unset = UNSET,
) -> Response[ErrorResponse | WorkspaceVariablesResponse]:
    """ListWorkspaceVariables

     Every scope in one response, or a single scope with `scope_profile` or `is_workspace_scope=true`.
    Secret values always come back `null`, and a scope holding nothing reads as an empty list rather
    than a 404. Requires the `ws:variables-read` grant, which a workspace owner and a run's agent can
    obtain.

    Args:
        workspace_id (UUID):
        scope_profile (None | str | Unset):
        is_workspace_scope (bool | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | WorkspaceVariablesResponse]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        scope_profile=scope_profile,
        is_workspace_scope=is_workspace_scope,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    scope_profile: None | str | Unset = UNSET,
    is_workspace_scope: bool | None | Unset = UNSET,
) -> ErrorResponse | WorkspaceVariablesResponse | None:
    """ListWorkspaceVariables

     Every scope in one response, or a single scope with `scope_profile` or `is_workspace_scope=true`.
    Secret values always come back `null`, and a scope holding nothing reads as an empty list rather
    than a 404. Requires the `ws:variables-read` grant, which a workspace owner and a run's agent can
    obtain.

    Args:
        workspace_id (UUID):
        scope_profile (None | str | Unset):
        is_workspace_scope (bool | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | WorkspaceVariablesResponse
    """
    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
        scope_profile=scope_profile,
        is_workspace_scope=is_workspace_scope,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    scope_profile: None | str | Unset = UNSET,
    is_workspace_scope: bool | None | Unset = UNSET,
) -> Response[ErrorResponse | WorkspaceVariablesResponse]:
    """ListWorkspaceVariables

     Every scope in one response, or a single scope with `scope_profile` or `is_workspace_scope=true`.
    Secret values always come back `null`, and a scope holding nothing reads as an empty list rather
    than a 404. Requires the `ws:variables-read` grant, which a workspace owner and a run's agent can
    obtain.

    Args:
        workspace_id (UUID):
        scope_profile (None | str | Unset):
        is_workspace_scope (bool | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | WorkspaceVariablesResponse]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        scope_profile=scope_profile,
        is_workspace_scope=is_workspace_scope,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    scope_profile: None | str | Unset = UNSET,
    is_workspace_scope: bool | None | Unset = UNSET,
) -> ErrorResponse | WorkspaceVariablesResponse | None:
    """ListWorkspaceVariables

     Every scope in one response, or a single scope with `scope_profile` or `is_workspace_scope=true`.
    Secret values always come back `null`, and a scope holding nothing reads as an empty list rather
    than a 404. Requires the `ws:variables-read` grant, which a workspace owner and a run's agent can
    obtain.

    Args:
        workspace_id (UUID):
        scope_profile (None | str | Unset):
        is_workspace_scope (bool | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | WorkspaceVariablesResponse
    """
    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            scope_profile=scope_profile,
            is_workspace_scope=is_workspace_scope,
        )
    ).parsed
