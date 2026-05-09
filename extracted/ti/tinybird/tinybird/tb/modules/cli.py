# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.
import json
import logging
import os
import re
import shutil
import socket
import subprocess
import sys
from glob import glob
from os import environ, getcwd
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from urllib.parse import urlencode

import click
import humanfriendly
import requests
from click import Context

from tinybird.tb import __cli__
from tinybird.tb.check_pypi import CheckPypi
from tinybird.tb.client import (
    AuthException,
    AuthNoTokenException,
    TinyB,
)
from tinybird.tb.config import get_clickhouse_host
from tinybird.tb.modules.common import (
    CatchAuthExceptions,
    CLIException,
    _get_tb_client,
    echo_json,
    echo_safe_format_table,
    force_echo,
    getenv_bool,
    try_update_config_with_remote,
)
from tinybird.tb.modules.config import CURRENT_VERSION, CLIConfig
from tinybird.tb.modules.datafile.build import build_graph
from tinybird.tb.modules.datafile.pull import folder_pull
from tinybird.tb.modules.exceptions import CLIChException
from tinybird.tb.modules.feedback_manager import FeedbackManager, get_cli_name
from tinybird.tb.modules.local_common import TB_LOCAL_HOST, TB_LOCAL_PORT, get_tinybird_local_client
from tinybird.tb.modules.login_common import check_current_folder_in_sessions
from tinybird.tb.modules.project import Project
from tinybird.tb.modules.py_project import PythonVirtualProject, get_python_virtual_project
from tinybird.tb.modules.ts_project import TypescriptVirtualProject, get_typescript_virtual_project

__old_click_echo = click.echo
__old_click_secho = click.secho
DEFAULT_PATTERNS: List[Tuple[str, Union[str, Callable[[str], str]]]] = [
    (r"p\.ey[A-Za-z0-9-_\.]+", lambda v: f"{v[:4]}...{v[-8:]}")
]
VERSION = f"{__cli__.__version__} (rev {__cli__.__revision__})"
DEV_MODE_MANUAL = "manual"
DEV_MODE_LOCAL = "local"
DEV_MODE_BRANCH = "branch"
DEV_MODE_VALUES = {DEV_MODE_MANUAL, DEV_MODE_LOCAL, DEV_MODE_BRANCH}
DEV_MODE_ROUTED_COMMANDS = {"build", "deploy"}
SDK_PROJECT_ROUTED_COMMANDS = {"build", "deploy", "preview"}
TS_PROJECT_ROUTED_COMMANDS = SDK_PROJECT_ROUTED_COMMANDS
COMMANDS_ALWAYS_CLOUD = {"infra", "branch", "environment", "workspace", "preview"}
PROJECT_TYPE_TYPESCRIPT = "ts-sdk"
PROJECT_TYPE_PYTHON = "python-sdk"
PROJECT_TYPE_CLI = "cli"
PROJECT_TYPES = {PROJECT_TYPE_TYPESCRIPT, PROJECT_TYPE_PYTHON, PROJECT_TYPE_CLI}


CLI_PROJECT_MARKERS = (
    "datasources",
    "pipes",
    "endpoints",
    "fixtures",
    "tests",
    "connections",
    "materializations",
    "copies",
    "sinks",
)
PROJECT_TYPE_SCAN_EXTENSIONS_PYTHON = {".py"}
PROJECT_TYPE_SCAN_EXTENSIONS_TYPESCRIPT = {".ts", ".tsx", ".mts", ".cts"}
PROJECT_TYPE_SCAN_IGNORED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    ".venv",
    "venv",
    ".e",
    "node_modules",
    ".pytest_cache",
    ".mypy_cache",
}
PROJECT_TYPE_SCAN_MAX_FILES = 5000
PROJECT_CONFIG_FILES = (
    "tinybird.config.py",
    "tinybird_config.py",
    "tinybird.config.mjs",
    "tinybird.config.cjs",
    "tinybird.config.json",
    "tinybird.json",
)
JSON_PROJECT_CONFIG_FILES = ("tinybird.config.json", "tinybird.json")


def _get_branch_from_ci_env() -> Optional[str]:
    ci_env_keys = (
        "VERCEL_GIT_COMMIT_REF",
        "CI_COMMIT_BRANCH",
        "CIRCLE_BRANCH",
        "BUILD_SOURCEBRANCHNAME",
        "BITBUCKET_BRANCH",
        "TRAVIS_BRANCH",
    )
    for key in ci_env_keys:
        branch = os.environ.get(key)
        if branch:
            return branch

    github_branch = os.environ.get("GITHUB_HEAD_REF") or os.environ.get("GITHUB_REF_NAME")
    if github_branch:
        return github_branch

    jenkins_branch = os.environ.get("GIT_BRANCH")
    if jenkins_branch:
        return jenkins_branch.replace("origin/", "", 1)

    return None


