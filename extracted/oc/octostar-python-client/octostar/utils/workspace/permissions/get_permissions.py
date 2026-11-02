import logging
from typing import List, Union

logger = logging.getLogger(__name__)

from .PermissionLevel import PermissionLevel
from ....api.workspace_permissions import get_permissions
from ....client import Client
from ...exceptions import ApiConnectionError


def _parse_permissions_response(response, client):
    """Parse the permissions response."""
    if response.status_code != 200:
        raise ApiConnectionError("get_permissions", response, client)

    parsed = response.parsed
    if parsed is None:
        raise ApiConnectionError("get_permissions", response, client)

    permissions_list = getattr(parsed, "additional_properties", {}).get("permissions")
    if permissions_list is None:
        raise ApiConnectionError("get_permissions", response, client)

    return {
        p["workspace"]: PermissionLevel(p["permission_level"])
        for p in permissions_list
        if "workspace" in p and "permission_level" in p
    }


def sync(os_workspace: Union[List[str], str], client: Client = None):
    """
    # Get permissions for workspaces

    Get the permissions for one or more workspaces.

    ## Arguments
    - `os_workspace`: The ID (or list of IDs) of the workspaces to find permissions for.
    - `client`: The Client with which to connect to Octostar, which is also the user for
                which the permissions are given. If None, the default one is used.

    ## Returns
    A dictionary, where each key is a workspace ID and each value is the permission
    level for that workspace.

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    if not isinstance(os_workspace, list):
        os_workspace = [os_workspace]
    response = get_permissions.sync_detailed(
        os_workspaces=",".join(os_workspace), client=client
    )
    return _parse_permissions_response(response, client)


async def asyncio(os_workspace: Union[List[str], str], client: Client = None):
    """
    # Get permissions for workspaces asynchronously

    Get asynchronously the permissions for one or more workspaces.

    ## Arguments
    - `os_workspace`: The ID (or list of IDs) of the workspaces to find permissions for.
    - `client`: The Client with which to connect to Octostar, which is also the user for
                which the permissions are given. If None, the default one is used.

    ## Returns
    A dictionary, where each key is a workspace ID and each value is the permission
    level for that workspace.

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    if not isinstance(os_workspace, list):
        os_workspace = [os_workspace]
    response = await get_permissions.asyncio_detailed(
        os_workspaces=",".join(os_workspace), client=client
    )
    return _parse_permissions_response(response, client)
