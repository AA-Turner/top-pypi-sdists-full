from io import StringIO
from json import dumps as json_dumps
import pathlib
import subprocess
import tempfile
from typing import Optional, Tuple

import click
import yaml

from anyscale._private.models.image_uri import ImageURI
from anyscale._private.sdk import _LAZY_SDK_SINGLETONS
from anyscale.cli_logger import BlockLogger
from anyscale.commands import command_examples
from anyscale.commands.util import AnyscaleCommand, convert_kv_strings_to_dict
import anyscale.workspace
from anyscale.workspace._private.workspace_sdk import ANYSCALE_WORKSPACES_SSH_OPTIONS
from anyscale.workspace.commands import _WORKSPACE_SDK_SINGLETON_KEY
from anyscale.workspace.models import (
    UpdateWorkspaceConfig,
    Workspace,
    WorkspaceConfig,
    WorkspaceState,
)


log = BlockLogger()  # CLI Logger


def _validate_workspace_name_and_id(
    name: Optional[str], id: Optional[str]  # noqa: A002
):
    if name is None and id is None:
        raise click.ClickException("One of '--name' and '--id' must be provided.")

    if name is not None and id is not None:
        raise click.ClickException("Only one of '--name' and '--id' can be provided.")


@click.group("workspace_v2", help="Anyscale workspace commands V2.")
def workspace_cli() -> None:
    pass


@workspace_cli.command(
    name="create",
    help="Create a workspace on Anyscale.",
    cls=AnyscaleCommand,
    example=command_examples.WORKSPACE_CREATE_EXAMPLE,
)
@click.option(
    "-f",
    "--config-file",
    required=False,
    default=None,
    type=str,
    help="Path to a YAML config file to deploy. When deploying from a file, import path and arguments cannot be provided. Command-line flags will overwrite values read from the file.",
)
@click.option(
    "-n", "--name", required=False, help="Name of the workspace to create.",
)
@click.option(
    "--image-uri",
    required=False,
    default=None,
    type=str,
    help="Container image to use for the workspace. This is exclusive with --containerfile.",
)
@click.option(
    "--registry-login-secret",
    required=False,
    default=None,
    type=str,
    help="Name or identifier of the secret containing credentials to authenticate to the docker registry hosting the image. "
    "This can only be used when 'image_uri' is specified and the image is not hosted on Anyscale.",
)
@click.option(
    "--containerfile",
    required=False,
    default=None,
    type=str,
    help="Path to a containerfile to build the image to use for the workspace. This is exclusive with --image-uri.",
)
@click.option(
    "--ray-version",
    required=False,
    default=None,
    type=str,
    help="The Ray version (X.Y.Z) to the image specified by --image-uri. This is only used when --image-uri is provided. If not provided, the latest Ray version will be used.",
)
@click.option(
    "--compute-config",
    required=False,
    default=None,
    type=str,
    help="Named compute configuration to use for the workspace.",
)
@click.option(
    "--cloud",
    required=False,
    default=None,
    type=str,
    help="The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
)
@click.option(
    "--project",
    required=False,
    default=None,
    type=str,
    help="Named project to use for the workspace. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
)
@click.option(
    "-r",
    "--requirements",
    required=False,
    default=None,
    type=str,
    help="Path to a requirements.txt file containing dependencies for the workspace. These will be installed on top of the image.",
)
@click.option(
    "--env",
    required=False,
    multiple=True,
    type=str,
    help="Environment variables to set for the workspace. The format is 'key=value'. This argument can be specified multiple times. When the same key is also specified in the config file, the value from the command-line flag will overwrite the value from the config file.",
)
def create(  # noqa: PLR0913, PLR0912, C901
    config_file: Optional[str],
    name: Optional[str],
    image_uri: Optional[str],
    registry_login_secret: Optional[str],
    ray_version: Optional[str],
    containerfile: Optional[str],
    compute_config: Optional[str],
    cloud: Optional[str],
    project: Optional[str],
    requirements: Optional[str],
    env: Optional[Tuple[str]],
) -> None:
    """Creates a new workspace.

    A name must be provided, either in the file or in the arguments.

    `$ anyscale workspace_v2 create -n my-workspace`

    or add all the information in the config file and do:

    `$ anyscale workspace_v2 create -f config-file.yaml`

    Command-line flags override values in the config file.
    """
    if config_file is not None:
        if not pathlib.Path(config_file).is_file():
            raise click.ClickException(f"Config file '{config_file}' not found.")

        config = WorkspaceConfig.from_yaml(config_file)
    else:
        config = WorkspaceConfig()

    if containerfile and image_uri:
        raise click.ClickException(
            "Only one of '--containerfile' and '--image-uri' can be provided."
        )

    if ray_version and (not image_uri and not containerfile):
        raise click.ClickException(
            "Ray version can only be used with an image or containerfile.",
        )

    if registry_login_secret and (
        not image_uri or ImageURI.from_str(image_uri).is_cluster_env_image()
    ):
        raise click.ClickException(
            "Registry login secret can only be used with an image that is not hosted on Anyscale."
        )

    if name is not None:
        config = config.options(name=name)

    if not config.name:
        raise click.ClickException("Workspace name must be configured")

    if image_uri is not None:
        config = config.options(image_uri=image_uri)

    if registry_login_secret is not None:
        config = config.options(registry_login_secret=registry_login_secret)

    if ray_version is not None:
        config = config.options(ray_version=ray_version)

    if containerfile is not None:
        config = config.options(containerfile=containerfile)

    if compute_config is not None:
        config = config.options(compute_config=compute_config)

    if cloud is not None:
        config = config.options(cloud=cloud)
    if project is not None:
        config = config.options(project=project)

    if requirements is not None:
        if not pathlib.Path(requirements).is_file():
            raise click.ClickException(f"Requirements file '{requirements}' not found.")
        config = config.options(requirements=requirements)
    if env:
        env_dict = convert_kv_strings_to_dict(env)
        if env_dict:
            config = config.options(env_vars=env_dict)

    anyscale.workspace.create(config,)