def get_current_git_branch() -> Optional[str]:
    try:
        # `symbolic-ref --short HEAD` works for regular and unborn branches.
        branch = subprocess.check_output(
            ["git", "symbolic-ref", "--short", "HEAD"],
            stderr=subprocess.PIPE,
            text=True,
        ).strip()
        if branch:
            return branch
    except Exception:
        pass

    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            stderr=subprocess.PIPE,
            text=True,
        ).strip()
        if branch != "HEAD":
            return branch
    except Exception:
        pass

    return _get_branch_from_ci_env()


def is_main_git_branch(branch_name: Optional[str]) -> bool:
    return branch_name in {"main", "master"}


def sanitize_branch_name(branch_name: str) -> str:
    sanitized = re.sub(r"[^a-zA-Z0-9_]", "_", branch_name)
    sanitized = re.sub(r"_+", "_", sanitized)
    return sanitized.strip("_")


def get_tinybird_branch_name_from_git_branch(branch_name: Optional[str]) -> Optional[str]:
    if not branch_name:
        return None
    sanitized = sanitize_branch_name(branch_name)
    return sanitized or None


def get_tinybird_branch_name() -> Optional[str]:
    return get_tinybird_branch_name_from_git_branch(get_current_git_branch())


def is_tinybird_local_running(timeout_seconds: float = 0.2) -> bool:
    try:
        with socket.create_connection((TB_LOCAL_HOST, TB_LOCAL_PORT), timeout=timeout_seconds):
            return True
    except OSError:
        return False


def is_datasource_create_invocation(command: Optional[str], argv: List[str]) -> bool:
    if command != "datasource":
        return False
    return any(argv[i] == "datasource" and argv[i + 1] == "create" for i in range(len(argv) - 1))


def resolve_datasource_create_target(
    command: Optional[str],
    argv: List[str],
    explicit_env_selector: bool,
    effective_cloud: bool,
) -> Tuple[bool, bool]:
    if effective_cloud or explicit_env_selector or not is_datasource_create_invocation(command, argv):
        return effective_cloud, False

    if is_tinybird_local_running():
        return effective_cloud, False

    return True, True


def validate_env_selector_for_command(command: Optional[str], env_flags_in_argv: List[str]) -> None:
    if command in COMMANDS_ALWAYS_CLOUD and "--local" in env_flags_in_argv:
        raise CLIException(
            FeedbackManager.error(
                message=(
                    f"`tb {command}` is a cloud-only command and cannot be used with `--local`. "
                    "Remove `--local` and run it against Tinybird Cloud."
                )
            )
        )


def get_dev_mode(config: Dict[str, Any]) -> str:
    raw_mode = config.get("dev_mode", DEV_MODE_MANUAL)
    if raw_mode is None:
        return DEV_MODE_MANUAL

    mode = str(raw_mode).lower()
    if mode not in DEV_MODE_VALUES:
        raise CLIException(
            FeedbackManager.error(
                message=(f"Invalid dev_mode '{raw_mode}'. Allowed values are: manual, local, branch.")
            )
        )
    return mode


def get_project_folder_from_tinybird_config(start_dir: str) -> Optional[str]:
    config_path, raw = _read_project_json_config(start_dir)
    if not config_path or not isinstance(raw, dict):
        return None

    folder = raw.get("folder")
    if isinstance(folder, str) and folder.strip():
        folder_path = Path(folder.strip())
        if not folder_path.is_absolute():
            folder_path = config_path.parent / folder_path
        return str(folder_path)

    include = raw.get("include")
    include_entries: List[str] = []
    if isinstance(include, str):
        include_entries = [include]
    elif isinstance(include, list):
        include_entries = [entry for entry in include if isinstance(entry, str)]

    if any(entry.strip() for entry in include_entries):
        return str(config_path.parent)

    return None


def get_dev_mode_from_tinybird_config(start_dir: str) -> Optional[str]:
    _, raw = _read_project_json_config(start_dir)
    if not isinstance(raw, dict):
        return None

    raw_mode = raw.get("devMode")
    if raw_mode is None:
        raw_mode = raw.get("dev_mode")
    if not isinstance(raw_mode, str):
        return None

    mode = raw_mode.strip().lower()
    if mode not in DEV_MODE_VALUES:
        return None
    return mode


def find_project_config_file(start_dir: Path) -> Optional[Path]:
    current = start_dir.resolve()
    while True:
        for filename in PROJECT_CONFIG_FILES:
            candidate = current / filename
            if candidate.exists():
                return candidate
        if current.parent == current:
            return None
        current = current.parent


def find_project_json_config_file(start_dir: Path) -> Optional[Path]:
    current = start_dir.resolve()
    while True:
        for filename in JSON_PROJECT_CONFIG_FILES:
            candidate = current / filename
            if candidate.exists():
                return candidate
        if current.parent == current:
            return None
        current = current.parent


