from typing import List, Optional, Tuple, Union

from anyscale._private.anyscale_client import AnyscaleClientInterface
from anyscale._private.sdk import sdk_docs
from anyscale._private.sdk.base_sdk import Timer
from anyscale.cli_logger import BlockLogger
from anyscale.workspace._private.workspace_sdk import PrivateWorkspaceSDK
from anyscale.workspace.commands import (
    _CREATE_ARG_DOCSTRINGS,
    _CREATE_EXAMPLE,
    _GENERATE_SSH_CONFIG_FILE_ARG_DOCSTRINGS,
    _GENERATE_SSH_CONFIG_FILE_EXAMPLE,
    _GET_ARG_DOCSTRINGS,
    _GET_EXAMPLE,
    _PULL_ARG_DOCSTRINGS,
    _PULL_EXAMPLE,
    _PUSH_ARG_DOCSTRINGS,
    _PUSH_EXAMPLE,
    _RUN_COMMAND_ARG_DOCSTRINGS,
    _RUN_COMMAND_EXAMPLE,
    _START_ARG_DOCSTRINGS,
    _START_EXAMPLE,
    _STATUS_ARG_DOCSTRINGS,
    _STATUS_EXAMPLE,
    _TERMINATE_ARG_DOCSTRINGS,
    _TERMINATE_EXAMPLE,
    _UPDATE_ARG_DOCSTRINGS,
    _UPDATE_EXAMPLE,
    _WAIT_ARG_DOCSTRINGS,
    _WAIT_EXAMPLE,
    create,
    generate_ssh_config_file,
    get,
    pull,
    push,
    run_command,
    start,
    status,
    terminate,
    update,
    wait,
)
from anyscale.workspace.models import (
    UpdateWorkspaceConfig,
    Workspace,
    WorkspaceConfig,
    WorkspaceState,
)