@workspace_cli.command(
    name="start",
    short_help="Starts a workspace.",
    cls=AnyscaleCommand,
    example=command_examples.WORKSPACE_START_EXAMPLE,
)
@click.option(
    "--id", "--workspace-id", required=False, help="Unique ID of the workspace."
)
@click.option("--name", "-n", required=False, help="Name of the workspace.")
@click.option(
    "--cloud",
    required=False,
    default=None,
    type=str,
    help="The Anyscale Cloud to run this workload on. If not provided, the organization default will be used.",
)
@click.option(
    "--project",
    required=False,
    default=None,
    type=str,
    help="Named project to use for the workpsace. If not provided, the default project for the cloud will be used.",
)
def start(
    id: Optional[str],  # noqa: A002
    name: Optional[str],
    cloud: Optional[str],
    project: Optional[str],
) -> None:
    """Start a workspace.

    To specify the workspace by name, use the --name flag. To specify the workspace by id, use the --id flag. Either name or
id should be used, specifying both will result in an error.
    """
    _validate_workspace_name_and_id(name=name, id=id)
    anyscale.workspace.start(name=name, id=id, cloud=cloud, project=project)


@workspace_cli.command(
    name="terminate",
    short_help="Terminate a workspace.",
    cls=AnyscaleCommand,
    example=command_examples.WORKSPACE_TERMINATE_EXAMPLE,
)
@click.option(
    "--id", "--workspace-id", required=False, help="Unique ID of the workspace."
)
@click.option("--name", "-n", required=False, help="Name of the workspace.")
@click.option(
    "--cloud",
    required=False,
    default=None,
    type=str,
    help="The Anyscale Cloud to run this workload on. If not provided, the organization default will be used.",
)
@click.option(
    "--project",
    required=False,
    default=None,
    type=str,
    help="Named project to use for the workpsace. If not provided, the default project for the cloud will be used.",
)
def terminate(
    id: Optional[str],  # noqa: A002
    name: Optional[str],
    cloud: Optional[str],
    project: Optional[str],
) -> None:
    """Terminate a workspace.

    To specify the workspace by name, use the --name flag. To specify the workspace by id, use the --id flag. Either name or
id should be used, specifying both will result in an error.
    """
    _validate_workspace_name_and_id(name=name, id=id)
    anyscale.workspace.terminate(name=name, id=id, cloud=cloud, project=project)


