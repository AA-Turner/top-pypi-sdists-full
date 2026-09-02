from pathlib import Path
from enum import Enum
from typing import Annotated

import typer

from runlayer_cli.api import RunlayerClient
from runlayer_cli.config import resolve_credentials, set_credentials_in_context
from runlayer_cli.terraform_export import (
    build_export_sections,
    list_groups_for_terraform,
    list_roles_for_terraform,
    list_users_for_terraform,
    render_tfvars,
)

app = typer.Typer(help="Export Terraform inputs for Runlayer resources")
_DEFAULT_OUTPUT_PATH = Path("runlayer.auto.tfvars")


class TerraformSection(str, Enum):
    USERS = "users"
    GROUPS = "groups"
    ROLES = "roles"


@app.callback(invoke_without_command=True)
def terraform_callback(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


@app.command("export")
def export(
    ctx: typer.Context,
    output: Annotated[
        Path,
        typer.Option(
            "--output",
            "-o",
            help="Path to write the generated tfvars file",
        ),
    ] = _DEFAULT_OUTPUT_PATH,
    only: Annotated[
        list[TerraformSection],
        typer.Option(
            "--only",
            help="Section to export: users, groups, roles. Repeat to filter.",
        ),
    ] = [],
    secret: str | None = typer.Option(
        None,
        "--secret",
        "-s",
        help="API secret for authentication (optional if logged in)",
    ),
    host: str | None = typer.Option(
        None,
        "--host",
        "-H",
        help="Runlayer host URL (required if not in config)",
    ),
    org_api_key: str | None = typer.Option(
        None,
        "--org-api-key",
        help="Name of a stored org API key to use for authentication",
    ),
) -> None:
    set_credentials_in_context(ctx, secret, host, org_api_key_name=org_api_key)
    credentials = resolve_credentials(ctx, require_auth=True)
    client = RunlayerClient(
        hostname=credentials["host"],
        secret=credentials["secret"],
    )

    selected_sections = tuple(
        dict.fromkeys(
            section.value
            for section in (
                only
                or [
                    TerraformSection.USERS,
                    TerraformSection.GROUPS,
                    TerraformSection.ROLES,
                ]
            )
        )
    )

    users = list_users_for_terraform(client) if "users" in selected_sections else []
    groups = list_groups_for_terraform(client) if "groups" in selected_sections else []
    roles = list_roles_for_terraform(client) if "roles" in selected_sections else []

    rendered = render_tfvars(
        build_export_sections(
            users=users,
            groups=groups,
            roles=roles,
            selected_sections=selected_sections,
        )
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered)
    typer.echo(f"Exported {', '.join(selected_sections)} to {output}")
