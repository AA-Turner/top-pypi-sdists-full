# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

from typing import Any, Dict, List, Optional

import click
import requests
from click import Context

from tinybird.tb.client import AuthNoTokenException, TinyB
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import (
    _get_workspace_plan_name,
    ask_for_organization,
    create_workspace_interactive,
    create_workspace_non_interactive,
    echo_safe_humanfriendly_tables_format_smart_table,
    get_current_main_workspace,
    get_organizations_by_user,
    get_user_token,
    switch_workspace,
    try_update_config_with_remote,
)
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.exceptions import CLIWorkspaceException
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.local_common import (
    TB_LOCAL_ADDRESS,
    TB_LOCAL_DEFAULT_WORKSPACE_NAME,
    get_local_tokens,
)


@cli.group()
@click.pass_context
def workspace(ctx: Context) -> None:
    """Workspace commands."""


@workspace.command(name="ls")
@click.pass_context
def workspace_ls(ctx: Context) -> None:
    """List all the workspaces you have access to in the account you're currently authenticated into."""

    config = CLIConfig.get_project_config()
    client: TinyB = ctx.ensure_object(dict)["client"]

    response = client.user_workspaces(version="v1")

    current_main_workspace = get_current_main_workspace(config)
    if not current_main_workspace:
        raise CLIWorkspaceException(FeedbackManager.error_unable_to_identify_main_workspace())

    columns = ["name", "id", "role", "plan", "current"]
    table = []
    click.echo(FeedbackManager.info_workspaces())

    for workspace in response["workspaces"]:
        table.append(
            [
                workspace["name"],
                workspace["id"],
                workspace["role"],
                _get_workspace_plan_name(workspace["plan"]),
                current_main_workspace["name"] == workspace["name"],
            ]
        )

    echo_safe_humanfriendly_tables_format_smart_table(table, column_names=columns)


@workspace.command(name="use")
@click.argument("workspace_name_or_id")
@click.pass_context
def workspace_use(ctx: Context, workspace_name_or_id: str) -> None:
    """Switch to another workspace. Use 'tb workspace ls' to list the workspaces you have access to."""
    config = CLIConfig.get_project_config()
    is_cloud = ctx.ensure_object(dict)["env"] == "cloud"
    if not is_cloud:
        raise CLIWorkspaceException(
            FeedbackManager.error(
                message="`tb workspace use` is not available in local mode. Use --cloud to switch to a cloud workspace and it will be used in Tinybird Local."
            )
        )

    switch_workspace(config, workspace_name_or_id)


@workspace.command(name="current")
@click.pass_context
def workspace_current(ctx: Context):
    """Show the workspace you're currently authenticated to"""
    config = CLIConfig.get_project_config()
    env = ctx.ensure_object(dict)["env"]
    client: TinyB = ctx.ensure_object(dict)["client"]
    if env == "cloud":
        _ = try_update_config_with_remote(config, only_if_needed=True)

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

    current_main_workspace = _get_current_workspace(user_workspaces, config.get("name", current_workspace["name"]))

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


@workspace.command(name="create", short_help="Create a new Workspace for your Tinybird user")
@click.argument("workspace_name", required=False)
@click.option(
    "--organization-id",
    "organization_id",
    type=str,
    required=False,
    help="When passed, the workspace will be created in the specified organization",
)
@click.pass_context
def create_workspace(
    ctx: Context,
    workspace_name: str,
    organization_id: Optional[str],
) -> None:
    config = CLIConfig.get_project_config()
    is_cloud = ctx.ensure_object(dict)["env"] == "cloud"
    if not is_cloud:
        raise CLIWorkspaceException(
            FeedbackManager.error(
                message="`tb workspace create` is not available in local mode. Use --cloud to create a workspace in Tinybird Cloud and it will be used in Tinybird Local."
            )
        )

    config = CLIConfig.get_project_config()
    user_token = get_user_token(config)
    fork = False

    if not user_token:
        raise CLIWorkspaceException(
            FeedbackManager.error(message="This action requires authentication. Run 'tb login' first.")
        )

    organization_name = None
    organizations = get_organizations_by_user(config, user_token)

    organization_id, organization_name = ask_for_organization(organizations, organization_id)
    if not organization_id:
        return

    # If we have at least workspace_name, we start the non interactive
    # process, creating an empty workspace
    if workspace_name:
        create_workspace_non_interactive(ctx, workspace_name, user_token, fork, organization_id, organization_name)
    else:
        create_workspace_interactive(ctx, workspace_name, user_token, fork, organization_id, organization_name)


