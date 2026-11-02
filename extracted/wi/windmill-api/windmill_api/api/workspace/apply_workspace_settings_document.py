from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.apply_workspace_settings_document_json_body import ApplyWorkspaceSettingsDocumentJsonBody
from ...models.apply_workspace_settings_document_response_200 import ApplyWorkspaceSettingsDocumentResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    *,
    json_body: ApplyWorkspaceSettingsDocumentJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/workspaces/settings_document".format(
            workspace=workspace,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ApplyWorkspaceSettingsDocumentResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ApplyWorkspaceSettingsDocumentResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ApplyWorkspaceSettingsDocumentResponse200]:
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
    json_body: ApplyWorkspaceSettingsDocumentJsonBody,
) -> Response[ApplyWorkspaceSettingsDocumentResponse200]:
    """apply a workspace settings document

     Applies a settings document, each setting through the endpoint that owns it. Admin only.

    Args:
        workspace (str):
        json_body (ApplyWorkspaceSettingsDocumentJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApplyWorkspaceSettingsDocumentResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ApplyWorkspaceSettingsDocumentJsonBody,
) -> Optional[ApplyWorkspaceSettingsDocumentResponse200]:
    """apply a workspace settings document

     Applies a settings document, each setting through the endpoint that owns it. Admin only.

    Args:
        workspace (str):
        json_body (ApplyWorkspaceSettingsDocumentJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApplyWorkspaceSettingsDocumentResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ApplyWorkspaceSettingsDocumentJsonBody,
) -> Response[ApplyWorkspaceSettingsDocumentResponse200]:
    """apply a workspace settings document

     Applies a settings document, each setting through the endpoint that owns it. Admin only.

    Args:
        workspace (str):
        json_body (ApplyWorkspaceSettingsDocumentJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApplyWorkspaceSettingsDocumentResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ApplyWorkspaceSettingsDocumentJsonBody,
) -> Optional[ApplyWorkspaceSettingsDocumentResponse200]:
    """apply a workspace settings document

     Applies a settings document, each setting through the endpoint that owns it. Admin only.

    Args:
        workspace (str):
        json_body (ApplyWorkspaceSettingsDocumentJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApplyWorkspaceSettingsDocumentResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            json_body=json_body,
        )
    ).parsed
