"""Hidden credentials commands for MDM provisioning."""

from typing import Optional

import typer

from runlayer_cli.config import load_config, resolve_host, save_config
from runlayer_cli.enrollment import (
    EnrollmentError,
    exchange_enrollment_key,
    write_enrollment_marker,
)

app = typer.Typer(hidden=True)
add_app = typer.Typer(help="Add a credential")
app.add_typer(add_app, name="add")


@app.callback(invoke_without_command=True)
def credentials_callback(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


@add_app.callback(invoke_without_command=True)
def add_callback(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


@add_app.command(name="org")
def add_org(
    ctx: typer.Context,
    label: str = typer.Argument(..., help="Label for this org API key"),
    secret: str = typer.Option(
        ...,
        "--secret",
        "-s",
        envvar="RUNLAYER_ORG_API_KEY",
        help="The org API key value (rl_org_...)",
    ),
    host: Optional[str] = typer.Option(
        None,
        "--host",
        "-H",
        help="Host to store the key for (defaults to current host)",
    ),
) -> None:
    """Store a named org API key for a host."""
    config = load_config()
    effective_host = resolve_host(ctx, host, config.default_host)
    try:
        config.set_org_api_key(effective_host, label, secret)
    except ValueError as exc:
        typer.secho(f"Error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1) from None
    save_config(config)
    typer.secho(
        f"Org API key '{label}' saved for {effective_host}.",
        fg=typer.colors.GREEN,
        err=True,
    )


@add_app.command(name="user")
def add_user(
    ctx: typer.Context,
    secret: str = typer.Option(
        ...,
        "--secret",
        "-s",
        envvar="RUNLAYER_API_KEY",
        help="User API key",
    ),
    host: Optional[str] = typer.Option(
        None,
        "--host",
        "-H",
        help="Host to store the key for (defaults to current host)",
    ),
) -> None:
    """Store a user API key for a host (keyring when available)."""
    config = load_config()
    effective_host = resolve_host(ctx, host, config.default_host)
    keyring_used = config.set_host_credentials(effective_host, secret)
    save_config(config)
    dest = "credential store" if keyring_used else "config file"
    typer.secho(
        f"User API key saved to {dest} for {effective_host}.",
        fg=typer.colors.GREEN,
        err=True,
    )


@app.command()
def enroll(
    ctx: typer.Context,
    enrollment_key: str = typer.Argument(
        ...,
        envvar="RUNLAYER_ENROLLMENT_API_KEY",
        help="Enrollment API key (rl_enroll_...)",
    ),
    host: Optional[str] = typer.Option(
        None,
        "--host",
        "-H",
        envvar="RUNLAYER_HOST",
        help="Runlayer host URL",
    ),
    username: Optional[str] = typer.Option(
        None,
        "--username",
        envvar="ENROLLMENT_USERNAME",
        help="Username to enroll (defaults to OS user on server side)",
    ),
    device_name: Optional[str] = typer.Option(
        None,
        "--device-name",
        envvar="ENROLLMENT_DEVICE_NAME",
        help="Device name for enrollment",
    ),
) -> None:
    """Enroll a device and store the returned user API key."""
    config = load_config()
    effective_host = resolve_host(ctx, host, config.default_host)

    try:
        result = exchange_enrollment_key(
            host=effective_host,
            enrollment_key=enrollment_key,
            username=username,
            device_name=device_name,
        )
    except EnrollmentError as exc:
        typer.secho(f"Error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1 if exc.status_code is not None else 2) from None

    config = load_config()
    keyring_used = config.set_host_credentials(effective_host, result.api_key)
    save_config(config)
    write_enrollment_marker(effective_host)
    dest = "credential store" if keyring_used else "config file"
    typer.secho(
        f"Enrollment successful. API key saved to {dest} for {effective_host}.",
        fg=typer.colors.GREEN,
        err=True,
    )


@app.command()
def check(
    ctx: typer.Context,
    host: Optional[str] = typer.Option(
        None,
        "--host",
        "-H",
        envvar="RUNLAYER_HOST",
        help="Host to check credentials for",
    ),
    org_api_key: Optional[str] = typer.Option(
        None,
        "--org-api-key",
        envvar="RUNLAYER_ORG_API_KEY_NAME",
        help="Named org API key label to verify",
    ),
    skip_org_check: bool = typer.Option(
        False,
        "--skip-org-check",
        help="Skip the org API key check",
    ),
    skip_user_check: bool = typer.Option(
        False,
        "--skip-user-check",
        help="Skip the user API key check",
    ),
) -> None:
    """Check whether credentials are provisioned for a host."""
    config = load_config()
    effective_host = resolve_host(ctx, host, config.default_host)
    ok = True

    if not skip_user_check:
        if config.get_secret_for_host(effective_host):
            typer.echo("user: ok", err=True)
        else:
            typer.secho("user: missing", fg=typer.colors.RED, err=True)
            ok = False

    if not skip_org_check:
        if not org_api_key:
            typer.secho(
                "Error: --org-api-key is required when org check is enabled.",
                fg=typer.colors.RED,
                err=True,
            )
            raise typer.Exit(1)
        if config.get_org_api_key(effective_host, org_api_key):
            typer.echo(f"org ({org_api_key}): ok", err=True)
        else:
            typer.secho(
                f"org ({org_api_key}): missing",
                fg=typer.colors.RED,
                err=True,
            )
            ok = False

    if not ok:
        raise typer.Exit(1)
