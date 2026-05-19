import json
import logging
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Optional

import click
import requests

from tinybird.tb.client import TinyB
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import (
    echo_safe_humanfriendly_tables_format_smart_table,
    sys_exit,
)
from tinybird.tb.modules.create import persist_tinybird_config
from tinybird.tb.modules.deployment_common import (
    create_deployment,
    discard_deployment,
    migrate_to_forward_workspace,
    promote_deployment,
)
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.project import Project


def download_github_contents(api_url: str, target_dir: Path) -> None:
    """
    Recursively downloads contents from GitHub API URL to target directory.

    Args:
        api_url: str - GitHub API URL to fetch contents from
        target_dir: Path - Directory to save downloaded files to
    """
    response = requests.get(api_url)
    if response.status_code != 200:
        click.echo(
            FeedbackManager.error(message=f"Failed to fetch contents from GitHub: {response.json().get('message', '')}")
        )
        return

    contents = response.json()
    if not isinstance(contents, list):
        click.echo(FeedbackManager.error(message="Invalid response from GitHub API"))
        return

    for item in contents:
        item_path = target_dir / item["name"]

        if item["type"] == "dir":
            # Create directory and recursively download its contents
            item_path.mkdir(parents=True, exist_ok=True)
            download_github_contents(item["url"], item_path)
        elif item["type"] == "file":
            # Download file
            file_response = requests.get(item["download_url"])
            if file_response.status_code == 200:
                item_path.write_bytes(file_response.content)
                click.echo(FeedbackManager.info(message=f"Downloaded {item['path']}"))
            else:
                click.echo(FeedbackManager.warning(message=f"Failed to download {item['path']}"))


def download_github_template(url: str) -> Optional[Path]:
    """
    Downloads a template from a GitHub URL and returns the path to the downloaded files.

    Args:
        url: str - GitHub URL in the format https://github.com/owner/repo/tree/branch/path

    Returns:
        Optional[Path] - Path to the downloaded template or None if download fails
    """
    # Parse GitHub URL components
    # From: https://github.com/owner/repo/tree/branch/path
    parts = url.replace("https://github.com/", "").split("/")
    if len(parts) < 5 or "tree" not in parts:
        click.echo(
            FeedbackManager.error(
                message="Invalid GitHub URL format. Expected: https://github.com/owner/repo/tree/branch/path"
            )
        )
        return None

    owner = parts[0]
    repo = parts[1]
    branch = parts[parts.index("tree") + 1]
    path = "/".join(parts[parts.index("tree") + 2 :])

    try:
        import shutil
        import subprocess
        import tempfile

        # Create a temporary directory for cloning
        with tempfile.TemporaryDirectory() as temp_dir:
            # Clone the specific branch with minimum depth
            repo_url = f"https://github.com/{owner}/{repo}.git"
            subprocess.run(
                ["git", "clone", "--depth", "1", "--branch", branch, repo_url, temp_dir],
                check=True,
                capture_output=True,
            )

            # Copy the specific path to current directory
            source_path = Path(temp_dir) / path
            if not source_path.exists():
                click.echo(FeedbackManager.error(message=f"Path {path} not found in repository"))
                return None

            dir = Path(".")
            if source_path.is_dir():
                # Copy directory contents
                for item in source_path.iterdir():
                    dest = dir / item.name
                    if item.is_dir():
                        shutil.copytree(item, dest)
                    else:
                        shutil.copy2(item, dest)
                    click.echo(FeedbackManager.info(message=f"Downloaded {item.name}"))
            else:
                # Copy single file
                shutil.copy2(source_path, dir / source_path.name)
                click.echo(FeedbackManager.info(message=f"Downloaded {source_path.name}"))

            return dir

    except subprocess.CalledProcessError as e:
        click.echo(FeedbackManager.error(message=f"Git clone failed: {e.stderr.decode()}"))
        return None
    except Exception as e:
        click.echo(FeedbackManager.error(message=f"Error downloading template: {str(e)}"))
        return None


# TODO(eclbg): This should eventually end up in client.py, but we're not using it here yet.
def api_fetch(url: str, headers: dict, request_from: Optional[str] = None) -> dict:
    request_params = {"from": request_from} if request_from and "from=" not in url else None
    r = requests.get(url, headers=headers, params=request_params)
    if r.status_code == 200:
        logging.debug(json.dumps(r.json(), indent=2))
        return r.json()
    # Try to parse and print the error from the response
    try:
        result = r.json()
        error = result.get("error")
        logging.debug(json.dumps(result, indent=2))
        click.echo(FeedbackManager.error(message=f"Error: {error}"))
        sys_exit("deployment_error", error)
    except Exception:
        message = "Error parsing response from API"
        click.echo(FeedbackManager.error(message=message))
        sys_exit("deployment_error", message)
    return {}