def _read_project_json_config(start_dir: str) -> Tuple[Optional[Path], Optional[Dict[str, Any]]]:
    config_path = find_project_json_config_file(Path(start_dir))
    if not config_path or config_path.suffix != ".json":
        return None, None

    try:
        with open(config_path) as file:
            raw = json.loads(file.read())
    except (OSError, json.JSONDecodeError):
        return config_path, None

    if not isinstance(raw, dict):
        return config_path, None

    return config_path, raw


def _iter_project_type_scan_targets(config_path: Path, raw_config: Dict[str, Any]) -> List[Path]:
    base_path = config_path.parent
    targets: List[Path] = []
    seen: set[Path] = set()

    def add_target(candidate: Path) -> None:
        resolved = candidate.resolve()
        if resolved in seen:
            return
        seen.add(resolved)
        targets.append(resolved)

    folder = raw_config.get("folder")
    if isinstance(folder, str) and folder.strip():
        folder_path = Path(folder.strip())
        if not folder_path.is_absolute():
            folder_path = base_path / folder_path
        add_target(folder_path)

    include = raw_config.get("include")
    include_entries: List[str] = []
    if isinstance(include, str):
        include_entries = [include]
    elif isinstance(include, list):
        include_entries = [entry for entry in include if isinstance(entry, str)]

    for entry in include_entries:
        include_path = entry.strip()
        if not include_path:
            continue
        if any(char in include_path for char in "*?[]"):
            pattern = include_path if os.path.isabs(include_path) else str(base_path / include_path)
            for match in glob(pattern, recursive=True):
                add_target(Path(match))
            continue

        resolved_path = Path(include_path)
        if not resolved_path.is_absolute():
            resolved_path = base_path / resolved_path
        add_target(resolved_path)

    return targets


def _paths_contain_extensions(paths: List[Path], extensions: set[str]) -> bool:
    if not paths:
        return False

    scanned_files = 0
    normalized_extensions = {ext.lower() for ext in extensions}
    for path in paths:
        if path.is_file():
            if path.suffix.lower() in normalized_extensions:
                return True
            scanned_files += 1
            if scanned_files > PROJECT_TYPE_SCAN_MAX_FILES:
                return False
            continue

        if not path.is_dir():
            continue

        for _root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in PROJECT_TYPE_SCAN_IGNORED_DIRS]
            for filename in files:
                scanned_files += 1
                if scanned_files > PROJECT_TYPE_SCAN_MAX_FILES:
                    return False
                if Path(filename).suffix.lower() in normalized_extensions:
                    return True

    return False


def get_project_type_from_tinybird_config(start_dir: str) -> Optional[str]:
    config_path = find_project_config_file(Path(start_dir))
    if config_path:
        if config_path.name in {"tinybird.config.mjs", "tinybird.config.cjs"}:
            return PROJECT_TYPE_TYPESCRIPT
        if config_path.name in {"tinybird.config.py", "tinybird_config.py"}:
            return PROJECT_TYPE_PYTHON
        if config_path.suffix == ".json":
            json_path, raw_config = _read_project_json_config(start_dir)
            if json_path and raw_config:
                scan_targets = _iter_project_type_scan_targets(json_path, raw_config)
                if _paths_contain_extensions(scan_targets, PROJECT_TYPE_SCAN_EXTENSIONS_PYTHON):
                    return PROJECT_TYPE_PYTHON
                if _paths_contain_extensions(scan_targets, PROJECT_TYPE_SCAN_EXTENSIONS_TYPESCRIPT):
                    return PROJECT_TYPE_TYPESCRIPT
                return PROJECT_TYPE_CLI

    if any((Path(start_dir).resolve() / marker).exists() for marker in CLI_PROJECT_MARKERS):
        return PROJECT_TYPE_CLI

    return None


def _set_config_to_main_workspace(config: Dict[str, Any], staging: bool) -> None:
    client, _ = _get_tb_client(config.get("token", ""), config["host"], staging=staging)
    response = client.user_workspaces_and_branches(version="v1")
    workspaces = response.get("workspaces", [])
    if not workspaces:
        raise CLIException(FeedbackManager.error(message="No workspaces found for current credentials."))

    current_workspace_id = config.get("id", response.get("id"))
    current_workspace = next((ws for ws in workspaces if ws.get("id") == current_workspace_id), None)
    if not current_workspace:
        current_workspace = next((ws for ws in workspaces if ws.get("current")), None)
    if not current_workspace:
        current_workspace = workspaces[0]

    main_workspace = current_workspace
    if current_workspace.get("is_branch"):
        main_workspace_id = current_workspace.get("main")
        main_workspace = next((ws for ws in workspaces if ws.get("id") == main_workspace_id), None)

    if not main_workspace:
        raise CLIException(FeedbackManager.error(message="Unable to resolve the main workspace for deployment target."))

    main_workspace_token = main_workspace.get("token")
    if not main_workspace_token:
        raise CLIException(
            FeedbackManager.error(message="Unable to resolve main workspace token for deployment target.")
        )

    config["id"] = main_workspace.get("id", config.get("id", ""))
    config["name"] = main_workspace.get("name", config.get("name", ""))
    config["token"] = main_workspace_token


