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
from ...models.list_scripts_archived import ListScriptsArchived
from ...models.list_scripts_response_200 import ListScriptsResponse200
from ...models.script_type import ScriptType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace_id: UUID,
    *,
    script_type: None | ScriptType | Unset = UNSET,
    archived: ListScriptsArchived | Unset = ListScriptsArchived.FALSE,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_script_type: None | str | Unset
    if isinstance(script_type, Unset):
        json_script_type = UNSET
    elif isinstance(script_type, ScriptType):
        json_script_type = script_type.value
    else:
        json_script_type = script_type
    params["script_type"] = json_script_type

    json_archived: str | Unset = UNSET
    if not isinstance(archived, Unset):
        json_archived = archived.value

    params["archived"] = json_archived

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/workspaces/{workspace_id}/scripts".format(
            workspace_id=quote(str(workspace_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ListScriptsResponse200
    | None
):
    if response.status_code == 200:
        response_200 = ListScriptsResponse200.from_dict(response.json())

        return response_200

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
    | ListScriptsResponse200
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
    script_type: None | ScriptType | Unset = UNSET,
    archived: ListScriptsArchived | Unset = ListScriptsArchived.FALSE,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ListScriptsResponse200
]:
    """ListScripts


    Gets all scripts for a workspace. Returns a paginated list of scripts ordered by name ascending. Can
    be filtered by script type (interactive or batch).

    Requires READ permission on the organization level.

    Args:
        workspace_id (UUID):
        script_type (None | ScriptType | Unset):
        archived (ListScriptsArchived | Unset):  Default: ListScriptsArchived.FALSE.
        limit (int | Unset): Maximum number of items to return. Default: 100.
        offset (int | Unset): Number of items to skip. Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ListScriptsResponse200]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        script_type=script_type,
        archived=archived,
        limit=limit,
        offset=offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    script_type: None | ScriptType | Unset = UNSET,
    archived: ListScriptsArchived | Unset = ListScriptsArchived.FALSE,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ListScriptsResponse200
    | None
):
    """ListScripts


    Gets all scripts for a workspace. Returns a paginated list of scripts ordered by name ascending. Can
    be filtered by script type (interactive or batch).

    Requires READ permission on the organization level.

    Args:
        workspace_id (UUID):
        script_type (None | ScriptType | Unset):
        archived (ListScriptsArchived | Unset):  Default: ListScriptsArchived.FALSE.
        limit (int | Unset): Maximum number of items to return. Default: 100.
        offset (int | Unset): Number of items to skip. Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ListScriptsResponse200
    """

    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
        script_type=script_type,
        archived=archived,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    script_type: None | ScriptType | Unset = UNSET,
    archived: ListScriptsArchived | Unset = ListScriptsArchived.FALSE,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ListScriptsResponse200
]:
    """ListScripts


    Gets all scripts for a workspace. Returns a paginated list of scripts ordered by name ascending. Can
    be filtered by script type (interactive or batch).

    Requires READ permission on the organization level.

    Args:
        workspace_id (UUID):
        script_type (None | ScriptType | Unset):
        archived (ListScriptsArchived | Unset):  Default: ListScriptsArchived.FALSE.
        limit (int | Unset): Maximum number of items to return. Default: 100.
        offset (int | Unset): Number of items to skip. Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ListScriptsResponse200]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        script_type=script_type,
        archived=archived,
        limit=limit,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    script_type: None | ScriptType | Unset = UNSET,
    archived: ListScriptsArchived | Unset = ListScriptsArchived.FALSE,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ListScriptsResponse200
    | None
):
    """ListScripts


    Gets all scripts for a workspace. Returns a paginated list of scripts ordered by name ascending. Can
    be filtered by script type (interactive or batch).

    Requires READ permission on the organization level.

    Args:
        workspace_id (UUID):
        script_type (None | ScriptType | Unset):
        archived (ListScriptsArchived | Unset):  Default: ListScriptsArchived.FALSE.
        limit (int | Unset): Maximum number of items to return. Default: 100.
        offset (int | Unset): Number of items to skip. Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ListScriptsResponse200
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            script_type=script_type,
            archived=archived,
            limit=limit,
            offset=offset,
        )
    ).parsed
