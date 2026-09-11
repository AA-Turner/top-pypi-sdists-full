from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.detailed_script_response import DetailedScriptResponse
from ...models.error_response_400 import ErrorResponse400
from ...models.error_response_401 import ErrorResponse401
from ...models.error_response_403 import ErrorResponse403
from ...models.error_response_404 import ErrorResponse404
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace_id: UUID,
    script_id_or_ref: str,
    *,
    recent_runs_limit: int | None | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_recent_runs_limit: int | None | Unset
    if isinstance(recent_runs_limit, Unset):
        json_recent_runs_limit = UNSET
    else:
        json_recent_runs_limit = recent_runs_limit
    params["recent_runs_limit"] = json_recent_runs_limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/workspaces/{workspace_id}/scripts/{script_id_or_ref}".format(
            workspace_id=quote(str(workspace_id), safe=""),
            script_id_or_ref=quote(str(script_id_or_ref), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    DetailedScriptResponse
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | None
):
    if response.status_code == 200:
        response_200 = DetailedScriptResponse.from_dict(response.json())

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
    DetailedScriptResponse
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: UUID,
    script_id_or_ref: str,
    *,
    client: AuthenticatedClient | Client,
    recent_runs_limit: int | None | Unset = UNSET,
) -> Response[
    DetailedScriptResponse
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
]:
    """GetScript

    Gets a script for a workspace, either by ID or by script name.

    Requires READ permission on the organization level.

    Args:
        workspace_id (UUID):
        script_id_or_ref (str):
        recent_runs_limit (int | None | Unset): Attach this many of the job's most recent runs.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DetailedScriptResponse | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        script_id_or_ref=script_id_or_ref,
        recent_runs_limit=recent_runs_limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: UUID,
    script_id_or_ref: str,
    *,
    client: AuthenticatedClient | Client,
    recent_runs_limit: int | None | Unset = UNSET,
) -> (
    DetailedScriptResponse
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | None
):
    """GetScript

    Gets a script for a workspace, either by ID or by script name.

    Requires READ permission on the organization level.

    Args:
        workspace_id (UUID):
        script_id_or_ref (str):
        recent_runs_limit (int | None | Unset): Attach this many of the job's most recent runs.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DetailedScriptResponse | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404
    """
    return sync_detailed(
        workspace_id=workspace_id,
        script_id_or_ref=script_id_or_ref,
        client=client,
        recent_runs_limit=recent_runs_limit,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    script_id_or_ref: str,
    *,
    client: AuthenticatedClient | Client,
    recent_runs_limit: int | None | Unset = UNSET,
) -> Response[
    DetailedScriptResponse
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
]:
    """GetScript

    Gets a script for a workspace, either by ID or by script name.

    Requires READ permission on the organization level.

    Args:
        workspace_id (UUID):
        script_id_or_ref (str):
        recent_runs_limit (int | None | Unset): Attach this many of the job's most recent runs.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DetailedScriptResponse | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        script_id_or_ref=script_id_or_ref,
        recent_runs_limit=recent_runs_limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    script_id_or_ref: str,
    *,
    client: AuthenticatedClient | Client,
    recent_runs_limit: int | None | Unset = UNSET,
) -> (
    DetailedScriptResponse
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | None
):
    """GetScript

    Gets a script for a workspace, either by ID or by script name.

    Requires READ permission on the organization level.

    Args:
        workspace_id (UUID):
        script_id_or_ref (str):
        recent_runs_limit (int | None | Unset): Attach this many of the job's most recent runs.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DetailedScriptResponse | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404
    """
    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            script_id_or_ref=script_id_or_ref,
            client=client,
            recent_runs_limit=recent_runs_limit,
        )
    ).parsed