def resolve_dev_mode_target(
    command: Optional[str],
    config: Dict[str, Any],
    cloud: bool,
    branch: Optional[str],
    staging: bool,
    explicit_env_selector: bool,
) -> Tuple[bool, Optional[str], str]:
    effective_cloud = cloud or bool(branch)
    effective_branch = branch
    dev_mode = get_dev_mode(config)

    if explicit_env_selector or command not in DEV_MODE_ROUTED_COMMANDS or dev_mode == DEV_MODE_MANUAL:
        return effective_cloud, effective_branch, dev_mode

    if command == "build":
        if dev_mode == DEV_MODE_LOCAL:
            return False, None, dev_mode

        git_branch = get_current_git_branch()
        if is_main_git_branch(git_branch):
            raise CLIException(
                FeedbackManager.error(
                    message=(
                        f"Cannot deploy to main workspace with '{get_cli_name()} build'. "
                        f"Use '{get_cli_name()} deploy' to deploy to production, or switch to a feature branch."
                    )
                )
            )

        tinybird_branch = get_tinybird_branch_name_from_git_branch(git_branch)
        if not tinybird_branch:
            raise CLIException(
                FeedbackManager.error(
                    message=(
                        "Cannot resolve a Tinybird branch from your current git branch. "
                        "Switch to a feature branch or use manual mode."
                    )
                )
            )
        return True, tinybird_branch, dev_mode

    if command == "deploy":
        _set_config_to_main_workspace(config, staging=staging)
        return True, None, dev_mode

    return effective_cloud, effective_branch, dev_mode