@workspace_cli.command(
    name="status",
    short_help="Get the status of a workspace.",
    cls=AnyscaleCommand,
    example=command_examples.WORKSPACE_STATUS_EXAMPLE,
)
@click.option(
    "--id", "--workspace-id", required=False, help="Unique ID of the workspace."
)
@click.option("--name", "-n", required=False, help="Name of the workspace.")
@click.option(
    "--cloud",
    required=False,
    default=None,
    type=str,
    help="The Anyscale Cloud to run this workload on. If not provided, the organization default will be used.",
)
@click.option(
    "--project",
    required=False,
    default=None,
    type=str,
    help="Named project to use for the workpsace. If not provided, the default project for the cloud will be used.",
)
def status(
    id: Optional[str],  # noqa: A002
    name: Optional[str],
    cloud: Optional[str],
    project: Optional[str],
) -> None:
    """Get the status of a workspace.

    To specify the workspace by name, use the --name flag. To specify the workspace by id, use the --id flag. Either name or
id should be used, specifying both will result in an error.
    """
    _validate_workspace_name_and_id(name=name, id=id)
    status = anyscale.workspace.status(name=name, id=id, cloud=cloud, project=project)
    log.info(status)


@workspace_cli.command(
    name="wait",
    short_help="Wait for a workspace to reach a certain status.",
    cls=AnyscaleCommand,
    example=command_examples.WORKSPACE_WAIT_EXAMPLE,
)
@click.option(
    "--id", "--workspace-id", required=False, help="Unique ID of the workspace."
)
@click.option("--name", "-n", required=False, help="Name of the workspace.")
@click.option(
    "--cloud",
    required=False,
    default=None,
    type=str,
    help="The Anyscale Cloud to run this workload on. If not provided, the organization default will be used.",
)
@click.option(
    "--project",
    required=False,
    default=None,
    type=str,
    help="Named project to use for the workpsace. If not provided, the default project for the cloud will be used.",
)
@click.option(
    "--timeout-s",
    required=False,
    default=1800,
    type=float,
    help="The maximum time in seconds to wait for the workspace to reach the desired state. Default to 30 minutes.",
)
@click.option(
    "--state",
    required=False,
    default=WorkspaceState.RUNNING,
    type=str,
    help="The desired terminal state to wait for. Default is 'RUNNING'.",
)
def wait(
    id: Optional[str],  # noqa: A002
    name: Optional[str],
    cloud: Optional[str],
    project: Optional[str],
    timeout_s: float,
    state: str,
) -> None:
    """Wait for a workspace to reach a terminal state.

    To specify the workspace by name, use the --name flag. To specify the workspace by id, use the --id flag. Either name or
id should be used, specifying both will result in an error.
    """
    _validate_workspace_name_and_id(name=name, id=id)
    try:
        state = WorkspaceState.validate(state)
    except ValueError as e:
        raise click.ClickException(str(e))
    anyscale.workspace.wait(
        name=name, id=id, cloud=cloud, project=project, timeout_s=timeout_s, state=state
    )


@workspace_cli.command(
    name="ssh",
    short_help="SSH into a workspace.",
    context_settings={"ignore_unknown_options": True, "allow_extra_args": True},
    cls=AnyscaleCommand,
    example=command_examples.WORKSPACE_SSH_EXAMPLE,
)
@click.option(
    "--id", "--workspace-id", required=False, help="Unique ID of the workspace."
)
@click.option("--name", "-n", required=False, help="Name of the workspace.")
@click.option(
    "--cloud",
    required=False,
    default=None,
    type=str,
    help="The Anyscale Cloud to run this workload on. If not provided, the organization default will be used.",
)
@click.option(
    "--project",
    required=False,
    default=None,
    type=str,
    help="Named project to use for the workpsace. If not provided, the default project for the cloud will be used.",
)
@click.pass_context
def ssh(
    ctx,
    id: Optional[str],  # noqa: A002
    name: Optional[str],
    cloud: Optional[str],
    project: Optional[str],
) -> None:
    """SSH into a workspace.

    To specify the workspace by name, use the --name flag. To specify the workspace by id, use the --id flag. Either name or
id should be used, specifying both will result in an error.

    You may pass extra args for the ssh command, for example to setup port forwarding:
    anyscale workspace_v2 ssh -n workspace-name -- -L 9000:localhost:9000
    """

    _validate_workspace_name_and_id(name=name, id=id)
    assert (
        anyscale.workspace.status(name=name, id=id, cloud=cloud, project=project)
        == WorkspaceState.RUNNING
    ), "Workspace must be running to SSH into it."
    workspace_private_sdk = _LAZY_SDK_SINGLETONS[_WORKSPACE_SDK_SINGLETON_KEY]
    dir_name = workspace_private_sdk.get_default_dir_name(
        name=name, id=id, cloud=cloud, project=project
    )
    command = f"cd {dir_name} && /bin/bash"
    with tempfile.TemporaryDirectory() as tmpdirname:
        host_name, config_file = anyscale.workspace.generate_ssh_config_file(
            name=name, id=id, cloud=cloud, project=project, ssh_config_path=tmpdirname
        )
        args = ctx.args
        ssh_command = (
            ["ssh"]
            + ANYSCALE_WORKSPACES_SSH_OPTIONS
            + [host_name]
            + ["-F", config_file]
            + ["-tt"]
            + (args if args and len(args) > 0 else [""])
            + [f"bash -i -c {command}"]
        )

        subprocess.run(ssh_command, check=False)


