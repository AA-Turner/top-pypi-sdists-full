from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.update_workspace_role_overrides_json_body import UpdateWorkspaceRoleOverridesJsonBody
from ...types import Response


def _get_kwargs(
    workspace: str,
    *,
    json_body: UpdateWorkspaceRoleOverridesJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/workspaces/role_overrides".format(
            workspace=workspace,
        ),
        "json": json_json_body,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
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
    json_body: UpdateWorkspaceRoleOverridesJsonBody,
) -> Response[Any]:
    """Replace the workspace's role overrides

     Replaces the workspace's overrides of instance roles, and its workspace-only roles (EE). Refuses
    removing a workspace-only role still held or referenced, and a change exceeding an offline license's
    seat cap. Requires workspace admin privileges.

    Args:
        workspace (str):
        json_body (UpdateWorkspaceRoleOverridesJsonBody): A workspace's overrides keyed by role
            name; a name the instance does not define adds a workspace-only role (EE).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateWorkspaceRoleOverridesJsonBody,
) -> Response[Any]:
    """Replace the workspace's role overrides

     Replaces the workspace's overrides of instance roles, and its workspace-only roles (EE). Refuses
    removing a workspace-only role still held or referenced, and a change exceeding an offline license's
    seat cap. Requires workspace admin privileges.

    Args:
        workspace (str):
        json_body (UpdateWorkspaceRoleOverridesJsonBody): A workspace's overrides keyed by role
            name; a name the instance does not define adds a workspace-only role (EE).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
