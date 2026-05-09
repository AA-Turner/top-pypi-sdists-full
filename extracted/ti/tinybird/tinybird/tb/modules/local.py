import json
import uuid
from pathlib import Path
from typing import Any

import click
import jwt
import requests
from docker.client import DockerClient

from tinybird.tb.client import AuthNoTokenException
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import (
    _get_workspace_plan_name,
    echo_json,
    echo_safe_humanfriendly_tables_format_smart_table,
    update_cli,
)
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.exceptions import CLILocalException
from tinybird.tb.modules.feedback_manager import FeedbackManager, get_cli_name
from tinybird.tb.modules.info import get_local_info
from tinybird.tb.modules.local_common import (
    TB_CONTAINER_NAME,
    TB_LOCAL_ADDRESS,
    get_docker_client,
    get_existing_container_with_matching_env,
    get_local_tokens,
    start_tinybird_local,
)
from tinybird.tb.modules.local_logs import (
    check_memory_sufficient,
    clickhouse_is_ready,
    container_is_ready,
    container_is_starting,
    container_is_stopping,
    container_is_unhealthy,
    container_stats,
    events_is_ready,
    local_authentication_is_ready,
    redis_is_ready,
    server_is_ready,
)


def _get_local_project_config() -> CLIConfig:
    return CLIConfig.get_project_config()


def stop_tinybird_local(docker_client: DockerClient) -> None:
    """Stop the Tinybird container."""
    try:
        container = docker_client.containers.get(TB_CONTAINER_NAME)
        container.stop()
    except Exception:
        pass


def remove_tinybird_local(docker_client: DockerClient, persist_data: bool) -> None:
    """Remove the Tinybird container."""
    try:
        container = docker_client.containers.get(TB_CONTAINER_NAME)
        if persist_data or click.confirm(
            FeedbackManager.warning(
                message="△ This step will remove all your data inside Tinybird Local. Are you sure? [y/N]:"
            ),
            show_default=False,
            prompt_suffix="",
        ):
            container.remove(force=True)
    except Exception:
        pass


def clear_local_workspace() -> None:
    """Clear current local workspace by deleting and recreating it."""
    config = _get_local_project_config()
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
        raise CLILocalException(FeedbackManager.error(message=f"Workspace '{ws_name}' not found."))

    requests.delete(f"{TB_LOCAL_ADDRESS}/v1/workspaces/{ws['id']}?token={user_token}&hard_delete_confirmation=yes")
    user_workspaces = user_client.user_workspaces(version="v1")
    ws = next((ws for ws in user_workspaces["workspaces"] if ws["name"] == ws_name), None)

    if ws:
        raise CLILocalException(
            FeedbackManager.error(message=f"Workspace '{ws_name}' was not cleared properly. Please try again.")
        )

    user_client.create_workspace(ws_name, assign_to_organization_id=user_org_id, version="v1")
    user_workspaces = requests.get(f"{TB_LOCAL_ADDRESS}/v1/user/workspaces?token={admin_token}").json()
    ws = next((ws for ws in user_workspaces["workspaces"] if ws["name"] == ws_name), None)

    if not ws:
        raise CLILocalException(
            FeedbackManager.error(message=f"Workspace '{ws_name}' was not cleared properly. Please try again.")
        )

    click.echo(FeedbackManager.success(message=f"✓ Workspace '{ws_name}' cleared"))


@cli.command()
def update() -> None:
    """Update Tinybird CLI to the latest version."""
    update_cli()


@cli.command(name="upgrade", hidden=True)
def upgrade() -> None:
    """Update Tinybird CLI to the latest version."""
    update_cli()


@cli.group()
@click.pass_context
def local(ctx: click.Context) -> None:
    """Manage the local Tinybird instance."""


@local.command()
def stop() -> None:
    """Stop Tinybird Local"""
    click.echo(FeedbackManager.highlight(message="» Shutting down Tinybird Local..."))
    docker_client = get_docker_client()
    stop_tinybird_local(docker_client)
    click.echo(FeedbackManager.success(message="✓ Tinybird Local stopped."))


@local.command(name="ls")
def local_ls() -> None:
    """List all Tinybird Local workspaces you have access to."""
    config = _get_local_project_config()
    tokens = get_local_tokens()
    local_client = config.get_client(host=TB_LOCAL_ADDRESS, token=tokens["user_token"])

    response = local_client.user_workspaces(version="v1")

    columns = ["name", "id", "role", "plan", "current"]
    current_workspace_name = config.get("name")
    click.echo(FeedbackManager.info_workspaces())

    table = [
        [
            workspace.get("name", ""),
            workspace.get("id", ""),
            workspace.get("role", ""),
            _get_workspace_plan_name(workspace.get("plan")),
            current_workspace_name == workspace.get("name"),
        ]
        for workspace in response.get("workspaces", [])
    ]

    echo_safe_humanfriendly_tables_format_smart_table(table, column_names=columns)