@workspace_cli.command(
    name="run_command",
    short_help="Run a command in a workspace.",
    cls=AnyscaleCommand,
    example=command_examples.WORKSPACE_RUN_COMMAND_EXAMPLE,
)
@click.option(
    "--id", "--workspace-id", required=False, help="Unique ID of the workspace."
)
@click.option("--name", "-n", required=False, help="Name of the workspace.")
@click.option(
    "--cloud",
    required=False,
    default=None,
    type=str,
    help="The Anyscale Cloud to run this workload on. If not provided, the organization default will be used.",
)
@click.option(
    "--project",
    required=False,
    default=None,
    type=str,
    help="Named project to use for the workpsace. If not provided, the default project for the cloud will be used.",
)
@click.argument("command", type=str)
def run_command(
    id: Optional[str],  # noqa: A002
    name: Optional[str],
    cloud: Optional[str],
    project: Optional[str],
    command: str,
) -> None:
    """Run a command in a workspace.

    To specify the workspace by name, use the --name flag. To specify the workspace by id, use the --id flag. Either name or
id should be used, specifying both will result in an error.
    """
    _validate_workspace_name_and_id(name=name, id=id)
    anyscale.workspace.run_command(
        name=name, id=id, cloud=cloud, project=project, command=command
    )


@workspace_cli.command(
    name="pull",
    short_help="Pull the working directory of a workspace.",
    context_settings={"ignore_unknown_options": True, "allow_extra_args": True},
    cls=AnyscaleCommand,
    example=command_examples.WORKSPACE_PULL_EXAMPLE,
)
@click.option(
    "--id", "--workspace-id", required=False, help="Unique ID of the workspace."
)
@click.option("--name", "-n", required=False, help="Name of the workspace.")
@click.option(
    "--cloud",
    required=False,
    default=None,
    type=str,
    help="The Anyscale Cloud to run this workload on. If not provided, the organization default will be used.",
)
@click.option(
    "--project",
    required=False,
    default=None,
    type=str,
    help="Named project to use for the workpsace. If not provided, the default project for the cloud will be used.",
)
@click.option(
    "--local-dir",
    required=False,
    default=None,
    type=str,
    help="Local directory to pull the workspace directory to. If not provided, the current directory will be used.",
)
@click.option(
    "--pull-git-state",
    required=False,
    default=False,
    is_flag=True,
    help="Pull the git state of the workspace.",
)
@click.option(
    "--delete",
    required=False,
    default=False,
    is_flag=True,
    help="Delete files in the local directory that are not in the workspace.",
)
@click.pass_context
def pull(  # noqa: PLR0913
    ctx,
    id: Optional[str],  # noqa: A002
    name: Optional[str],
    cloud: Optional[str],
    project: Optional[str],
    local_dir: Optional[str],
    pull_git_state: bool = False,
    delete: bool = False,
) -> None:
    """Pull the working directory of a workspace. New files will be created, existing files will be overwritten.

    To specify the workspace by name, use the --name flag. To specify the workspace by id, use the --id flag. Either name or
id should be used, specifying both will result in an error.

    This command depends on rsync, please make sure it is installed on your system.

    You may pass extra args for the rsync command, for example to exclude files:
    anyscale workspace_v2 pull -n workspace-name -- --exclude='log.txt'
    """
    _validate_workspace_name_and_id(name=name, id=id)
    anyscale.workspace.pull(
        name=name,
        id=id,
        cloud=cloud,
        project=project,
        local_dir=local_dir,
        pull_git_state=pull_git_state,
        rsync_args=ctx.args,
        delete=delete,
    )


