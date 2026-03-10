import os
import re
from typing import Any, Dict, Iterable, List, Optional, Tuple

import click

from tinybird.tb.client import TinyB
from tinybird.tb.config import get_clickhouse_host, get_display_cloud_host
from tinybird.tb.modules.cli import CLIConfig, cli
from tinybird.tb.modules.common import echo_json, force_echo, format_robust_table
from tinybird.tb.modules.exceptions import CLILocalException
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.local_common import TB_LOCAL_ADDRESS, get_tinybird_local_config
from tinybird.tb.modules.project import Project


@cli.command(name="info")
@click.option("--skip-local", is_flag=True, default=False, help="Skip local info")
@click.pass_context
def info(ctx: click.Context, skip_local: bool) -> None:
    """Get information about the project that is currently being used"""
    ctx_config = ctx.ensure_object(dict)["config"]
    project: Project = ctx.ensure_object(dict)["project"]
    output = ctx.ensure_object(dict)["output"]

    if output not in {"human", "json"}:
        force_echo(FeedbackManager.error_invalid_output_format(formats=", ".join(["human", "json"])))
        return

    click.echo(FeedbackManager.highlight(message="» Tinybird Cloud:"))
    cloud_table, cloud_columns = get_cloud_info(ctx_config)

    local_error: Optional[str] = None
    if not skip_local:
        click.echo(FeedbackManager.highlight(message="\n» Tinybird Local:"))
        try:
            local_table, local_columns = get_local_info(ctx_config, silent=True)
        except CLILocalException as e:
            local_table, local_columns = [], []
            local_error = _clean_error_message(str(e))
            click.echo(FeedbackManager.error(message=f"Error: {local_error}"))

    click.echo(FeedbackManager.highlight(message="\n» Project:"))
    project_table, project_columns = get_project_info(project.folder)

    branches_summary = get_branches_summary(ctx_config)

    if output == "human":
        click.echo(FeedbackManager.highlight(message="\n» Branches:"))
        click.echo(f"Current branch: {branches_summary['current']}")
        click.echo(f"Branch count: {branches_summary['count']}")
        if branches_summary["table"]:
            click.echo(format_robust_table(branches_summary["table"], column_names=branches_summary["columns"]))
        elif branches_summary.get("error"):
            click.echo(FeedbackManager.warning(message=branches_summary["error"]))

    if output == "json":
        response: dict[str, Any] = {}

        cloud_data = {}
        if cloud_columns and cloud_table and isinstance(cloud_table, list) and len(cloud_table) > 0:
            cloud_data = {column: cloud_table[0][i] for i, column in enumerate(cloud_columns)}
        response["cloud"] = cloud_data

        if not skip_local:
            local_data = {}
            if local_error:
                local_data["error"] = local_error
            if local_columns and local_table and isinstance(local_table, list) and len(local_table) > 0:
                local_data = {column: local_table[0][i] for i, column in enumerate(local_columns)}
            response["local"] = local_data

        project_data = {}
        if project_columns and project_table and isinstance(project_table, list) and len(project_table) > 0:
            project_data = {column: project_table[0][i] for i, column in enumerate(project_columns)}
        response["project"] = project_data

        response["branches"] = {
            "current": branches_summary["current"],
            "count": branches_summary["count"],
            "items": branches_summary["items"],
        }

        echo_json(response)


def get_cloud_info(ctx_config: Dict[str, Any]) -> Tuple[Iterable[Any], List[str]]:
    config = CLIConfig.get_project_config()

    try:
        client = config.get_client()
        token = config.get_token() or "No workspace token found"
        api_host = config.get("host") or "No API host found"
        ui_host = get_display_cloud_host(api_host)
        ch_host = get_clickhouse_host(api_host)
        user_email = config.get("user_email") or "No user email found"
        user_token = config.get_user_token() or "No user token found"
        return get_env_info(client, ctx_config, user_email, token, user_token, api_host, ui_host, ch_host)
    except Exception:
        click.echo(
            FeedbackManager.warning(
                message="\n⚠  Could not retrieve Tinybird Cloud info. Please run `tb login` first or check that you are located in the correct directory."
            )
        )
        return [], []


def _clean_error_message(error: str) -> str:
    ansi_clean = re.sub(r"\x1b\[[0-9;]*m", "", error).strip()
    if ansi_clean.startswith("Error: "):
        return ansi_clean[len("Error: ") :]
    return ansi_clean


def get_local_info(config: Dict[str, Any], silent: bool = False) -> Tuple[Iterable[Any], List[str]]:
    try:
        local_config = get_tinybird_local_config(config, test=False, silent=silent)
        local_client = local_config.get_client(host=TB_LOCAL_ADDRESS, staging=False)
        user_email = local_config.get_user_email() or "No user email found"
        token = local_config.get_token() or "No token found"
        user_token = local_config.get_user_token() or "No user token found"
        api_host = TB_LOCAL_ADDRESS
        ui_host = get_display_cloud_host(api_host)
        ch_host = get_clickhouse_host(api_host)
        return get_env_info(
            local_client, config, user_email, token, user_token, api_host, ui_host, ch_host, is_local=True
        )
    except CLILocalException as e:
        raise e
    except Exception as e:
        click.echo(
            FeedbackManager.warning(
                message=f"\n⚠  Tinybird Local is running but could not retrieve the workspace info. Please run `tb login` first or check that you are located in the correct directory. {e}"
            )
        )
        return [], []


