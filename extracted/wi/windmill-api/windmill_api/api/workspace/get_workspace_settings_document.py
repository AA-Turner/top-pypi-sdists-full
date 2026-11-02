from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_workspace_settings_document_response_200 import GetWorkspaceSettingsDocumentResponse200
from ...models.get_workspace_settings_document_secrets import GetWorkspaceSettingsDocumentSecrets
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    secrets: Union[Unset, None, GetWorkspaceSettingsDocumentSecrets] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    json_secrets: Union[Unset, None, str] = UNSET
    if not isinstance(secrets, Unset):
        json_secrets = secrets.value if secrets else None

    params["secrets"] = json_secrets

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/workspaces/settings_document".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetWorkspaceSettingsDocumentResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetWorkspaceSettingsDocumentResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetWorkspaceSettingsDocumentResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    secrets: Union[Unset, None, GetWorkspaceSettingsDocumentSecrets] = UNSET,
) -> Response[GetWorkspaceSettingsDocumentResponse200]:
    """get the workspace settings document

     The workspace's settings in the layout of the settings.yaml that `wmill sync` writes. Admin only.

    Args:
        workspace (str):
        secrets (Union[Unset, None, GetWorkspaceSettingsDocumentSecrets]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetWorkspaceSettingsDocumentResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        secrets=secrets,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    secrets: Union[Unset, None, GetWorkspaceSettingsDocumentSecrets] = UNSET,
) -> Optional[GetWorkspaceSettingsDocumentResponse200]:
    """get the workspace settings document

     The workspace's settings in the layout of the settings.yaml that `wmill sync` writes. Admin only.

    Args:
        workspace (str):
        secrets (Union[Unset, None, GetWorkspaceSettingsDocumentSecrets]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetWorkspaceSettingsDocumentResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        secrets=secrets,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    secrets: Union[Unset, None, GetWorkspaceSettingsDocumentSecrets] = UNSET,
) -> Response[GetWorkspaceSettingsDocumentResponse200]:
    """get the workspace settings document

     The workspace's settings in the layout of the settings.yaml that `wmill sync` writes. Admin only.

    Args:
        workspace (str):
        secrets (Union[Unset, None, GetWorkspaceSettingsDocumentSecrets]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetWorkspaceSettingsDocumentResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        secrets=secrets,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    secrets: Union[Unset, None, GetWorkspaceSettingsDocumentSecrets] = UNSET,
) -> Optional[GetWorkspaceSettingsDocumentResponse200]:
    """get the workspace settings document

     The workspace's settings in the layout of the settings.yaml that `wmill sync` writes. Admin only.

    Args:
        workspace (str):
        secrets (Union[Unset, None, GetWorkspaceSettingsDocumentSecrets]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetWorkspaceSettingsDocumentResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            secrets=secrets,
        )
    ).parsed