@workspace_cli.command(
    name="push",
    short_help="Push a local directory to a workspace.",
    context_settings={"ignore_unknown_options": True, "allow_extra_args": True},
    cls=AnyscaleCommand,
    example=command_examples.WORKSPACE_PUSH_EXAMPLE,
)
@click.option(
    "--id", "--workspace-id", required=False, help="Unique ID of the workspace."
)
@click.option("--name", "-n", required=False, help="Name of the workspace.")
@click.option(
    "--cloud",
    required=False,
    default=None,
    type=str,
    help="The Anyscale Cloud to run this workload on. If not provided, the organization default will be used.",
)
@click.option(
    "--project",
    required=False,
    default=None,
    type=str,
    help="Named project to use for the workpsace. If not provided, the default project for the cloud will be used.",
)
@click.option(
    "--local-dir",
    required=False,
    default=None,
    type=str,
    help="Local directory to push to the workspace. If not provided, the current directory will be used.",
)
@click.option(
    "--push-git-state",
    required=False,
    default=False,
    is_flag=True,
    help="Push the git state of the workspace.",
)
@click.option(
    "--delete",
    required=False,
    default=False,
    is_flag=True,
    help="Delete files in the workspace that are not in the local directory.",
)
@click.pass_context
def push(  # noqa: PLR0913
    ctx,
    id: Optional[str],  # noqa: A002
    name: Optional[str],
    cloud: Optional[str],
    project: Optional[str],
    local_dir: Optional[str],
    push_git_state: bool = False,
    delete: bool = False,
) -> None:
    """Push a local directory to a workspace. New files will be created, existing files will be overwritten.

    To specify the workspace by name, use the --name flag. To specify the workspace by id, use the --id flag. Either name or
id should be used, specifying both will result in an error.

    This command depends on rsync, please make sure it is installed on your system.

    You may pass extra args for the rsync command, for example to exclude files:
    anyscale workspace_v2 push -n workspace-name -- --exclude='log.txt'
    """
    _validate_workspace_name_and_id(name=name, id=id)
    anyscale.workspace.push(
        name=name,
        id=id,
        cloud=cloud,
        project=project,
        local_dir=local_dir,
        push_git_state=push_git_state,
        rsync_args=ctx.args,
        delete=delete,
    )


