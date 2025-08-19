from dataclasses import dataclass
from enum import Enum
import importlib.resources
from io import StringIO
from json import dumps as json_dumps
import pathlib
import shlex
import subprocess
import sys
import tempfile
from typing import List, Optional, Tuple
from urllib.parse import urlparse

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

# Constants for SSH configuration
HTTPS_PORT = "443"
SSH_TEST_TIMEOUT_SECONDS = 8
WSS_PATH = "/sshws"
PREFERRED_AUTH_METHOD = "PreferredAuthentications=publickey"


def _validate_workspace_name_and_id(
    name: Optional[str], id: Optional[str]  # noqa: A002
):
    if name is None and id is None:
        raise click.ClickException("One of '--name' and '--id' must be provided.")

    if name is not None and id is not None:
        raise click.ClickException("Only one of '--name' and '--id' can be provided.")


def _check_workspace_is_running(
    name: Optional[str],
    id: Optional[str],  # noqa: A002
    cloud: Optional[str],
    project: Optional[str],
) -> None:
    """Verify that the workspace is in RUNNING state."""
    try:
        workspace_status = anyscale.workspace.status(
            name=name, id=id, cloud=cloud, project=project
        )
        if workspace_status != WorkspaceState.RUNNING:
            raise click.ClickException(
                f"Workspace must be running to SSH into it. Current status: {workspace_status}"
            )
    except ValueError as e:
        # Handle workspace not found or other value errors
        error_msg = str(e)
        if "not found" in error_msg.lower():
            workspace_identifier = name if name else id
            raise click.ClickException(
                f"Workspace '{workspace_identifier}' not found. Please check the workspace name/id and try again."
            )
        else:
            raise click.ClickException(f"Error checking workspace status: {error_msg}")
    except (AttributeError, KeyError, TypeError):
        # Handle any other errors from status check
        raise click.ClickException(
            "Failed to check workspace status. Please ensure the workspace exists and you have access to it."
        )


def _get_workspace_directory_name(
    name: Optional[str],
    id: Optional[str],  # noqa: A002
    cloud: Optional[str],
    project: Optional[str],
) -> str:
    """Get the default directory name for the workspace."""
    try:
        workspace_private_sdk = _LAZY_SDK_SINGLETONS[_WORKSPACE_SDK_SINGLETON_KEY]
        return workspace_private_sdk.get_default_dir_name(
            name=name, id=id, cloud=cloud, project=project
        )
    except (AttributeError, KeyError, ValueError, TypeError):
        # Handle errors getting default directory name
        raise click.ClickException(
            "Failed to retrieve workspace configuration. Please try again later."
        )


def _create_directory_setup_command(dir_name: str) -> str:
    """Create shell command to set up the workspace directory."""
    # Even though dir_name comes from our API, we should still shell escape it.
    dir_name_escaped = shlex.quote(dir_name)
    return (
        f'if [ -d "$HOME/{dir_name_escaped}" ]; then '
        f'cd "$HOME/{dir_name_escaped}"; '
        f"else "
        f'mkdir -p "$HOME/{dir_name_escaped}" 2>/dev/null && '
        f'cd "$HOME/{dir_name_escaped}" && '
        f'echo "Created directory $HOME/{dir_name_escaped} (it did not exist)." >&2 || '
        f'echo "Warning: Could not access or create directory $HOME/{dir_name_escaped}. Staying in home directory." >&2; '
        f"fi"
    )


class ConnectionType(Enum):
    HTTPS = "https"
    LEGACY = "legacy"


@dataclass
class SSHConfig:
    """Configuration for SSH connection to workspace."""

    target_host: str
    config_file: str
    connection_type: ConnectionType
    proxy_command: Optional[str] = None
    port: Optional[str] = None

    @property
    def ssh_options(self) -> List[str]:
        """Get SSH options based on connection type."""
        if self.connection_type == ConnectionType.HTTPS:
            options = [
                "-p",
                self.port or HTTPS_PORT,
                "-o",
                PREFERRED_AUTH_METHOD,
            ]
            if self.proxy_command:
                options.extend(["-o", f"ProxyCommand={self.proxy_command}"])
            return options
        return []


