from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response_400 import ErrorResponse400
from ...models.interactive_url_response import InteractiveUrlResponse
from ...types import Response


def _get_kwargs(
    workspace_id: UUID,
    run_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/workspaces/{workspace_id}/runs/{run_id}/interactive-url".format(
            workspace_id=quote(str(workspace_id), safe=""),
            run_id=quote(str(run_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ErrorResponse400 | InteractiveUrlResponse | None:
    if response.status_code == 200:
        response_200 = InteractiveUrlResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ErrorResponse400 | InteractiveUrlResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: UUID,
    run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | ErrorResponse400 | InteractiveUrlResponse]:
    """GetRunInteractiveUrl

     Return a PASETO-signed interactive URL. Auth: ``DataplaneUserJwt`` with a ``ws:read`` grant on the
    URL ``workspace_id``.

    Args:
        workspace_id (UUID):
        run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorResponse400 | InteractiveUrlResponse]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        run_id=run_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: UUID,
    run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Any | ErrorResponse400 | InteractiveUrlResponse | None:
    """GetRunInteractiveUrl

     Return a PASETO-signed interactive URL. Auth: ``DataplaneUserJwt`` with a ``ws:read`` grant on the
    URL ``workspace_id``.

    Args:
        workspace_id (UUID):
        run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorResponse400 | InteractiveUrlResponse
    """

    return sync_detailed(
        workspace_id=workspace_id,
        run_id=run_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | ErrorResponse400 | InteractiveUrlResponse]:
    """GetRunInteractiveUrl

     Return a PASETO-signed interactive URL. Auth: ``DataplaneUserJwt`` with a ``ws:read`` grant on the
    URL ``workspace_id``.

    Args:
        workspace_id (UUID):
        run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorResponse400 | InteractiveUrlResponse]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        run_id=run_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Any | ErrorResponse400 | InteractiveUrlResponse | None:
    """GetRunInteractiveUrl

     Return a PASETO-signed interactive URL. Auth: ``DataplaneUserJwt`` with a ``ws:read`` grant on the
    URL ``workspace_id``.

    Args:
        workspace_id (UUID):
        run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorResponse400 | InteractiveUrlResponse
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            run_id=run_id,
            client=client,
        )
    ).parsed
