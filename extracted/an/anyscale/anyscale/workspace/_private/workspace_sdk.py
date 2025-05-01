from functools import partial
import os
import subprocess
import tempfile
from typing import cast, Dict, List, Optional, Tuple, Union

import click

from anyscale._private.workload.workload_sdk import WorkloadSDK
from anyscale.client.openapi_client.models import (
    CreateExperimentalWorkspace,
    ExperimentalWorkspace,
)
from anyscale.client.openapi_client.models.session_state import SessionState
from anyscale.client.openapi_client.models.workspace_dataplane_proxied_artifacts import (
    WorkspaceDataplaneProxiedArtifacts,
)
from anyscale.utils.runtime_env import parse_requirements_file
from anyscale.workspace.models import (
    UpdateWorkspaceConfig,
    Workspace,
    WorkspaceConfig,
    WorkspaceState,
)


SSH_TEMPLATE = """
Host Head-Node
  HostName {head_node_ip}
  User ubuntu
  IdentityFile {key_path}
  StrictHostKeyChecking false
  UserKnownHostsFile /dev/null
  IdentitiesOnly yes
  LogLevel ERROR

Host {name}
  HostName 0.0.0.0
  ProxyJump Head-Node
  Port 5020
  User ray
  IdentityFile {key_path}
  StrictHostKeyChecking false
  UserKnownHostsFile /dev/null
  IdentitiesOnly yes
  LogLevel ERROR
"""

# TODO(bryce): These options are already stated in the SSH_TEMPLATE, but we
# still pass them in the ssh command. It should be safe to remove them.
ANYSCALE_WORKSPACES_SSH_OPTIONS = [
    "-o",
    "StrictHostKeyChecking=no",
    "-o",
    "UserKnownHostsFile=/dev/null",
    "-o",
    "IdentitiesOnly=yes",
]