def _setup_https_connection(
    workspace_obj: Workspace, workspace_private_sdk, host_name: str, config_file: str
) -> SSHConfig:
    """Set up HTTPS connection and return SSHConfig object."""
    cluster = workspace_private_sdk.client.get_workspace_cluster(workspace_obj.id)

    if not cluster:
        raise click.ClickException(
            "Could not retrieve cluster details for the workspace."
        )

    # Get hostname with multiple fallback methods
    public_hostname = _get_public_hostname(cluster)

    # Get cluster access token
    cluster_access_token = _get_cluster_access_token(cluster, workspace_private_sdk)

    # Set up proxy command
    proxy_cmd = _create_proxy_command(public_hostname, cluster_access_token)

    return SSHConfig(
        target_host=f"ray@{host_name}",
        config_file=config_file,
        connection_type=ConnectionType.HTTPS,
        proxy_command=proxy_cmd,
        port=HTTPS_PORT,
    )


def _get_public_hostname(cluster) -> str:
    """Extract public hostname from cluster with fallback methods."""
    # Attempt 1: Use cluster.hostname
    if hasattr(cluster, "hostname") and cluster.hostname:
        return cluster.hostname

    # Attempt 2: Fallback to parsing webterminal_auth_url
    if hasattr(cluster, "webterminal_auth_url") and cluster.webterminal_auth_url:
        parsed_url = urlparse(cluster.webterminal_auth_url)
        if parsed_url.netloc:
            return parsed_url.netloc

        # webterminal_auth_url was present but parsing failed
        raise click.ClickException(
            "Could not extract hostname from cluster configuration. "
            "The URL appears to be malformed."
        )

    # Both methods failed
    raise click.ClickException(
        "Could not retrieve hostname for HTTPS connection. "
        "Required cluster configuration is not available."
    )


def _get_cluster_access_token(cluster, workspace_private_sdk) -> str:
    """Get cluster access token for HTTPS connection."""
    if not hasattr(cluster, "id") or not cluster.id:
        raise click.ClickException(
            "Cluster configuration is incomplete, cannot retrieve access token."
        )

    from anyscale.client.openapi_client.exceptions import (
        ApiException,
        ApiTypeError,
        ApiValueError,
    )

    try:
        # We need to use the internal API here as there's no public API available
        # This might be updated in future SDK versions
        cluster_access_token = workspace_private_sdk.client._internal_api_client.get_cluster_access_token_api_v2_authentication_cluster_id_cluster_access_token_get(  # noqa: SLF001
            cluster_id=cluster.id
        )

        if not cluster_access_token:
            raise click.ClickException(
                "Failed to retrieve authentication token. Please try again."
            )

        return cluster_access_token

    except (ApiException, ApiTypeError, ApiValueError):
        # Don't expose API details in error messages
        raise click.ClickException(
            "Failed to authenticate. Please check your permissions and try again."
        ) from None
    except click.ClickException:
        raise  # Re-raise click exceptions as-is
    except (AttributeError, KeyError, ValueError, TypeError, RuntimeError) as e:
        # Generic error without exposing internal details
        raise click.ClickException(
            "An error occurred during authentication. Please try again."
        ) from e


def _create_proxy_command(public_hostname: str, cluster_access_token: str) -> str:
    """Create the proxy command for HTTPS connection."""
    wss_url = f"wss://{public_hostname}{WSS_PATH}"

    try:
        with importlib.resources.path(
            "anyscale.utils", "ssh_websocket_proxy.py"
        ) as proxy_path:
            proxy_script_path = str(proxy_path)
    except (ModuleNotFoundError, ImportError) as e:
        raise click.ClickException(f"Could not locate SSH proxy script: {e}") from e

    # Properly escape the proxy command arguments
    return " ".join(
        [
            shlex.quote(sys.executable),
            shlex.quote(proxy_script_path),
            shlex.quote(wss_url),
            shlex.quote(cluster_access_token),
        ]
    )