@click.group(
    cls=CatchAuthExceptions,
    context_settings={
        "help_option_names": ["-h", "--help"],
        "max_content_width": shutil.get_terminal_size().columns - 10,
    },
    invoke_without_command=True,
)
@click.option(
    "--debug/--no-debug",
    default=False,
    help="Prints internal representation, can be combined with any command to get more information.",
)
@click.option("--token", help="Use auth token, defaults to TB_TOKEN envvar, then to the .tinyb file.")
@click.option("--user-token", help="Use user token, defaults to TB_USER_TOKEN envvar, then to the .tinyb file.")
@click.option("--host", help="Use custom host, defaults to TB_HOST envvar, then to https://api.tinybird.co")
@click.option(
    "--version-warning/--no-version-warning",
    envvar="TB_VERSION_WARNING",
    default=True,
    help="Don't print version warning message if there's a new available version. You can use TB_VERSION_WARNING envar",
)
@click.option("--show-tokens", is_flag=True, default=False, help="Enable the output of tokens.")
@click.option("--cloud/--local", is_flag=True, default=False, help="Run against cloud or local.")
@click.option("--branch", help="Run against a branch.")
@click.option("--staging", is_flag=True, default=False, help="Run against a staging deployment.")
@click.option(
    "--output", type=click.Choice(["human", "json", "csv"], case_sensitive=False), default="human", help="Output format"
)
@click.option("--max-depth", type=int, default=3, help="Maximum depth of the project files.")
@click.version_option(version=VERSION)
@click.pass_context
def cli(
    ctx: Context,
    debug: bool,
    token: str,
    user_token: str,
    host: str,
    version_warning: bool,
    show_tokens: bool,
    cloud: bool,
    branch: Optional[str],
    staging: bool,
    output: str,
    max_depth: int,
) -> None:
    """
    Tinybird Forward CLI.
    """

    # We need to unpatch for our tests not to break
    if output != "human":
        __hide_click_output()
    elif show_tokens or not cloud or ctx.invoked_subcommand == "build":
        __unpatch_click_output()
    else:
        __patch_click_output()

    if getenv_bool("TB_DISABLE_SSL_CHECKS", False):
        click.echo(FeedbackManager.warning_disabled_ssl_checks())

    has_subcommand = ctx.invoked_subcommand is not None
    if not environ.get("PYTEST", None) and version_warning and not token and has_subcommand:
        latest_version = CheckPypi().get_latest_version()
        if latest_version:
            if "x.y.z" in CURRENT_VERSION:
                click.echo(FeedbackManager.warning_development_cli())

            if "x.y.z" not in CURRENT_VERSION and latest_version != CURRENT_VERSION:
                cli = get_cli_name(get_project_type_from_tinybird_config(os.getcwd()))
                click.echo(
                    FeedbackManager.warning(message=f"** New version available. {CURRENT_VERSION} -> {latest_version}")
                )
                click.echo(
                    FeedbackManager.warning(
                        message=f"** Run `{cli} update` to update or `export TB_VERSION_WARNING=0` to skip the check.\n"
                    )
                )

    if debug:
        logging.basicConfig(level=logging.DEBUG)

    # Check for conflicting environment flags.
    env_flags_in_argv = [arg for arg in sys.argv if arg in ("--cloud", "--local") or arg.startswith("--branch")]
    if len(env_flags_in_argv) > 1:
        raise CLIException(
            FeedbackManager.error(
                message=f"Cannot use multiple environment flags at the same time: {', '.join(env_flags_in_argv)}. "
                "Please use only one of the following: --cloud, --local, --branch=<branch_name>."
            )
        )
    explicit_env_selector = len(env_flags_in_argv) > 0
    validate_env_selector_for_command(ctx.invoked_subcommand, env_flags_in_argv)

    config_temp = CLIConfig.get_project_config()

    if token:
        config_temp.set_token(token)
    if host:
        config_temp.set_host(host)
    if user_token:
        config_temp.set_user_token(user_token)
    if token or host or user_token:
        try_update_config_with_remote(config_temp, auto_persist=True, raise_on_errors=False)

    # Overwrite token and host with env vars manually, without resorting to click.
    #
    # We need this to avoid confusing the new config class about where are
    # token and host coming from (we need to show the proper origin in
    # `tb auth info`)
    if not token and "TB_TOKEN" in os.environ:
        token = os.environ.get("TB_TOKEN", "")
    if not host and "TB_HOST" in os.environ:
        host = os.environ.get("TB_HOST", "")
    if not user_token and "TB_USER_TOKEN" in os.environ:
        user_token = os.environ.get("TB_USER_TOKEN", "")

    config = get_config(host, token, user_token=user_token, config_file=config_temp._path)
    project_type = get_project_type_from_tinybird_config(os.getcwd()) or PROJECT_TYPE_CLI
    ctx.ensure_object(dict)["project_type"] = project_type
    client, _ = _get_tb_client(config.get("token", ""), config["host"], request_from=project_type)

    tinybird_dev_mode = get_dev_mode_from_tinybird_config(os.getcwd())
    if tinybird_dev_mode:
        config["dev_mode"] = tinybird_dev_mode

    # Resolve project folder from tinybird.config.json (preferred) or legacy .tinyb cwd.
    folder_from_config = get_project_folder_from_tinybird_config(os.getcwd())
    if folder_from_config:
        folder = folder_from_config
    else:
        tinyb_dir = os.path.dirname(config_temp._path)  # Directory containing .tinyb file
        cwd_config = config.get("cwd", ".")

        if os.path.isabs(cwd_config):
            folder = cwd_config
        else:
            folder = os.path.normpath(os.path.join(tinyb_dir, cwd_config))

    project = Project(folder=folder, workspace_name=config.get("name", ""), max_depth=max_depth)

    sdk_virtual_project: Optional[Union[PythonVirtualProject, TypescriptVirtualProject]] = None
    if ctx.invoked_subcommand in SDK_PROJECT_ROUTED_COMMANDS:
        try:
            if project_type == PROJECT_TYPE_PYTHON:
                sdk_virtual_project = get_python_virtual_project(
                    project_folder=folder,
                    workspace_name=config.get("name", ""),
                    max_depth=max_depth,
                )
                if sdk_virtual_project:
                    project = sdk_virtual_project.project
                    ctx.ensure_object(dict)["_python_virtual_project"] = sdk_virtual_project
            elif project_type == PROJECT_TYPE_TYPESCRIPT:
                sdk_virtual_project = get_typescript_virtual_project(
                    project_folder=folder,
                    workspace_name=config.get("name", ""),
                    max_depth=max_depth,
                )
                if sdk_virtual_project:
                    project = sdk_virtual_project.project
                    ctx.ensure_object(dict)["_typescript_virtual_project"] = sdk_virtual_project
        except Exception as exc:
            raise CLIException(str(exc))

    # Keep config path pointing to the user project root even when using a virtual SDK project.
    config["path"] = folder if sdk_virtual_project else str(project.path)
    # If they have passed a token or host as parameter and it's different that record in .tinyb, refresh the workspace id
    if token or host:
        try:
            workspace = client.workspace_info(version="v1")
            config["id"] = workspace.get("id", "")
            config["name"] = workspace.get("name", "")
        except (AuthNoTokenException, AuthException):
            pass

    ctx.ensure_object(dict)["config"] = config

    logging.debug("debug enabled")

    if "--help" in sys.argv or "-h" in sys.argv:
        return

    ctx.ensure_object(dict)["project"] = project

    if not has_subcommand:
        click.echo(ctx.get_help())
        return

    effective_cloud, effective_branch, dev_mode = resolve_dev_mode_target(
        command=ctx.invoked_subcommand,
        config=config,
        cloud=cloud,
        branch=branch,
        staging=staging,
        explicit_env_selector=explicit_env_selector,
    )
    effective_cloud, switched_datasource_create_to_cloud = resolve_datasource_create_target(
        command=ctx.invoked_subcommand,
        argv=sys.argv,
        explicit_env_selector=explicit_env_selector,
        effective_cloud=effective_cloud,
    )

    if switched_datasource_create_to_cloud:
        click.echo(
            FeedbackManager.gray(
                message=(
                    f"Tinybird Local is not running. Running `{get_cli_name()} datasource create` against Tinybird Cloud."
                )
            )
        )

    if not explicit_env_selector and dev_mode != DEV_MODE_MANUAL and ctx.invoked_subcommand in DEV_MODE_ROUTED_COMMANDS:
        if ctx.invoked_subcommand == "build" and dev_mode == DEV_MODE_BRANCH and effective_branch:
            click.echo(
                FeedbackManager.gray(
                    message=f"Using dev_mode=branch. Running build against Tinybird branch '{effective_branch}'."
                )
            )
        elif ctx.invoked_subcommand == "build" and dev_mode == DEV_MODE_LOCAL:
            click.echo(FeedbackManager.gray(message="Using dev_mode=local. Running build against Tinybird Local."))
        elif ctx.invoked_subcommand == "deploy":
            click.echo(
                FeedbackManager.gray(message=f"Using dev_mode={dev_mode}. Running deploy against Tinybird Cloud main.")
            )

    client = create_ctx_client(
        ctx,
        config,
        effective_cloud,
        staging,
        project=project,
        project_type=project_type,
        show_warnings=version_warning,
        branch=effective_branch,
        create_branch_if_missing=(
            not explicit_env_selector
            and ctx.invoked_subcommand == "build"
            and dev_mode == DEV_MODE_BRANCH
            and bool(effective_branch)
        ),
    )

    if client:
        ctx.ensure_object(dict)["client"] = client

    force_cloud_env = ctx.invoked_subcommand in COMMANDS_ALWAYS_CLOUD
    ctx.ensure_object(dict)["env"] = get_target_env(effective_cloud or force_cloud_env, effective_branch)
    ctx.ensure_object(dict)["branch"] = effective_branch
    ctx.ensure_object(dict)["dev_mode"] = dev_mode
    ctx.ensure_object(dict)["output"] = output

    # Check if current folder is tracked from previous sessions
    check_current_folder_in_sessions(ctx)