def get_env_info(
    client: TinyB,
    config: Dict[str, Any],
    user_email: str,
    token: str,
    user_token: str,
    api_host: str,
    ui_host: str,
    ch_host: str,
    is_local=False,
) -> Tuple[List[Any], List[str]]:
    user_workspaces = client.user_workspaces(version="v1")
    current_workspace = client.workspace_info(version="v1")

    def _get_current_workspace(user_workspaces: Dict[str, Any], current_workspace_id: str) -> Optional[Dict[str, Any]]:
        def get_workspace_by_name(workspaces: List[Dict[str, Any]], name: str) -> Optional[Dict[str, Any]]:
            return next((ws for ws in workspaces if ws["name"] == name), None)

        workspaces: Optional[List[Dict[str, Any]]] = user_workspaces.get("workspaces")
        if not workspaces:
            return None

        current: Optional[Dict[str, Any]] = get_workspace_by_name(workspaces, current_workspace_id)
        return current

    current_main_workspace = _get_current_workspace(user_workspaces, config.get("name") or current_workspace["name"])

    assert isinstance(current_main_workspace, dict)

    columns = ["user", "workspace_name", "workspace_id", "token", "user_token", "api", "ui", "clickhouse"]
    if current_main_workspace["name"]:
        ui_host += f"/{current_main_workspace['name']}"
    table = [
        (
            user_email,
            current_main_workspace["name"],
            current_main_workspace["id"],
            token,
            user_token,
            api_host,
            ui_host,
            ch_host,
        )
    ]

    if is_local and (
        "Tinybird_Local_Build_" in current_main_workspace["name"]
        or "Tinybird_Local_Testing" in current_main_workspace["name"]
    ):
        click.echo(
            FeedbackManager.warning(
                message="\n⚠  Tinybird Local is running but you are logged locally in a temporal workspace until you run `tb login` or check that you are located in the correct directory."
            )
        )
    click.echo(format_robust_table(table, column_names=columns))
    return table, columns


def get_project_info(project_path: Optional[str] = None) -> Tuple[Iterable[Any], List[str]]:
    config = CLIConfig.get_project_config()
    tinyb_path = config.get_tinyb_file()
    current_path = os.getcwd()

    if project_path:
        # Use the provided project path
        pass
    elif tinyb_path:
        # Use the directory containing the .tinyb file as the project path
        project_path = os.path.dirname(tinyb_path)
    else:
        # No .tinyb file found, use current directory
        project_path = current_path
        tinyb_path = "Not found"

    columns = ["current", ".tinyb", "project"]
    table: Iterable[Any] = [(current_path, tinyb_path, project_path)]
    click.echo(format_robust_table(table, column_names=columns))
    return table, columns


def get_branches_summary(ctx_config: Dict[str, Any]) -> Dict[str, Any]:
    columns = ["name", "current", "token", "ui"]

    try:
        config = CLIConfig.get_project_config()
        client = config.get_client()
        api_host = config.get("host") or ""
        ui_host = get_display_cloud_host(api_host) if api_host else ""

        workspaces_response = client.user_workspaces_and_branches(version="v1")
        workspaces = workspaces_response.get("workspaces", [])

        current_workspace = next((ws for ws in workspaces if ws.get("id") == ctx_config.get("id")), None)
        if not current_workspace:
            current_workspace = next((ws for ws in workspaces if ws.get("current")), None)
        if not current_workspace:
            current_workspace = client.workspace_info(version="v1")

        main_workspace_name = current_workspace.get("name", "No workspace")
        if current_workspace.get("is_branch"):
            main_workspace_id = current_workspace.get("main")
            main_workspace = next((ws for ws in workspaces if ws.get("id") == main_workspace_id), None)
            if main_workspace and main_workspace.get("name"):
                main_workspace_name = main_workspace["name"]

        branches = client.branches().get("environments", [])

        current_branch = "main"
        if current_workspace.get("is_branch"):
            current_branch = current_workspace.get("name", "main")

        items = []
        for branch in branches:
            branch_name = branch.get("name") or "No branch name"
            branch_token = branch.get("token") or "No token found"
            branch_current = current_workspace.get("id") == branch.get("id")
            branch_ui = (
                f"{ui_host}/{main_workspace_name}~{branch_name}"
                if ui_host and main_workspace_name and branch_name != "No branch name"
                else "No UI URL found"
            )

            items.append(
                {
                    "name": branch_name,
                    "current": branch_current,
                    "token": branch_token,
                    "ui": branch_ui,
                }
            )

        items.sort(key=lambda branch: (not branch["current"], branch["name"]))
        table = [(branch["name"], branch["current"], branch["token"], branch["ui"]) for branch in items]

        return {
            "current": current_branch,
            "count": len(items),
            "items": items,
            "table": table,
            "columns": columns,
            "error": None,
        }
    except Exception:
        return {
            "current": "main",
            "count": 0,
            "items": [],
            "table": [],
            "columns": columns,
            "error": "Could not retrieve branch info.",
        }