def _get_classic_workspace_branches(client: TinyB, workspace_id: str) -> list[dict[str, Any]]:
    branches: list[dict[str, Any]] = client.user_workspace_branches(version="v0").get("workspaces", [])
    return [branch for branch in branches if str(branch.get("main")) == workspace_id]


def _cleanup_classic_migration_blockers(client: TinyB, config: Dict[str, Any]) -> None:
    workspace_id = str(config["id"])

    try:
        branches = _get_classic_workspace_branches(client, workspace_id)
        if not branches:
            return

        for branch in branches:
            client.delete_branch(id=str(branch["id"]))
    except Exception as e:
        message = f"Error cleaning up Classic branches or releases before migration: {str(e)}"
        click.echo(FeedbackManager.error(message=message))
        sys_exit("migration_error", message)


def _persist_migrate_to_forward_config(project: Project) -> None:
    root_folder = os.getcwd()
    project_folder = os.path.relpath(project.path.resolve(), root_folder)

    config_changed, config_created = persist_tinybird_config(
        root_folder=root_folder,
        project_type="cli",
        dev_mode="manual",
        folder=project_folder,
    )

    if not config_changed:
        return

    message = "Created tinybird.config.json for the Forward CLI"
    if not config_created:
        message = "Updated tinybird.config.json for the Forward CLI"
    click.echo(FeedbackManager.info(message=message))


@cli.group(name="deployment")
def deployment_group() -> None:
    """
    Deployment commands.
    """


@deployment_group.command(name="create")
@click.option(
    "--wait/--no-wait",
    is_flag=True,
    default=False,
    help="Wait for deploy to finish. Disabled by default.",
)
@click.option(
    "--auto/--no-auto",
    is_flag=True,
    default=False,
    help="Auto-promote the deployment when it's ready. Disabled by default",
)
@click.option(
    "--check/--no-check",
    is_flag=True,
    default=False,
    help="Validate the deployment before creating it. Disabled by default.",
)
@click.option(
    "--allow-destructive-operations/--no-allow-destructive-operations",
    is_flag=True,
    default=False,
    help="Allow removing datasources. Disabled by default.",
)
@click.option(
    "--template",
    default=None,
    help="URL of the template to use for the deployment. Example: https://github.com/tinybirdco/web-analytics-starter-kit/tree/main/tinybird",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    help="Show verbose output. Disabled by default.",
)
@click.pass_context
def deployment_create(
    ctx: click.Context,
    wait: bool,
    auto: bool,
    check: bool,
    allow_destructive_operations: bool,
    template: Optional[str],
    verbose: bool,
) -> None:
    """
    Deploy your project to your workspace
    """
    create_deployment_cmd(ctx, wait, auto, check, allow_destructive_operations, template, verbose)


@deployment_group.command(name="ls")
@click.option(
    "--include-deleted",
    is_flag=True,
    default=False,
    help="Include deleted deployments. Disabled by default.",
)
@click.pass_context
def deployment_ls(ctx: click.Context, include_deleted: bool) -> None:
    """
    List all the deployments you have in the project.
    """
    client = ctx.ensure_object(dict)["client"]
    output = ctx.ensure_object(dict)["output"]

    TINYBIRD_API_KEY = client.token
    HEADERS = {"Authorization": f"Bearer {TINYBIRD_API_KEY}"}
    url = f"{client.host}/v1/deployments"
    if include_deleted:
        url += "?include_deleted=true"

    result = api_fetch(url, HEADERS, request_from=getattr(client, "request_from", None))
    status_map = {
        "calculating": "Creating - Calculating steps",
        "creating_schema": "Creating - Creating schemas",
        "schema_ready": "Creating - Migrating data",
        "data_ready": "Staging",
        "deleting": "Deleting",
        "deleted": "Deleted",
        "failed": "Failed",
    }
    columns = ["ID", "Status", "Created at"]
    table = []
    for deployment in result.get("deployments", []):
        if deployment.get("id") == "0":
            continue

        table.append(
            [
                deployment.get("id"),
                "Live" if deployment.get("live") else status_map.get(deployment.get("status"), "In progress"),
                datetime.fromisoformat(deployment.get("created_at")).strftime("%Y-%m-%d %H:%M:%S"),
            ]
        )

    table.reverse()

    # Handle different output formats
    if output == "json":
        # Create JSON structure
        deployments_json = [{"id": row[0], "status": row[1], "created_at": row[2]} for row in table]
        from tinybird.tb.modules.common import echo_json

        echo_json({"deployments": deployments_json})
    elif output == "csv":
        # Create CSV output
        csv_output = f"{columns[0]},{columns[1]},{columns[2]}\n"
        for row in table:
            csv_output += f"{row[0]},{row[1]},{row[2]}\n"
        from tinybird.tb.modules.common import force_echo

        force_echo(csv_output)
    else:
        # Default human-readable output
        echo_safe_humanfriendly_tables_format_smart_table(table, column_names=columns)