@workspace.command(name="delete", short_help="Delete a workspace for your Tinybird user")
@click.argument("workspace_name_or_id")
@click.option(
    "--confirm_hard_delete",
    default=None,
    help="Enter the name of the workspace to confirm you want to run a hard delete over the workspace",
    hidden=True,
)
@click.option("--yes", is_flag=True, default=False, help="Don't ask for confirmation")
@click.pass_context
def delete_workspace(ctx: Context, workspace_name_or_id: str, confirm_hard_delete: Optional[str], yes: bool) -> None:
    """Delete a workspace where you are an admin."""

    is_cloud = ctx.ensure_object(dict)["env"] == "cloud"
    config = CLIConfig.get_project_config()
    if is_cloud:
        user_token = get_user_token(config)
    else:
        user_token = get_local_tokens()["user_token"]
    client: TinyB = ctx.ensure_object(dict)["client"]

    workspaces = (client.user_workspaces(version="v1")).get("workspaces", [])
    workspace_to_delete = next(
        (
            workspace
            for workspace in workspaces
            if workspace["name"] == workspace_name_or_id or workspace["id"] == workspace_name_or_id
        ),
        None,
    )

    if not workspace_to_delete:
        raise CLIWorkspaceException(FeedbackManager.error_workspace(workspace=workspace_name_or_id))

    if workspace_to_delete.get("name") == TB_LOCAL_DEFAULT_WORKSPACE_NAME:
        raise CLIWorkspaceException(
            FeedbackManager.error(message="You cannot delete your default Tinybird Local workspace.")
        )

    if yes or click.confirm(
        FeedbackManager.warning_confirm_delete_workspace(workspace_name=workspace_to_delete.get("name"))
    ):
        client.token = user_token

        try:
            client.delete_workspace(workspace_to_delete["id"], confirm_hard_delete, version="v1")
            click.echo(FeedbackManager.success_workspace_deleted(workspace_name=workspace_to_delete["name"]))
        except Exception as e:
            raise CLIWorkspaceException(FeedbackManager.error_exception(error=str(e)))


@workspace.command(name="clear", short_help="Clear a workspace. Only available against Tinybird Local.")
@click.option("--yes", is_flag=True, default=False, help="Don't ask for confirmation")
@click.pass_context
def workspace_clear(ctx: Context, yes: bool) -> None:
    """Delete a workspace where you are an admin."""
    is_cloud = ctx.ensure_object(dict)["env"] == "cloud"
    if is_cloud:
        raise CLIWorkspaceException(
            FeedbackManager.error(
                message="`tb workspace clear` is not available against Tinybird Cloud. Use `tb --cloud deploy` instead."
            )
        )
    yes = yes or click.confirm(
        FeedbackManager.warning(message="Are you sure you want to clear the workspace? [y/N]:"),
        show_default=False,
        prompt_suffix="",
    )
    if yes:
        clear_workspace()


def clear_workspace() -> None:
    config = CLIConfig.get_project_config()
    tokens = get_local_tokens()

    user_token = tokens["user_token"]
    admin_token = tokens["admin_token"]
    user_client = config.get_client(host=TB_LOCAL_ADDRESS, token=user_token)
    ws_name = config.get("name")
    if not ws_name:
        raise AuthNoTokenException()

    user_workspaces = requests.get(
        f"{TB_LOCAL_ADDRESS}/v1/user/workspaces?with_organization=true&token={admin_token}"
    ).json()
    user_org_id = user_workspaces.get("organization_id", {})
    local_workspaces = user_workspaces.get("workspaces", [])

    ws = next((ws for ws in local_workspaces if ws["name"] == ws_name), None)

    if not ws:
        raise CLIWorkspaceException(FeedbackManager.error(message=f"Workspace '{ws_name}' not found."))

    requests.delete(f"{TB_LOCAL_ADDRESS}/v1/workspaces/{ws['id']}?token={user_token}&hard_delete_confirmation=yes")
    user_workspaces = user_client.user_workspaces(version="v1")
    ws = next((ws for ws in user_workspaces["workspaces"] if ws["name"] == ws_name), None)

    if ws:
        raise CLIWorkspaceException(
            FeedbackManager.error(message=f"Workspace '{ws_name}' was not cleared properly. Please try again.")
        )

    user_client.create_workspace(ws_name, assign_to_organization_id=user_org_id, version="v1")
    user_workspaces = requests.get(f"{TB_LOCAL_ADDRESS}/v1/user/workspaces?token={admin_token}").json()
    ws = next((ws for ws in user_workspaces["workspaces"] if ws["name"] == ws_name), None)

    if not ws:
        raise CLIWorkspaceException(
            FeedbackManager.error(message=f"Workspace '{ws_name}' was not cleared properly. Please try again.")
        )

    click.echo(FeedbackManager.success(message=f"✓ Workspace '{ws_name}' cleared"))
