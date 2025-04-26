from typing import Any, Dict, List, Optional, Tuple

from anyscale._private.sdk import sdk_command
from anyscale.workspace._private.workspace_sdk import PrivateWorkspaceSDK
from anyscale.workspace.models import (
    UpdateWorkspaceConfig,
    Workspace,
    WorkspaceConfig,
    WorkspaceState,
)


_WORKSPACE_SDK_SINGLETON_KEY = "workspace_sdk"

_CREATE_EXAMPLE = """
import anyscale
from anyscale.workspace.models import WorkspaceConfig

anyscale.workspace.create(
    WorkspaceConfig(
        name="my-workspace",
        idle_termination_minutes=120,
    ),
)
"""

_CREATE_ARG_DOCSTRINGS = {"config": "The config for defining the workspace."}
_WAIT_TIMEOUT_SECONDS = 1800.0


@sdk_command(
    _WORKSPACE_SDK_SINGLETON_KEY,
    PrivateWorkspaceSDK,
    doc_py_example=_CREATE_EXAMPLE,
    arg_docstrings=_CREATE_ARG_DOCSTRINGS,
)
def create(
    config: WorkspaceConfig, *, _private_sdk: Optional[PrivateWorkspaceSDK] = None
) -> str:
    """Create a workspace.

    Returns the id of the created workspace.
    """
    return _private_sdk.create(config)  # type: ignore


_START_EXAMPLE = """
import anyscale

anyscale.workspace.start(
    name="my-workspace",
)
"""

_START_ARG_DOCSTRINGS = {
    "name": "Name of the workspace.",
    "id": "Unique ID of the workspace",
    "cloud": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the workspace. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
}


@sdk_command(
    _WORKSPACE_SDK_SINGLETON_KEY,
    PrivateWorkspaceSDK,
    doc_py_example=_START_EXAMPLE,
    arg_docstrings=_START_ARG_DOCSTRINGS,
)
def start(
    *,
    name: Optional[str] = None,
    id: Optional[str] = None,  # noqa: A002
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    _private_sdk: Optional[PrivateWorkspaceSDK] = None,
) -> str:
    """Start a workspace.

    Returns the id of the started workspace.
    """
    return _private_sdk.start(name=name, id=id, cloud=cloud, project=project)  # type: ignore


_TERMINATE_EXAMPLE = """
import anyscale

anyscale.workspace.terminate(
    name="my-workspace",
)
"""

_TERMINATE_ARG_DOCSTRINGS = {
    "name": "Name of the workspace.",
    "id": "Unique ID of the workspace",
    "cloud": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the workspace. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
}


@sdk_command(
    _WORKSPACE_SDK_SINGLETON_KEY,
    PrivateWorkspaceSDK,
    doc_py_example=_TERMINATE_EXAMPLE,
    arg_docstrings=_TERMINATE_ARG_DOCSTRINGS,
)
def terminate(
    *,
    name: Optional[str] = None,
    id: Optional[str] = None,  # noqa: A002
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    _private_sdk: Optional[PrivateWorkspaceSDK] = None,
) -> str:
    """Terminate a workspace.

    Returns the id of the terminated workspace.
    """
    return _private_sdk.terminate(name=name, id=id, cloud=cloud, project=project)  # type: ignore


_STATUS_EXAMPLE = """
import anyscale

status = anyscale.workspace.status(
    name="my-workspace",
)
"""

_STATUS_ARG_DOCSTRINGS = {
    "name": "Name of the workspace.",
    "id": "Unique ID of the workspace",
    "cloud": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the workspace. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
}


@sdk_command(
    _WORKSPACE_SDK_SINGLETON_KEY,
    PrivateWorkspaceSDK,
    doc_py_example=_STATUS_EXAMPLE,
    arg_docstrings=_STATUS_ARG_DOCSTRINGS,
)
def status(
    *,
    name: Optional[str] = None,
    id: Optional[str] = None,  # noqa: A002
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    _private_sdk: Optional[PrivateWorkspaceSDK] = None,
) -> str:
    """Get the status of a workspace.

    Returns the status of the workspace.
    """
    return _private_sdk.status(name=name, id=id, cloud=cloud, project=project)  # type: ignore


_WAIT_EXAMPLE = """
import anyscale

anyscale.workspace.wait(
    name="my-workspace",
)
"""