@deployment_group.command(name="promote")
@click.pass_context
@click.option(
    "--wait/--no-wait",
    is_flag=True,
    default=False,
    help="Wait for deploy to finish. Disabled by default.",
)
def deployment_promote(ctx: click.Context, wait: bool) -> None:
    """
    Promote last deploy to ready and remove old one.
    """
    client = ctx.ensure_object(dict)["client"]

    TINYBIRD_API_KEY = client.token
    HEADERS = {"Authorization": f"Bearer {TINYBIRD_API_KEY}"}

    promote_deployment(client.host, HEADERS, wait=wait, request_from=getattr(client, "request_from", None))


@deployment_group.command(name="discard")
@click.pass_context
@click.option(
    "--wait/--no-wait",
    is_flag=True,
    default=False,
    help="Wait for deploy to finish. Disabled by default.",
)
def deployment_discard(ctx: click.Context, wait: bool) -> None:
    """
    Discard the current deployment.
    """
    client = ctx.ensure_object(dict)["client"]

    TINYBIRD_API_KEY = client.token
    HEADERS = {"Authorization": f"Bearer {TINYBIRD_API_KEY}"}

    discard_deployment(client.host, HEADERS, wait=wait, request_from=getattr(client, "request_from", None))


@cli.command(name="deploy")
@click.option(
    "--wait/--no-wait",
    is_flag=True,
    default=True,
    help="Wait for deploy to finish. Enabled by default.",
)
@click.option(
    "--auto/--no-auto",
    is_flag=True,
    default=True,
    help="Auto-promote the deployment when it's ready. Enabled by default.",
)
@click.option(
    "--check",
    is_flag=True,
    default=False,
    help="Validate the deployment before creating it. Disabled by default.",
)
@click.option(
    "--allow-destructive-operations/--no-allow-destructive-operations",
    is_flag=True,
    default=False,
    help="Allow removing datasources. Disabled by default.",
)
@click.option(
    "--template",
    default=None,
    help="URL of the template to use for the deployment. Example: https://github.com/tinybirdco/web-analytics-starter-kit/tree/main/tinybird",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    help="Show verbose output. Disabled by default.",
)
@click.pass_context
def deploy(
    ctx: click.Context,
    wait: bool,
    auto: bool,
    check: bool,
    allow_destructive_operations: bool,
    template: Optional[str],
    verbose: bool,
) -> None:
    """
    Deploy your project to your workspace. Equivalent to `tb deployment create --auto --wait`
    """
    create_deployment_cmd(ctx, wait, auto, check, allow_destructive_operations, template, verbose)


@cli.command(name="migrate-to-forward")
@click.option(
    "--allow-destructive-operations/--no-allow-destructive-operations",
    is_flag=True,
    default=False,
    help="Allow destructive operations in deployments (for example replacing a Pipe with a Data Source).",
)
@click.pass_context
def migrate_to_forward(ctx: click.Context, allow_destructive_operations: bool) -> None:
    """Migrate a Tinybird Classic cloud workspace to Tinybird Forward."""
    client = ctx.ensure_object(dict)["client"]
    project: Project = ctx.ensure_object(dict)["project"]
    config: Dict[str, Any] = ctx.ensure_object(dict)["config"]
    env = ctx.ensure_object(dict)["env"]
    output = ctx.ensure_object(dict)["output"]

    try:
        client.workspace_info(version="v1")
        message = "This command is unavailable for Tinybird Forward workspaces."
        click.echo(FeedbackManager.error(message=message))
        sys_exit("migration_error", message)
    except Exception:
        pass

    try:
        client.workspace_info(version="v0")
    except Exception as e:
        message = f"Error checking workspace status: {str(e)}"
        click.echo(FeedbackManager.error(message=message))
        sys_exit("migration_error", message)

    click.echo(
        FeedbackManager.warning(
            message=(
                "This operation is irreversible: once your workspace is migrated to Tinybird Forward, "
                "you cannot switch it back to Tinybird Classic. It will also run your first Forward deployment."
            )
        )
    )

    if not click.confirm("Do you want to proceed and run the deployment check now?", default=False):
        click.echo(FeedbackManager.info(message="Migration cancelled."))
        return

    check_result = create_deployment(
        project,
        client,
        config,
        wait=False,
        auto=False,
        verbose=False,
        check=True,
        allow_destructive_operations=allow_destructive_operations,
        output=output,
        env=env,
        show_migrate_to_forward_hint=False,
        return_check_result=True,
        validate_forward_workspace=False,
        is_classic_migration=True,
    )
    if not check_result:
        message = "Deployment check did not complete. Migration cancelled."
        click.echo(FeedbackManager.error(message=message))
        sys_exit("migration_error", message)

    if not click.confirm(
        "Do you want to continue with the migration? This will also delete your branches, releases and switch your workspace from Classic to Forward.",
        default=False,
    ):
        click.echo(FeedbackManager.info(message="Migration cancelled."))
        return

    _cleanup_classic_migration_blockers(client, config)
    _persist_migrate_to_forward_config(project)
    migrate_to_forward_workspace(client=client, output=output, dry_run=False)
    create_deployment(
        project,
        client,
        config,
        wait=True,
        auto=True,
        verbose=False,
        check=False,
        allow_destructive_operations=allow_destructive_operations,
        output=output,
        env=env,
        validate_forward_workspace=False,
        is_classic_migration=True,
    )