def _build_ssh_command(
    ssh_config: SSHConfig, user_args: List[str], shell_command: str,
) -> List[str]:
    """Build the final SSH command with all options."""
    # Build SSH command with basic options
    base_cmd = (
        ["ssh"]
        + ANYSCALE_WORKSPACES_SSH_OPTIONS
        + ssh_config.ssh_options
        + [ssh_config.target_host, "-F", ssh_config.config_file]
    )

    # Process user-supplied arguments
    if not user_args:
        # No user args, use default interactive shell
        return base_cmd + ["-tt", f"bash -c '{shell_command} && exec bash -i'"]

    # Parse user arguments into options and commands
    user_options, user_command = _parse_user_args(user_args)

    ssh_cmd = base_cmd + user_options

    if user_command:
        # User supplied their own command, use it directly
        ssh_cmd.extend(user_command)
    else:
        # Only options provided, add interactive shell
        # Use -tt for interactive shell unless -T or -N was specified
        if not any(opt in {"-T", "-N"} for opt in user_options):
            ssh_cmd.append("-tt")
        ssh_cmd.append(f"bash -c '{shell_command} && exec bash -i'")

    return ssh_cmd


def _parse_user_args(user_args: List[str]) -> Tuple[List[str], List[str]]:
    """Parse user arguments into options and commands."""
    # Find where command section starts (first non-option argument)
    command_start_idx = None
    for i, arg in enumerate(user_args):
        if arg and not arg.startswith("-"):
            command_start_idx = i
            break

    if command_start_idx is not None:
        user_options = [arg for arg in user_args[:command_start_idx] if arg]
        user_command = [arg for arg in user_args[command_start_idx:] if arg]
    else:
        user_options = [arg for arg in user_args if arg]
        user_command = []

    return user_options, user_command


def _test_https_connectivity(
    workspace_obj: Workspace, workspace_private_sdk, host_name: str, config_file: str,
) -> bool:
    """Test HTTPS SSH connectivity with a quick command. Returns True if available."""
    try:
        cluster = workspace_private_sdk.client.get_workspace_cluster(workspace_obj.id)
        if not cluster:
            return False

        ssh_config = _setup_https_connection(
            workspace_obj, workspace_private_sdk, host_name, config_file
        )

        # Build a test command using the same logic as the actual connection
        # but with a simple echo command that exits immediately
        test_args = [
            "-o",
            "ConnectTimeout=5",
            "-o",
            "BatchMode=yes",
            "echo",
            "connectivity_test",
        ]
        test_cmd = _build_ssh_command(ssh_config, test_args, "")

        # Run test with a timeout
        result = subprocess.run(
            test_cmd,
            check=False,
            timeout=SSH_TEST_TIMEOUT_SECONDS,
            capture_output=True,
            text=True,
        )

        # Check if we got the expected output
        if result.returncode == 0 and "connectivity_test" in result.stdout:
            return True

        # Connection failed - no need to show error code to user
        return False

    except subprocess.TimeoutExpired:
        # Silent failure - the main code will show a user-friendly message
        return False
    except OSError:
        # Silent failure
        return False
    except (click.ClickException, ValueError, AttributeError, KeyError, TypeError):
        # Silent failure
        return False


def _execute_https_ssh(
    workspace_obj: Workspace,
    workspace_private_sdk,
    host_name: str,
    config_file: str,
    ctx_args: List[str],
    shell_command: str,
) -> None:
    """Execute HTTPS SSH connection without timeout."""
    ssh_config = _setup_https_connection(
        workspace_obj, workspace_private_sdk, host_name, config_file
    )
    ssh_cmd = _build_ssh_command(ssh_config, ctx_args, shell_command)
    # Run the actual SSH session without any timeout
    subprocess.run(ssh_cmd, check=False)