@cli.command(hidden=True)
@click.option("--only-vendored", is_flag=True, default=False, help="Only update vendored files")
@click.option("-f", "--force", is_flag=True, default=False, help="Override existing files")
@click.option("--fmt", is_flag=True, default=False, help="Format files before saving")
@click.pass_context
def pull(ctx: Context, only_vendored: bool, force: bool, fmt: bool) -> None:
    """Retrieve latest versions for project files from Tinybird."""

    client = ctx.ensure_object(dict)["client"]
    project = ctx.ensure_object(dict)["project"]

    if only_vendored:
        force = True

    written_files = folder_pull(client, project.path, force, only_vendored=only_vendored, fmt=fmt)

    if only_vendored:
        for_user_to_delete = set(project.get_vendored_files()) - set(written_files)
        if for_user_to_delete:
            # TODO(eclbg): this prints the full path of the files. Let's print the relative path from the project root
            display_paths = []
            for full_path in for_user_to_delete:
                try:
                    display_paths.append(str(Path(full_path).relative_to(project.path)))
                except:
                    display_paths.append(full_path)
            click.echo(
                FeedbackManager.warning(
                    message=(
                        f"This workspace no longer has access to the following files: {display_paths}. "
                        "Please remove them manually to be able to deploy."
                    )
                )
            )


