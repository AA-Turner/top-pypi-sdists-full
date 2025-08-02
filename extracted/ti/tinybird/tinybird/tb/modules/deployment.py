import json
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Optional

import click
import requests

from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import (
    echo_safe_humanfriendly_tables_format_smart_table,
    sys_exit,
)
from tinybird.tb.modules.deployment_common import (
    create_deployment,
    discard_deployment,
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
def api_fetch(url: str, headers: dict) -> dict:
    r = requests.get(url, headers=headers)
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


@cli.group(name="deployment")
def deployment_group() -> None:
    """
    Deployment commands.
    """
    pass


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
    help="Auto-promote the deployment. Only works if --wait is enabled. Disabled by default.",
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
    Validate and deploy the project server side.
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

    result = api_fetch(url, HEADERS)
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
        deployments_json = []
        for row in table:
            deployments_json.append({"id": row[0], "status": row[1], "created_at": row[2]})
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

    promote_deployment(client.host, HEADERS, wait=wait)


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

    discard_deployment(client.host, HEADERS, wait=wait)


@cli.command(name="deploy")
@click.option(
    "--wait/--no-wait",
    is_flag=True,
    default=True,
    help="Wait for deploy to finish. Disabled by default.",
)
@click.option(
    "--auto/--no-auto",
    is_flag=True,
    default=True,
    help="Auto-promote or auto-discard the deployment. Only works if --wait is enabled. Disabled by default.",
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
    Deploy the project.
    """
    create_deployment_cmd(ctx, wait, auto, check, allow_destructive_operations, template, verbose)


def create_deployment_cmd(
    ctx: click.Context,
    wait: bool,
    auto: bool,
    check: Optional[bool] = None,
    allow_destructive_operations: Optional[bool] = None,
    template: Optional[str] = None,
    verbose: bool = False,
) -> None:
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
