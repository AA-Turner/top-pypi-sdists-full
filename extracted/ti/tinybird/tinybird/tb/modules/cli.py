# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.
import json
import logging
import os
import shutil
import sys
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
from tinybird.tb.modules.agent import run_agent
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
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.local_common import get_tinybird_local_client
from tinybird.tb.modules.login_common import check_current_folder_in_sessions
from tinybird.tb.modules.project import Project

__old_click_echo = click.echo
__old_click_secho = click.secho
DEFAULT_PATTERNS: List[Tuple[str, Union[str, Callable[[str], str]]]] = [
    (r"p\.ey[A-Za-z0-9-_\.]+", lambda v: f"{v[:4]}...{v[-8:]}")
]
VERSION = f"{__cli__.__version__} (rev {__cli__.__revision__})"


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
@click.option(
    "--dangerously-skip-permissions",
    is_flag=True,
    default=False,
    help="Skip permissions check in Tinybird Code.",
)
@click.option(
    "--prompt",
    "-p",
    help="Run Tinybird Code in prompt mode with the provided input and exit.",
)
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
    dangerously_skip_permissions: bool,
    prompt: Optional[str] = None,
) -> None:
    """
    Run just `tb` to use Tinybird Code to interact with your project.
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

    is_agent_mode = ctx.invoked_subcommand is None
    if not environ.get("PYTEST", None) and version_warning and not token and not is_agent_mode:
        latest_version = CheckPypi().get_latest_version()
        if latest_version:
            if "x.y.z" in CURRENT_VERSION:
                click.echo(FeedbackManager.warning_development_cli())

            if "x.y.z" not in CURRENT_VERSION and latest_version != CURRENT_VERSION:
                click.echo(
                    FeedbackManager.warning(message=f"** New version available. {CURRENT_VERSION} -> {latest_version}")
                )
                click.echo(
                    FeedbackManager.warning(
                        message="** Run `tb update` to update or `export TB_VERSION_WARNING=0` to skip the check.\n"
                    )
                )

    if debug:
        logging.basicConfig(level=logging.DEBUG)

    # Check for conflicting environment flags
    # Users should not use multiple environment selectors at the same time
    env_flags_in_argv = [arg for arg in sys.argv if arg in ("--cloud", "--local") or arg.startswith("--branch")]
    if len(env_flags_in_argv) > 1:
        raise CLIException(
            FeedbackManager.error(
                message=f"Cannot use multiple environment flags at the same time: {', '.join(env_flags_in_argv)}. "
                "Please use only one of the following: --cloud, --local, --branch=<branch_name>."
            )
        )

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
    client = _get_tb_client(config.get("token", ""), config["host"])

    # Calculate project folder path properly
    tinyb_dir = os.path.dirname(config_temp._path)  # Directory containing .tinyb file
    cwd_config = config.get("cwd", ".")

    if os.path.isabs(cwd_config):
        # If cwd is absolute, use it directly
        folder = cwd_config
    else:
        # If cwd is relative, resolve it relative to .tinyb directory
        folder = os.path.normpath(os.path.join(tinyb_dir, cwd_config))

    project = Project(folder=folder, workspace_name=config.get("name", ""), max_depth=max_depth)
    config["path"] = str(project.path)
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
    client = create_ctx_client(
        ctx,
        config,
        cloud or bool(branch),
        staging,
        project=project,
        show_warnings=version_warning,
        branch=branch,
    )

    if client:
        ctx.ensure_object(dict)["client"] = client

    ctx.ensure_object(dict)["env"] = get_target_env(cloud, branch)
    ctx.ensure_object(dict)["branch"] = branch
    ctx.ensure_object(dict)["output"] = output

    # Check if current folder is tracked from previous sessions
    check_current_folder_in_sessions(ctx)

    is_prompt_mode = prompt is not None

    if is_agent_mode or is_prompt_mode:
        if any(arg in sys.argv for arg in ["--cloud", "--local", "--branch"]):
            raise CLIException(
                FeedbackManager.error(
                    message="Tinybird Code does not support --cloud, --local or --branch flags. It will choose the correct environment based on your prompts."
                )
            )

        run_agent(config, project, dangerously_skip_permissions, prompt=prompt)


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
            dd = []
            for d in res["data"]:
                dd.append(d.values())
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
    import re

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
    show_warnings: bool = True,
    branch: Optional[str] = None,
):
    commands_without_ctx_client = [
        "auth",
        "check",
        "local",
        "login",
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
    ]
    command = ctx.invoked_subcommand
    if not command or command in commands_without_ctx_client:
        return None

    commands_always_cloud = ["infra", "branch", "environment"]
    commands_always_local = ["create"]
    command_always_test = ["test"]

    if (
        (cloud or command in commands_always_cloud)
        and command not in commands_always_local
        and command not in command_always_test
    ):
        if show_warnings:
            click.echo(
                FeedbackManager.gray(
                    message=f"Running against Tinybird Cloud: Workspace {config.get('name', 'default')}"
                )
            )

        method = None
        if ctx.params.get("token"):
            method = "token via --token option"
        elif os.environ.get("TB_TOKEN"):
            method = "token from TB_TOKEN environment variable"
        if method and show_warnings:
            click.echo(FeedbackManager.gray(message=f"Authentication method: {method}"))

        return _get_tb_client(config.get("token", ""), config["host"], staging=staging, branch=branch)
    local = command in commands_always_local
    test = command in command_always_test
    if show_warnings and not local and command not in commands_always_local and command:
        click.echo(FeedbackManager.gray(message="Running against Tinybird Local"))
    return get_tinybird_local_client(config, test=test, staging=staging)


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
    return config