class WorkspaceSDK:
    def __init__(
        self,
        *,
        client: Optional[AnyscaleClientInterface] = None,
        logger: Optional[BlockLogger] = None,
        timer: Optional[Timer] = None,
    ):
        self._private_sdk = PrivateWorkspaceSDK(
            client=client, logger=logger, timer=timer
        )

    @sdk_docs(
        doc_py_example=_CREATE_EXAMPLE, arg_docstrings=_CREATE_ARG_DOCSTRINGS,
    )
    def create(self, config: Optional[WorkspaceConfig]) -> str:  # noqa: F811
        """Create a workspace.

        Returns the id of the workspace.
        """
        return self._private_sdk.create(config=config)  # type: ignore

    @sdk_docs(
        doc_py_example=_START_EXAMPLE, arg_docstrings=_START_ARG_DOCSTRINGS,
    )
    def start(  # noqa: F811
        self,
        *,
        name: Optional[str] = None,
        id: Optional[str] = None,  # noqa: A002
        cloud: Optional[str] = None,
        project: Optional[str] = None,
    ) -> str:
        """Start a workspace.

        Returns the id of the started workspace.
        """
        return self._private_sdk.start(name=name, id=id, cloud=cloud, project=project)

    @sdk_docs(
        doc_py_example=_TERMINATE_EXAMPLE, arg_docstrings=_TERMINATE_ARG_DOCSTRINGS,
    )
    def terminate(  # noqa: F811
        self,
        *,
        name: Optional[str] = None,
        id: Optional[str] = None,  # noqa: A002
        cloud: Optional[str] = None,
        project: Optional[str] = None,
    ) -> str:
        """Terminate a workspace.

        Returns the id of the terminated workspace.
        """
        return self._private_sdk.terminate(
            name=name, id=id, cloud=cloud, project=project
        )

    @sdk_docs(
        doc_py_example=_STATUS_EXAMPLE, arg_docstrings=_STATUS_ARG_DOCSTRINGS,
    )
    def status(  # noqa: F811
        self,
        *,
        name: Optional[str] = None,
        id: Optional[str] = None,  # noqa: A002
        cloud: Optional[str] = None,
        project: Optional[str] = None,
    ) -> str:
        """Get the status of a workspace.

        Returns the status of the workspace.
        """
        return self._private_sdk.status(name=name, id=id, cloud=cloud, project=project)

    @sdk_docs(
        doc_py_example=_WAIT_EXAMPLE, arg_docstrings=_WAIT_ARG_DOCSTRINGS,
    )
    def wait(  # noqa: F811
        self,
        *,
        name: Optional[str] = None,
        id: Optional[str] = None,  # noqa: A002
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        timeout_s: float = 1800,
        state: Union[str, WorkspaceState] = WorkspaceState.RUNNING,
    ) -> str:
        """Wait for a workspace to reach a terminal state.

        Returns the id of the workspace.
        """
        return self._private_sdk.wait(
            name=name,
            id=id,
            cloud=cloud,
            project=project,
            timeout_s=timeout_s,
            state=state,
        )

    @sdk_docs(
        doc_py_example=_GENERATE_SSH_CONFIG_FILE_EXAMPLE,
        arg_docstrings=_GENERATE_SSH_CONFIG_FILE_ARG_DOCSTRINGS,
    )
    def generate_ssh_config_file(  # noqa: F811
        self,
        *,
        name: Optional[str] = None,
        id: Optional[str] = None,  # noqa: A002
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        ssh_config_path: Optional[str] = None,
    ) -> Tuple[str, str]:
        """Generate an SSH config file for a workspace.

        Returns a tuple of host name and config file path.
        """
        return self._private_sdk.generate_ssh_config_file(
            name=name,
            id=id,
            cloud=cloud,
            project=project,
            ssh_config_path=ssh_config_path,
        )

    @sdk_docs(
        doc_py_example=_RUN_COMMAND_EXAMPLE, arg_docstrings=_RUN_COMMAND_ARG_DOCSTRINGS,
    )
    def run_command(  # noqa: F811
        self,
        *,
        name: Optional[str] = None,
        id: Optional[str] = None,  # noqa: A002
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        command: str,
        **kwargs,
    ):
        """Run a command on a workspace.

        Returns the output of the command.
        """
        return self._private_sdk.run_command(
            name=name, id=id, cloud=cloud, project=project, command=command, **kwargs
        )

    @sdk_docs(
        doc_py_example=_PULL_EXAMPLE, arg_docstrings=_PULL_ARG_DOCSTRINGS,
    )
    def pull(  # noqa: F811
        self,
        *,
        name: Optional[str] = None,
        id: Optional[str] = None,  # noqa: A002
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        local_dir: Optional[str] = None,
        pull_git_state: bool = False,
        rsync_args: Optional[List[str]] = None,
        delete: bool = False,
    ):
        """Pull a file from a workspace."""
        self._private_sdk.pull(
            name=name,
            id=id,
            cloud=cloud,
            project=project,
            local_dir=local_dir,
            pull_git_state=pull_git_state,
            rsync_args=rsync_args,
            delete=delete,
        )

    @sdk_docs(
        doc_py_example=_PUSH_EXAMPLE, arg_docstrings=_PUSH_ARG_DOCSTRINGS,
    )
    def push(  # noqa: F811
        self,
        *,
        name: Optional[str] = None,
        id: Optional[str] = None,  # noqa: A002
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        local_dir: Optional[str] = None,
        push_git_state: bool = False,
        rsync_args: Optional[List[str]] = None,
        delete: bool = False,
    ):
        """Push a directory to a workspace."""
        self._private_sdk.push(
            name=name,
            id=id,
            cloud=cloud,
            project=project,
            local_dir=local_dir,
            push_git_state=push_git_state,
            rsync_args=rsync_args,
            delete=delete,
        )

    @sdk_docs(
        doc_py_example=_UPDATE_EXAMPLE, arg_docstrings=_UPDATE_ARG_DOCSTRINGS,
    )
    def update(  # noqa: F811
        self, *, id: Optional[str] = None, config: UpdateWorkspaceConfig  # noqa: A002
    ):
        """Update a workspace."""
        self._private_sdk.update(
            id=id, config=config,  # type: ignore
        )

    @sdk_docs(
        doc_py_example=_GET_EXAMPLE, arg_docstrings=_GET_ARG_DOCSTRINGS,
    )
    def get(  # noqa: F811
        self,
        *,
        name: Optional[str] = None,
        id: Optional[str] = None,  # noqa: A002
        cloud: Optional[str] = None,
        project: Optional[str] = None,
    ) -> Workspace:
        """Get a workspace."""
        return self._private_sdk.get(name=name, id=id, cloud=cloud, project=project)