def create_deployment_cmd(
    ctx: click.Context,
    wait: bool,
    auto: bool,
    check: Optional[bool] = None,
    allow_destructive_operations: Optional[bool] = None,
    template: Optional[str] = None,
    verbose: bool = False,
) -> None:
    output = ctx.ensure_object(dict)["output"]
    env = ctx.ensure_object(dict)["env"]
    project: Project = ctx.ensure_object(dict)["project"]
    if template:
        if project.get_project_files():
            click.echo(
                FeedbackManager.error(
                    message="You are trying to deploy a template from a folder that already contains data files. "
                    "Please remove the data files from the current folder or use a different folder and try again."
                )
            )
            sys_exit(
                "deployment_error",
                "Deployment using a template is not allowed when the project already contains data files",
            )

        click.echo(FeedbackManager.info(message="» Downloading template..."))
        try:
            download_github_template(template)
        except Exception as e:
            click.echo(FeedbackManager.error(message=f"Error downloading template: {str(e)}"))
            sys_exit("deployment_error", f"Failed to download template {template}")
        click.echo(FeedbackManager.success(message="Template downloaded successfully"))
    client = ctx.ensure_object(dict)["client"]
    config: Dict[str, Any] = ctx.ensure_object(dict)["config"]
    is_web_analytics_starter_kit = bool(template and "web-analytics-starter-kit" in template)
    create_deployment(
        project,
        client,
        config,
        wait,
        auto,
        verbose,
        check,
        allow_destructive_operations,
        ingest_hint=not is_web_analytics_starter_kit,
        output=output,
        env=env,
    )
    show_web_analytics_starter_kit_hints(client, is_web_analytics_starter_kit)


def show_web_analytics_starter_kit_hints(client, is_web_analytics_starter_kit: bool) -> None:
    try:
        if not is_web_analytics_starter_kit:
            return

        from tinybird.tb.modules.cli import __unpatch_click_output

        __unpatch_click_output()
        tokens = client.tokens()
        tracker_token = next((token for token in tokens if token["name"] == "tracker"), None)
        if tracker_token:
            click.echo(FeedbackManager.highlight(message="» Ingest data using the script below:"))
            click.echo(
                FeedbackManager.info(
                    message=f"""
<script
defer
src="https://unpkg.com/@tinybirdco/flock.js"
data-token="{tracker_token["token"]}"
data-host="{client.host}"
></script>
            """
                )
            )

        try:
            ttl = timedelta(days=365 * 10)
            expiration_time = int((ttl + datetime.now(timezone.utc)).timestamp())
            datasources = client.datasources()
            pipes = client.pipes()

            scopes = []
            for res in pipes:
                scope_data = {
                    "type": "PIPES:READ",
                    "resource": res["name"],
                }

                scopes.append(scope_data)

            for res in datasources:
                scope_data = {
                    "type": "DATASOURCES:READ",
                    "resource": res["name"],
                }

                scopes.append(scope_data)

            response = client.create_jwt_token("web_analytics_starter_kit_jwt", expiration_time, scopes)
            click.echo(FeedbackManager.highlight(message="» Open this URL in your browser to see the dashboard:\n"))
            click.echo(
                FeedbackManager.info(
                    message=f"https://analytics.tinybird.co?token={response['token']}&host={client.host}"
                )
            )
        except Exception:
            dashboard_token = next((token for token in tokens if token["name"] == "dashboard"), None)
            if dashboard_token:
                click.echo(FeedbackManager.highlight(message="» Open this URL in your browser to see the dashboard:\n"))
                click.echo(
                    FeedbackManager.info(
                        message=f"https://analytics.tinybird.co?token={dashboard_token['token']}&host={client.host}"
                    )
                )
    except Exception:
        pass
