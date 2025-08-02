import os
from typing import Any, Dict, Iterable, List, Optional, Tuple

import click

from tinybird.tb.client import TinyB
from tinybird.tb.config import get_display_cloud_host
from tinybird.tb.modules.cli import CLIConfig, cli
from tinybird.tb.modules.common import echo_json, force_echo, format_robust_table
from tinybird.tb.modules.exceptions import CLILocalException
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.local_common import TB_LOCAL_ADDRESS, get_tinybird_local_config
from tinybird.tb.modules.project import Project


@cli.command(name="info")
@click.pass_context
def info(ctx: click.Context) -> None:
    """Get information about the project that is currently being used"""
    ctx_config = ctx.ensure_object(dict)["config"]
    project: Project = ctx.ensure_object(dict)["project"]
    output = ctx.ensure_object(dict)["output"]

    if output not in {"human", "json"}:
        force_echo(FeedbackManager.error_invalid_output_format(formats=", ".join(["human", "json"])))
        return

    click.echo(FeedbackManager.highlight(message="» Tinybird Cloud:"))
    cloud_table, cloud_columns = get_cloud_info(ctx_config)
    click.echo(FeedbackManager.highlight(message="\n» Tinybird Local:"))
    local_table, local_columns = get_local_info(ctx_config)
    click.echo(FeedbackManager.highlight(message="\n» Project:"))
    project_table, project_columns = get_project_info(project.folder)
    if output == "json":
        cloud_data = {}
        if cloud_columns and cloud_table and isinstance(cloud_table, list) and len(cloud_table) > 0:
            cloud_data = {column: cloud_table[0][i] for i, column in enumerate(cloud_columns)}

        local_data = {}
        if local_columns and local_table and isinstance(local_table, list) and len(local_table) > 0:
            local_data = {column: local_table[0][i] for i, column in enumerate(local_columns)}

        project_data = {}
        if project_columns and project_table and isinstance(project_table, list) and len(project_table) > 0:
            project_data = {column: project_table[0][i] for i, column in enumerate(project_columns)}
        echo_json({"cloud": cloud_data, "local": local_data, "project": project_data})


def get_cloud_info(ctx_config: Dict[str, Any]) -> Tuple[Iterable[Any], List[str]]:
    config = CLIConfig.get_project_config()

    try:
        client = config.get_client()
        token = config.get_token() or "No workspace token found"
        api_host = config.get("host") or "No API host found"
        ui_host = get_display_cloud_host(api_host)
        user_email = config.get("user_email") or "No user email found"
        user_token = config.get_user_token() or "No user token found"
        return get_env_info(client, ctx_config, user_email, token, user_token, api_host, ui_host)
    except Exception:
        click.echo(
            FeedbackManager.warning(
                message="\n⚠  Could not retrieve Tinybird Cloud info. Please run `tb login` first or check that you are located in the correct directory."
            )
        )
        return [], []


def get_local_info(config: Dict[str, Any]) -> Tuple[Iterable[Any], List[str]]:
    try:
        local_config = get_tinybird_local_config(config, test=False, silent=False)
        local_client = local_config.get_client(host=TB_LOCAL_ADDRESS, staging=False)
        user_email = local_config.get_user_email() or "No user email found"
        token = local_config.get_token() or "No token found"
        user_token = local_config.get_user_token() or "No user token found"
        api_host = TB_LOCAL_ADDRESS
        ui_host = get_display_cloud_host(api_host)
        return get_env_info(local_client, config, user_email, token, user_token, api_host, ui_host, is_local=True)
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

    columns = ["user", "workspace_name", "workspace_id", "token", "user_token", "api", "ui"]
    if current_main_workspace["name"]:
        ui_host += f"/{current_main_workspace['name']}"
    table = [
        (user_email, current_main_workspace["name"], current_main_workspace["id"], token, user_token, api_host, ui_host)
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