def _execute_legacy_ssh(
    ssh_target_host: str, config_file: str, ctx_args: List[str], shell_command: str,
) -> None:
    """Execute legacy SSH connection."""
    legacy_ssh_config = SSHConfig(
        target_host=ssh_target_host,
        config_file=config_file,
        connection_type=ConnectionType.LEGACY,
        proxy_command=None,
        port=None,
    )

    ssh_cmd = _build_ssh_command(legacy_ssh_config, ctx_args, shell_command)
    subprocess.run(ssh_cmd, check=False)


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
    help="The Ray version (X.Y.Z) to the image specified by --image-uri. This is only used when --image-uri is provided. If you don't specify a Ray version, Anyscale defaults to the latest Ray version available at the time of the Anyscale CLI/SDK release.",
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
@click.option(
    "--legacy",
    is_flag=True,
    default=False,
    help="Use legacy SSH connection method, bypassing HTTPS SSH.",
)
@click.pass_context
def ssh(
    ctx,
    id: Optional[str],  # noqa: A002
    name: Optional[str],
    cloud: Optional[str],
    project: Optional[str],
    legacy: bool,
) -> None:
    """SSH into a workspace.

    To specify the workspace by name, use the --name flag. To specify the workspace by id, use the --id flag. Either name or
id should be used, specifying both will result in an error.

    You may pass extra args for the ssh command, for example to setup port forwarding:
    anyscale workspace_v2 ssh -n workspace-name -- -L 9000:localhost:9000

    Use the --legacy flag to bypass HTTPS SSH and use the legacy connection method directly.
    """
    try:
        _validate_workspace_name_and_id(name=name, id=id)

        # Verify workspace is running
        _check_workspace_is_running(name, id, cloud, project)

        # Inform user that connection might take time (earliest point after verifying workspace is running)
        connection_mode = " (Legacy SSH)" if legacy else ""
        print(
            f"Connecting to workspace{connection_mode}... This might take a while. Press Ctrl+C to cancel."
        )

        # Get workspace directory name
        dir_name = _get_workspace_directory_name(name, id, cloud, project)

        # Create the shell command that will:
        # 1. Try to cd to the directory
        # 2. If that fails, create it and cd to it
        # 3. If that fails too, just stay in home directory with a warning
        shell_command = _create_directory_setup_command(dir_name)

        with tempfile.TemporaryDirectory() as tmpdirname:
            try:
                host_name, config_file = anyscale.workspace.generate_ssh_config_file(
                    name=name,
                    id=id,
                    cloud=cloud,
                    project=project,
                    ssh_config_path=tmpdirname,
                )
            except ValueError as e:
                error_msg = str(e)
                if "not found" in error_msg.lower():
                    workspace_identifier = name if name else id
                    raise click.ClickException(
                        f"Workspace '{workspace_identifier}' not found or not accessible."
                    )
                else:
                    raise click.ClickException("Failed to generate SSH configuration.")
            except (
                OSError,
                IOError,
                RuntimeError,
                AttributeError,
                KeyError,
                TypeError,
            ):
                # Handle any other errors from SSH config generation
                raise click.ClickException(
                    "Failed to generate SSH configuration. Please check your network connection and try again."
                )

            # Get workspace and cluster information to determine connection method
            ssh_target_host = host_name

            # Skip HTTPS if --legacy flag is used
            https_connection_successful = False
            if not legacy:
                # Try HTTPS first (unless legacy flag is set)
                try:
                    workspace_obj = anyscale.workspace.get(
                        name=name, id=id, cloud=cloud, project=project
                    )
                    workspace_private_sdk = _LAZY_SDK_SINGLETONS[
                        _WORKSPACE_SDK_SINGLETON_KEY
                    ]
                    cluster = workspace_private_sdk.client.get_workspace_cluster(
                        workspace_obj.id
                    )

                    if cluster:
                        https_connection_successful = _test_https_connectivity(
                            workspace_obj,
                            workspace_private_sdk,
                            host_name,
                            config_file,
                        )

                except (ValueError, AttributeError, KeyError, TypeError):
                    # If we can't get workspace/cluster info, proceed with legacy SSH
                    pass

            # Execute the appropriate SSH connection based on test results
            if https_connection_successful:
                # HTTPS connectivity test passed, run actual SSH session without timeout
                _execute_https_ssh(
                    workspace_obj,
                    workspace_private_sdk,
                    host_name,
                    config_file,
                    ctx.args,
                    shell_command,
                )
            else:
                # HTTPS test failed or --legacy was specified, use legacy SSH
                if not legacy:  # Only show message if we tried HTTPS first
                    print("Connecting via standard SSH...")
                _execute_legacy_ssh(
                    ssh_target_host, config_file, ctx.args, shell_command
                )

    except click.ClickException:
        # Re-raise click exceptions as they already have user-friendly messages
        raise
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        raise click.ClickException("SSH connection cancelled by user.")
    except (
        OSError,
        IOError,
        RuntimeError,
        ValueError,
        AttributeError,
        KeyError,
        TypeError,
    ):
        # Catch any unexpected exceptions and provide a generic user-friendly message
        raise click.ClickException(
            "An unexpected error occurred while establishing SSH connection. "
            "Please try again or contact support if the issue persists."
        )


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
