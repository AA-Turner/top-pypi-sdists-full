from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.export_installation_response_200 import ExportInstallationResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    installation_id: int,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/w/{workspace}/github_app/export/{installationId}".format(
            workspace=workspace,
            installationId=installation_id,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ExportInstallationResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ExportInstallationResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ExportInstallationResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    installation_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ExportInstallationResponse200]:
    """Export GitHub installation JWT token

     Exports the JWT token for a specific GitHub installation in the workspace

    Args:
        workspace (str):
        installation_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExportInstallationResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        installation_id=installation_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    installation_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ExportInstallationResponse200]:
    """Export GitHub installation JWT token

     Exports the JWT token for a specific GitHub installation in the workspace

    Args:
        workspace (str):
        installation_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExportInstallationResponse200
    """

    return sync_detailed(
        workspace=workspace,
        installation_id=installation_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    installation_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ExportInstallationResponse200]:
    """Export GitHub installation JWT token

     Exports the JWT token for a specific GitHub installation in the workspace

    Args:
        workspace (str):
        installation_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExportInstallationResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        installation_id=installation_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    installation_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ExportInstallationResponse200]:
    """Export GitHub installation JWT token

     Exports the JWT token for a specific GitHub installation in the workspace

    Args:
        workspace (str):
        installation_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExportInstallationResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            installation_id=installation_id,
            client=client,
        )
    ).parsed