@cli.command()
@click.argument("query", required=False)
@click.option("--rows-limit", default=100, help="Max number of rows retrieved")
@click.option("--pipeline", default=None, help="The name of the pipe to run the SQL Query")
@click.option("--pipe", default=None, help="The path to the .pipe file to run the SQL Query of a specific NODE")
@click.option("--node", default=None, help="The NODE name")
@click.option("--stats/--no-stats", default=False, help="Show query stats")
@click.pass_context
def sql(
    ctx: Context,
    query: str,
    rows_limit: int,
    pipeline: Optional[str],
    pipe: Optional[str],
    node: Optional[str],
    stats: bool,
) -> None:
    """Run SQL query over data sources and pipes."""
    client = ctx.ensure_object(dict)["client"]
    output = ctx.ensure_object(dict)["output"]

    req_format = "CSVWithNames" if output == "csv" else "JSON"
    res = None
    try:
        if not query and not sys.stdin.isatty():  # Check if there's piped input
            query = sys.stdin.read().strip()

        if query:
            if query.endswith(";"):
                query = query[:-1].strip()
            q = query.lower().strip()
            if q.startswith("insert"):
                click.echo(FeedbackManager.info_append_data())
                raise CLIException(FeedbackManager.error_invalid_query())
            if q.startswith("delete"):
                raise CLIException(FeedbackManager.error_invalid_query())
            res = client.query(f"SELECT * FROM ({query}) LIMIT {rows_limit} FORMAT {req_format}", pipeline=pipeline)
        elif pipe and node:
            filenames = [pipe]

            # build graph to get new versions for all the files involved in the query
            # dependencies need to be processed always to get the versions
            dependencies_graph = build_graph(
                filenames,
                client,
                dir_path=".",
                process_dependencies=True,
                skip_connectors=True,
            )

            query = ""
            for elem in dependencies_graph.to_run.values():
                for _node in elem["nodes"]:
                    if _node["params"]["name"].lower() == node.lower():
                        query = "".join(_node["sql"])
            pipeline = pipe.split("/")[-1].split(".pipe")[0]
            res = client.query(f"SELECT * FROM ({query}) LIMIT {rows_limit} FORMAT {req_format}", pipeline=pipeline)

    except AuthNoTokenException:
        raise
    except Exception as e:
        raise CLIException(FeedbackManager.error_exception(error=str(e)))

    if isinstance(res, dict) and "error" in res:
        raise CLIException(FeedbackManager.error_exception(error=res["error"]))

    if stats:
        stats_query = f"SELECT * FROM ({query}) LIMIT {rows_limit} FORMAT JSON"
        stats_res = client.query(stats_query, pipeline=pipeline)
        stats_dict = stats_res["statistics"]
        seconds = stats_dict["elapsed"]
        rows_read = humanfriendly.format_number(stats_dict["rows_read"])
        bytes_read = humanfriendly.format_size(stats_dict["bytes_read"])
        click.echo(FeedbackManager.info_query_stats(seconds=seconds, rows=rows_read, bytes=bytes_read))

    if output == "csv":
        force_echo(str(res))
    elif isinstance(res, dict) and "data" in res and res["data"]:
        if output == "json":
            echo_json(res, indent=8)
        else:
            dd = [d.values() for d in res["data"]]
            echo_safe_format_table(dd, columns=res["meta"])
    else:
        click.echo(FeedbackManager.info_no_rows())


@cli.command(
    name="ch",
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    ),
)
@click.option(
    "--query",
    type=str,
    default=None,
    required=False,
    help="The query to run against ClickHouse.",
)
@click.option(
    "--user",
    required=False,
    help="User field is not used for authentication but helps identify the connection.",
)
@click.option(
    "--password",
    required=False,
    help="Your Tinybird Auth Token. If not provided, the token will be your current workspace token.",
)
@click.option(
    "-m",
    "--multiline",
    is_flag=True,
    default=False,
    help="Enable multiline mode - read the query from multiple lines until a semicolon.",
)
@click.pass_context
def ch(ctx: Context, query: str, user: Optional[str], password: Optional[str], multiline: bool) -> None:
    """Run a query against ClickHouse native HTTP interface."""
    try:
        query_arg = next((arg for arg in ctx.args if not arg.startswith("--param_")), None)
        if query_arg and not query:
            query = query_arg

        if not query and not sys.stdin.isatty():  # Check if there's piped input
            query = sys.stdin.read().strip()

        if not query:
            click.echo(FeedbackManager.warning(message="Nothing to do. No query provided"))
            return

        if multiline:
            queries = [query.strip() for query in query.split(";") if query.strip()]
        else:
            queries = [query]

        client: TinyB = ctx.ensure_object(dict)["client"]
        config = ctx.ensure_object(dict)["config"]
        password = password or client.token
        user = user or config.get("name", None)
        ch_host = get_clickhouse_host(client.host)
        headers = {"X-ClickHouse-Key": password}
        if user:
            headers["X-ClickHouse-User"] = user

        params = {}

        for param in ctx.args:
            if param.startswith("--param_"):
                param_name = param.split("=")[0].replace("--", "")
                param_value = param.split("=")[1]
                params[param_name] = param_value

        for query in queries:
            query_params = {**params, "query": query}
            url = f"{ch_host}?{urlencode(query_params)}"
            res = requests.get(url=url, headers=headers)

            if res.status_code != 200:
                raise Exception(res.text)

            click.echo(res.text)

    except Exception as e:
        raise CLIChException(FeedbackManager.error(message=str(e)))


def __patch_click_output():
    CUSTOM_PATTERNS: List[str] = []

    _env_patterns = os.getenv("OBFUSCATE_REGEX_PATTERN", None)
    if _env_patterns:
        CUSTOM_PATTERNS = _env_patterns.split(os.getenv("OBFUSCATE_PATTERN_SEPARATOR", "|"))

    def _obfuscate(msg: Any, *args: Any, **kwargs: Any) -> Any:
        for pattern in CUSTOM_PATTERNS:
            msg = re.sub(pattern, "****...****", str(msg))

        for pattern, substitution in DEFAULT_PATTERNS:
            if isinstance(substitution, str):
                msg = re.sub(pattern, substitution, str(msg))
            else:
                msg = re.sub(pattern, lambda m: substitution(m.group(0)), str(msg))  # noqa: B023
        return msg

    def _obfuscate_echo(msg: Any, *args: Any, **kwargs: Any) -> None:
        msg = _obfuscate(msg, *args, **kwargs)
        __old_click_echo(msg, *args, **kwargs)

    def _obfuscate_secho(msg: Any, *args: Any, **kwargs: Any) -> None:
        msg = _obfuscate(msg, *args, **kwargs)
        __old_click_secho(msg, *args, **kwargs)

    click.echo = lambda msg, *args, **kwargs: _obfuscate_echo(msg, *args, **kwargs)
    click.secho = lambda msg, *args, **kwargs: _obfuscate_secho(msg, *args, **kwargs)


