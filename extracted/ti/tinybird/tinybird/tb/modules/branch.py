# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

from typing import List, Optional, Tuple

import click

from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import (
    MAIN_BRANCH,
    create_workspace_branch,
    echo_safe_humanfriendly_tables_format_smart_table,
    get_current_main_workspace,
    get_current_workspace_branches,
    get_workspace_member_email,
    switch_to_workspace_by_user_workspace_data,
    try_update_config_with_remote,
)
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.exceptions import CLIBranchException, CLIException
from tinybird.tb.modules.feedback_manager import FeedbackManager


@cli.group()
def branch() -> None:
    """Branch commands. Custom branches is an experimental feature in beta."""
    pass


@branch.command(name="ls")
@click.option("--sort/--no-sort", default=False, help="Sort the table rows by name")
def branch_ls(sort: bool) -> None:
    """List all the branches available in the current workspace"""

    config = CLIConfig.get_project_config()
    _ = try_update_config_with_remote(config, only_if_needed=True)

    client = config.get_client()

    current_main_workspace = get_current_main_workspace(config)
    assert isinstance(current_main_workspace, dict)

    if current_main_workspace["id"] != config["id"]:
        client = config.get_client(token=current_main_workspace["token"])

    response = client.branches()

    columns = ["name", "id", "created_at", "owner", "current"]

    table: List[Tuple[str, str, str, str, bool]] = []

    for branch in response["environments"]:
        branch_owner_email = get_workspace_member_email(branch, branch["owner"])

        table.append(
            (branch["name"], branch["id"], branch["created_at"], branch_owner_email, config["id"] == branch["id"])
        )

    current_branch = [row for row in table if row[4]]
    other_branches = [row for row in table if not row[4]]

    if sort:
        other_branches.sort(key=lambda x: x[0])

    sorted_table = current_branch + other_branches

    click.echo(FeedbackManager.info(message="\n** Branches:"))
    echo_safe_humanfriendly_tables_format_smart_table(sorted_table, column_names=columns)


@branch.command(name="create", short_help="Create a new branch in the current Workspace")
@click.argument("branch_name", required=False)
@click.option(
    "--last-partition",
    is_flag=True,
    default=False,
    help="Attach the last modified partition from the current workspace to the new branch",
)
@click.option(
    "-i",
    "--ignore-datasource",
    "ignore_datasources",
    type=str,
    multiple=True,
    help="Ignore specified data source partitions",
)
@click.option(
    "--wait/--no-wait",
    is_flag=True,
    default=True,
    help="Wait for data branch jobs to finish, showing a progress bar. Disabled by default.",
)
def create_branch(branch_name: Optional[str], last_partition: bool, ignore_datasources: List[str], wait: bool) -> None:
    create_workspace_branch(branch_name, last_partition, False, list(ignore_datasources), wait)


@branch.command(name="rm", short_help="Removes an branch from the workspace. It can't be recovered.")
@click.argument("branch_name_or_id")
@click.option("--yes", is_flag=True, default=False, help="Do not ask for confirmation")
def delete_branch(branch_name_or_id: str, yes: bool) -> None:
    """Remove an branch"""

    config = CLIConfig.get_project_config()
    _ = try_update_config_with_remote(config)

    client = config.get_client()

    if branch_name_or_id == MAIN_BRANCH:
        raise CLIException(FeedbackManager.error_not_allowed_in_main_branch())

    try:
        workspace_branches = get_current_workspace_branches(config)
        workspace_to_delete = next(
            (
                workspace
                for workspace in workspace_branches
                if workspace["name"] == branch_name_or_id or workspace["id"] == branch_name_or_id
            ),
            None,
        )
    except Exception as e:
        raise CLIBranchException(FeedbackManager.error_exception(error=str(e)))

    if not workspace_to_delete:
        raise CLIBranchException(FeedbackManager.error_branch(branch=branch_name_or_id))

    if yes or click.confirm(FeedbackManager.warning_confirm_delete_branch(branch=workspace_to_delete["name"])):
        need_to_switch_to_main = workspace_to_delete.get("main") and config["id"] == workspace_to_delete["id"]
        # get origin workspace if deleting current branch
        if need_to_switch_to_main:
            try:
                workspaces = (client.user_workspaces()).get("workspaces", [])
                workspace_main = next(
                    (workspace for workspace in workspaces if workspace["id"] == workspace_to_delete["main"]), None
                )
            except Exception:
                workspace_main = None
        try:
            client.delete_branch(workspace_to_delete["id"])
            click.echo(FeedbackManager.success_branch_deleted(branch_name=workspace_to_delete["name"]))
        except Exception as e:
            raise CLIBranchException(FeedbackManager.error_exception(error=str(e)))
        else:
            if need_to_switch_to_main:
                if workspace_main:
                    switch_to_workspace_by_user_workspace_data(config, workspace_main)
                else:
                    raise CLIException(FeedbackManager.error_switching_to_main())