@local.command()
@click.pass_context
def status(ctx: click.Context) -> None:
    """Check status of Tinybird Local"""

    click.echo(FeedbackManager.highlight(message="» Checking status..."))
    docker_client = get_docker_client()
    container = get_existing_container_with_matching_env(docker_client, TB_CONTAINER_NAME, {})

    try:
        if container:
            if container_is_ready(container):
                stats = container_stats(container, docker_client)
                click.echo(FeedbackManager.info(message=f"✓ Tinybird Local container ({stats})"))

                # Check memory sufficiency
                is_sufficient, warning_msg = check_memory_sufficient(container, docker_client)
                if not is_sufficient and warning_msg:
                    click.echo(FeedbackManager.warning(message=f"△ {warning_msg}"))

                if not clickhouse_is_ready(container):
                    raise Exception("Clickhouse is not ready.")
                click.echo(FeedbackManager.info(message="✓ Clickhouse"))

                if not redis_is_ready(container):
                    raise Exception("Redis is not ready.")
                click.echo(FeedbackManager.info(message="✓ Redis"))

                if not server_is_ready(container):
                    raise Exception("Server is not ready.")
                click.echo(FeedbackManager.info(message="✓ Server"))

                if not events_is_ready(container):
                    raise Exception("Events is not ready.")
                click.echo(FeedbackManager.info(message="✓ Events"))

                if not local_authentication_is_ready(container):
                    raise Exception("Tinybird Local authentication is not ready.")
                click.echo(FeedbackManager.info(message="✓ Tinybird Local authentication"))

                click.echo(FeedbackManager.success(message="✓ Tinybird Local is ready!"))
                click.echo(FeedbackManager.highlight(message="\n» Tinybird Local:"))
                config = ctx.ensure_object(dict).get("config", {})
                get_local_info(config)
            elif container_is_starting(container):
                click.echo(FeedbackManager.highlight(message="* Tinybird Local is starting..."))
            elif container_is_stopping(container):
                click.echo(FeedbackManager.highlight(message="* Tinybird Local is stopping..."))
            elif container_is_unhealthy(container):
                is_sufficient, warning_msg = check_memory_sufficient(container, docker_client)
                if not is_sufficient and warning_msg:
                    click.echo(FeedbackManager.warning(message=f"△ {warning_msg}"))
                click.echo(
                    FeedbackManager.error(
                        message=f"* Tinybird Local is unhealthy. Try running `{get_cli_name()} local restart` in a few seconds."
                    )
                )
            else:
                click.echo(
                    FeedbackManager.error(
                        message=f"✗ Tinybird Local is not running. Run '{get_cli_name()} local start' to start it"
                    )
                )
        else:
            click.echo(
                FeedbackManager.error(
                    message=f"✗ Tinybird Local is not running. Run '{get_cli_name()} local start' to start it"
                )
            )
    except Exception as e:
        raise CLILocalException(FeedbackManager.error(message=f"Tinybird Local is not ready. Reason: {e}"))


@local.command()
def remove() -> None:
    """Remove Tinybird Local"""
    click.echo(FeedbackManager.highlight(message="» Removing Tinybird Local..."))
    docker_client = get_docker_client()
    remove_tinybird_local(docker_client, persist_data=False)
    click.echo(FeedbackManager.success(message="✓ Tinybird Local removed"))


@local.command()
@click.option(
    "--use-aws-creds",
    default=False,
    is_flag=True,
    help="Use local AWS credentials from your environment and pass them to the Tinybird docker container",
)
@click.option(
    "--volumes-path",
    default=None,
    help="Path to the volumes directory. If not provided, the container data won't be persisted.",
)
@click.option(
    "--skip-new-version",
    default=False,
    is_flag=True,
    help="Skip pulling the latest Tinybird Local image. Use directly your current local image.",
)
@click.option(
    "--user-token",
    default=None,
    envvar="TB_LOCAL_USER_TOKEN",
    help="User token to use for the Tinybird Local container.",
)
@click.option(
    "--workspace-token",
    default=None,
    envvar="TB_LOCAL_WORKSPACE_TOKEN",
    help="Workspace token to use for the Tinybird Local container.",
)
@click.option(
    "--daemon/--watch",
    "-d/-w",
    default=False,
    is_flag=True,
    help="Run Tinybird Local in the background.",
)
def start(
    use_aws_creds: bool,
    volumes_path: str,
    skip_new_version: bool,
    user_token: str,
    workspace_token: str,
    daemon: bool,
) -> None:
    """Start Tinybird Local"""
    if volumes_path is not None:
        absolute_path = Path(volumes_path).absolute()
        absolute_path.mkdir(parents=True, exist_ok=True)
        volumes_path = str(absolute_path)

    click.echo(FeedbackManager.highlight(message="» Starting Tinybird Local..."))
    docker_client = get_docker_client()
    watch = not daemon
    start_tinybird_local(
        docker_client, use_aws_creds, volumes_path, skip_new_version, user_token, workspace_token, watch=watch
    )
    if daemon:
        click.echo(FeedbackManager.success(message="✓ Tinybird Local is ready!"))


