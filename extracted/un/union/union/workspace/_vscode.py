import asyncio
import inspect
import json
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import typing
from multiprocessing import Process
from pathlib import Path
from shutil import which
from string import Template
from subprocess import run
from textwrap import dedent
from time import time
from typing import List, NamedTuple, Optional, Union

import fsspec
import yaml
from flytekit import PythonFunctionTask, current_context
from flytekit.configuration import AuthType, ImageConfig, SerializationSettings
from flytekit.core.base_task import Task
from flytekit.core.context_manager import FlyteContextManager
from flytekit.core.utils import ClassDecorator
from flytekit.extend import TaskResolverMixin
from flytekit.remote import FlyteTask
from flytekit.tools.translator import get_serializable
from flytekit.types.directory import FlyteDirectory
from google.protobuf.json_format import MessageToDict
from rich.console import Console

import union
from union._async import merge, run_sync
from union._config import _VANITY_UNION_URLS, _clean_endpoint
from union.remote import UnionRemote
from union.workspace._config import WorkspaceConfig
from union.workspace._vscode_remote import WorkspaceRemote, _generate_workspace_name

VSCODE_TYPE_VALUE = "vscode"
# Config keys to store in task template
TASK_FUNCTION_SOURCE_PATH = "TASK_FUNCTION_SOURCE_PATH"

WORKSPACE_IMAGE_NAME = "workspace"
CODE_SERVER_CLI_NAME = "code-server"
DEFAULT_PORT = 8080
DOWNLOAD_DIR = Path.home() / ".code-server"
WORKSPACE_DIR = Path("/workspace")
HEARTBEAT_PATH = Path.home() / ".local" / "share" / "code-server" / "heartbeat"
CODE_SERVER_SETTINGS_PATH = Path.home() / ".local" / "share" / "code-server" / "User" / "settings.json"
CODE_SERVER_VERSION = "4.23.1"
CODE_SERVER_DOWNLOAD_URL = (
    "https://github.com/coder/code-server/releases/download/v{version}/code-server-{version}-linux-{arch}.tar.gz"
)
CODE_SERVER_CLI_NAME_TEMPLATE = "code-server-{version}-linux-{arch}"
HEARTBEAT_CHECK_SECONDS = 60
WATCH_WORKSPACE_INSTANCE_CHECK_SECONDS = 30
GH_VERSION = "2.49.0"

ROOT_PATH = Path.home()
BASHRC_PATH = Path.home() / ".bashrc"
UNION_GITHUB_TOKEN_ENV = "UNION_WORKSPACE_GITHUB_TOKEN"
UNION_SERVERLESS_API_KEY_ENV = "UNION_WORKSPACE_SERVERLESS_API_KEY"
GIT_CONFIG_PATH = Path.home() / ".gitconfig"
TERMINATE_WORKSPACE_FILE_NAME = "terminate_workspace.py"
WORKSPACE_API_KEY_NAME = "WORKSPACE_API_KEY"


GIT_CONFIG_TEMPLATE = Template(
    """\
$USER_INFO

[credential "https://github.com"]
    helper =
    helper = !/usr/bin/gh auth git-credential
[credential "https://gist.github.com"]
    helper =
    helper = !/usr/bin/gh auth git-credential

[url "https://$GITHUB_TOKEN@github.com/"]
    insteadOf = https://github.com/
"""
)

WorkspaceOutput = NamedTuple("WorkspaceOutput", [("state_dir", FlyteDirectory)])


def configure_python_path():
    python_bin = os.path.dirname(sys.executable)
    with BASHRC_PATH.open("a") as f:
        f.write(os.linesep)
        f.write(f"export PATH={python_bin}:$PATH")
        f.write(os.linesep)
        f.write(r'export PS1="\[\e[0;34m\]\w\[\e[m\]\$ "')


def configure_union_remote(host: str):
    from union._config import _write_config_to_path

    _write_config_to_path(host, AuthType.DEVICEFLOW.value)


