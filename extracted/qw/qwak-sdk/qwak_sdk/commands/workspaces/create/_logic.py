from _qwak_proto.qwak.instance_template.instance_template_pb2 import InstanceType
from _qwak_proto.qwak.workspace.workspace_pb2 import DefaultWorkspaceDetails
from qwak.clients.instance_template.client import InstanceTemplateManagementClient
from qwak.clients.workspace_manager import WorkspaceManagerClient

from qwak_sdk.commands.workspaces._logic.workspace_validations import (
    _validate_workspace_name,
    _verify_image_id,
    _verify_instance,
)
from qwak_sdk.commands.workspaces.config.workspace_config import WorkspaceConfig


def _create_workspace(config: WorkspaceConfig):
    """
    Creating a new workspace

    Args:
        config: The workspace configuration

    """
    print(f"Creating a new workspace with the name {config.workspace.name}")
    workspace_manager_client = WorkspaceManagerClient()
    default_details: DefaultWorkspaceDetails = (
        workspace_manager_client.get_default_workspace_details()
    )

    _validate_workspace_name(config.workspace.name)
    if config.workspace.instance:
        _verify_instance(config.workspace.instance)
    else:
        config.workspace.instance = (
            default_details.cpu_compute_resources.template_spec.template_id
        )

    if config.workspace.image:
        _verify_image_id(config.workspace.image, workspace_manager_client)
    else:
        instance_spec = InstanceTemplateManagementClient().get_instance_template(
            config.workspace.instance
        )
        config.workspace.image = (
            default_details.cpu_image_id
            if instance_spec.instance_type == InstanceType.INSTANCE_TYPE_CPU
            else default_details.gpu_image_id
        )

    response = workspace_manager_client.create_workspace(
        config.workspace.name, config.workspace.image, config.workspace.instance
    )

    print(
        f"Workspace {config.workspace.name} was created successfully with id: {response.workspace_id}"
    )
