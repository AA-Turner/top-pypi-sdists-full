import os
import shlex
import subprocess
from typing import Any, List, Optional

import click
import tabulate

from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client.models.create_experimental_workspace import (
    CreateExperimentalWorkspace,
)
from anyscale.client.openapi_client.models.experimental_workspace import (
    ExperimentalWorkspace,
)
from anyscale.controllers.base_controller import BaseController
from anyscale.feature_flags import FLAG_DEFAULT_WORKING_DIR_FOR_PROJ
from anyscale.project_utils import get_default_project
from anyscale.util import get_endpoint
from anyscale.utils.workspace_utils import (
    extract_workspace_parameters,
    WorkspaceCommandContext,
)
from anyscale.workspace_utils import (
    load_workspace_id_or_throw,
    write_workspace_id_to_disk,
)


ANYSCALE_WORKSPACES_SSH_OPTIONS = [
    "-o",
    "StrictHostKeyChecking=no",
    "-o",
    "UserKnownHostsFile=/dev/null",
    "-o",
    "IdentitiesOnly=yes",
]


class WorkspaceController(BaseController):
    def __init__(
        self,
        log: Optional[BlockLogger] = None,
        initialize_auth_api_client: bool = True,
    ):
        if log is None:
            log = BlockLogger()

        super().__init__(initialize_auth_api_client=initialize_auth_api_client)
        self.log = log

    def create(
        self,
        name: str,
        cloud_id: str,
        compute_config_id: str,
        cluster_environment_build_id: str,
        project_id: Optional[str],
    ) -> None:
        compute_config = self.api_client.get_compute_template_api_v2_compute_templates_template_id_get(
            compute_config_id
        ).result

        if compute_config.config.cloud_id != cloud_id:
            raise click.ClickException(
                "The compute config and cloud must be in the same cloud."
            )

        if not project_id:
            default_project = get_default_project(
                parent_cloud_id=cloud_id,
                api_client=self.api_client,
                anyscale_api_client=self.anyscale_api_client,  # type: ignore
            )
            project_id = default_project.id

        self.api_client.create_workspace_api_v2_experimental_workspaces_post(
            CreateExperimentalWorkspace(
                name=name,
                project_id=project_id,
                cloud_id=cloud_id,
                compute_config_id=compute_config_id,
                cluster_environment_build_id=cluster_environment_build_id,
            )
        )

    def list(self) -> None:
        """
        prints a non-exhaustive tabular list of information about non-deleted workspaces.
        """
        workspaces_data: List[
            ExperimentalWorkspace
        ] = self.api_client.list_workspaces_api_v2_experimental_workspaces_get().results

        workspaces_table: List[List[Any]] = [
            [
                workspace.name,
                workspace.id,
                workspace.state,
                get_endpoint(f"/workspaces/{workspace.id}/{workspace.cluster_id}"),
            ]
            for workspace in workspaces_data
            if not workspace.is_deleted
        ]

        table = tabulate.tabulate(
            workspaces_table, headers=["NAME", "ID", "STATE", "URL",], tablefmt="plain",
        )

        print(f"Workspaces:\n{table}")

    def clone(self, workspace: ExperimentalWorkspace) -> None:
        dir_name = workspace.name
        os.makedirs(dir_name)

        workspace_id = workspace.id
        write_workspace_id_to_disk(workspace_id, dir_name)

    def get_activated_workspace(self) -> ExperimentalWorkspace:
        workspace_id = load_workspace_id_or_throw()
        return self.api_client.get_workspace_api_v2_experimental_workspaces_workspace_id_get(
            workspace_id
        ).result

    def get_workspace_dir_name(self) -> str:
        """
        Currently the directory name of Workspaces/Clusters
        is determiend by the project name.
        """
        workspace = self.get_activated_workspace()
        project = self.api_client.get_project_api_v2_projects_project_id_get(
            workspace.project_id
        ).result
        if self.api_client.check_is_feature_flag_on_api_v2_userinfo_check_is_feature_flag_on_get(
            FLAG_DEFAULT_WORKING_DIR_FOR_PROJ
        ).result.is_on:
            return project.directory_name
        else:
            return project.name

    def _get_workspace_command_context(self) -> WorkspaceCommandContext:
        workspace = self.get_activated_workspace()

        cluster_id = workspace.cluster_id
        project_id = workspace.project_id

        return extract_workspace_parameters(
            cluster_id,
            project_id,
            api_client=self.api_client,
            ssh_dir="/tmp/anyscale/.ssh",
        )

    def run_cmd(self, cmd: str, args: List[str]):
        workspace_command_context = self._get_workspace_command_context()

        ssh_info = workspace_command_context.ssh

        head_ip = workspace_command_context.head_ip
        target_host = f"{ssh_info.user}@{head_ip}"

        command = shlex.quote(cmd)

        ssh_command = (
            ["ssh"]
            + ANYSCALE_WORKSPACES_SSH_OPTIONS
            + [
                "-o",
                f"ProxyCommand=ssh -W %h:%p -i {ssh_info.key_path} -o StrictHostKeyChecking=accept-new {target_host}",
            ]
            + ["-tt", "-i", ssh_info.key_path]
            + ["ray@0.0.0.0", "-p", "5020"]
            + (args if args and len(args) > 0 else [""])
            + [f"bash -i -c {command}"]
        )

        subprocess.run(ssh_command, check=False)

    def run_rsync(
        self,
        *,
        local_path: str,
        remote_path: Optional[str] = None,
        down: bool,
        rsync_filters: List[str],
        rsync_excludes: List[str],
        delete_existing_files_in_destination: bool = False,
        verbose: bool = False,
    ) -> None:
        """
        Args:
            local_path: The local path to sync from/to.
            remote_path: The remote path to sync to/from. If not provided, the
                remote path will be set to the working directory.
            down: Whether to sync from 1. remote to local, or 2. local to remote.
            rsync_filters: A list of rsync filters to apply.
            rsync_excludes: A list of rsync excludes to apply.
            delete_existing_files_in_destination: Whether to delete existing files in the destination.
        """
        workspace_command_context = self._get_workspace_command_context()
        ssh_info = workspace_command_context.ssh
        head_ip = workspace_command_context.head_ip

        identity_file_option = ["-i", ssh_info.key_path]
        proxy_thorugh_ssh_user_option = [
            "-o",
            f"ProxyCommand=ssh -W %h:%p -i {ssh_info.key_path} -o StrictHostKeyChecking=accept-new {ssh_info.user}@{head_ip}",
        ]
        ray_user_ssh_port_option = ["-p", "5020"]
        base_ssh_command = (
            ["ssh"]
            + (["-vvv"] if verbose else [])
            + identity_file_option
            + ANYSCALE_WORKSPACES_SSH_OPTIONS
            + proxy_thorugh_ssh_user_option
            + ray_user_ssh_port_option
        )

        rsync_command = [
            "rsync",
            "--rsh",
            subprocess.list2cmdline(base_ssh_command),
            "-rvzl",
        ]

        if delete_existing_files_in_destination:
            rsync_command.append("--delete")

        for rsync_exclude in rsync_excludes:
            rsync_command.extend(["--exclude", rsync_exclude])

        for rsync_filter in rsync_filters:
            rsync_command.extend(["--filter", f"dir-merge,- {rsync_filter}"])

        # TODO: Perhaps include this in cluster_config somewhere so that below isn't hardcoded
        # if either the user or host for the ray container is changed in the future
        ray_user_on_host = "ray@0.0.0.0"
        if not remote_path:
            # if not specified, default to the working directory
            remote_path = workspace_command_context.working_dir

        if down:
            rsync_command += [
                f"{ray_user_on_host}:{remote_path}",
                local_path,
            ]
        else:
            rsync_command += [
                local_path,
                f"{ray_user_on_host}:{remote_path}",
            ]

        subprocess.run(rsync_command, check=True)