def configure_git(repo: str, workspace_dir: Path, git_name: str, git_email: str) -> str:
    """Configures workspace built with ImageSpec on Union's hosted image builder."""

    ctx = current_context()
    secrets = ctx.secrets

    with BASHRC_PATH.open("a") as f:
        github_token = secrets.get(key=UNION_GITHUB_TOKEN_ENV)
        f.write(f"export GITHUB_TOKEN={github_token}")

    user_info = dedent(
        f"""\
    [user]
        name = {git_name}
        email = {git_email}
    """
    )
    git_config = GIT_CONFIG_TEMPLATE.substitute(
        USER_INFO=user_info,
        GITHUB_TOKEN=github_token,
    )

    GIT_CONFIG_PATH.write_text(git_config)

    root_dir = workspace_dir

    if repo != "":
        workspace_dir.mkdir(exist_ok=True)
        subprocess.run(["/usr/bin/git", "clone", repo], cwd=workspace_dir, text=True, check=False)
        for item in workspace_dir.iterdir():
            if item.is_dir():
                root_dir = item
                break
    return root_dir


class vscode(ClassDecorator):
    """Union specific VSCode extension."""

    def __init__(self, task_function: Optional[callable] = None):
        super().__init__(task_function=task_function)

    def execute(self, *args, **kwargs):
        ctx = FlyteContextManager.current_context()
        ctx.user_space_params.builder().add_attr(
            TASK_FUNCTION_SOURCE_PATH, inspect.getsourcefile(self.task_function)
        ).build()

        if ctx.execution_state.is_local_execution():
            return

        return self.task_function(*args, **kwargs)

    def get_extra_config(self):
        return {self.LINK_TYPE_KEY: VSCODE_TYPE_VALUE, self.PORT_KEY: f"{DEFAULT_PORT}"}


def run_on_startup_commands(on_startup: Union[str, List[str]], workspace_dir: Path):
    if on_startup is not None:
        if isinstance(on_startup, str):
            on_startup = [on_startup]

        commands = [
            # ensure that contents in the workspace directory is writable by the
            # user. This is needed e.g. when cloned git repos are checked out
            # as part of on_startup, but the state_dir needs to overwrite files
            # in the .git directory
            "chmod 775 -R .",
            *on_startup,
        ]

        for cmd in commands:
            subprocess.run(cmd.split(), cwd=workspace_dir, text=True, check=False)


def build_workspace_image(
    remote: UnionRemote, ws_config: WorkspaceConfig, dry_run: bool = False
) -> typing.Optional[FlyteTask]:
    name = ws_config.name
    project = ws_config.project
    domain = ws_config.domain

    task = image_builder_resolver.get_task_for_workspace(ws_config)
    console = Console()
    console.print("✨ Building workspace image...")

    try:
        source_root = task.container_image.source_root
    except AttributeError:
        source_root = None

    serialization_settings = SerializationSettings(
        project=project, domain=domain, image_config=ImageConfig.auto_default_image(), source_root=source_root
    )
    if dry_run:
        m = typing.OrderedDict()
        task_entity = get_serializable(m, settings=serialization_settings, entity=task)
        yaml_output = yaml.safe_dump(
            MessageToDict(task_entity.to_flyte_idl()), sort_keys=False, default_flow_style=False
        )
        console.print("Would register:")
        console.print(yaml_output)
        return

    return remote.register_task(
        task,
        serialization_settings=serialization_settings,
        version=_generate_workspace_name(name),
    )


@vscode
def workspace(
    config_content: str,
    host: str,
    console_http_domain: str,
    state_dir: Optional[FlyteDirectory] = None,
) -> WorkspaceOutput:
    ROOT_PATH.mkdir(exist_ok=True)
    configure_python_path()
    configure_union_remote(host)

    workspace_config = WorkspaceConfig.from_yaml(config_content)
    workspace_dir = Path(workspace_config.workspace_root).expanduser()
    workspace_dir.mkdir(exist_ok=True)

    code_server_cli = download_and_configure_vscode(CODE_SERVER_VERSION)
    run_on_startup_commands(workspace_config.on_startup, workspace_dir)

    if state_dir is not None:
        state_dir.download()
        shutil.copytree(state_dir.path, workspace_dir, dirs_exist_ok=True)

    # overwrite the config with the new config
    config_path = workspace_dir / "config.yaml"
    config_path.write_text(config_content)

    # Configure code-server
    configure_code_server_config()

    start_vscode_service(
        code_server_cli,
        host,
        console_http_domain,
        workspace_dir,
        workspace_config.ttl_seconds,
        workspace_config.working_dir,
    )
    logger = union.current_context().logging
    logger.info(f"Vscode service terminated, saving contents of {workspace_dir} to state_dir output")
    return WorkspaceOutput(state_dir=FlyteDirectory(path=str(workspace_dir)))


