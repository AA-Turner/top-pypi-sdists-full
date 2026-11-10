from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.hpc_workspace_overview import HpcWorkspaceOverview
from ...types import Response


def _get_kwargs(
    uuid: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/hpc-workspaces/{uuid}/",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> HpcWorkspaceOverview:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = HpcWorkspaceOverview.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[HpcWorkspaceOverview]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[HpcWorkspaceOverview]:
    """HPC workspace overview

     Allocation, the user's cluster identity and FirecREST system health. Problems reaching FirecREST are
    reported in 'error' rather than failing the request; 'sign_in_provider' names the identity provider
    to sign in through again when that is the remedy. Without FirecREST ('firecrest_enabled' false) the
    health is left out.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HpcWorkspaceOverview]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> HpcWorkspaceOverview:
    """HPC workspace overview

     Allocation, the user's cluster identity and FirecREST system health. Problems reaching FirecREST are
    reported in 'error' rather than failing the request; 'sign_in_provider' names the identity provider
    to sign in through again when that is the remedy. Without FirecREST ('firecrest_enabled' false) the
    health is left out.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HpcWorkspaceOverview
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[HpcWorkspaceOverview]:
    """HPC workspace overview

     Allocation, the user's cluster identity and FirecREST system health. Problems reaching FirecREST are
    reported in 'error' rather than failing the request; 'sign_in_provider' names the identity provider
    to sign in through again when that is the remedy. Without FirecREST ('firecrest_enabled' false) the
    health is left out.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HpcWorkspaceOverview]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> HpcWorkspaceOverview:
    """HPC workspace overview

     Allocation, the user's cluster identity and FirecREST system health. Problems reaching FirecREST are
    reported in 'error' rather than failing the request; 'sign_in_provider' names the identity provider
    to sign in through again when that is the remedy. Without FirecREST ('firecrest_enabled' false) the
    health is left out.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HpcWorkspaceOverview
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
        )
    ).parsed
