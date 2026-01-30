# This is the common file for our CLI. Please keep it clean (as possible)
#
# - Put here any common utility function you consider.
# - If any function is only called within a specific command, consider moving
#   the function to the proper command file.
# - Please, **do not** define commands here.

import json
import logging
import os
import re
import socket
import subprocess
import sys
import time
import uuid
from contextlib import closing
from copy import deepcopy
from enum import Enum
from os import getcwd, getenv
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Literal, Optional, Set, Tuple, TypedDict, Union
from urllib.parse import urlparse

import click
import click.formatting
import humanfriendly
import humanfriendly.tables
import pyperclip
import requests
from click import Context
from click._termui_impl import ProgressBar
from humanfriendly.tables import format_pretty_table
from thefuzz import process

from tinybird.tb.client import (
    AuthException,
    AuthNoTokenException,
    DoesNotExistException,
    JobException,
    OperationCanNotBePerformed,
    TinyB,
)
from tinybird.tb.config import (
    DEFAULT_API_HOST,
    DEFAULT_UI_HOST,
    VERSION,
    FeatureFlags,
    get_config,
    get_display_cloud_host,
)
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.exceptions import (
    CLIAuthException,
    CLIConnectionException,
    CLIException,
    CLIWorkspaceException,
)
from tinybird.tb.modules.feedback_manager import FeedbackManager, warning_message
from tinybird.tb.modules.local_common import get_tinybird_local_client
from tinybird.tb.modules.regions import Region
from tinybird.tb.modules.table import format_table
from tinybird.tb.modules.telemetry import (
    add_telemetry_event,
    add_telemetry_sysinfo_event,
    flush_telemetry,
    init_telemetry,
)

# Pre-compiled regex patterns
_PATTERN_NORMALIZE_NAME = re.compile(r"[^0-9a-zA-Z_]")
_PATTERN_AWS_ARN = re.compile(r"arn:aws:iam::(\d+):root")

SUPPORTED_FORMATS = ["csv", "ndjson", "json", "parquet"]
OLDEST_ROLLBACK = "oldest_rollback"
MAIN_BRANCH = "main"