_WAIT_ARG_DOCSTRINGS = {
    "name": "Name of the workspace.",
    "id": "Unique ID of the workspace",
    "cloud": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the workspace. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
    "timeout_s": "The maximum time to wait for the workspace to reach a terminal state.",
    "state": "The desired terminal state to wait for, defaults to RUNNING.",
}


@sdk_command(
    _WORKSPACE_SDK_SINGLETON_KEY,
    PrivateWorkspaceSDK,
    doc_py_example=_WAIT_EXAMPLE,
    arg_docstrings=_WAIT_ARG_DOCSTRINGS,
)
def wait(
    *,
    name: Optional[str] = None,
    id: Optional[str] = None,  # noqa: A002
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    timeout_s: float = _WAIT_TIMEOUT_SECONDS,
    state: str = WorkspaceState.RUNNING,
    _private_sdk: Optional[PrivateWorkspaceSDK] = None,
) -> str:
    """Wait for a workspace to reach a terminal state.

    Returns the status of the workspace.
    """
    return _private_sdk.wait(  # type: ignore
        name=name,
        id=id,
        cloud=cloud,
        project=project,
        timeout_s=timeout_s,
        state=state,
    )


_GENERATE_SSH_CONFIG_FILE_EXAMPLE = """
import anyscale
import subprocess

host_name, config_file = anyscale.workspace.generate_ssh_config_file(
    name="my-workspace",
)

# run an ssh command using the generated config file
subprocess.run(["ssh", "-F", config_path, host_name, "ray --version"])
"""

_GENERATE_SSH_CONFIG_FILE_ARG_DOCSTRINGS = {
    "name": "Name of the workspace.",
    "id": "Unique ID of the workspace",
    "cloud": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the workspace. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
    "ssh_config_path": "The directory to write the generated config file to.",
}


@sdk_command(
    _WORKSPACE_SDK_SINGLETON_KEY,
    PrivateWorkspaceSDK,
    doc_py_example=_GENERATE_SSH_CONFIG_FILE_EXAMPLE,
    arg_docstrings=_GENERATE_SSH_CONFIG_FILE_ARG_DOCSTRINGS,
)
def generate_ssh_config_file(
    *,
    name: Optional[str] = None,
    id: Optional[str] = None,  # noqa: A002
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    ssh_config_path: Optional[str] = None,
    _private_sdk: Optional[PrivateWorkspaceSDK] = None,
) -> Tuple[str, str]:
    """Generate an SSH config file for a workspace.

    Returns the hostname and path to the generated config file.
    """
    return _private_sdk.generate_ssh_config_file(  # type: ignore
        name=name, id=id, cloud=cloud, project=project, ssh_config_path=ssh_config_path,
    )


_RUN_COMMAND_EXAMPLE = """
import anyscale

process = anyscale.workspace.run_command(
    name="my-workspace",
    command="ray_version",
    capture_output=True,
    text=True,
)
print(process.stdout)
"""

_RUN_COMMAND_ARG_DOCSTRINGS = {
    "name": "Name of the workspace.",
    "id": "Unique ID of the workspace",
    "cloud": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the workspace. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
    "command": "The command to run.",
    "kwargs": "Additional arguments to pass to subprocess.run.",
}


@sdk_command(
    _WORKSPACE_SDK_SINGLETON_KEY,
    PrivateWorkspaceSDK,
    doc_py_example=_RUN_COMMAND_EXAMPLE,
    arg_docstrings=_RUN_COMMAND_ARG_DOCSTRINGS,
)
def run_command(
    *,
    name: Optional[str] = None,
    id: Optional[str] = None,  # noqa: A002
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    command: str,
    _private_sdk: Optional[PrivateWorkspaceSDK] = None,
    **kwargs: Dict[str, Any],
):
    """Run a command in a workspace.

    Returns a subprocess.CompletedProcess object.
    """
    return _private_sdk.run_command(  # type: ignore
        name=name, id=id, cloud=cloud, project=project, command=command, **kwargs,
    )


_PULL_EXAMPLE = """
import anyscale

anyscale.workspace.pull(
    name="my-workspace",
)
"""

_PULL_ARG_DOCSTRINGS = {
    "name": "Name of the workspace.",
    "id": "Unique ID of the workspace",
    "cloud": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the workspace. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
    "local_dir": "The local directory to pull the workspace to. If not provided, the current working directory will be used.",
    "pull_git_state": "Whether to pull the git state of the workspace.",
    "rsync_args": "Additional arguments to pass to rsync.",
}