@union.task
def _workspace_image_build_noop(): ...


class WorkspaceResolver(TaskResolverMixin):
    def __init__(self, task_function, task_type):
        super().__init__()
        self.task_type = task_type
        self.task_function = task_function

    @property
    def location(self) -> str:
        return "union.workspace._vscode.resolver"

    @property
    def name(self) -> str:
        return "union.workspace.vscode"

    def get_task_for_workspace(
        self,
        config: WorkspaceConfig,
    ) -> PythonFunctionTask:
        return PythonFunctionTask(
            task_config=None,
            task_function=self.task_function,
            task_type=self.task_type,
            task_resolver=self,
            requests=config.resources,
            container_image=config.container_image,
        )

    def load_task(self, loader_args: List[str]) -> PythonFunctionTask:
        return PythonFunctionTask(
            task_config=None,
            task_function=self.task_function,
            task_type=self.task_type,
            task_resolver=self,
        )

    def loader_args(self, settings: SerializationSettings, task: PythonFunctionTask) -> List[str]:
        return ["workspace"]

    def get_all_tasks(self) -> List[Task]:
        raise NotImplementedError


resolver = WorkspaceResolver(task_function=workspace, task_type="workspace")
image_builder_resolver = WorkspaceResolver(
    task_function=_workspace_image_build_noop, task_type="_workspace_image_build_noop"
)


def download_http(url: str, local_dest_path: Path) -> Path:
    """Download URL to `download_dir`. Returns Path of downloaded file."""
    logger = union.current_context().logging

    fs = fsspec.filesystem("http")
    logger.info(f"Downloading {url} to {local_dest_path}")
    fs.get(url, local_dest_path)
    logger.info("File downloaded successfully!")

    return local_dest_path


def download_and_configure_vscode(version: str) -> str:
    """Download and configure vscode."""
    logger = union.current_context().logging
    code_server_cli = which(CODE_SERVER_CLI_NAME)
    if code_server_cli is not None:
        logger.info(f"Code server binary already exists at {code_server_cli}")
        logger.info("Skipping downloading coe server")
        return code_server_cli

    # Download code-server
    logger.info(f"Code server is not in $PATH, downloading code server to {DOWNLOAD_DIR}...")
    DOWNLOAD_DIR.mkdir(exist_ok=True)

    machine_info = platform.machine()
    logger.info(f"machine type: {machine_info}")

    if machine_info == "aarch64":
        arch = "arm64"
    elif machine_info == "x86_64":
        arch = "amd64"
    else:
        msg = (
            "Automatic download is only supported on AMD64 and ARM64 architectures. "
            "If you are using a different architecture, please visit the code-server official "
            "website to manually download the appropriate version for your image."
        )
        raise ValueError(msg)

    code_server_tar_path_url = CODE_SERVER_DOWNLOAD_URL.format(version=version, arch=arch)
    code_server_local_path = DOWNLOAD_DIR / "code-server.tar.gz"
    download_http(code_server_tar_path_url, code_server_local_path)
    with tarfile.open(code_server_local_path, "r:gz") as tar:
        tar.extractall(path=DOWNLOAD_DIR)

    code_server_cli = (
        DOWNLOAD_DIR / CODE_SERVER_CLI_NAME_TEMPLATE.format(version=version, arch=arch) / "bin" / CODE_SERVER_CLI_NAME
    )
    return os.fspath(code_server_cli)