@workspace_cli.command(
    name="update",
    help="Update an existing workspace on Anyscale.",
    cls=AnyscaleCommand,
    example=command_examples.WORKSPACE_UPDATE_EXAMPLE,
)
@click.argument("workspace-id", type=str)
@click.option(
    "-f",
    "--config-file",
    required=False,
    default=None,
    type=str,
    help="Path to a YAML config file to update. Command-line flags will overwrite values read from the file. Unspecified fields will retain their current values, while specified fields will be updated.",
)
@click.option(
    "-n", "--name", required=False, help="New name of the workspace.",
)
@click.option(
    "--image-uri",
    required=False,
    default=None,
    type=str,
    help="New container image to use for the workspace. This is exclusive with --containerfile.",
)
@click.option(
    "--registry-login-secret",
    required=False,
    default=None,
    type=str,
    help="Name or identifier of the secret containing credentials to authenticate to the docker registry hosting the image. "
    "This can only be used when 'image_uri' is specified and the image is not hosted on Anyscale.",
)
@click.option(
    "--containerfile",
    required=False,
    default=None,
    type=str,
    help="Path to a containerfile to build the image to use for the workspace. This is exclusive with --image-uri.",
)
@click.option(
    "--ray-version",
    required=False,
    default=None,
    type=str,
    help="New Ray version (X.Y.Z) to use with the image specified by --image-uri. This is only used when --image-uri is provided. If not provided, the latest Ray version will be used.",
)
@click.option(
    "--compute-config",
    required=False,
    default=None,
    type=str,
    help="New named compute configuration to use for the workspace.",
)
@click.option(
    "-r",
    "--requirements",
    required=False,
    default=None,
    type=str,
    help="Path to a requirements.txt file containing dependencies for the workspace. These will be installed on top of the image.",
)
@click.option(
    "--env",
    required=False,
    multiple=True,
    type=str,
    help="New environment variables to set for the workspace. The format is 'key=value'. This argument can be specified multiple times. When the same key is also specified in the config file, the value from the command-line flag will overwrite the value from the config file.",
)
def update(  # noqa: PLR0913, PLR0912
    workspace_id: str,
    config_file: Optional[str],
    name: Optional[str],
    image_uri: Optional[str],
    registry_login_secret: Optional[str],
    ray_version: Optional[str],
    containerfile: Optional[str],
    compute_config: Optional[str],
    requirements: Optional[str],
    env: Optional[Tuple[str]],
) -> None:
    """Updates an existing workspace.

    Example:
    `$ anyscale workspace_v2 update <workspace-id> --name new-name`

    Command-line flags override values in the config file.
    Unspecified fields will retain their current values, while specified fields will be updated.
    """

    if config_file is not None:
        if not pathlib.Path(config_file).is_file():
            raise click.ClickException(f"Config file '{config_file}' not found.")

        config = UpdateWorkspaceConfig.from_yaml(config_file)
    else:
        config = UpdateWorkspaceConfig()

    if containerfile and image_uri:
        raise click.ClickException(
            "Only one of '--containerfile' and '--image-uri' can be provided."
        )

    if ray_version and (not image_uri and not containerfile):
        raise click.ClickException(
            "Ray version can only be used with an image or containerfile.",
        )

    if registry_login_secret and (
        not image_uri or ImageURI.from_str(image_uri).is_cluster_env_image()
    ):
        raise click.ClickException(
            "Registry login secret can only be used with an image that is not hosted on Anyscale."
        )

    if name is not None:
        config = config.options(name=name)

    if image_uri is not None:
        config = config.options(image_uri=image_uri)

    if registry_login_secret is not None:
        config = config.options(registry_login_secret=registry_login_secret)

    if ray_version is not None:
        config = config.options(ray_version=ray_version)

    if containerfile is not None:
        config = config.options(containerfile=containerfile)

    if compute_config is not None:
        config = config.options(compute_config=compute_config)

    if requirements is not None:
        if not pathlib.Path(requirements).is_file():
            raise click.ClickException(f"Requirements file '{requirements}' not found.")
        config = config.options(requirements=requirements)

    if env:
        env_dict = convert_kv_strings_to_dict(env)
        if env_dict:
            config = config.options(env_vars=env_dict)

    # Apply the update
    anyscale.workspace.update(id=workspace_id, config=config)


@workspace_cli.command(
    name="get",
    short_help="Get a workspace.",
    cls=AnyscaleCommand,
    example=command_examples.WORKSPACE_GET_EXAMPLE,
)
@click.option(
    "--id", "--workspace-id", required=False, help="Unique ID of the workspace."
)
@click.option("--name", "-n", required=False, help="Name of the workspace.")
@click.option(
    "--cloud",
    required=False,
    default=None,
    type=str,
    help="The Anyscale Cloud to run this workload on. If not provided, the organization default will be used.",
)
@click.option(
    "--project",
    required=False,
    default=None,
    type=str,
    help="Named project to use for the workpsace. If not provided, the default project for the cloud will be used.",
)
@click.option(
    "-j",
    "--json",
    is_flag=True,
    default=False,
    help="Output the workspace in a structured JSON format.",
)
@click.option(
    "-v", "--verbose", is_flag=True, default=False, help="Include verbose details.",
)
def get(
    id: Optional[str],  # noqa: A002
    name: Optional[str],
    cloud: Optional[str],
    project: Optional[str],
    json: bool,
    verbose: bool,
) -> None:
    """Retrieve workspace details by name or ID.

    Use --name to specify by name or --id for the workspace ID; using both will result in an error.
    """
    _validate_workspace_name_and_id(name=name, id=id)
    workspace: Workspace = anyscale.workspace.get(
        name=name, id=id, cloud=cloud, project=project
    )
    workspace_dict = workspace.to_dict()

    if not verbose:
        workspace_dict.pop("config", None)

    if json:
        print(json_dumps(workspace_dict, indent=4, sort_keys=False))
    else:
        stream = StringIO()
        yaml.safe_dump(workspace_dict, stream, sort_keys=False)
        print(stream.getvalue(), end="")
