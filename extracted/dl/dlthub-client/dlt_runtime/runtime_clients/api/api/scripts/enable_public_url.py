from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.enable_public_url_response_409 import EnablePublicUrlResponse409
from ...models.error_response_400 import ErrorResponse400
from ...models.error_response_401 import ErrorResponse401
from ...models.error_response_403 import ErrorResponse403
from ...models.error_response_404 import ErrorResponse404
from ...models.script_response import ScriptResponse
from ...types import Response


def _get_kwargs(
    workspace_id: UUID,
    script_id_or_ref: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/workspaces/{workspace_id}/scripts/{script_id_or_ref}/public-url".format(
            workspace_id=quote(str(workspace_id), safe=""),
            script_id_or_ref=quote(str(script_id_or_ref), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    EnablePublicUrlResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ScriptResponse
    | None
):
    if response.status_code == 201:
        response_201 = ScriptResponse.from_dict(response.json())

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

    if response.status_code == 409:
        response_409 = EnablePublicUrlResponse409.from_dict(response.json())

        return response_409

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    EnablePublicUrlResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ScriptResponse
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
) -> Response[
    EnablePublicUrlResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ScriptResponse
]:
    """EnablePublicUrl


    Enables or regenerates the public URL for a script. This creates a new public_secret UUID
    that can be used to access the script without authentication. Calling this endpoint again
    will generate a new UUID, invalidating any previous public URLs.

    Requires WRITE permission on the organization level.

    Args:
        workspace_id (UUID):
        script_id_or_ref (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EnablePublicUrlResponse409 | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ScriptResponse]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        script_id_or_ref=script_id_or_ref,
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
) -> (
    EnablePublicUrlResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ScriptResponse
    | None
):
    """EnablePublicUrl


    Enables or regenerates the public URL for a script. This creates a new public_secret UUID
    that can be used to access the script without authentication. Calling this endpoint again
    will generate a new UUID, invalidating any previous public URLs.

    Requires WRITE permission on the organization level.

    Args:
        workspace_id (UUID):
        script_id_or_ref (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EnablePublicUrlResponse409 | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ScriptResponse
    """

    return sync_detailed(
        workspace_id=workspace_id,
        script_id_or_ref=script_id_or_ref,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    script_id_or_ref: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[
    EnablePublicUrlResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ScriptResponse
]:
    """EnablePublicUrl


    Enables or regenerates the public URL for a script. This creates a new public_secret UUID
    that can be used to access the script without authentication. Calling this endpoint again
    will generate a new UUID, invalidating any previous public URLs.

    Requires WRITE permission on the organization level.

    Args:
        workspace_id (UUID):
        script_id_or_ref (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EnablePublicUrlResponse409 | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ScriptResponse]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        script_id_or_ref=script_id_or_ref,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    script_id_or_ref: str,
    *,
    client: AuthenticatedClient | Client,
) -> (
    EnablePublicUrlResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ScriptResponse
    | None
):
    """EnablePublicUrl


    Enables or regenerates the public URL for a script. This creates a new public_secret UUID
    that can be used to access the script without authentication. Calling this endpoint again
    will generate a new UUID, invalidating any previous public URLs.

    Requires WRITE permission on the organization level.

    Args:
        workspace_id (UUID):
        script_id_or_ref (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EnablePublicUrlResponse409 | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ScriptResponse
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            script_id_or_ref=script_id_or_ref,
            client=client,
        )
    ).parsed