def obfuscate_token(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    return f"{value[:4]}...{value[-8:]}"


def gather_with_concurrency(n, *tasks):
    results = []
    for task in tasks:
        if callable(task):
            results.append(task())
        else:
            results.append(task)
    return results


def format_robust_table(data: Iterable[Any], column_names: List[str]):
    return humanfriendly.tables.format_robust_table(data, column_names=column_names)


def echo_safe_humanfriendly_tables_format_smart_table(data: Iterable[Any], column_names: List[str]) -> None:
    """
    There is a bug in the humanfriendly library: it breaks to render the small table for small terminals
    (`format_robust_table`) if we call format_smart_table with an empty dataset. This catches the error and prints
    what we would call an empty "robust_table".
    """
    try:
        click.echo(humanfriendly.tables.format_smart_table(data, column_names=column_names))
    except ValueError as exc:
        if str(exc) == "max() arg is an empty sequence":
            click.echo("------------")
            click.echo("Empty")
            click.echo("------------")
        else:
            raise exc


def echo_safe_humanfriendly_tables_format_pretty_table(data: Iterable[Any], column_names: List[str]) -> None:
    """
    There is a bug in the humanfriendly library: it breaks to render the small table for small terminals
    (`format_robust_table`) if we call format_smart_table with an empty dataset. This catches the error and prints
    what we would call an empty "robust_table".
    """
    try:
        click.echo(humanfriendly.tables.format_pretty_table(data, column_names=column_names))
    except ValueError as exc:
        if str(exc) == "max() arg is an empty sequence":
            click.echo("------------")
            click.echo("Empty")
            click.echo("------------")
        else:
            raise exc


def echo_safe_format_table(data: Iterable[Any], columns) -> None:
    """
    There is a bug in the humanfriendly library: it breaks to render the small table for small terminals
    (`format_robust_table`) if we call format_smart_table with an empty dataset. This catches the error and prints
    what we would call an empty "robust_table".
    """
    try:
        click.echo(format_table(data, columns))
    except ValueError as exc:
        if str(exc) == "max() arg is an empty sequence":
            click.echo("------------")
            click.echo("Empty")
            click.echo("------------")
        else:
            raise exc


def normalize_datasource_name(s: str) -> str:
    s = _PATTERN_NORMALIZE_NAME.sub("_", s)
    if s[0] in "0123456789":
        return "c_" + s
    return s


def generate_datafile(
    datafile: str,
    filename: str,
    data: Optional[bytes],
    force: Optional[bool] = False,
    _format: Optional[str] = "csv",
    folder: Optional[str] = None,
) -> Path:
    p = Path(filename)
    base = Path("datasources")
    if folder:
        base = Path(folder) / base
    datasource_name = normalize_datasource_name(p.stem)
    if not base.exists():
        if folder:
            base = Path(folder)
        else:
            base = Path()
    f = base / (datasource_name + ".datasource")

    if not f.exists() or force:
        with open(f"{f}", "w") as ds_file:
            ds_file.write(datafile)
        click.echo(FeedbackManager.info_file_created(file=f.relative_to(folder or ".")))

        if data and (base / "fixtures").exists():
            # Generating a fixture for Parquet files is not so trivial, since Parquet format
            # is column-based. We would need to add PyArrow as a dependency (which is huge)
            # just to analyze the whole Parquet file to extract one single row.
            if _format == "parquet":
                click.echo(FeedbackManager.warning_parquet_fixtures_not_supported())
            else:
                f = base / "fixtures" / (p.stem + f".{_format}")
                newline = b"\n"  # TODO: guess
                with open(f, "wb") as fixture_file:
                    fixture_file.write(data[: data.rfind(newline)])
    else:
        click.echo(FeedbackManager.error_file_already_exists(file=f))
    return f


def get_current_workspace(config: CLIConfig) -> Optional[Dict[str, Any]]:
    client = config.get_client()
    workspaces: List[Dict[str, Any]] = (client.user_workspaces_and_branches(version="v1")).get("workspaces", [])
    return _get_current_workspace_common(workspaces, config["id"])


def get_workspace_member_email(workspace, member_id) -> str:
    return next((member["email"] for member in workspace["members"] if member["id"] == member_id), "-")


def _get_current_workspace_common(
    workspaces: List[Dict[str, Any]], current_workspace_id: str
) -> Optional[Dict[str, Any]]:
    return next((workspace for workspace in workspaces if workspace["id"] == current_workspace_id), None)


def get_current_environment(client, config):
    workspaces: List[Dict[str, Any]] = (client.user_workspaces_and_branches(version="v1")).get("workspaces", [])
    return next((workspace for workspace in workspaces if workspace["id"] == config["id"]), None)


class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        # Step one: built-in commands as normal
        cm = click.Group.get_command(self, ctx, cmd_name)
        if cm is not None:
            return cm

    def resolve_command(self, ctx, args):
        # always return the command's name, not the alias
        _, cmd, args = super().resolve_command(ctx, args)
        return cmd.name, cmd, args  # type: ignore[union-attr]


class CatchAuthExceptions(AliasedGroup):
    """utility class to get all the auth exceptions"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        init_telemetry()
        add_telemetry_sysinfo_event()
        super().__init__(*args, **kwargs)

    def format_epilog(self, ctx: Context, formatter: click.formatting.HelpFormatter) -> None:
        super().format_epilog(ctx, formatter)

        formatter.write_paragraph()
        formatter.write_heading("Telemetry")
        formatter.write_text(
            """
  Tinybird collects usage data and errors to improve the command
line experience. To opt-out, set TB_CLI_TELEMETRY_OPTOUT to '1' or 'true'."""
        )
        formatter.write_paragraph()

    def __call__(self, *args, **kwargs) -> None:
        error_msg: Optional[str] = None
        silent_error_msg: Optional[str] = None
        error_event: str = "error"

        exit_code: int = 0

        try:
            self.main(*args, **kwargs)
        except AuthNoTokenException:
            error_msg = FeedbackManager.error_notoken()
            error_event = "auth_error"
            exit_code = 1
        except AuthException as ex:
            error_msg = FeedbackManager.error_exception(error=str(ex))
            error_event = "auth_error"
            exit_code = 1
        except SystemExit as ex:
            if isinstance(ex.code, str):
                exit_code = 1
                error_event, silent_error_msg = get_error_event(ex.code)
            else:
                exit_code = ex.code or 0
        except Exception as ex:
            error_msg = str(ex)
            exit_code = 1

        if error_msg or silent_error_msg:
            if error_msg:
                click.echo(error_msg)
            add_telemetry_event(error_event, error=error_msg or silent_error_msg)
        flush_telemetry(wait=True)

        sys.exit(exit_code)

    def get_command(self, ctx: click.Context, cmd_name: str) -> Optional[click.Command]:
        """
        Override get_command to add suggestion functionality.

        Args:
            ctx: Click context
            cmd_name: Command name entered by user

        Returns:
            Click command if found, None otherwise
        """
        # First, try to get the command normally
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv

        # Get all available commands
        commands: List[str] = list_commands(self, ctx)

        # Find closest matching command using thefuzz
        matches = process.extract(cmd_name, commands, limit=1)
        if not matches:
            return None

        suggestion, score = matches[0]

        # Only suggest if the similarity score is high enough (adjust threshold as needed)
        if score >= 65:
            # Build the suggested command from the raw arguments,
            # preserving only those explicitly passed by the user.
            raw_args = sys.argv[1:]
            try:
                idx = raw_args.index(cmd_name)
            except ValueError:
                # If the mistyped command isn't found, use all as 'after'.
                before = []
                after = raw_args
            else:
                before = raw_args[:idx]
                after = raw_args[idx + 1 :]

            full_tokens = [ctx.command_path, *before, suggestion, *after]
            full_command = " ".join(full_tokens)

            click.echo(f"\nWARNING: '{cmd_name}' is not a valid command. ", nl=False)
            # Ask for confirmation
            if click.confirm(f"Execute '{full_command}' instead?"):
                return click.Group.get_command(self, ctx, suggestion)

        return None


def list_commands(self, ctx: Context):
    all_commands = self.list_commands(ctx)
    return [cmd for cmd in all_commands if not self.get_command(ctx, cmd).hidden]


def getenv_bool(key: str, default: bool) -> bool:
    v: Optional[str] = getenv(key)
    if v is None:
        return default
    return v.lower() == "true" or v == "1"


def _get_tb_client(token: str, host: str, staging: bool = False, branch: Optional[str] = None) -> TinyB:
    disable_ssl: bool = getenv_bool("TB_DISABLE_SSL_CHECKS", False)
    cloud_client = TinyB(
        token,
        host,
        version=VERSION,
        disable_ssl_checks=disable_ssl,
        send_telemetry=True,
        staging=staging,
    )

    if not branch:
        return cloud_client

    workspaces = cloud_client.user_workspaces_and_branches(version="v1")
    workspace = next((w for w in workspaces.get("workspaces", []) if w.get("name") == branch), None)
    if not workspace:
        raise CLIException(FeedbackManager.error_exception(error=f"Branch {branch} not found"))

    return TinyB(
        workspace.get("token", ""),
        host,
        version=VERSION,
        disable_ssl_checks=disable_ssl,
        send_telemetry=True,
        staging=staging,
    )


def create_tb_client(ctx: Context) -> TinyB:
    token = ctx.ensure_object(dict)["config"].get("token", "")
    host = ctx.ensure_object(dict)["config"].get("host", DEFAULT_API_HOST)
    return _get_tb_client(token, host)


def _analyze(filename: str, client: TinyB, format: str):
    data: Optional[bytes] = None
    parsed = urlparse(filename)
    if parsed.scheme in ("http", "https"):
        meta = client.datasource_analyze(filename)
    else:
        with open(filename, "rb") as file:
            # We need to read the whole file in binary for Parquet, while for the
            # others we just read 1KiB
            if format == "parquet":
                data = file.read()
            else:
                data = file.read(1024 * 1024)

        meta = client.datasource_analyze_file(data)
    return meta, data


def analyze_file(filename: str, client: TinyB, format: str):
    meta, data = _analyze(filename, client, format)
    schema = meta["analysis"]["schema"]
    schema = schema.replace(", ", ",\n    ")
    content = f"""DESCRIPTION >
    Generated from {filename}

SCHEMA >
    {schema}

ENGINE "MergeTree"
# ENGINE_SORTING_KEY "user_id, timestamp"
# ENGINE_TTL "timestamp + toIntervalDay(60)"
# Learn more at https://www.tinybird.co/docs/forward/dev-reference/datafiles/datasource-files"""
    return content


def _generate_datafile(
    filename: str,
    client: TinyB,
    format: str,
    force: Optional[bool] = False,
    folder: Optional[str] = None,
):
    meta, data = _analyze(filename, client, format)
    schema = meta["analysis"]["schema"]
    schema = schema.replace(", ", ",\n    ")
    datafile = f"""DESCRIPTION >
    Generated from {filename}

SCHEMA >
    {schema}

ENGINE "MergeTree"
# ENGINE_SORTING_KEY "user_id, timestamp"
# ENGINE_TTL "timestamp + toIntervalDay(60)"
# Learn more at https://www.tinybird.co/docs/forward/dev-reference/datafiles/datasource-files"""
    return generate_datafile(datafile, filename, data, force, _format=format, folder=folder)


def _compare_region_host(region_name_or_host: str, region: Dict[str, Any]) -> bool:
    if region["name"].lower() == region_name_or_host:
        return True
    if region["host"] == region_name_or_host:
        return True
    return region["api_host"] == region_name_or_host


def ask_for_region_interactively(regions):
    region_index = -1

    while region_index == -1:
        for index, region in enumerate(regions):
            provider = f" ({region.get('provider')})" if region.get("provider") else ""
            click.echo(
                f"  [{index + 1}] {region['name'].lower()}{provider} ({region['host'].replace('app.tinybird.co', 'cloud.tinybird.co')}) "
            )
        click.echo("  [0] Cancel")

        region_index = click.prompt("\nUse region", default=1)

        if region_index == 0:
            click.echo(FeedbackManager.warning(message="Region selection cancelled by user"))
            return None

        try:
            return regions[int(region_index) - 1]
        except Exception:
            available_options = ", ".join(map(str, range(1, len(regions) + 1)))
            click.echo(FeedbackManager.error_region_index(host_index=region_index, available_options=available_options))
            region_index = -1


def get_region_info(ctx, region=None):
    name = region["name"] if region else "default"
    api_host = format_host(
        region["api_host"] if region else ctx.obj["config"].get("host", DEFAULT_API_HOST), subdomain="api"
    )
    ui_host = format_host(
        region["host"] if region else ctx.obj["config"].get("host", DEFAULT_UI_HOST), subdomain="cloud"
    )

    return name, api_host, ui_host


def format_host(host: str, subdomain: Optional[str] = None) -> str:
    """
    >>> format_host('api.tinybird.co')
    'https://api.tinybird.co'
    >>> format_host('https://api.tinybird.co')
    'https://api.tinybird.co'
    >>> format_host('http://localhost:8001')
    'http://localhost:8001'
    >>> format_host('localhost:8001')
    'http://localhost:8001'
    >>> format_host('localhost:8001', subdomain='ui')
    'http://localhost:8001'
    >>> format_host('localhost:8001', subdomain='api')
    'http://localhost:8001'
    >>> format_host('https://api.tinybird.co', subdomain='ui')
    'https://ui.tinybird.co'
    >>> format_host('https://api.us-east.tinybird.co', subdomain='ui')
    'https://ui.us-east.tinybird.co'
    >>> format_host('https://api.us-east.tinybird.co', subdomain='api')
    'https://api.us-east.tinybird.co'
    >>> format_host('https://ui.us-east.tinybird.co', subdomain='api')
    'https://api.us-east.tinybird.co'
    >>> format_host('https://inditex-rt-pro.tinybird.co', subdomain='ui')
    'https://inditex-rt-pro.tinybird.co'
    >>> format_host('https://cluiente-tricky.tinybird.co', subdomain='api')
    'https://cluiente-tricky.tinybird.co'
    """
    is_localhost = FeatureFlags.is_localhost()
    if subdomain and not is_localhost:
        url_info = urlparse(host)
        current_subdomain = url_info.netloc.split(".")[0]
        if current_subdomain in ("api", "ui", "app", "cloud"):
            host = host.replace(current_subdomain, subdomain)
    if "localhost" in host or is_localhost:
        host = f"http://{host}" if "http" not in host else host
    elif not host.startswith("http"):
        host = f"https://{host}"
    return host.replace("app.tinybird.co", "cloud.tinybird.co")


def region_from_host(region_name_or_host, regions):
    """Returns the region that matches region_name_or_host"""

    return next((r for r in regions if _compare_region_host(region_name_or_host, r)), None)


def ask_for_user_token(action: str, ui_host: str) -> str:
    return click.prompt(
        f'\nUse the token called "user token" to {action}. Copy it from {ui_host}/tokens and paste it here',
        hide_input=True,
        show_default=False,
        default=None,
    )


def check_user_token(ctx: Context, token: str):
    client: TinyB = ctx.ensure_object(dict)["client"]
    try:
        user_client: TinyB = deepcopy(client)
        user_client.token = token

        is_authenticated = user_client.check_auth_login()
    except Exception as e:
        raise CLIWorkspaceException(FeedbackManager.error_exception(error=str(e)))

    if not is_authenticated.get("is_valid", False):
        raise CLIWorkspaceException(
            FeedbackManager.error_exception(
                error='Invalid token. Make sure you are using the "user token" instead of the "admin your@email" token.'
            )
        )
    if is_authenticated.get("is_valid") and not is_authenticated.get("is_user", False):
        raise CLIWorkspaceException(
            FeedbackManager.error_exception(
                error='Invalid user authentication. Make sure you are using the "user token" instead of the "admin your@email" token.'
            )
        )


def check_user_token_with_client(client: TinyB, token: str):
    try:
        user_client: TinyB = deepcopy(client)
        user_client.token = token

        is_authenticated = user_client.check_auth_login()
    except Exception as e:
        raise CLIWorkspaceException(FeedbackManager.error_exception(error=str(e)))

    if not is_authenticated.get("is_valid", False):
        raise CLIWorkspaceException(
            FeedbackManager.error_exception(
                error='Invalid token. Make sure you are using the "user token" instead of the "admin your@email" token.'
            )
        )
    if is_authenticated.get("is_valid") and not is_authenticated.get("is_user", False):
        raise CLIWorkspaceException(
            FeedbackManager.error_exception(
                error='Invalid user authentication. Make sure you are using the "user token" instead of the "admin your@email" token.'
            )
        )


def fork_workspace(client: TinyB, user_client: TinyB, created_workspace):
    config = CLIConfig.get_project_config()

    datasources = client.datasources()
    for datasource in datasources:
        user_client.datasource_share(datasource["id"], config["id"], created_workspace["id"])


def create_workspace_non_interactive(
    ctx: Context,
    workspace_name: str,
    user_token: str,
    fork: bool,
    organization_id: Optional[str],
    organization_name: Optional[str],
):
    """Creates a workspace using the provided name"""
    client: TinyB = ctx.ensure_object(dict)["client"]

    try:
        user_client: TinyB = deepcopy(client)
        user_client.token = user_token

        created_workspace = user_client.create_workspace(workspace_name, organization_id, version="v1")
        if organization_id and organization_name:
            click.echo(
                FeedbackManager.success_workspace_created_with_organization(
                    workspace_name=workspace_name, organization_name=organization_name, organization_id=organization_id
                )
            )
        else:
            click.echo(FeedbackManager.success_workspace_created(workspace_name=workspace_name))

        if fork:
            fork_workspace(client, user_client, created_workspace)

    except Exception as e:
        raise CLIWorkspaceException(FeedbackManager.error_exception(error=str(e)))


def create_workspace_interactive(
    ctx: Context,
    workspace_name: Optional[str],
    user_token: str,
    fork: bool,
    organization_id: Optional[str],
    organization_name: Optional[str],
):
    if not workspace_name:
        """Creates a workspace guiding the user"""
        click.echo("\n")
        click.echo(FeedbackManager.info_workspace_create_greeting())
        default_name = f"new_workspace_{uuid.uuid4().hex[0:4]}"
        workspace_name = click.prompt("\nWorkspace name", default=default_name, err=True, type=str)

    if not workspace_name:
        raise CLIException(FeedbackManager.error_workspace_name_required())

    create_workspace_non_interactive(
        ctx,
        workspace_name,
        user_token,
        fork,
        organization_id,
        organization_name,
    )


def print_data_branch_summary(client, job_id, response=None):
    response = client.job(job_id) if job_id else response or {"partitions": []}
    columns = ["Data Source", "Partition", "Status", "Error"]
    table = []
    for partition in response["partitions"]:
        for p in partition["partitions"]:
            table.append([partition["datasource"]["name"], p["partition"], p["status"], p.get("error", "")])
    echo_safe_humanfriendly_tables_format_smart_table(table, column_names=columns)


def print_branch_regression_tests_summary(client, job_id, host, response=None):
    def format_metric(metric: Union[str, float], is_percentage: bool = False) -> str:
        if isinstance(metric, float):
            if is_percentage:
                return f"{round(metric, 3):+} %"
            else:
                return f"{round(metric, 3)} seconds"
        else:
            return metric

    failed = False
    response = client.job(job_id) if job_id else response or {"progress": []}
    output = "\n"
    for step in response["progress"]:
        run = step["run"]
        if run["output"]:
            # If the output contains an alert emoji, it means that it should be ou
            output += (
                warning_message(run["output"])()
                if isinstance(run["output"], str) and "🚨" in run["output"]
                else "".join(run["output"])
            )
        if not run["was_successfull"]:
            failed = True
    click.echo(output)

    if failed:
        click.echo("")
        click.echo("")
        click.echo("==== Failures Detail ====")
        click.echo("")
        for step in response["progress"]:
            if not step["run"]["was_successfull"]:
                for failure in step["run"]["failed"]:
                    try:
                        click.echo(f"❌ {failure['name']}")
                        click.echo(FeedbackManager.error_branch_check_pipe(error=failure["error"]))
                        click.echo("")
                    except Exception:
                        pass

    click.echo("")
    click.echo("")
    click.echo("==== Performance metrics ====")
    click.echo("")
    for step in response["progress"]:
        run = step["run"]
        if run.get("metrics_summary") and run.get("metrics_timing"):
            column_names = [f"{run['pipe_name']}({run['test_type']})", "Origin", "Branch", "Delta"]

            click.echo(
                format_pretty_table(
                    [
                        [
                            metric,
                            format_metric(run["metrics_timing"][metric][0]),
                            format_metric(run["metrics_timing"][metric][1]),
                            format_metric(run["metrics_timing"][metric][2], is_percentage=True),
                        ]
                        for metric in [
                            "min response time",
                            "max response time",
                            "mean response time",
                            "median response time",
                            "p90 response time",
                            "min read bytes",
                            "max read bytes",
                            "mean read bytes",
                            "median read bytes",
                            "p90 read bytes",
                        ]
                    ],
                    column_names=column_names,
                )
            )

    click.echo("")
    click.echo("")
    click.echo("==== Results Summary ====")
    click.echo("")
    click.echo(
        format_pretty_table(
            [
                [
                    step["run"]["pipe_name"],
                    step["run"]["test_type"],
                    step["run"]["metrics_summary"].get("run", 0),
                    step["run"]["metrics_summary"].get("passed", 0),
                    step["run"]["metrics_summary"].get("failed", 0),
                    format_metric(
                        (
                            step["run"]["metrics_timing"]["mean response time"][2]
                            if "mean response time" in step["run"]["metrics_timing"]
                            else 0.0
                        ),
                        is_percentage=True,
                    ),
                    format_metric(
                        (
                            step["run"]["metrics_timing"]["mean read bytes"][2]
                            if "mean read bytes" in step["run"]["metrics_timing"]
                            else 0.0
                        ),
                        is_percentage=True,
                    ),
                ]
                for step in response["progress"]
            ],
            column_names=["Endpoint", "Test", "Run", "Passed", "Failed", "Mean response time", "Mean read bytes"],
        )
    )
    click.echo("")
    if failed:
        for step in response["progress"]:
            if not step["run"]["was_successfull"]:
                for failure in step["run"]["failed"]:
                    click.echo(f"❌ FAILED {failure['name']}\n")
    if failed:
        raise CLIException(
            "Check Failures Detail above for more information. If the results are expected, skip asserts or increase thresholds, see 💡 Hints above (note skip asserts flags are applied to all regression tests, so use them when it makes sense).\n\nIf you are using the CI template for GitHub or GitLab you can add skip asserts flags as labels to the MR and they are automatically applied. Find available flags to skip asserts and thresholds here => https://www.tinybird.co/docs/production/implementing-test-strategies.html#fixture-tests"
        )


class PlanName(Enum):
    DEV = "Build"
    PRO = "Pro"
    ENTERPRISE = "Enterprise"


def _get_workspace_plan_name(plan):
    """
    >>> _get_workspace_plan_name("dev")
    'Build'
    >>> _get_workspace_plan_name("pro")
    'Pro'
    >>> _get_workspace_plan_name("enterprise")
    'Enterprise'
    >>> _get_workspace_plan_name("branch_enterprise")
    'Enterprise'
    >>> _get_workspace_plan_name("other_plan")
    'Custom'
    """
    if plan == "dev":
        return PlanName.DEV.value
    if plan == "pro":
        return PlanName.PRO.value
    if plan in ("enterprise", "branch_enterprise"):
        return PlanName.ENTERPRISE.value
    return "Custom"


def get_format_from_filename_or_url(filename_or_url: str) -> str:
    """
    >>> get_format_from_filename_or_url('wadus_parquet.csv')
    'csv'
    >>> get_format_from_filename_or_url('wadus_csv.parquet')
    'parquet'
    >>> get_format_from_filename_or_url('wadus_csv.ndjson')
    'ndjson'
    >>> get_format_from_filename_or_url('wadus_csv.json')
    'ndjson'
    >>> get_format_from_filename_or_url('wadus_parquet.csv?auth=pepe')
    'csv'
    >>> get_format_from_filename_or_url('wadus_csv.parquet?auth=pepe')
    'parquet'
    >>> get_format_from_filename_or_url('wadus_parquet.ndjson?auth=pepe')
    'ndjson'
    >>> get_format_from_filename_or_url('wadus.json?auth=pepe')
    'ndjson'
    >>> get_format_from_filename_or_url('wadus_csv_')
    'csv'
    >>> get_format_from_filename_or_url('wadus_json_csv_')
    'csv'
    >>> get_format_from_filename_or_url('wadus_json_')
    'ndjson'
    >>> get_format_from_filename_or_url('wadus_ndjson_')
    'ndjson'
    >>> get_format_from_filename_or_url('wadus_parquet_')
    'parquet'
    >>> get_format_from_filename_or_url('wadus')
    'csv'
    >>> get_format_from_filename_or_url('https://storage.googleapis.com/tinybird-waduscom/stores_stock__v2_1646741850424_final.csv?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=44444444444-compute@developer.gserviceaccount.com/1234/auto/storage/goog4_request&X-Goog-Date=20220308T121750Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=8888888888888888888888888888888888888888888888888888888')
    'csv'
    """
    filename_or_url = filename_or_url.lower()
    if filename_or_url.endswith(("json", "ndjson")):
        return "ndjson"
    if filename_or_url.endswith("parquet"):
        return "parquet"
    if filename_or_url.endswith("csv"):
        return "csv"
    try:
        parsed = urlparse(filename_or_url)
        if parsed.path.endswith(("json", "ndjson")):
            return "ndjson"
        if parsed.path.endswith("parquet"):
            return "parquet"
        if parsed.path.endswith("csv"):
            return "csv"
    except Exception:
        pass
    if "csv" in filename_or_url:
        return "csv"
    if "json" in filename_or_url:
        return "ndjson"
    if "parquet" in filename_or_url:
        return "parquet"
    return "csv"


def push_data(
    client: TinyB,
    datasource_name: str,
    url,
    mode: str = "append",
    sql_condition: Optional[str] = None,
    replace_options=None,
    concurrency: int = 1,
    silent: bool = False,
):
    if url and type(url) is tuple:
        url = url[0]

    def cb(res):
        if cb.First:  # type: ignore[attr-defined]
            blocks_to_process = len([x for x in res["block_log"] if x["status"] == "idle"])
            if blocks_to_process:
                cb.bar = click.progressbar(label=FeedbackManager.info_progress_blocks(), length=blocks_to_process)  # type: ignore[attr-defined]
                cb.bar.update(0)  # type: ignore[attr-defined]
                cb.First = False  # type: ignore[attr-defined]
                cb.blocks_to_process = blocks_to_process  # type: ignore[attr-defined]
        else:
            done = len([x for x in res["block_log"] if x["status"] == "done"])
            if done * 2 > cb.blocks_to_process:  # type: ignore[attr-defined]
                cb.bar.label = FeedbackManager.info_progress_current_blocks()  # type: ignore[attr-defined]
            cb.bar.update(done - cb.prev_done)  # type: ignore[attr-defined]
            cb.prev_done = done  # type: ignore[attr-defined]

    cb.First = True  # type: ignore[attr-defined]
    cb.prev_done = 0  # type: ignore[attr-defined]

    if not silent:
        if mode == "replace":
            click.echo(FeedbackManager.highlight(message=f"\n» Replacing data in {datasource_name}..."))
        else:
            click.echo(FeedbackManager.highlight(message=f"\n» Appending data to {datasource_name}..."))

    if isinstance(url, list):
        urls = url
    else:
        urls = [url]

    def process_url(
        datasource_name: str, url: str, mode: str, sql_condition: Optional[str], replace_options: Optional[Set[str]]
    ):
        parsed = urlparse(url)
        # poor man's format detection
        _format = get_format_from_filename_or_url(url)
        if parsed.scheme in ("http", "https"):
            res = client.datasource_create_from_url(
                datasource_name,
                url,
                mode=mode,
                status_callback=cb,
                sql_condition=sql_condition,
                format=_format,
                replace_options=replace_options,
            )
        else:
            res = client.datasource_append_data(
                datasource_name,
                file=url,
                mode=mode,
                sql_condition=sql_condition,
                format=_format,
                replace_options=replace_options,
            )

        datasource_name = res["datasource"]["name"]
        try:
            datasource = client.get_datasource(datasource_name)
        except DoesNotExistException:
            raise CLIException(FeedbackManager.error_datasource_does_not_exist(datasource=datasource_name))
        except Exception as e:
            raise CLIException(FeedbackManager.error_exception(error=str(e)))

        total_rows = (datasource.get("statistics", {}) or {}).get("row_count", 0)
        appended_rows = 0
        parser = None

        if res.get("error"):
            raise CLIException(FeedbackManager.error_exception(error=res["error"]))
        if res.get("errors"):
            raise CLIException(FeedbackManager.error_exception(error=res["errors"]))
        if res.get("blocks"):
            for block in res["blocks"]:
                if "process_return" in block and block["process_return"] is not None:
                    process_return = block["process_return"][0]
                    parser = process_return["parser"] if process_return.get("parser") else parser
                    if parser and parser != "clickhouse":
                        parser = process_return["parser"]
                        appended_rows += process_return["lines"]

        return parser, total_rows, appended_rows

    try:
        tasks = [process_url(datasource_name, url, mode, sql_condition, replace_options) for url in urls]
        output = gather_with_concurrency(concurrency, *tasks)
        parser, total_rows, appended_rows = list(output)[-1]
    except AuthNoTokenException:
        raise
    except OperationCanNotBePerformed as e:
        raise CLIException(FeedbackManager.error_operation_can_not_be_performed(error=e))
    except Exception as e:
        raise CLIException(FeedbackManager.error_exception(error=e))
    else:
        if not silent:
            if mode == "append" and parser and parser != "clickhouse":
                click.echo(FeedbackManager.success_appended_rows(appended_rows=appended_rows))

            if mode == "replace":
                click.echo(FeedbackManager.success_replaced_datasource(datasource=datasource_name))

            click.echo(FeedbackManager.success_progress_blocks())


def sync_data(ctx, datasource_name: str, yes: bool):
    client: TinyB = ctx.obj["client"]
    datasource = client.get_datasource(datasource_name)

    VALID_DATASOURCES = ["s3", "gcs"]
    if datasource["type"] not in VALID_DATASOURCES:
        raise CLIException(FeedbackManager.error_sync_not_supported(valid_datasources=VALID_DATASOURCES))

    warning_message = (
        FeedbackManager.warning_datasource_sync_bucket(datasource=datasource_name)
        if datasource["type"] in ["s3", "gcs"]
        else FeedbackManager.warning_datasource_sync(
            datasource=datasource_name,
        )
    )
    if yes or click.confirm(warning_message):
        client.datasource_sync(datasource["id"])
        click.echo(FeedbackManager.success_sync_datasource(datasource=datasource_name))


# eval "$(_TB_COMPLETE=source_bash tb)"
def autocomplete_topics(ctx: Context, args, incomplete):
    try:
        config = get_config(None, None)
        ctx.ensure_object(dict)["config"] = config
        client = create_tb_client(ctx)
        topics = client.kafka_list_topics(args[2])
        return [t for t in topics if incomplete in t]
    except Exception:
        return []


def validate_datasource_name(name):
    if not isinstance(name, str) or name == "":
        raise CLIException(FeedbackManager.error_datasource_name())


def validate_connection_id(connection_id):
    if not isinstance(connection_id, str) or connection_id == "":
        raise CLIException(FeedbackManager.error_datasource_connection_id())


def validate_kafka_topic(topic):
    if not isinstance(topic, str):
        raise CLIException(FeedbackManager.error_kafka_topic())


def validate_kafka_group(group):
    if not isinstance(group, str):
        raise CLIException(FeedbackManager.error_kafka_group())


def validate_kafka_auto_offset_reset(auto_offset_reset):
    valid_values = {"latest", "earliest", "none"}
    if auto_offset_reset not in valid_values:
        raise CLIException(FeedbackManager.error_kafka_auto_offset_reset())


def validate_kafka_schema_registry_url(schema_registry_url):
    if not is_url_valid(schema_registry_url):
        raise CLIException(FeedbackManager.error_kafka_registry())


def is_url_valid(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def validate_kafka_bootstrap_servers(host_and_port):
    if not isinstance(host_and_port, str):
        raise CLIException(FeedbackManager.error_kafka_bootstrap_server())
    parts = host_and_port.split(":")
    if len(parts) > 2:
        raise CLIException(FeedbackManager.error_kafka_bootstrap_server())
    host = parts[0]
    port_str = parts[1] if len(parts) == 2 else "9092"
    try:
        port = int(port_str)
    except Exception:
        raise CLIException(FeedbackManager.error_kafka_bootstrap_server())
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        try:
            sock.settimeout(3)
            sock.connect((host, port))
        except TimeoutError:
            raise CLIException(FeedbackManager.error_kafka_bootstrap_server_conn_timeout(host=host, port=port))
        except Exception:
            raise CLIException(FeedbackManager.error_kafka_bootstrap_server_conn(host=host, port=port))


def validate_kafka_key(s):
    if not isinstance(s, str):
        raise CLIException("Key format is not correct, it must be a string")


def validate_kafka_secret(s):
    if not isinstance(s, str):
        raise CLIException("Password format is not correct, it must be a string")


def validate_string_connector_param(param, s):
    if not isinstance(s, str):
        raise CLIConnectionException(param + " format is not correct, it must be a string")


def validate_connection_name(client, connection_name, service):
    if client.get_connector(connection_name, service) is not None:
        raise CLIConnectionException(FeedbackManager.error_connection_already_exists(name=connection_name))


def _get_setting_value(connection, setting, sensitive_settings):
    if setting in sensitive_settings:
        return "*****"
    return connection.get(setting, "")


def get_current_workspace_branches(config: CLIConfig) -> List[Dict[str, Any]]:
    current_main_workspace: Optional[Dict[str, Any]] = get_current_main_workspace(config)
    if not current_main_workspace:
        raise CLIException(FeedbackManager.error_unable_to_identify_main_workspace())

    client = config.get_client()
    user_branches: List[Dict[str, Any]] = (client.user_workspace_branches("v1")).get("workspaces", [])
    all_branches: List[Dict[str, Any]] = (client.branches()).get("environments", [])
    branches = user_branches + [branch for branch in all_branches if branch not in user_branches]

    return [branch for branch in branches if branch.get("main") == current_main_workspace["id"]]


def switch_workspace(config: CLIConfig, workspace_name_or_id: str, only_environments: bool = False) -> None:
    try:
        if only_environments:
            workspaces = get_current_workspace_branches(config)
        else:
            response = config.get_client().user_workspaces(version="v1")
            workspaces = response["workspaces"]

        workspace = next(
            (
                workspace
                for workspace in workspaces
                if workspace["name"] == workspace_name_or_id or workspace["id"] == workspace_name_or_id
            ),
            None,
        )

        if not workspace:
            raise CLIException(FeedbackManager.error_workspace(workspace=workspace_name_or_id))

        config.set_token(workspace["token"])
        config.set_token_for_host(workspace["token"], config.get_host())
        _ = try_update_config_with_remote(config)

        # Set the id and name afterwards.
        # When working with branches the call to try_update_config_with_remote above
        # sets the data with the main branch ones
        config["id"] = workspace["id"]
        config["name"] = workspace["name"]

        config.persist_to_file()

        click.echo(FeedbackManager.success_now_using_config(name=config["name"], id=config["id"]))
    except AuthNoTokenException:
        raise
    except CLIException:
        raise
    except Exception as e:
        raise CLIException(FeedbackManager.error_exception(error=str(e)))


def switch_to_workspace_by_user_workspace_data(config: CLIConfig, user_workspace_data: Dict[str, Any]):
    try:
        config["id"] = user_workspace_data["id"]
        config["name"] = user_workspace_data["name"]
        config.set_token(user_workspace_data["token"])
        config.set_token_for_host(user_workspace_data["token"], config.get_host())
        config.persist_to_file()

        click.echo(FeedbackManager.success_now_using_config(name=config["name"], id=config["id"]))
    except Exception as e:
        raise CLIException(FeedbackManager.error_exception(error=str(e)))


def print_current_workspace(config: CLIConfig) -> None:
    _ = try_update_config_with_remote(config, only_if_needed=True)

    current_main_workspace = get_current_main_workspace(config)
    assert isinstance(current_main_workspace, dict)

    columns = ["name", "id", "role", "plan", "current"]

    table = [
        (
            current_main_workspace["name"],
            current_main_workspace["id"],
            current_main_workspace["role"],
            _get_workspace_plan_name(current_main_workspace["plan"]),
            True,
        )
    ]

    click.echo(FeedbackManager.info_current_workspace())
    echo_safe_humanfriendly_tables_format_smart_table(table, column_names=columns)


class ConnectionReplacements:
    _PARAMS_REPLACEMENTS: Dict[str, Dict[str, str]] = {
        "s3": {
            "service": "service",
            "connection_name": "name",
            "key": "s3_access_key_id",
            "secret": "s3_secret_access_key",
            "region": "s3_region",
        },
        "s3_iamrole": {
            "service": "service",
            "connection_name": "name",
            "role_arn": "s3_iamrole_arn",
            "region": "s3_iamrole_region",
        },
        "gcs_hmac": {
            "service": "service",
            "connection_name": "name",
            "key": "gcs_hmac_access_id",
            "secret": "gcs_hmac_secret",
            "region": "gcs_region",
        },
        "gcs": {
            "project_id": "gcs_project_id",
            "client_id": "gcs_client_id",
            "client_email": "gcs_client_email",
            "client_x509_cert_url": "gcs_client_x509_cert_url",
            "private_key": "gcs_private_key",
            "private_key_id": "gcs_private_key_id",
            "connection_name": "name",
        },
        "dynamodb": {
            "service": "service",
            "connection_name": "name",
            "role_arn": "dynamodb_iamrole_arn",
            "region": "dynamodb_iamrole_region",
        },
    }

    @staticmethod
    def map_api_params_from_prompt_params(service: str, **params: Any) -> Dict[str, Any]:
        """Maps prompt parameters to API parameters."""

        api_params = {}
        for key in params.keys():
            try:
                api_params[ConnectionReplacements._PARAMS_REPLACEMENTS[service][key]] = params[key]
            except KeyError:
                api_params[key] = params[key]

        api_params["service"] = service
        return api_params


# ======
# Temporal new functions while we fully merge the new CLIConfig
# ======


def get_host_from_region(
    config: CLIConfig, region_name_or_host_or_id: str, host: Optional[str] = None
) -> Tuple[List[Region], str]:
    regions: List[Region]
    region: Optional[Region]

    host = host or config.get_host(use_defaults_if_needed=True)

    try:
        regions = get_regions(config)
        assert isinstance(regions, list)
    except Exception:
        regions = []

    if not regions:
        assert isinstance(host, str)
        click.echo(f"No regions available, using host: {host}")
        return [], host

    try:
        index = int(region_name_or_host_or_id)
        try:
            host = regions[index - 1]["api_host"]
        except Exception:
            raise CLIException(FeedbackManager.error_getting_region_by_index())
    except ValueError:
        region_name = region_name_or_host_or_id.lower()
        try:
            region = get_region_from_host(region_name, regions)
            host = region["api_host"] if region else None
        except Exception:
            raise CLIException(FeedbackManager.error_getting_region_by_name_or_url())

    if not host:
        raise CLIException(FeedbackManager.error_getting_region_by_name_or_url())

    return regions, host


def get_regions(config: CLIConfig) -> List[Region]:
    regions: List[Region] = []
    try:
        response = config.get_client().regions()
        regions = response.get("regions", [])
        first_default_region = next((region for region in regions if region["api_host"] == DEFAULT_API_HOST), None)
        if first_default_region:
            regions.remove(first_default_region)
            regions.insert(0, first_default_region)
    except Exception:
        pass

    return regions


def get_region_from_host(region_name_or_host: str, regions: List[Region]) -> Optional[Region]:
    """Returns the region that matches region_name_or_host by name, API host or ui host"""
    for region in regions:
        if region_name_or_host in (region["name"].lower(), region["host"], region["api_host"]):
            return region
    return None


def try_update_config_with_remote(
    config: CLIConfig, raise_on_errors: bool = True, only_if_needed: bool = False, auto_persist: bool = True
) -> bool:
    response: Dict[str, Any]

    if not config.get_token():
        if not raise_on_errors:
            return False
        raise AuthNoTokenException()

    if "id" in config and only_if_needed:
        return True

    try:
        response = config.get_client().workspace_info(version="v1")
    except AuthException:
        if raise_on_errors:
            raise CLIAuthException(FeedbackManager.error_invalid_token_for_host(host=config.get_host()))
        return False
    except Exception as ex:
        if raise_on_errors:
            ex_message = str(ex)
            if "cannot parse" in ex_message.lower():
                raise CLIAuthException(FeedbackManager.error_invalid_host(host=config.get_host()))

            raise CLIAuthException(FeedbackManager.error_exception(error=ex_message))
        return False

    for k in ("id", "name", "user_email", "user_id", "scope"):
        if k in response:
            config[k] = response[k]

    config.set_token_for_host(config.get_token(), config.get_host())

    if auto_persist:
        config.persist_to_file()

    return True


def ask_for_admin_token_interactively(ui_host: str, default_token: Optional[str]) -> str:
    return (
        click.prompt(
            f'\nCopy the "admin your@email" token from {ui_host}/tokens and paste it here {"OR press enter to use the token from the .tinyb file" if default_token else ""}',
            hide_input=True,
            show_default=False,
            default=default_token,
            type=str,
        )
        or ""
    )


def try_authenticate(
    config: CLIConfig,
    regions: Optional[List[Region]] = None,
    interactive: bool = False,
    try_all_regions: bool = False,
) -> bool:
    host: Optional[str] = config.get_host()

    if not regions and interactive:
        regions = get_regions(config)

    selected_region: Optional[Region] = None
    default_password: Optional[str] = None

    if regions:
        if interactive:
            selected_region = ask_for_region_interactively(regions)
            if selected_region is None:
                return False

            host = selected_region.get("api_host")
            default_password = selected_region.get("default_password")
        else:
            assert isinstance(host, str)
            selected_region = get_region_from_host(host, regions)

    name: str
    api_host: str
    ui_host: str
    token: Optional[str]
    if host and not selected_region:
        name, api_host, ui_host = (host, format_host(host, subdomain="api"), format_host(host, subdomain="cloud"))
        token = config.get_token()
    else:
        name, api_host, ui_host = get_region_info(config, selected_region)
        token = config.get_token_for_host(api_host)
    config.set_host(api_host)

    if not token:
        token = ask_for_admin_token_interactively(get_display_cloud_host(ui_host), default_token=default_password)
    config.set_token(token)

    add_telemetry_event("auth_token", token=token)
    authenticated: bool = try_update_config_with_remote(config, raise_on_errors=not try_all_regions)

    # No luck? Let's try auth in all other regions
    if not authenticated and try_all_regions and not interactive:
        if not regions:
            regions = get_regions(config)

        # Check other regions, ignoring the previously tested region
        for region in [r for r in regions if r is not selected_region]:
            name, host, ui_host = get_region_info(config, region)
            config.set_host(host)
            authenticated = try_update_config_with_remote(config, raise_on_errors=False)
            if authenticated:
                click.echo(FeedbackManager.success_using_host(name=name, host=get_display_cloud_host(ui_host)))
                break

    if not authenticated:
        raise CLIAuthException(FeedbackManager.error_invalid_token())

    config.persist_to_file()

    click.echo(FeedbackManager.success_auth())
    click.echo(FeedbackManager.success_remember_api_host(api_host=host))

    if not config.get("scope"):
        click.echo(FeedbackManager.warning_token_scope())

    add_telemetry_event("auth_success")

    return True


def wait_job(
    tb_client: TinyB,
    job_id: str,
    job_url: str,
    label: str,
    wait_observer: Optional[Callable[[Dict[str, Any], ProgressBar], None]] = None,
) -> Dict[str, Any]:
    progress_bar: ProgressBar
    with click.progressbar(
        label=f"{label} ",
        length=100,
        show_eta=False,
        show_percent=wait_observer is None,
        fill_char=click.style("█", fg="green"),
    ) as progress_bar:

        def progressbar_cb(res: Dict[str, Any]):
            if wait_observer:
                wait_observer(res, progress_bar)
                return

            if "progress_percentage" in res:
                progress_bar.update(int(round(res["progress_percentage"])) - progress_bar.pos)
            elif res["status"] != "working":
                progress_bar.update(progress_bar.length if progress_bar.length else 0)

        try:
            result = wait_job_no_ui(tb_client, job_id, progressbar_cb)
            if result["status"] != "done":
                raise CLIException(FeedbackManager.error_while_running_job(error=result["error"]))
            return result
        except TimeoutError:
            raise CLIException(FeedbackManager.error_while_running_job(error="Reach timeout, job cancelled"))
        except JobException as e:
            raise CLIException(FeedbackManager.error_while_running_job(error=str(e)))
        except Exception as e:
            raise CLIException(FeedbackManager.error_getting_job_info(error=str(e), url=job_url))


def wait_job_no_ui(
    tb_client: TinyB,
    job_id: str,
    status_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
) -> Dict[str, Any]:
    try:
        result = tb_client.wait_for_job(job_id, status_callback=status_callback)
        if result["status"] != "done":
            raise JobException(result.get("error"))
        return result
    except TimeoutError:
        tb_client.job_cancel(job_id)
        raise


def get_current_main_workspace(config: CLIConfig) -> Optional[Dict[str, Any]]:
    current_workspace = config.get_client().user_workspaces_and_branches(version="v1")
    return _get_current_main_workspace_common(current_workspace, config.get("id", current_workspace["id"]))


def _get_current_main_workspace_common(
    user_workspace_and_branches: Dict[str, Any], current_workspace_id: str
) -> Optional[Dict[str, Any]]:
    def get_workspace_by_id(workspaces: List[Dict[str, Any]], id: str) -> Optional[Dict[str, Any]]:
        return next((ws for ws in workspaces if ws["id"] == id), None)

    workspaces: Optional[List[Dict[str, Any]]] = user_workspace_and_branches.get("workspaces")
    if not workspaces:
        return None

    current: Optional[Dict[str, Any]] = get_workspace_by_id(workspaces, current_workspace_id)
    if current and current.get("is_branch"):
        current = get_workspace_by_id(workspaces, current["main"])

    return current


def run_aws_iamrole_connection_flow(
    config: dict[str, Any],
    client: TinyB,
    service: str,
    connection_name: str,
    policy: str,
    local_unavailable: bool = False,
) -> Tuple[str, str, Optional[TinyB], Optional[TinyB]]:
    """
    Run the interactive AWS IAM Role connection flow for S3.

    Guides the user through creating an IAM policy and role with the appropriate
    trust policy that includes AWS account IDs from the selected environments.

    Args:
        config: The CLI configuration dictionary.
        client: The TinyB client instance.
        service: The data connector service type (e.g., 's3').
        connection_name: The name for the connection being created.
        policy: The access policy type ('read' or 'write').
        local_unavailable: If True, local environment is unavailable (e.g., missing AWS credentials).

    Returns:
        A tuple containing:
            - role_arn (str): The AWS IAM Role ARN entered by the user.
            - region (str): The AWS region where the bucket is located.
            - cloud_client (Optional[TinyB]): The TinyB client instance for the cloud environment.
            - local_client (Optional[TinyB]): The TinyB client instance for the local environment.
    """
    if service == DataConnectorType.AMAZON_DYNAMODB:
        raise NotImplementedError("DynamoDB is not supported")

    bucket_name = click.prompt(
        FeedbackManager.highlight(
            message="? Bucket name (specific name recommended, use '*' for unrestricted access in IAM policy)"
        ),
        prompt_suffix="\n> ",
    )
    validate_string_connector_param("Bucket", bucket_name)

    region = click.prompt(
        FeedbackManager.highlight(message="? Region (the region where the bucket is located)"),
        default="us-east-1",
        show_default=True,
        prompt_suffix="\n> ",
    )
    validate_string_connector_param("Region", region)

    # Determine which clients to use based on selection
    use_local = False
    use_cloud = False

    # If local is unavailable, skip to cloud only
    if local_unavailable:
        use_local = False
        use_cloud = True
        click.echo(FeedbackManager.info(message="Using Cloud environment only (local environment unavailable)."))
    else:
        # Ask which environments will use this connection
        click.echo(
            FeedbackManager.highlight(
                message="? Which environments will use this connection? (AWS account ID of selected environments will be included in the trust policy)"
            )
        )
        click.echo("  [1] Local only")
        click.echo("  [2] Cloud only")
        click.echo("  [3] Both")

        env_choice = click.prompt("\nSelect option", default=3, type=int)

        if env_choice == 1:
            use_local = True
            use_cloud = False
            click.echo(
                FeedbackManager.info(
                    message="The provided AWS account ID from your local environment will be used to generate the trust policy."
                )
            )
        elif env_choice == 2:
            use_local = False
            use_cloud = True
            click.echo(
                FeedbackManager.info(
                    message="The provided AWS account ID from your cloud environment will be used to generate the trust policy."
                )
            )
        elif env_choice == 3:
            use_local = True
            use_cloud = True
            click.echo(
                FeedbackManager.info(
                    message="The provided AWS account IDs from both local and cloud environments will be included in the trust policy."
                )
            )
        else:
            click.echo(FeedbackManager.warning(message="Invalid option. Defaulting to 'Both'."))
            use_local = True
            use_cloud = True

    local_client: Optional[TinyB] = None
    cloud_client: Optional[TinyB] = None

    if use_local:
        try:
            local_client = get_tinybird_local_client(config)
        except Exception as e:
            click.echo(FeedbackManager.warning(message=f"Failed to initialize local client: {e}"))
            click.echo(FeedbackManager.warning(message="Continuing without local environment."))

    if use_cloud:
        try:
            cloud_client = TinyB(
                token=config.get("token", ""),
                host=config.get("host", ""),
                staging=False,
            )
        except Exception as e:
            click.echo(FeedbackManager.warning(message=f"Failed to initialize cloud client: {e}"))
            click.echo(FeedbackManager.warning(message="Continuing without cloud environment."))

    # Use cloud_client as the main client if local is unavailable
    policy_client = cloud_client if local_unavailable and cloud_client else client

    access_policy, trust_policy, _ = get_aws_iamrole_policies(
        policy_client,
        service=service,
        policy=policy,
        bucket=bucket_name,
        external_id_seed=connection_name,
        cloud_client=cloud_client if not local_unavailable else None,
        local_client=local_client,
    )

    click.echo(FeedbackManager.gray(message="\n» Step 1: AWS Authentication"))
    click.echo(
        FeedbackManager.info(
            message="Please log into your AWS Console. We'll guide you through creating the necessary permissions: https://console.aws.amazon.com/"
        )
    )
    click.echo(
        FeedbackManager.info(
            message="You'll be creating a single IAM Policy and Role to access your S3 data. Using IAM Roles improves security by providing temporary credentials and following least privilege principles."
        )
    )
    click.echo(FeedbackManager.click_enter_to_continue())
    input()

    access_policy_copied = True
    try:
        pyperclip.copy(access_policy)
    except Exception:
        access_policy_copied = False

    click.echo(FeedbackManager.gray(message="» Step 2: Create IAM Policy"))
    click.echo(
        FeedbackManager.info(
            message=f"1. Go to AWS IAM > Create Policy: https://console.aws.amazon.com/iamv2/home?region={region}#/policies/create"
        )
    )
    click.echo(FeedbackManager.info(message="2. Select the JSON tab"))
    if access_policy_copied:
        click.echo(FeedbackManager.info(message="3. Paste the following policy (already copied to clipboard):"))
    else:
        click.echo(FeedbackManager.info(message="3. Copy and paste the following policy:"))
    click.echo(FeedbackManager.highlight(message=f"\n{access_policy}\n"))
    click.echo(
        FeedbackManager.info(message=f"4. Name the policy something meaningful (e.g., TinybirdS3Access-{bucket_name})")
    )
    click.echo(FeedbackManager.info(message="5. Click 'Create policy'"))
    click.echo(FeedbackManager.click_enter_to_continue())
    input()

    trust_policy_copied = True
    try:
        pyperclip.copy(trust_policy)
    except Exception:
        trust_policy_copied = False

    click.echo(FeedbackManager.gray(message="» Step 3: Create IAM Role"))
    click.echo(
        FeedbackManager.info(
            message=f"1. Go to AWS IAM > Create Role: https://console.aws.amazon.com/iamv2/home?region={region}#/roles/create"
        )
    )
    click.echo(FeedbackManager.info(message='2. Choose "Custom trust policy"'))
    if trust_policy_copied:
        click.echo(FeedbackManager.info(message="3. Paste the following trust policy (already copied to clipboard):"))
    else:
        click.echo(FeedbackManager.info(message="3. Paste the following trust policy:"))
    click.echo(FeedbackManager.highlight(message=f"\n{trust_policy}\n"))
    click.echo(FeedbackManager.info(message="4. Click Next, search for and select the policy you just created"))
    click.echo(
        FeedbackManager.info(message=f"5. Name the role something meaningful (e.g., TinybirdS3Role-{bucket_name})")
    )
    click.echo(FeedbackManager.info(message="6. Click 'Create role'"))
    click.echo(FeedbackManager.info(message="7. Copy the Role ARN from the role details page"))

    role_arn = click.prompt(
        FeedbackManager.highlight(message="? Please enter the ARN of the role you just created"),
        show_default=False,
    )
    validate_string_connector_param("Role ARN", role_arn)

    return role_arn, region, cloud_client, local_client


def run_gcp_svc_account_connection_flow(
    environment: str,
) -> None:
    click.echo(FeedbackManager.prompt_gcs_svc_account_login_gcp())
    click.echo(FeedbackManager.click_enter_to_continue())
    input()

    click.echo(FeedbackManager.prompt_gcs_service_account_creation_flow(environment=environment))
    click.echo(FeedbackManager.click_enter_to_continue())
    input()

    click.echo(FeedbackManager.prompt_gcs_service_account_key_creation())
    click.echo(FeedbackManager.click_enter_to_continue())
    input()


def production_aws_iamrole_only(
    prod_client: TinyB,
    service: str,
    region: str,
    bucket_name: str,
    environment: str,
    connection_name: str,
    policy: str,
) -> Tuple[str, str, str]:
    _, trust_policy, external_id = get_aws_iamrole_policies(
        prod_client, service=service, policy=policy, bucket=bucket_name, external_id_seed=connection_name
    )

    trust_policy_copied = True
    try:
        pyperclip.copy(trust_policy)
    except Exception:
        trust_policy_copied = False

    role_arn = click.prompt(
        (
            FeedbackManager.prompt_s3_iamrole_connection_role(
                trust_policy=trust_policy,
                aws_region=region,
                bucket=bucket_name,
                environment=environment.upper(),
                step="4",
            )
            if trust_policy_copied
            else FeedbackManager.prompt_s3_iamrole_connection_role_not_copied(
                trust_policy=trust_policy,
                aws_region=region,
                bucket=bucket_name,
                environment=environment.upper(),
                step="4",
            )
        ),
        show_default=False,
    )
    validate_string_connector_param("Role ARN", role_arn)

    return role_arn, region, external_id


def _merge_trust_policies(trust_policy_local: Dict[str, Any], trust_policy_cloud: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge two trust policies into a single policy with both account IDs.
    Both policies must have the same external ID.

    Args:
        trust_policy_local: Trust policy from local environment
        trust_policy_cloud: Trust policy from cloud environment

    Returns:
        Merged trust policy with both account IDs in the Principal
    """
    # Extract account IDs from both policies
    local_principal = trust_policy_local["Statement"][0]["Principal"]["AWS"]
    cloud_principal = trust_policy_cloud["Statement"][0]["Principal"]["AWS"]

    # Extract external IDs (should be the same)
    local_external_id = trust_policy_local["Statement"][0]["Condition"]["StringEquals"]["sts:ExternalId"]
    cloud_external_id = trust_policy_cloud["Statement"][0]["Condition"]["StringEquals"]["sts:ExternalId"]

    if local_external_id != cloud_external_id:
        raise CLIConnectionException(
            FeedbackManager.error(
                message="External IDs from local and cloud environments do not match. This should not happen."
            )
        )

    # Collect unique account IDs
    account_ids: List[str] = []
    seen_account_ids: Set[str] = set()

    # Handle both string and list formats for Principal.AWS
    principals_to_process: List[str] = []
    if isinstance(local_principal, str):
        principals_to_process.append(local_principal)
    elif isinstance(local_principal, list):
        principals_to_process.extend(local_principal)

    if isinstance(cloud_principal, str):
        principals_to_process.append(cloud_principal)
    elif isinstance(cloud_principal, list):
        principals_to_process.extend(cloud_principal)

    # Extract account IDs from ARNs (format: arn:aws:iam::ACCOUNT_ID:root)
    for principal in principals_to_process:
        match = _PATTERN_AWS_ARN.search(principal)
        if match:
            account_id = match.group(1)
            if account_id not in seen_account_ids:
                account_ids.append(account_id)
                seen_account_ids.add(account_id)

    # Create merged policy
    merged_principals = [f"arn:aws:iam::{account_id}:root" for account_id in account_ids]

    merged_statement = {
        "Effect": "Allow",
        "Action": "sts:AssumeRole",
        "Principal": {"AWS": merged_principals},
        "Condition": {"StringEquals": {"sts:ExternalId": local_external_id}},
    }

    return {
        "Version": "2012-10-17",
        "Statement": [merged_statement],
    }


def get_aws_iamrole_policies(
    client: TinyB,
    service: str,
    policy: str = "write",
    bucket: Optional[str] = None,
    external_id_seed: Optional[str] = None,
    cloud_client: Optional[TinyB] = None,
    local_client: Optional[TinyB] = None,
) -> Tuple[str, str, str]:
    """
    Get AWS IAM role policies. If cloud_client is provided, merges trust policies from both environments.

    Args:
        client: TinyB client for the current environment (local or cloud)
        service: Service type (e.g., "s3")
        policy: Access policy type ("read" or "write")
        bucket: Optional bucket name
        external_id_seed: Optional seed for external ID generation
        cloud_client: Optional TinyB client for cloud environment (for merging trust policies)

    Returns:
        Tuple of (access_policy_json, trust_policy_json, external_id)
    """
    access_policy: Dict[str, Any] = {}
    if service == DataConnectorType.AMAZON_S3_IAMROLE:
        service = DataConnectorType.AMAZON_S3
    try:
        if policy == "write":
            access_policy = client.get_access_write_policy(service, bucket)
        elif policy == "read":
            access_policy = client.get_access_read_policy(service, bucket)
        else:
            raise Exception(f"Access policy {policy} not supported. Choose from 'read' or 'write'")
        if not len(access_policy) > 0:
            raise Exception(f"{service.upper()} Integration not supported in this region")
    except Exception as e:
        raise CLIConnectionException(FeedbackManager.error_connection_integration_not_available(error=str(e)))

    trust_policy: Dict[str, Any] = {}
    try:
        trust_policy = client.get_trust_policy(service, external_id_seed)
        if not len(trust_policy) > 0:
            raise Exception(f"{service.upper()} Integration not supported in this region")

        # If cloud_client is provided, merge trust policies from both environments
        if cloud_client is not None:
            try:
                cloud_trust_policy = cloud_client.get_trust_policy(service, external_id_seed)
                if len(cloud_trust_policy) > 0:
                    trust_policy = _merge_trust_policies(trust_policy, cloud_trust_policy)
            except Exception as e:
                # If cloud client fails, log warning but continue with local trust policy
                logging.warning(f"Failed to get cloud trust policy, using local only: {e}")
        elif local_client is not None:
            try:
                local_trust_policy = local_client.get_trust_policy(service, external_id_seed)
                if len(local_trust_policy) > 0:
                    trust_policy = _merge_trust_policies(trust_policy, local_trust_policy)
            except Exception as e:
                logging.warning(f"Failed to get local trust policy: {e}")

    except Exception as e:
        raise CLIConnectionException(FeedbackManager.error_connection_integration_not_available(error=str(e)))
    try:
        external_id = trust_policy["Statement"][0]["Condition"]["StringEquals"]["sts:ExternalId"]
    except Exception:
        external_id = ""
    return json.dumps(access_policy, indent=4), json.dumps(trust_policy, indent=4), external_id


def get_s3_connection_name(project_folder: str, connection_name: Optional[str] = None) -> str:
    return get_connection_name(project_folder=project_folder, connection_type="S3", connection_name=connection_name)


def get_gcs_connection_name(project_folder) -> str:
    return get_connection_name(project_folder=project_folder, connection_type="GCS")


def get_kafka_connection_name(project_folder: str, connection_name: Optional[str] = None) -> str:
    return get_connection_name(project_folder=project_folder, connection_type="KAFKA", connection_name=connection_name)


def get_connection_name(project_folder: str, connection_type: str, connection_name: Optional[str] = None) -> str:
    valid_pattern = r"^[a-zA-Z][a-zA-Z0-9_]*$"

    while not connection_name:
        short_id = str(uuid.uuid4())[:4]
        default_name = f"{connection_type.lower()}_{short_id}"
        connection_name = click.prompt(
            FeedbackManager.highlight(
                message=f"? Connection name (only alphanumeric characters and underscores) [{default_name}]"
            ),
            show_default=False,
            default=default_name,
        )
        assert isinstance(connection_name, str)

        # Validate against invalid characters
        if not re.match(valid_pattern, connection_name):
            if not connection_name[0].isalpha():
                click.echo("Error: Connection name must start with a letter.")
            else:
                click.echo("Error: Connection name can only contain letters, numbers, and underscores.")
            connection_name = None
            continue

        # Check for existing connection with the same name
        project_folder_path = Path(project_folder)
        connection_files = list(project_folder_path.glob("*.connection"))
        for conn_file in connection_files:
            if conn_file.stem == connection_name:
                click.echo(FeedbackManager.error_connection_file_already_exists(name=f"{connection_name}.connection"))
                connection_name = None
                break
    return connection_name


def get_gcs_svc_account_creds() -> str:
    creds = None

    while not creds:
        creds = click.edit(
            "🔗 IMPORTANT: THIS LINE MUST BE DELETED. Enter your GCP credentials (JSON):", extension=".json"
        )

    assert isinstance(creds, str)
    creds_without_new_lines = creds.replace("\n", "")

    return creds_without_new_lines


class DataConnectorType(str, Enum):
    KAFKA = "kafka"
    GCLOUD_SCHEDULER = "gcscheduler"
    GCLOUD_STORAGE = "gcs"
    GCLOUD_STORAGE_HMAC = "gcs_hmac"
    GCLOUD_STORAGE_SA = "gcs_service_account"
    AMAZON_S3 = "s3"
    AMAZON_S3_IAMROLE = "s3_iamrole"
    AMAZON_DYNAMODB = "dynamodb"

    def __str__(self) -> str:
        return self.value


def create_aws_iamrole_connection(client: TinyB, service: str, connection_name, role_arn, region) -> None:
    conn_file_name = f"{connection_name}.connection"
    conn_file_path = Path(getcwd(), conn_file_name)

    if os.path.isfile(conn_file_path):
        raise CLIConnectionException(FeedbackManager.error_connection_file_already_exists(name=conn_file_name))

    if service == DataConnectorType.AMAZON_S3_IAMROLE:
        click.echo(FeedbackManager.info_creating_s3_iamrole_connection(connection_name=connection_name))
    if service == DataConnectorType.AMAZON_DYNAMODB:
        click.echo(FeedbackManager.info_creating_dynamodb_connection(connection_name=connection_name))

    params = ConnectionReplacements.map_api_params_from_prompt_params(
        service, connection_name=connection_name, role_arn=role_arn, region=region
    )

    click.echo("** Creating connection...")
    try:
        _ = client.connection_create(params)
    except Exception as e:
        raise CLIConnectionException(
            FeedbackManager.error_connection_create(connection_name=connection_name, error=str(e))
        )

    with open(conn_file_path, "w") as f:
        f.write(
            f"""TYPE {service}

"""
        )
    click.echo(FeedbackManager.success_connection_file_created(name=conn_file_name))


def get_ca_pem_content(ca_pem: Optional[str], filename: Optional[str] = None) -> Optional[str]:
    if not ca_pem:
        return None

    def is_valid_content(text_content: str) -> bool:
        return text_content.startswith("-----BEGIN CERTIFICATE-----")

    ca_pem_content = ca_pem
    base_path = Path(getcwd(), filename).parent if filename else Path(getcwd())
    ca_pem_path = Path(base_path, ca_pem)
    path_exists = os.path.exists(ca_pem_path)

    if not path_exists:
        raise CLIConnectionException(FeedbackManager.error_connection_ca_pem_not_found(ca_pem=ca_pem))

    if ca_pem.endswith(".pem") and path_exists:
        with open(ca_pem_path, "r") as f:
            ca_pem_content = f.read()

    if not is_valid_content(ca_pem_content):
        raise CLIConnectionException(FeedbackManager.error_connection_invalid_ca_pem())

    return ca_pem_content


requests_get = requests.get
requests_delete = requests.delete


def format_data_to_ndjson(data: List[Dict[str, Any]]) -> str:
    return "\n".join([json.dumps(row) for row in data])


def send_batch_events(client: TinyB, datasource_name: str, data: List[Dict[str, Any]], batch_size: int = 10) -> None:
    rows = len(data)
    time_start = time.time()
    for i in range(0, rows, batch_size):
        batch = data[i : i + batch_size]
        ndjson_data = format_data_to_ndjson(batch)
        client.datasource_events(datasource_name, ndjson_data)
    time_end = time.time()
    elapsed_time = time_end - time_start
    cols = len(data[0].keys()) if len(data) > 0 else 0
    click.echo(FeedbackManager.highlight(message=f"» {rows} rows x {cols} cols in {elapsed_time:.1f}s"))


def get_organizations_by_user(config: CLIConfig, user_token: Optional[str] = None) -> List[Dict[str, str]]:
    """Fetches all organizations by user using the provided user token"""
    organizations = []

    try:
        user_client = config.get_client(token=user_token) if user_token else config.get_user_client()
        user_workspaces = user_client.user_workspaces_with_organization(version="v1")
        admin_org_id = user_workspaces.get("organization_id")
        seen_org_ids = set()

        for workspace in user_workspaces.get("workspaces"):
            org = workspace.get("organization")
            if org and org.get("id") not in seen_org_ids:
                org["is_admin"] = org.get("id") == admin_org_id
                organizations.append(org)
                seen_org_ids.add(org.get("id"))

        # Case: user is admin of an organization but not a member of any workspace in it
        if admin_org_id and admin_org_id not in seen_org_ids:
            org = user_client.organization(admin_org_id)
            org["id"] = admin_org_id
            org["is_admin"] = True
            organizations.append(org)

    except Exception as e:
        raise CLIWorkspaceException(FeedbackManager.error_while_fetching_orgs(error=str(e)))
    return organizations


OrgType = Literal["tinybird", "domain", "admin", "member"]


class Organization(TypedDict):
    id: str
    name: str
    role: str
    domains: Optional[List[str]]
    type: OrgType


def sort_organizations_by_user(organizations: List[Dict[str, Any]], user_email: Optional[str]) -> List[Organization]:
    """Sort organizations based on type: tinybird > domain > admin > member"""
    sorted_organizations: List[Organization] = []
    user_domain = user_email.split("@")[1] if user_email else None
    is_tinybird_user = user_domain == "tinybird.co"

    for org in organizations:
        domain = org.get("domain") or ""
        domains = domain.split(",") if domain else None
        role: OrgType = "admin" if org.get("is_admin") else "member"
        type = role
        if domains and user_domain and user_domain in domains:
            type = "domain"
        if org.get("name") == "Tinybird" and is_tinybird_user:
            type = "tinybird"

        sorted_organizations.append(
            {
                "id": org.get("id") or "",
                "name": org.get("name") or "",
                "role": role,
                "domains": [domain.strip() for domain in domains] if domains else None,
                "type": type,
            }
        )

    type_priority: Dict[OrgType, int] = {"tinybird": 0, "domain": 1, "admin": 2, "member": 3}

    sorted_organizations.sort(key=lambda x: type_priority[x["type"]])

    return sorted_organizations


def ask_for_organization_interactively(organizations: List[Organization]) -> Optional[Organization]:
    rows = [(index + 1, org["name"], org["role"], org["id"]) for index, org in enumerate(organizations)]

    echo_safe_humanfriendly_tables_format_smart_table(rows, column_names=["Idx", "Name", "Role", "Id"])
    click.echo("")
    click.echo("   [0] to cancel")

    org_index = -1
    while org_index == -1:
        org_index = click.prompt("\nSelect an organization to include the workspace in", default=1)
        if org_index < 0 or org_index > len(organizations):
            click.echo(FeedbackManager.error_organization_index(organization_index=org_index))
            org_index = -1

    if org_index == 0:
        click.echo(FeedbackManager.info_cancelled_by_user())
        return None

    return organizations[org_index - 1]


def ask_for_organization_name(config: CLIConfig) -> str:
    user_email = config.get_user_email()
    default_organization_name = (
        user_email.split("@")[1].split(".")[0] if user_email else None
    )  # Example: "jane.doe@tinybird.com" -> "tinybird"
    # check if domain is a common domain
    if default_organization_name in ["gmail", "yahoo", "hotmail", "outlook"]:
        default_organization_name = (
            user_email.split("@")[0] if user_email else None
        )  # Example: "jane.doe@gmail.com" -> "jane.doe"
    return click.prompt(
        "\nYou need to create an organization to continue.\nEnter organization name",
        hide_input=False,
        show_default=True,
        default=default_organization_name,
    )


def create_organization_and_add_workspaces(
    config: CLIConfig, organization_name: str, user_token: str
) -> Dict[str, Any]:
    client: TinyB = config.get_client(token=user_token)
    try:
        organization = client.create_organization(organization_name)
        click.echo(FeedbackManager.success_organization_created(organization_name=organization_name))
    except Exception as e:
        raise CLIWorkspaceException(FeedbackManager.error_organization_creation(error=str(e)))

    # Add existing orphan workspaces to the organization - this is only needed for backwards compatibility
    user_workspaces = client.user_workspaces_with_organization(version="v1")
    workspaces_to_migrate = []
    for workspace in user_workspaces["workspaces"]:
        if workspace.get("organization") is None and workspace.get("role") == "admin":
            workspaces_to_migrate.append(workspace["id"])
    client.add_workspaces_to_organization(organization["id"], workspaces_to_migrate)

    return organization


def get_user_token(config: CLIConfig, user_token: Optional[str] = None) -> str:
    client = config.get_client()
    host = config.get_host() or CLIConfig.DEFAULTS["host"]
    ui_host = get_display_cloud_host(host)

    if not user_token:
        user_token = config.get_user_token()
        if user_token:
            try:
                check_user_token_with_client(client, user_token)
            except Exception:
                user_token = None
                pass
        if not user_token:
            user_token = ask_for_user_token("delete a workspace", ui_host)
        if not user_token:
            raise CLIWorkspaceException(
                FeedbackManager.error_exception(
                    error='Invalid user authentication. Make sure you are using the "user token" instead of the "admin your@email" token.'
                )
            )

    check_user_token_with_client(client, user_token)

    return user_token


def ask_for_organization(
    organizations: Optional[List[Dict[str, Any]]],
    organization_id: Optional[str] = None,
    user_token: Optional[str] = None,
) -> Tuple[Optional[str], Optional[str]]:
    config = CLIConfig.get_project_config()
    user_email = config.get_user_email()

    if organization_id:
        if organizations and len(organizations) > 0:
            organization = next((org for org in organizations if org.get("id") == organization_id), None)
        if not organization:
            raise CLIException(FeedbackManager.error_organization_not_found(organization_id=organization_id))
        organization_name = organization.get("name")
        return organization_id, organization_name

    if organizations is None or len(organizations) == 0:
        organization_name = ask_for_organization_name(config)
        user_token = get_user_token(config, user_token)
        organization = create_organization_and_add_workspaces(config, organization_name, user_token)
        organization_id = organization.get("id")
    elif len(organizations) == 1:
        organization_name = organizations[0]["name"]
        organization_id = organizations[0]["id"]
    else:
        sorted_organizations = sort_organizations_by_user(organizations, user_email=user_email)
        current_organization = ask_for_organization_interactively(sorted_organizations)
        if current_organization:
            organization_id = current_organization.get("id")
            organization_name = current_organization.get("name")
        else:
            return None, None
    return organization_id, organization_name


event_error_separator = "__error__"


def sys_exit(event: str, msg: str) -> None:
    sys.exit(f"{event}{event_error_separator}{msg}")


def get_error_event(error: str) -> Tuple[str, str]:
    try:
        error_event = error.split(event_error_separator)[0]
        silent_error_msg = error.split(event_error_separator)[1]
    except Exception:
        error_event = "error"
        silent_error_msg = "Unknown error"
    return error_event, silent_error_msg


def force_echo(string: str) -> None:
    click.echo(string, force_output=True)  # type: ignore


def echo_json(data: Dict[str, Any], indent: Union[None, int, str] = None) -> None:
    force_echo(json.dumps(data, indent=indent))


def update_cli() -> None:
    click.echo(FeedbackManager.highlight(message="» Updating Tinybird CLI..."))

    try:
        process = subprocess.Popen(
            ["uv", "tool", "upgrade", "tinybird"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError:
        raise CLIException(
            FeedbackManager.error(
                message="Cannot find required tool: uv. Reinstall using: curl https://tinybird.co | sh"
            )
        )

    stdout, stderr = process.communicate()
    if "Nothing to upgrade" not in stdout + stderr:
        for line in stdout.split("\n") + stderr.split("\n"):
            if "Updated tinybird" in line:
                click.echo(FeedbackManager.info(message=f"» {line}"))
        click.echo(FeedbackManager.success(message="✓ Tinybird CLI updated"))
    else:
        click.echo(FeedbackManager.info(message="✓ Tinybird CLI is already up-to-date"))


def create_workspace_branch(
    branch_name: Optional[str],
    last_partition: bool,
    all: bool,
    ignore_datasources: Optional[List[str]],
    wait: Optional[bool],
) -> None:
    """
    Creates a workspace branch
    """
    config = CLIConfig.get_project_config()
    _ = try_update_config_with_remote(config)

    try:
        workspace = get_current_workspace(config)
        if not workspace:
            raise CLIWorkspaceException(FeedbackManager.error_workspace())

        if not branch_name:
            click.echo(FeedbackManager.info_workspace_branch_create_greeting())
            default_name = f"{workspace['name']}_{uuid.uuid4().hex[0:4]}"
            branch_name = click.prompt("\Branch name", default=default_name, err=True, type=str)
        assert isinstance(branch_name, str)

        response = config.get_client().create_workspace_branch(
            branch_name,
            last_partition,
            all,
            ignore_datasources,
        )
        assert isinstance(response, dict)

        is_job: bool = "job" in response
        is_summary: bool = "partitions" in response

        if not is_job and not is_summary:
            raise CLIException(str(response))

        if all and not is_job:
            raise CLIException(str(response))

        click.echo(
            FeedbackManager.success_workspace_branch_created(workspace_name=workspace["name"], branch_name=branch_name)
        )

        job_id: Optional[str] = None

        if is_job:
            job_id = response["job"]["job_id"]
            job_url = response["job"]["job_url"]
            click.echo(FeedbackManager.info_data_branch_job_url(url=job_url))

        if wait and is_job:
            assert isinstance(job_id, str)

            # Await the job to finish and get the result dict
            job_response = wait_job(config.get_client(), job_id, job_url, "Environment creation")
            if job_response is None:
                raise CLIException(f"Empty job API response (job_id: {job_id}, job_url: {job_url})")
            else:
                response = job_response.get("result", {})
                is_summary = "partitions" in response

    except Exception as e:
        raise CLIException(FeedbackManager.error_exception(error=str(e)))


async def print_current_branch(config: CLIConfig) -> None:
    _ = try_update_config_with_remote(config, only_if_needed=True)

    response = config.get_client().user_workspaces_and_branches("v1")

    columns = ["name", "id", "workspace"]
    table = []

    for workspace in response["workspaces"]:
        if config["id"] == workspace["id"]:
            click.echo(FeedbackManager.info_current_branch())
            if workspace.get("is_branch"):
                name = workspace["name"]
                main_workspace = get_current_main_workspace(config)
                assert isinstance(main_workspace, dict)
                main_name = main_workspace["name"]
            else:
                name = MAIN_BRANCH
                main_name = workspace["name"]
            table.append([name, workspace["id"], main_name])
            break

    echo_safe_humanfriendly_tables_format_smart_table(table, column_names=columns)
