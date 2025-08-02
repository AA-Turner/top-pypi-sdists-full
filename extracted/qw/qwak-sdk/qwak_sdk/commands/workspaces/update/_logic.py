from qwak.clients.workspace_manager import WorkspaceManagerClient

from qwak_sdk.commands.workspaces._logic.tools import get_workspace_by_name
from qwak_sdk.commands.workspaces._logic.workspace_validations import (
    _validate_workspace_name,
    _verify_image_id,
    _verify_instance,
    validate_id_or_name,
)
from qwak_sdk.commands.workspaces.config.workspace_config import WorkspaceConfig


def _update_workspace(config: WorkspaceConfig):
    """
    Updating a workspace

    Args:
        config: The workspace configuration

    """
    validate_id_or_name(
        workspace_id=config.workspace.workspace_id, workspace_name=config.workspace.name
    )
    workspace_manager_client = WorkspaceManagerClient()
    if config.workspace.workspace_id:
        print(
            f"Updating a workspace with the workspace id {config.workspace.workspace_id}"
        )
        current_workspace = workspace_manager_client.get_workspace_by_id(
            workspace_id=config.workspace.workspace_id
        ).workspace
    else:
        print(f"Updating a workspace with the workspace name {config.workspace.name}")
        current_workspace = get_workspace_by_name(
            workspace_name=config.workspace.name,
            workspace_manager_client=workspace_manager_client,
        )

    workspace_id = current_workspace.workspace_id
    workspace_name = config.workspace.name
    image_id = config.workspace.image
    instance = config.workspace.instance

    if _is_not_empty_and_not_none(workspace_name):
        _validate_workspace_name(workspace_name)

    if _is_not_empty_and_not_none(image_id):
        _verify_image_id(image_id, workspace_manager_client)

    if _is_not_empty_and_not_none(instance):
        _verify_instance(instance)

    name = (
        workspace_name
        if _is_not_empty_and_not_none(workspace_name)
        else current_workspace.workspace_name
    )
    image_id = (
        image_id if _is_not_empty_and_not_none(image_id) else current_workspace.image_id
    )

    instance = (
        instance
        if _is_not_empty_and_not_none(instance)
        else current_workspace.client_pod_compute_resources.template_spec.template_id
    )

    workspace_manager_client.update_workspace(
        workspace_id=workspace_id,
        image_id=image_id,
        template_id=instance,
        workspace_name=name,
    )

    if config.workspace.workspace_id:
        print(f"Workspace {workspace_id} was updated successfully")
    else:
        print(f"Workspace {workspace_name} was updated successfully")


def _is_not_empty_and_not_none(value: str) -> bool:
    return value is not None and value != ""