def __unpatch_click_output():
    click.echo = __old_click_echo
    click.secho = __old_click_secho


def __hide_click_output() -> None:
    """
    Modify click.echo and click.secho to only output when explicitly requested.
    Adds a 'force_output' parameter to both functions that defaults to False.
    """

    def silent_echo(msg: Any, *args: Any, force_output: bool = False, **kwargs: Any) -> None:
        if force_output:
            __old_click_echo(msg, *args, **kwargs)

    def silent_secho(msg: Any, *args: Any, force_output: bool = False, **kwargs: Any) -> None:
        if force_output:
            __old_click_secho(msg, *args, **kwargs)

    click.echo = silent_echo  # type: ignore
    click.secho = silent_secho  # type: ignore


def create_ctx_client(
    ctx: Context,
    config: Dict[str, Any],
    cloud: bool,
    staging: bool,
    project: Project,
    project_type: str = PROJECT_TYPE_CLI,
    show_warnings: bool = True,
    branch: Optional[str] = None,
    create_branch_if_missing: bool = False,
):
    commands_without_ctx_client = [
        "auth",
        "binary",
        "check",
        "create",
        "local",
        "login",
        "mock",
        "logout",
        "update",
        "upgrade",
        "info",
        "tag",
        "push",
        "branch",
        "environment",
        "diff",
        "fmt",
        "init",
        "project",
        "preview",
    ]
    command = ctx.invoked_subcommand
    if not command or command in commands_without_ctx_client:
        return None

    command_always_test = ["test"]

    if (cloud or command in COMMANDS_ALWAYS_CLOUD) and command not in command_always_test:
        if show_warnings:
            target_message = f"Running against Tinybird Cloud: Workspace {config.get('name', 'default')}"
            if branch:
                target_message = f"{target_message} | branch {branch}"
            click.echo(FeedbackManager.gray(message=target_message))

        method = None
        if ctx.params.get("token"):
            method = "token via --token option"
        elif os.environ.get("TB_TOKEN"):
            method = "token from TB_TOKEN environment variable"
        if method and show_warnings:
            click.echo(FeedbackManager.gray(message=f"Authentication method: {method}"))

        client, branch_created = _get_tb_client(
            config.get("token", ""),
            config["host"],
            staging=staging,
            branch=branch,
            create_branch_if_missing=create_branch_if_missing,
            request_from=project_type,
        )
        ctx.ensure_object(dict)["branch_created"] = branch_created
        return client
    test = command in command_always_test
    if show_warnings and command:
        click.echo(FeedbackManager.gray(message="Running against Tinybird Local"))
    local_branch = None
    if command in ("build", "dev") and not test:
        git_branch = get_current_git_branch()
        if git_branch and not is_main_git_branch(git_branch):
            local_branch = get_tinybird_branch_name_from_git_branch(git_branch)
            ctx.ensure_object(dict)["git_branch"] = git_branch
    client, workspace_created = get_tinybird_local_client(config, test=test, staging=staging, branch=local_branch)
    if local_branch:
        ctx.ensure_object(dict)["local_branch"] = local_branch
        ctx.ensure_object(dict)["branch_created"] = workspace_created
    return client


def get_target_env(cloud: bool, branch: Optional[str]) -> str:
    if cloud or bool(branch):
        return "cloud"
    return "local"


def get_config(
    host: str,
    token: Optional[str],
    user_token: Optional[str],
    semver: Optional[str] = None,
    config_file: Optional[str] = None,
) -> Dict[str, Any]:
    if host:
        host = host.rstrip("/")

    config = {}
    try:
        with open(config_file or Path(getcwd()) / ".tinyb") as file:
            res = file.read()
            config = json.loads(res)
    except OSError:
        pass
    except json.decoder.JSONDecodeError:
        click.echo(FeedbackManager.error_load_file_config(config_file=config_file))
        return config

    config["token_passed"] = token
    config["token"] = token or config.get("token", None)
    config["user_token"] = user_token or config.get("user_token", None)
    config["semver"] = semver or config.get("semver", None)
    config["host"] = host or config.get("host", "https://api.europe-west2.gcp.tinybird.co")
    config["workspaces"] = config.get("workspaces", [])
    config["cwd"] = config.get("cwd", getcwd())
    config["dev_mode"] = get_dev_mode(config)
    return config
