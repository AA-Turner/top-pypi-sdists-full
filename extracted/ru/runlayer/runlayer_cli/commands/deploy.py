"""Deploy command group for Runlayer CLI."""

import typer
from typing import Optional

from runlayer_cli.config import resolve_credentials, set_credentials_in_context
from runlayer_cli.deploy import (
    deploy_service,
    init_deployment_config,
    destroy_deployment,
    validate_service,
    pull_deployment,
)

app = typer.Typer(help="Deploy services to Runlayer infrastructure")


@app.callback(invoke_without_command=True)
def deploy_callback(
    ctx: typer.Context,
    config_path: str = typer.Option(
        "runlayer.yaml", "--config", "-c", help="Path to runlayer.yaml config file"
    ),
    secret: Optional[str] = typer.Option(
        None, "--secret", "-s", help="API secret for authentication"
    ),
    host: Optional[str] = typer.Option(
        None, "--host", "-H", help="Runlayer host URL (required if not in config)"
    ),
    env_file: Optional[str] = typer.Option(
        None,
        "--env-file",
        "-e",
        help="Path to .env file for environment variable substitution",
    ),
):
    """
    Deploy a service based on runlayer.yaml configuration.

    This command will:
    1. Load and validate the configuration
    2. Create or update the deployment
    3. Build the Docker image (if build mode) OR use provided image (if image mode)
    4. Push the image to ECR (if build mode)
    5. Trigger the deployment
    """
    if ctx.invoked_subcommand is not None:
        return

    set_credentials_in_context(ctx, secret, host)
    credentials = resolve_credentials(ctx, allow_org_key=True)

    deploy_service(
        config_path=config_path,
        secret=credentials["secret"],
        host=credentials["host"],
        env_file=env_file,
    )


@app.command(name="init", help="Initialize a new deployment configuration")
def init(
    ctx: typer.Context,
    config_path: str = typer.Option(
        "runlayer.yaml",
        "--config",
        "-c",
        help="Path to create runlayer.yaml config file",
    ),
    secret: Optional[str] = typer.Option(
        None, "--secret", "-s", help="API secret for authentication"
    ),
    host: Optional[str] = typer.Option(
        None, "--host", "-H", help="Runlayer host URL (required if not in config)"
    ),
):
    """Initialize a new deployment and create runlayer.yaml configuration file."""
    set_credentials_in_context(ctx, secret, host)
    credentials = resolve_credentials(ctx, allow_org_key=True)

    name = typer.prompt("Enter deployment name (lowercase, URL-friendly)")
    init_deployment_config(
        name=name,
        config_path=config_path,
        secret=credentials["secret"],
        host=credentials["host"],
    )


@app.command(name="validate", help="Validate runlayer.yaml configuration")
def validate(
    ctx: typer.Context,
    config_path: str = typer.Option(
        "runlayer.yaml",
        "--config",
        "-c",
        help="Path to runlayer.yaml config file",
    ),
    secret: Optional[str] = typer.Option(
        None, "--secret", "-s", help="API secret for authentication"
    ),
    host: Optional[str] = typer.Option(
        None, "--host", "-H", help="Runlayer host URL (required if not in config)"
    ),
    env_file: Optional[str] = typer.Option(
        None,
        "--env-file",
        "-e",
        help="Path to .env file for environment variable substitution",
    ),
):
    """
    Validate runlayer.yaml configuration without deploying.

    This command validates the configuration file by checking:
    - YAML syntax correctness
    - Required fields and structure
    - Configuration values against backend schema

    No deployment is created or modified. Use this to check your
    configuration before running the full deploy command.
    """
    set_credentials_in_context(ctx, secret, host)
    credentials = resolve_credentials(ctx, allow_org_key=True)

    validate_service(
        config_path=config_path,
        secret=credentials["secret"],
        host=credentials["host"],
        env_file=env_file,
    )


@app.command(name="destroy", help="Destroy a deployment and its infrastructure")
def destroy(
    ctx: typer.Context,
    config_path: str = typer.Option(
        "runlayer.yaml",
        "--config",
        "-c",
        help="Path to runlayer.yaml config file (contains deployment ID)",
    ),
    deployment_id: Optional[str] = typer.Option(
        None,
        "--deployment-id",
        "-d",
        help="Deployment ID to destroy (overrides config file)",
    ),
    secret: Optional[str] = typer.Option(
        None, "--secret", "-s", help="API secret for authentication"
    ),
    host: Optional[str] = typer.Option(
        None, "--host", "-H", help="Runlayer host URL (required if not in config)"
    ),
):
    """
    Destroy a deployment and tear down its infrastructure.

    This command will:
    1. Load the deployment ID from config or use provided ID
    2. Confirm the destruction with the user
    3. Trigger infrastructure teardown via the backend
    4. Queue the deletion process

    You can specify the deployment either by:
    - Using --config to read the ID from runlayer.yaml (default)
    - Using --deployment-id to specify the ID directly
    """
    set_credentials_in_context(ctx, secret, host)
    credentials = resolve_credentials(ctx, allow_org_key=True)

    destroy_deployment(
        config_path=config_path,
        secret=credentials["secret"],
        host=credentials["host"],
        deployment_id=deployment_id,
    )


@app.command(name="pull", help="Pull deployment configuration from backend")
def pull(
    ctx: typer.Context,
    config_path: str = typer.Option(
        "runlayer.yaml",
        "--config",
        "-c",
        help="Path to save runlayer.yaml config file",
    ),
    deployment_id: Optional[str] = typer.Option(
        None,
        "--deployment-id",
        "-d",
        help="Deployment ID to pull (overrides config file)",
    ),
    secret: Optional[str] = typer.Option(
        None, "--secret", "-s", help="API secret for authentication"
    ),
    host: Optional[str] = typer.Option(
        None, "--host", "-H", help="Runlayer host URL (required if not in config)"
    ),
):
    """
    Pull deployment configuration from the backend and save as YAML.

    This command will:
    1. Fetch the deployment configuration from the backend
    2. Create a backup of existing runlayer.yaml (if present)
    3. Save the configuration to the specified file

    Environment variables are shown as ${VAR_NAME} placeholders.
    System variables (like $$DEPLOYMENT_URL) are preserved as-is.

    You can specify the deployment either by:
    - Using --config to read the ID from an existing runlayer.yaml
    - Using --deployment-id to specify the ID directly
    """
    set_credentials_in_context(ctx, secret, host)
    credentials = resolve_credentials(ctx, allow_org_key=True)

    pull_deployment(
        config_path=config_path,
        secret=credentials["secret"],
        host=credentials["host"],
        deployment_id=deployment_id,
    )