class PrivateWorkspaceSDK(WorkloadSDK):
    _POLLING_INTERVAL_SECONDS = 10.0
    _WAIT_TIMEOUT_SECONDS = 1800.0

    _BACKEND_SESSION_STATE_TO_WORKSPACE_STATE = {
        SessionState.STOPPED: WorkspaceState.TERMINATED,
        SessionState.TERMINATED: WorkspaceState.TERMINATED,
        SessionState.STARTINGUP: WorkspaceState.STARTING,
        SessionState.STARTUPERRORED: WorkspaceState.ERRORED,
        SessionState.RUNNING: WorkspaceState.RUNNING,
        SessionState.UPDATING: WorkspaceState.UPDATING,
        SessionState.UPDATINGERRORED: WorkspaceState.ERRORED,
        SessionState.STOPPING: WorkspaceState.TERMINATING,
        SessionState.TERMINATING: WorkspaceState.TERMINATING,
        SessionState.AWAITINGSTARTUP: WorkspaceState.STARTING,
        SessionState.AWAITINGFILEMOUNTS: WorkspaceState.STARTING,
        SessionState.TERMINATINGERRORED: WorkspaceState.ERRORED,
        SessionState.STOPPINGERRORED: WorkspaceState.ERRORED,
    }

    def _resolve_to_workspace_model(
        self,
        *,
        id: Optional[str] = None,  # noqa: A002
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
    ) -> ExperimentalWorkspace:
        if name is None and id is None:
            raise ValueError("One of 'name' or 'id' must be provided.")

        if name is not None and id is not None:
            raise ValueError("Only one of 'name' or 'id' can be provided.")

        if id is not None and (cloud is not None or project is not None):
            raise ValueError("'cloud' and 'project' should only be used with 'name'.")

        model: Optional[ExperimentalWorkspace] = self.client.get_workspace(
            name=name, id=id, cloud=cloud, project=project
        )
        if model is None:
            if name is not None:
                raise ValueError(f"Workspace with name '{name}' was not found.")
            else:
                raise ValueError(f"Workspace with ID '{id}' was not found.")

        return model

    def create(self, config: WorkspaceConfig) -> str:
        if not config or config.name is None:
            raise ValueError("Workspace name must be configured")

        name = config.name

        compute_config_id, cloud_id = self.resolve_compute_config_and_cloud_id(
            compute_config=config.compute_config, cloud=config.cloud,  # type: ignore
        )

        project_id = self.client.get_project_id(
            parent_cloud_id=cloud_id, name=config.project
        )

        build_id = None

        if config.containerfile is not None:
            build_id = self._image_sdk.build_image_from_containerfile(
                name=f"image-for-workspace-{name}",
                containerfile=self.get_containerfile_contents(config.containerfile),
                ray_version=config.ray_version,
            )
        elif config.image_uri is not None:
            build_id = self._image_sdk.registery_image(
                image_uri=config.image_uri,
                registry_login_secret=config.registry_login_secret,
                ray_version=config.ray_version,
            )

        dynamic_requirements = None
        if (
            config.requirements
            and self._image_sdk.enable_image_build_for_tracked_requirements
        ):
            requirements = (
                parse_requirements_file(config.requirements)
                if isinstance(config.requirements, str)
                else config.requirements
            )
            if requirements:
                build_id = self._image_sdk.build_image_from_requirements(
                    name=f"image-for-workspace-{name}",
                    base_build_id=self.client.get_default_build_id(),
                    requirements=requirements,
                )
        elif config.requirements:
            dynamic_requirements = (
                parse_requirements_file(config.requirements)
                if isinstance(config.requirements, str)
                else config.requirements
            )

        if build_id is None:
            build_id = self.client.get_default_build_id()

        workspace_id = self.client.create_workspace(
            model=CreateExperimentalWorkspace(
                name=name,
                project_id=project_id,
                compute_config_id=compute_config_id,
                cluster_environment_build_id=build_id,
                idle_timeout_minutes=config.idle_termination_minutes,
                cloud_id=cloud_id,
                skip_start=True,
            )
        )

        self._logger.info(f"Workspace created successfully id: {workspace_id}")

        if dynamic_requirements:
            self.client.update_workspace_dependencies_offline_only(
                workspace_id=workspace_id, requirements=dynamic_requirements
            )
            self._logger.info(f"Applied dynamic requirements to workspace id: {name}")
        if config.env_vars:
            self.client.update_workspace_env_vars_offline_only(
                workspace_id=workspace_id, env_vars=config.env_vars
            )
            self._logger.info(f"Applied environment variables to workspace id: {name}")

        return workspace_id

    def start(
        self,
        *,
        id: Optional[str] = None,  # noqa: A002
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
    ) -> str:
        workspace_model = self._resolve_to_workspace_model(
            id=id, name=name, cloud=cloud, project=project
        )
        self.client.start_workspace(workspace_model.id)
        self.logger.info(f"Starting workspace '{workspace_model.name}'")
        return workspace_model.id

    def terminate(
        self,
        *,
        id: Optional[str] = None,  # noqa: A002
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
    ) -> str:
        workspace_model = self._resolve_to_workspace_model(
            id=id, name=name, cloud=cloud, project=project
        )
        self.client.terminate_workspace(workspace_model.id)
        self.logger.info(f"Terminating workspace '{workspace_model.name}'")
        return workspace_model.id

    def status(
        self,
        *,
        id: Optional[str] = None,  # noqa: A002
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
    ) -> str:
        workspace_model = self._resolve_to_workspace_model(
            id=id, name=name, cloud=cloud, project=project
        )

        status = self._get_workspace_status(workspace_model.id)
        return status

    def wait(  # noqa: PLR0912
        self,
        *,
        id: Optional[str] = None,  # noqa: A002
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        timeout_s: float = _WAIT_TIMEOUT_SECONDS,
        state: Union[str, WorkspaceState] = WorkspaceState.RUNNING,
        interval_s: float = _POLLING_INTERVAL_SECONDS,
    ):
        if not isinstance(timeout_s, (int, float)):
            raise TypeError("timeout_s must be a float")
        if timeout_s <= 0:
            raise ValueError("timeout_s must be >= 0")

        if not isinstance(interval_s, (int, float)):
            raise TypeError("interval_s must be a float")
        if interval_s <= 0:
            raise ValueError("interval_s must be >= 0")

        if isinstance(state, str):
            try:
                state = WorkspaceState.validate(state)
            except KeyError:
                raise ValueError(f"Invalid state: {state}")

        if not isinstance(state, WorkspaceState):
            raise TypeError("'state' must be a WorkspaceState.")

        workspace_model = self._resolve_to_workspace_model(
            id=id, name=name, cloud=cloud, project=project
        )

        workspace_id_or_name = workspace_model.id or workspace_model.name
        curr_state = self._get_workspace_status(workspace_model.id)

        self.logger.info(
            f"Waiting for workspace '{workspace_id_or_name}' to reach target state {state}, currently in state: {curr_state}"
        )
        for _ in self.timer.poll(timeout_s=timeout_s, interval_s=interval_s):
            new_state = self._get_workspace_status(workspace_model.id)

            if new_state != curr_state:
                self.logger.info(
                    f"Workspace '{workspace_id_or_name}' transitioned from {curr_state} to {new_state}"
                )
                curr_state = new_state

            if curr_state == state:
                self.logger.info(
                    f"Workspace '{workspace_id_or_name}' reached target state, exiting"
                )
                break
        else:
            raise TimeoutError(
                f"Workspace '{workspace_id_or_name}' did not reach target state {state} within {timeout_s}s. Last seen state: {curr_state}."
            )

    def _get_workspace_status(self, workspace_id: Optional[str]) -> WorkspaceState:

        cluster = self.client.get_workspace_cluster(workspace_id)
        if not cluster:
            raise ValueError(f"Workspace {workspace_id} cluster not found.")
        return self._convert_cluster_state_to_workspace_state(cluster.state)

    def generate_ssh_config_file(
        self,
        *,
        id: Optional[str] = None,  # noqa: A002
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        ssh_config_path: Optional[str] = None,
    ) -> Tuple[str, str]:
        workspace_model = self._resolve_to_workspace_model(
            id=id, name=name, cloud=cloud, project=project
        )

        assert (
            self.status(id=workspace_model.id) == WorkspaceState.RUNNING
        ), "Workspace must be running to generate SSH config file"

        head_node_ip = self.client.get_cluster_head_node_ip(workspace_model.cluster_id)
        ssh_key = self.client.get_cluster_ssh_key(workspace_model.cluster_id)

        def _store_ssh_key(name: str, ssh_key: str, key_dir: str) -> str:
            key_path = os.path.join(key_dir, f"{name}.pem")
            os.makedirs(os.path.dirname(key_path), exist_ok=True)

            with open(key_path, "w", opener=partial(os.open, mode=0o600)) as f:
                f.write(ssh_key)

            return key_path

        if ssh_config_path is None:
            ssh_config_path = tempfile.mkdtemp()

        key_path = _store_ssh_key(
            ssh_key.key_name, ssh_key.private_key, ssh_config_path
        )

        ssh_config = SSH_TEMPLATE.format(
            head_node_ip=head_node_ip, key_path=key_path, name=workspace_model.name
        )

        config_file_name = os.path.join(ssh_config_path, "config")
        with open(config_file_name, "w") as f:
            f.write(ssh_config)

        return workspace_model.name, config_file_name

    def run_command(
        self,
        command: str,
        *,
        id: Optional[str] = None,  # noqa: A002
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        **kwargs,
    ) -> subprocess.CompletedProcess:
        workspace_model = self._resolve_to_workspace_model(
            id=id, name=name, cloud=cloud, project=project
        )
        host_name, config_file = self.generate_ssh_config_file(id=workspace_model.id)
        return subprocess.run(
            ["ssh"]
            + ANYSCALE_WORKSPACES_SSH_OPTIONS
            + ["-F", config_file, host_name, command],
            **kwargs,
        )

    def get_default_dir_name(
        self,
        *,
        id: Optional[str] = None,  # noqa: A002
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
    ) -> str:
        workspace_model = self._resolve_to_workspace_model(
            id=id, name=name, cloud=cloud, project=project
        )
        return self.client.get_workspace_default_dir_name(workspace_model.id)

    def _parse_rsync_dry_run_output(
        self, dry_run_output: str
    ) -> Tuple[List[str], List[str]]:
        """Parse rsync dry-run output to detect file changes vs additions.
        Note that --itemize-changes is needed to detect file changes.
        Format is like "<fcsT...... test.py" where:
        - First char indicates operations (>, <, *)
        - Third char (c or .) indicates if checksum changed (only if --checksum is used)

        Returns:
            Tuple of (modifying_files, deleting_files)
        """
        modifying_files = []
        deleting_files = []

        ITEMISZED_PREFIX_LEN = 12

        changes = dry_run_output.strip().split("\n")
        for line in changes:
            if (
                not line or len(line) < ITEMISZED_PREFIX_LEN
            ):  # Need at least "<fcsT......" part
                continue
            if line.startswith("*deleting"):
                deleting_files.append(line[ITEMISZED_PREFIX_LEN:])
            elif line[2] == "c":  # Check the checksum position
                modifying_files.append(line[ITEMISZED_PREFIX_LEN:])

        return modifying_files, deleting_files

    def _dry_run_rsync(self, rsync_command: List[str], delete: bool):
        """Run rsync with --dry-run and warn if files are being deleted.
        """

        # --itemize-changes is needed to detect file changes
        dry_run_options = ["--dry-run", "--itemize-changes"]
        should_warn_delete = False

        if not delete:
            # --delete-excluded is needed to detect files that are being deleted in the destination
            should_warn_delete = True
            dry_run_options.append("--delete-excluded")

        try:
            result = subprocess.run(
                rsync_command + dry_run_options,
                capture_output=True,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            self._logger.error(f"Error running rsync command: {e}")
            self._logger.error(f">>> stdout: {e.stdout}")
            self._logger.error(f">>> stderr: {e.stderr}")
            raise RuntimeError(f"Rsync failed with return code {e.returncode}")

        _, deleting_files = self._parse_rsync_dry_run_output(result.stdout)

        if should_warn_delete and len(deleting_files):
            click.echo(
                "Detected files that exist in the destination but not in the source. The files will not be deleted by default. You can add '--delete' option to delete the files:"
            )
            click.echo(
                "\n".join([click.style(file, fg="red") for file in deleting_files])
            )

    def _run_rsync(
        self,
        *,
        id: Optional[str] = None,  # noqa: A002
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        local_dir: Optional[str] = None,
        rsync_args: Optional[List[str]] = None,
        is_pull: bool = False,
        include_git_state: bool = False,
        delete: bool = False,
    ):
        workspace_model = self._resolve_to_workspace_model(
            id=id, name=name, cloud=cloud, project=project
        )

        default_dir_name = self.get_default_dir_name(id=workspace_model.id)

        local_dir = local_dir or os.path.join(os.getcwd(), "")

        with tempfile.TemporaryDirectory() as tmp_dir:
            host_name, config_file = self.generate_ssh_config_file(
                id=workspace_model.id, ssh_config_path=tmp_dir
            )

            if is_pull:
                source = f"ray@{host_name}:~/{default_dir_name}/"
                destination = local_dir
            else:
                source = local_dir
                destination = f"ray@{host_name}:~/{default_dir_name}/"

            rsync_args = rsync_args or []

            # exclude .git/objects/info/alternates since we will repack the git repo if needed
            # exclude .anyscale.yaml for legacy reasons
            rsync_args += [
                "--exclude",
                ".git/objects/info/alternates",
                "--exclude",
                ".anyscale.yaml",
            ]

            # repack git repos if needed
            if include_git_state and is_pull:
                self.run_command(
                    id=workspace_model.id,
                    command=f"cd ~/{default_dir_name} && python -m snapshot_util repack_git_repos",
                )
            elif not include_git_state:
                rsync_args += ["--exclude", ".git"]

            # Use -c (--checksum) to avoid retransmitting files that haven't changed
            args = [
                "rsync",
                "-rzlc",
                "-e",
                f"ssh -F {config_file} {subprocess.list2cmdline(ANYSCALE_WORKSPACES_SSH_OPTIONS)}",
                source,
                destination,
            ]

            if delete:
                # --delete-excluded is needed to delete files in the destination that are not in the source
                # Note: We need --delete-excluded instead of --delete to delete files that are excluded from the sync, e.g. .git
                args.append("--delete-excluded")

            if rsync_args:
                args.extend(rsync_args)

            self._dry_run_rsync(args, delete)

            # Add -v / --verbose to the rsync command to be explicit about what is being transferred
            args += ["-v"]

            try:
                subprocess.run(args, check=True, capture_output=True, text=True)
            except subprocess.CalledProcessError as e:
                self._logger.error(f">>> Error running rsync command: {e}")
                self._logger.error(f">>> stdout: {e.stdout}")
                self._logger.error(f">>> stderr: {e.stderr}")
                raise RuntimeError(f"Rsync failed with return code {e.returncode}")

    def pull(
        self,
        *,
        id: Optional[str] = None,  # noqa: A002
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        local_dir: Optional[str] = None,
        pull_git_state: bool = False,
        rsync_args: Optional[List[str]] = None,
        delete: bool = False,
    ):
        self._run_rsync(
            id=id,
            name=name,
            cloud=cloud,
            project=project,
            local_dir=local_dir,
            rsync_args=rsync_args,
            is_pull=True,
            include_git_state=pull_git_state,
            delete=delete,
        )

    def push(
        self,
        *,
        id: Optional[str] = None,  # noqa: A002
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        local_dir: Optional[str] = None,
        push_git_state: bool = False,
        rsync_args: Optional[List[str]] = None,
        delete: bool = False,
    ):
        self._run_rsync(
            id=id,
            name=name,
            cloud=cloud,
            project=project,
            local_dir=local_dir,
            is_pull=False,
            include_git_state=push_git_state,
            rsync_args=rsync_args,
            delete=delete,
        )

    def update(
        self, *, id: Optional[str], config: UpdateWorkspaceConfig  # noqa: A002
    ) -> str:
        workspace = self.client.get_workspace(id=id)  # type: ignore

        if not workspace:
            raise ValueError(f"Workspace with id '{id}' was not found.")

        current_status = self._get_workspace_status(id)
        if current_status != WorkspaceState.TERMINATED:
            raise ValueError(
                "Workspace must be in the TERMINATED state to be updated. Use `anyscale workspace terminate` to terminate the workspace, and `anyscale workspace wait` to wait for the workspace to terminate."
            )

        name = config.name or workspace.name

        compute_config_id = None
        if config.compute_config:
            compute_config_id, _ = self.resolve_compute_config_and_cloud_id(
                compute_config=config.compute_config, cloud=None,  # type: ignore
            )

        build_id = None
        if config.containerfile is not None:
            build_id = self._image_sdk.build_image_from_containerfile(
                name=f"image-for-workspace-{name}",
                containerfile=self.get_containerfile_contents(config.containerfile),
                ray_version=config.ray_version,
            )
        elif config.image_uri is not None:
            build_id = self._image_sdk.registery_image(
                image_uri=config.image_uri,
                registry_login_secret=config.registry_login_secret,
                ray_version=config.ray_version,
            )

        dynamic_requirements = None
        if (
            config.requirements
            and self._image_sdk.enable_image_build_for_tracked_requirements
        ):
            requirements = (
                parse_requirements_file(config.requirements)
                if isinstance(config.requirements, str)
                else config.requirements
            )
            if requirements:
                build_id = self._image_sdk.build_image_from_requirements(
                    name=f"image-for-workspace-{name}",
                    base_build_id=self.client.get_default_build_id(),
                    requirements=requirements,
                )
        elif config.requirements:
            dynamic_requirements = (
                parse_requirements_file(config.requirements)
                if isinstance(config.requirements, str)
                else config.requirements
            )

        self.client.update_workspace(
            workspace_id=id,
            name=config.name,
            compute_config_id=compute_config_id,
            cluster_environment_build_id=build_id,
            idle_timeout_minutes=config.idle_termination_minutes,
        )

        self._logger.info(f"Workspace updated successfully id: {id}")

        if dynamic_requirements:
            self.client.update_workspace_dependencies_offline_only(
                workspace_id=id, requirements=dynamic_requirements
            )
            self._logger.info(f"Applied dynamic requirements to workspace id: {id}")
        if config.env_vars:
            self.client.update_workspace_env_vars_offline_only(
                workspace_id=id, env_vars=config.env_vars
            )
            self._logger.info(f"Applied environment variables to workspace id: {id}")

        return id  # type: ignore

    def _convert_cluster_state_to_workspace_state(
        self, state: SessionState
    ) -> WorkspaceState:
        return cast(
            WorkspaceState,
            self._BACKEND_SESSION_STATE_TO_WORKSPACE_STATE.get(  # type: ignore
                state, WorkspaceState.UNKNOWN
            ),
        )

    def _convert_env_var_list_to_dict(
        self, env_vars: Optional[List[str]]
    ) -> Dict[str, str]:
        if not env_vars:
            return {}
        return dict([env_var.split("=", 1) for env_var in env_vars])

    def _convert_requirements_str_to_list(
        self, requirements: Optional[str]
    ) -> List[str]:
        if not requirements:
            return []
        return [req for req in requirements.split("\n") if req]

    def _transform_internal_to_external_workspace_model(
        self, model: ExperimentalWorkspace
    ) -> Workspace:
        """Transforms an internal workspace model to a public-facing workspace model."""
        cluster = self.client.get_workspace_cluster(model.id)
        if not cluster:
            raise ValueError(
                f"Workspace cluster with ID '{model.cluster_id}' was not found."
            )

        workspace_status = self._convert_cluster_state_to_workspace_state(cluster.state)
        idle_termination_minutes = cluster.idle_timeout

        build_id = cluster.build_id
        image_uri = self._image_sdk.get_image_uri_from_build_id(build_id)
        if image_uri is None:
            raise RuntimeError(f"Failed to get image URI for ID {build_id}.")
        image_build = self._image_sdk.get_image_build(build_id)
        if image_build is None:
            raise RuntimeError(f"Failed to get image build for ID {build_id}.")

        compute_config = self.get_user_facing_compute_config(model.compute_config_id)

        cloud = self.client.get_cloud(cloud_id=model.cloud_id)
        project = self.client.get_project(project_id=model.project_id)

        workspace_dataplane_artifacts: WorkspaceDataplaneProxiedArtifacts = self.client.get_workspace_proxied_dataplane_artifacts(
            workspace_id=model.id
        )
        env_vars_dict = self._convert_env_var_list_to_dict(
            workspace_dataplane_artifacts.environment_variables
        )
        requirements = self._convert_requirements_str_to_list(
            workspace_dataplane_artifacts.requirements
        )

        return Workspace(
            id=model.id,
            name=model.name,
            config=WorkspaceConfig(
                name=model.name,
                compute_config=compute_config,
                registry_login_secret=image_build.registry_login_secret,
                image_uri=str(image_uri),
                requirements=requirements if requirements else None,
                idle_termination_minutes=idle_termination_minutes,
                env_vars=env_vars_dict,
                project=project.name if project else None,
                cloud=cloud.name if cloud else None,
            ),
            state=workspace_status,
        )

    def get(
        self,
        *,
        id: Optional[str] = None,  # noqa: A002
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
    ) -> Workspace:  # noqa: A002
        internal_workspace_model = self._resolve_to_workspace_model(
            id=id, name=name, cloud=cloud, project=project
        )
        return self._transform_internal_to_external_workspace_model(
            internal_workspace_model
        )