@local.command()
@click.option(
    "--use-aws-creds",
    default=False,
    is_flag=True,
    help="Use local AWS credentials from your environment and pass them to the Tinybird docker container",
)
@click.option(
    "--volumes-path",
    default=None,
    help="Path to the volumes directory. If not provided, the container data won't be persisted.",
)
@click.option(
    "--skip-new-version",
    default=False,
    is_flag=True,
    help="Skip pulling the latest Tinybird Local image. Use directly your current local image.",
)
@click.option(
    "--yes",
    default=False,
    is_flag=True,
    help="Skip the confirmation prompt. If provided, the container will be restarted without asking for confirmation.",
)
def restart(use_aws_creds: bool, volumes_path: str, skip_new_version: bool, yes: bool) -> None:
    """Restart Tinybird Local"""
    if volumes_path is not None:
        absolute_path = Path(volumes_path).absolute()
        absolute_path.mkdir(parents=True, exist_ok=True)
        volumes_path = str(absolute_path)

    click.echo(FeedbackManager.highlight(message="» Restarting Tinybird Local..."))
    docker_client = get_docker_client()
    persist_data = volumes_path is not None or yes
    remove_tinybird_local(docker_client, persist_data)
    click.echo(FeedbackManager.info(message="✓ Tinybird Local stopped"))
    start_tinybird_local(docker_client, use_aws_creds, volumes_path, skip_new_version)
    click.echo(FeedbackManager.success(message="✓ Tinybird Local is ready!"))


@local.command(
    name="clear",
    short_help="Clear all resources and deployments inside the current Tinybird Local workspace.",
)
@click.option("--yes", is_flag=True, default=False, help="Don't ask for confirmation")
def clear(yes: bool) -> None:
    """Clear current local workspace."""
    confirmed = yes or click.confirm(
        FeedbackManager.warning(message="Are you sure you want to clear the workspace? [y/N]:"),
        show_default=False,
        prompt_suffix="",
    )
    if confirmed:
        clear_local_workspace()


@local.command()
def version() -> None:
    """Show Tinybird Local version"""
    response = requests.get(f"{TB_LOCAL_ADDRESS}/version")
    click.echo(FeedbackManager.success(message=f"✓ Tinybird Local version: {response.text}"))


@local.command()
@click.pass_context
def generate_tokens(ctx: click.Context) -> None:
    """Generate static tokens for initializing Tinybird Local"""
    output = ctx.ensure_object(dict).get("output")
    user_id = str(uuid.uuid4())
    workspace_id = str(uuid.uuid4())
    user_token_id = str(uuid.uuid4())
    workspace_token_id = str(uuid.uuid4())
    payload = {"u": user_id, "id": user_token_id, "host": None}
    user_token = generate_token(payload)
    payload = {"u": workspace_id, "id": workspace_token_id, "host": None}
    workspace_token = generate_token(payload)

    if output == "json":
        echo_json({"workspace_token": workspace_token, "user_token": user_token})
    else:
        click.echo(FeedbackManager.gray(message="Workspace token: ") + FeedbackManager.info(message=workspace_token))
        click.echo(FeedbackManager.gray(message="User token: ") + FeedbackManager.info(message=user_token))
        click.echo(FeedbackManager.success(message="✓ Tinybird Local tokens generated!"))


def generate_token(payload: dict[str, Any]) -> str:
    algo = jwt.algorithms.get_default_algorithms()["HS256"]
    msg = json.dumps(payload)
    msg_base64 = jwt.utils.base64url_encode(msg.encode())
    sign_key = algo.prepare_key("abcd")
    signature = algo.sign(msg_base64, sign_key)
    token = msg_base64 + b"." + jwt.utils.base64url_encode(signature)
    return "p." + token.decode()
