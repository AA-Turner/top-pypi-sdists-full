from typing import Any, Dict, Optional

import click
from click.core import ParameterSource

from tinybird.tb.client import TinyB
from tinybird.tb.modules.cli import (
    cli,
    ensure_valid_workspace_name,
    get_current_git_branch,
    sanitize_branch_name,
)
from tinybird.tb.modules.common import _get_tb_client
from tinybird.tb.modules.deployment_common import create_deployment
from tinybird.tb.modules.feedback_manager import FeedbackManager, get_cli_name
from tinybird.tb.modules.project import Project


def generate_preview_branch_name(git_branch: Optional[str]) -> str:
    branch_part = sanitize_branch_name(git_branch or "", enforce_workspace_prefix_rules=False)
    return f"tmp_ci_{branch_part or 'unknown'}"


def _delete_preview_branch_if_exists(cloud_client: TinyB, preview_branch_name: str) -> None:
    workspaces = cloud_client.user_workspaces_and_branches(version="v1").get("workspaces", [])
    existing_branch = next(
        (
            workspace
            for workspace in workspaces
            if workspace.get("name") == preview_branch_name and workspace.get("is_branch")
        ),
        None,
    )
    if not existing_branch:
        return

    click.echo(FeedbackManager.info(message=f"» Removing existing preview branch '{preview_branch_name}'..."))
    cloud_client.delete_branch(existing_branch["id"])


def _create_preview_branch(cloud_client: TinyB, preview_branch_name: str) -> None:
    click.echo(FeedbackManager.highlight(message=f"» Creating preview branch '{preview_branch_name}'..."))
    response = cloud_client.create_workspace_branch(
        branch_name=preview_branch_name,
        last_partition=False,
        all=False,
    )

    job_data = response.get("job") if isinstance(response, dict) else None
    if not isinstance(job_data, dict):
        return

    job_id = job_data.get("job_id") or job_data.get("id")
    if isinstance(job_id, str):
        cloud_client.wait_for_job(job_id)


def run_preview_cloud(
    project: Project,
    config: Dict[str, Any],
    preview_branch_name: str,
    check: bool,
    output: str,
) -> None:
    cloud_client, _ = _get_tb_client(config.get("token", ""), config["host"])
    _delete_preview_branch_if_exists(cloud_client, preview_branch_name)
    _create_preview_branch(cloud_client, preview_branch_name)

    branch_client, _ = _get_tb_client(
        config.get("token", ""),
        config["host"],
        branch=preview_branch_name,
        create_branch_if_missing=True,
    )
    preview_config = dict(config)
    preview_config["name"] = preview_branch_name

    click.echo(FeedbackManager.highlight(message=f"» Deploying preview branch '{preview_branch_name}'..."))
    create_deployment(
        project=project,
        client=branch_client,
        config=preview_config,
        wait=True,
        auto=True,
        check=check,
        allow_destructive_operations=True,
        output=output,
    )
    click.echo(FeedbackManager.success(message=f"✓ Preview branch '{preview_branch_name}' is live"))


@cli.command()
@click.option(
    "--dry-run", is_flag=True, default=False, help="Generate preview target and exit without creating/deploying."
)
@click.option("--check", is_flag=True, default=False, help="Validate deploy with Tinybird API without applying.")
@click.option("--name", default=None, help="Override preview branch/workspace name.")
@click.pass_context
def preview(ctx: click.Context, dry_run: bool, check: bool, name: Optional[str]) -> None:
    """Create a preview environment and deploy project resources."""
    parent_ctx = ctx.parent
    cloud_source = parent_ctx.get_parameter_source("cloud") if parent_ctx else None
    if cloud_source == ParameterSource.COMMANDLINE and parent_ctx and parent_ctx.params.get("cloud") is False:
        raise click.ClickException(
            FeedbackManager.error(
                message=f"`{get_cli_name()} preview` does not support `--local`. Preview always deploys to a cloud branch."
            )
        )

    obj: Dict[str, Any] = ctx.ensure_object(dict)
    project: Project = obj["project"]
    config: Dict[str, Any] = obj["config"]
    output: str = obj.get("output", "human")

    git_branch = get_current_git_branch()
    preview_name = ensure_valid_workspace_name(name) if name else generate_preview_branch_name(git_branch)

    if dry_run:
        click.echo(FeedbackManager.info(message=f"[dry-run] Preview target '{preview_name}' (cloud)"))
        return

    run_preview_cloud(
        project=project,
        config=config,
        preview_branch_name=preview_name,
        check=check,
        output=output,
    )