def configure_code_server_config():
    logger = union.current_context().logging
    config = {
        "terminal.integrated.defaultProfile.linux": "bash",
        "remote.autoForwardPortsSource": "hybrid",
        "commands.treeViewStatusBarVisibleSymbol": "",
        "commands.commands": {
            "⏹️ Terminate Workspace": {
                "sequence": [
                    {
                        "command": "commands.runInTerminal",
                        "args": {
                            "text": "python ~/workspace/terminate_workspace.py",
                            "name": "terminate",
                            "waitForExit": False,
                            "reuse": "newest",
                        },
                    },
                    {
                        "command": "commands.focusTerminal",
                        "args": "terminate",
                    },
                ],
                "statusBar": {
                    "alignment": "left",
                    "text": "$(stop) Terminate Workspace",
                    "backgroundColor": "warning",
                    "priority": -9999,
                },
            },
        },
        "workbench.colorCustomizations": {
            "sideBar.background": "#FFF8F3",
            "sideBarSectionHeader.background": "#FFEED5",
            "activityBar.background": "#FFF8F3",
            "statusBar.background": "#FFF8F3",
            "titleBar.activeBackground": "#FFF8F3",
        },
        "files.exclude": {
            "**/__pycache__/**": True,
            "**/.vscode/**": True,
        },
    }
    if not CODE_SERVER_SETTINGS_PATH.parent.exists():
        logger.info(f"Creating code server settings directory {CODE_SERVER_SETTINGS_PATH.parent}")
        CODE_SERVER_SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)

    with CODE_SERVER_SETTINGS_PATH.open("w") as file:
        json.dump(config, file, indent=4)


def prepare_terminate_workspace_python(
    console_http_domain: str,
    workspace_root: Path,
    pid: int,
):
    """
    Generate a Python script for users to resume the task.
    """

    if console_http_domain.startswith("https://"):
        redirect_url = f"{console_http_domain}/"
    else:
        redirect_url = f"https://{console_http_domain}/"

    python_script = dedent(f"""\
    import argparse
    import os
    import signal
    import time
    import webbrowser

    if __name__ == "__main__":
        parser = argparse.ArgumentParser()
        parser.add_argument("--force", action="store_true", help="Force terminate the workspace.")
        args = parser.parse_args()

        if args.force:
            answer = "Y"
        else:
            print(
                "⛔️ This operation will terminate the workspace. The contents "
                "in the {workspace_root} directory will not be saved."
            )
            answer = input("Do you really want to terminate? [Y/n]: ").strip().upper()

        if answer in ['Y', '']:
            os.kill({pid}, signal.SIGTERM)
            print(f"🛑 The server is terminating. You will be redirected to Union in a few seconds.")
            time.sleep(3)
            webbrowser.open("{redirect_url}", new=0)
            print("⤴️ Redirecting to Union.")
        else:
            print("Operation canceled.")
    """)

    with (workspace_root / TERMINATE_WORKSPACE_FILE_NAME).open("w") as file:
        file.write(python_script)


def prepare_task_json(workspace_root: Path, working_dir: Path):
    tasks_json = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "terminate",
                "type": "shell",
                "command": f"python {workspace_root / TERMINATE_WORKSPACE_FILE_NAME!s}",
            }
        ],
    }

    vscode_directory = working_dir / ".vscode"
    if not os.path.exists(vscode_directory):
        os.makedirs(vscode_directory)

    with open(os.path.join(vscode_directory, "tasks.json"), "w") as file:
        json.dump(tasks_json, file, indent=4)


