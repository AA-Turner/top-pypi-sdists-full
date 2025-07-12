import logging
import sys
from typing import List

import click
from click import shell_completion

from tecton._internals import metadata_service
from tecton.cli import printer
from tecton_core import conf
from tecton_proto.common import compute_identity__client_pb2 as compute_identity_pb2
from tecton_proto.data import workspace__client_pb2 as workspace_pb2
from tecton_proto.metadataservice import metadata_service__client_pb2 as metadata_service_pb2


logger = logging.getLogger(__name__)


def create_workspace(workspace_name: str, materializable: bool):
    request = metadata_service_pb2.CreateWorkspaceRequest(
        workspace_name=workspace_name, capabilities=workspace_pb2.WorkspaceCapabilities(materializable=materializable)
    )
    metadata_service.instance().CreateWorkspace(request)
    printer.safe_print(f'Created workspace "{workspace_name}".')


def update_workspace(
    workspace_name: str,
    capabilities: workspace_pb2.WorkspaceCapabilities,
    compute_identities: List[compute_identity_pb2.ComputeIdentity],
):
    request = metadata_service_pb2.UpdateWorkspaceRequest(
        workspace=workspace_name, capabilities=capabilities, compute_identities=compute_identities
    )
    metadata_service.instance().UpdateWorkspace(request)


def delete_workspace(workspace_name: str):
    request = metadata_service_pb2.DeleteWorkspaceRequest(workspace=workspace_name)
    response = metadata_service.instance().DeleteWorkspace(request)
    printer.safe_print(f'Deleted workspace "{workspace_name}, {response.message}".')


def get_workspace(workspace_name: str):
    request = metadata_service_pb2.GetWorkspaceRequest(workspace_name=workspace_name)
    response = metadata_service.instance().GetWorkspace(request)
    return response.workspace


def list_workspaces():
    request = metadata_service_pb2.ListWorkspacesRequest()
    response = metadata_service.instance().ListWorkspaces(request)
    return response.workspaces


def is_live_workspace(workspace_name: str) -> bool:
    request = metadata_service_pb2.GetWorkspaceRequest(workspace_name=workspace_name)
    response = metadata_service.instance().GetWorkspace(request)
    return response.workspace.capabilities.materializable


def check_workspace_exists(workspace_name: str):
    workspace_names = {w.name for w in list_workspaces()}
    if workspace_name not in workspace_names:
        printer.safe_print(
            f'Workspace "{workspace_name}" not found. Run `tecton workspace list` to see list of available workspaces.'
        )
        sys.exit(1)


class WorkspaceType(click.ParamType):
    name = "workspace"

    def shell_complete(self, ctx, param, incomplete):
        try:
            workspace_names = {w.name for w in list_workspaces()}
        except (Exception, SystemExit) as e:
            logger.error(f"\nTab-completion failed with error: {e}")
            return []

        return [shell_completion.CompletionItem(name) for name in workspace_names if name.startswith(incomplete)]


def switch_to_workspace(workspace_name: str):
    """
    Switch the selected workspace

    :param workspace_name: name of the workspace to switch to
    """
    conf.set("TECTON_WORKSPACE", workspace_name)
    conf.save_tecton_configs()
    printer.safe_print(f'Switched to workspace "{workspace_name}".')