@sdk_command(
    _WORKSPACE_SDK_SINGLETON_KEY,
    PrivateWorkspaceSDK,
    doc_py_example=_PULL_EXAMPLE,
    arg_docstrings=_PULL_ARG_DOCSTRINGS,
)
def pull(
    *,
    name: Optional[str] = None,
    id: Optional[str] = None,  # noqa: A002
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    local_dir: Optional[str] = None,
    pull_git_state: bool = False,
    rsync_args: Optional[List[str]] = None,
    delete: bool = False,
    _private_sdk: Optional[PrivateWorkspaceSDK] = None,
) -> None:
    """Pull a workspace to a local directory.

    Returns the path to the pulled workspace.
    """
    _private_sdk.pull(  # type: ignore
        name=name,
        id=id,
        cloud=cloud,
        project=project,
        local_dir=local_dir,
        pull_git_state=pull_git_state,
        rsync_args=rsync_args,
        delete=delete,
    )


_PUSH_EXAMPLE = """
import anyscale

anyscale.workspace.push(
    name="my-workspace",
    local_dir="~/workspace",
)
"""

_PUSH_ARG_DOCSTRINGS = {
    "name": "Name of the workspace.",
    "id": "Unique ID of the workspace",
    "cloud": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the workspace. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
    "local_dir": "The local directory to push to the workspace. If not provided, the current working directory will be used.",
    "push_git_state": "Whether to push the git state of the workspace.",
    "rsync_args": "Additional arguments to pass to rsync.",
    "delete": "Whether to delete files in the workspace that are not in the local directory.",
}


@sdk_command(
    _WORKSPACE_SDK_SINGLETON_KEY,
    PrivateWorkspaceSDK,
    doc_py_example=_PUSH_EXAMPLE,
    arg_docstrings=_PUSH_ARG_DOCSTRINGS,
)
def push(
    *,
    name: Optional[str] = None,
    id: Optional[str] = None,  # noqa: A002
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    local_dir: Optional[str] = None,
    push_git_state: bool = False,
    rsync_args: Optional[List[str]] = None,
    delete: bool = False,
    _private_sdk: Optional[PrivateWorkspaceSDK] = None,
) -> None:
    """Push a local directory to a workspace.

    Returns the path to the pushed workspace.
    """
    _private_sdk.push(  # type: ignore
        name=name,
        id=id,
        cloud=cloud,
        project=project,
        local_dir=local_dir,
        push_git_state=push_git_state,
        rsync_args=rsync_args,
        delete=delete,
    )


_UPDATE_EXAMPLE = """
import anyscale

anyscale.workspace.update(
    id="<workspace-id>",
    config=UpdateWorkspaceConfig(
        name="new-workspace-name",
        idle_termination_minutes=120,
    ),
)
"""

_UPDATE_ARG_DOCSTRINGS = {
    "id": "Unique ID of the workspace",
    "config": "The config for updating the workspace. Unspecified fields will retain their current values, while specified fields will be updated.",
}


@sdk_command(
    _WORKSPACE_SDK_SINGLETON_KEY,
    PrivateWorkspaceSDK,
    doc_py_example=_UPDATE_EXAMPLE,
    arg_docstrings=_UPDATE_ARG_DOCSTRINGS,
)
def update(
    *,
    id: Optional[str] = None,  # noqa: A002
    config: UpdateWorkspaceConfig,
    _private_sdk: Optional[PrivateWorkspaceSDK] = None,
) -> None:
    """Update a workspace."""
    _private_sdk.update(  # type: ignore
        id=id, config=config,
    )


_GET_EXAMPLE = """
import anyscale
from anyscale.workspace.models import Workspace

workspace: Workspace = anyscale.workspace.get(
    name='my-workspace',
)
"""

_GET_ARG_DOCSTRINGS = {
    "name": "Name of the workspace.",
    "id": "Unique ID of the workspace",
    "cloud": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the workspace. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
}


@sdk_command(
    _WORKSPACE_SDK_SINGLETON_KEY,
    PrivateWorkspaceSDK,
    doc_py_example=_GET_EXAMPLE,
    arg_docstrings=_GET_ARG_DOCSTRINGS,
)
def get(
    *,
    name: Optional[str] = None,
    id: Optional[str] = None,  # noqa: A002
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    _private_sdk: Optional[PrivateWorkspaceSDK] = None,
) -> Workspace:
    """Get a workspace."""
    return _private_sdk.get(name=name, id=id, cloud=cloud, project=project)  # type: ignore