def start_vscode_service(
    code_server_cli: str,
    host: str,
    console_http_domain: str,
    workspace_root: Path,
    ttl_seconds: int,
    working_dir: Optional[str] = None,
):
    logger = union.current_context().logging
    code_server_host = f"0.0.0.0:{DEFAULT_PORT}"

    command = [
        code_server_cli,
        "--bind-addr",
        code_server_host,
        "--disable-workspace-trust",
        "--auth",
        "none",
    ]

    workspace_root = workspace_root.absolute()
    if working_dir is not None:
        working_dir: Path = workspace_root / working_dir
    else:
        working_dir: Path = workspace_root

    command.append(os.fspath(working_dir))

    if not workspace_root.exists():
        logger.info(f"Creating workspace root directory {workspace_root}")
        workspace_root.mkdir(parents=True, exist_ok=True)

    if not working_dir.exists():
        logger.info(f"Creating working directory {working_dir}")
        working_dir.mkdir(parents=True, exist_ok=True)

    workspace_api_key = f"{os.getenv('FLYTE_SECRETS_ENV_PREFIX')}{WORKSPACE_API_KEY_NAME}"
    if workspace_api_key in os.environ:
        if "UNION_API_KEY" not in os.environ:
            os.environ["UNION_API_KEY"] = os.environ[workspace_api_key]
    else:
        raise RuntimeError(f"{workspace_api_key} is not set")

    env = os.environ.copy()
    host = _clean_endpoint(host)
    env["_UNION_ENDPOINT"] = _VANITY_UNION_URLS.get(host, host)

    child_process = Process(
        target=run,
        args=[command],
        kwargs={"text": True, "env": env},
    )
    child_process.start()

    logger.info(f"Preparing terminate workspace python script in {workspace_root}, pid: {child_process.pid}")
    prepare_terminate_workspace_python(console_http_domain, workspace_root, child_process.pid)

    logger.info(f"Preparing launch.json in {workspace_root}")
    prepare_task_json(workspace_root, working_dir)

    project = os.getenv("FLYTE_INTERNAL_PROJECT")
    domain = os.getenv("FLYTE_INTERNAL_DOMAIN")

    assert project is not None, "FLYTE_INTERNAL_PROJECT must be set"
    assert domain is not None, "FLYTE_INTERNAL_DOMAIN must be set"

    workspace_instance_name = os.getenv("UNION_INTERNAL_WORKSPACE_INSTANCE_NAME")
    assert workspace_instance_name is not None, "UNION_INTERNAL_WORKSPACE_INSTANCE_NAME must be set"

    remote = WorkspaceRemote(default_project=project, default_domain=domain, union_remote=union.UnionRemote())
    run_sync(
        monitor_vscode,
        remote,
        workspace_instance_name,
        child_process,
        ttl_seconds,
    )
    return


async def watch_heartbeat(
    child_process: Process,
    start_time: float,
    ttl_seconds: int,
    logger,
):
    while child_process.is_alive():
        if not HEARTBEAT_PATH.exists():
            logger.info(f"Code server heartbeat file does not exist, using start time {start_time}")
            delta = time() - start_time
        else:
            file_mod_time = HEARTBEAT_PATH.stat().st_mtime
            logger.info(f"Code server heartbeat file exists, using file modification time {file_mod_time}")
            delta = time() - file_mod_time

        logger.info(f"The latest activity on code server was {delta} ago.")
        if delta > ttl_seconds:
            logger.info(
                f"code server is idle for more than {ttl_seconds} seconds. Terminating process {child_process.pid}"
            )
            yield True
            break

        logger.info("Continuing to monitor code server heartbeat")
        yield False
        await asyncio.sleep(HEARTBEAT_CHECK_SECONDS)
    else:
        logger.info("Code server process is already terminated")
        yield True


async def poll_workspace_instance(
    child_process: Process,
    remote: WorkspaceRemote,
    workspace_instance_name: str,
    logger,
):
    """
    This is a fallback method to make sure that the workspace instance is stopping.
    """
    while child_process.is_alive():
        logger.info("Waiting for workspace instance to stop")
        is_stopping = await remote.workspace_instance_is_stopping(workspace_instance_name, logger=logger)
        if is_stopping:
            logger.info("Workspace instance is stopping")
            yield is_stopping
            break

        logger.info("Sleeping workspace instance check")
        yield False
        await asyncio.sleep(WATCH_WORKSPACE_INSTANCE_CHECK_SECONDS)
    else:
        logger.info("Code server process is already terminated")
        yield True


async def monitor_vscode(
    remote: WorkspaceRemote,
    workspace_instance_name: str,
    child_process: Process,
    ttl_seconds: int,
):
    logger = union.current_context().logging
    start_time = time()

    loop = asyncio.get_running_loop()

    logger.info("Starting to monitor workspace instance for termination signal")

    watch_heartbeat_task = watch_heartbeat(child_process, start_time, ttl_seconds, logger)
    watch_workspace_instance_task = remote.watch_workspace_instance(workspace_instance_name, logger=logger)
    poll_workspace_instance_task = poll_workspace_instance(child_process, remote, workspace_instance_name, logger)

    try:
        async for stop_event in merge(
            loop,
            watch_heartbeat_task,
            watch_workspace_instance_task,
            poll_workspace_instance_task,
        ):
            if stop_event:
                child_process.terminate()
                child_process.join()
                logger.info(f"Code server process {child_process.pid} terminated")
                return
            else:
                logger.info("Code server process is still running")
    finally:
        watch_heartbeat_task.aclose()
        watch_workspace_instance_task.aclose()
        poll_workspace_instance_task.aclose()
