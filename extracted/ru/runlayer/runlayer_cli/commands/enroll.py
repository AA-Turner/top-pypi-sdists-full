"""``aiwatch enroll`` typer command (idempotent; exits 0 ok, 1 endpoint, 2 missing input)."""

from __future__ import annotations

from typing import Optional

import typer

from runlayer_cli.config import load_config, save_config
from runlayer_cli.enrollment import (
    EnrollmentError,
    exchange_enrollment_key,
    resolve_enrollment_key,
    resolve_host,
    resolve_mdm_device_name,
    resolve_mdm_username,
    write_enrollment_marker,
)


def enroll(
    enrollment_key: Optional[str] = typer.Option(
        None,
        "--enrollment-key",
        "-k",
        envvar="RUNLAYER_ENROLLMENT_API_KEY",
        help="Enrollment API key (rl_enroll_...); falls back to MDM EnrollmentKey.",
    ),
    host: Optional[str] = typer.Option(
        None,
        "--host",
        "-H",
        envvar="RUNLAYER_HOST",
        help="Runlayer host URL; falls back to MDM Host.",
    ),
    username: Optional[str] = typer.Option(
        None,
        "--username",
        envvar="ENROLLMENT_USERNAME",
        help="Username to enroll; falls back to MDM Username (server resolves OS user when empty).",
    ),
    device_name: Optional[str] = typer.Option(
        None,
        "--device-name",
        envvar="ENROLLMENT_DEVICE_NAME",
        help="Device name to enroll; falls back to MDM DeviceName.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Re-enroll even when a credential already exists for the host.",
    ),
) -> None:
    """Enroll this device against an MDM-pushed enrollment key (idempotent unless ``--force``)."""
    resolved_host = resolve_host(host)
    if not resolved_host:
        typer.secho(
            "Error: no host configured (pass --host, set RUNLAYER_HOST, or push "
            "MDM Host).",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(2)

    config = load_config()
    existing = config.get_secret_for_host(resolved_host)
    if existing and not force:
        # Self-migration: pre-marker-file enrollments only have a YAML host entry;
        # refresh the marker so the bootstrap gate sees this user as enrolled.
        write_enrollment_marker(resolved_host)
        typer.secho(
            f"Already enrolled for {resolved_host}; pass --force to re-enroll.",
            fg=typer.colors.GREEN,
            err=True,
        )
        raise typer.Exit(0)

    resolved_key = resolve_enrollment_key(enrollment_key)
    if not resolved_key:
        typer.secho(
            "Error: no enrollment key (pass --enrollment-key, set "
            "RUNLAYER_ENROLLMENT_API_KEY, or push MDM EnrollmentKey).",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(2)

    try:
        result = exchange_enrollment_key(
            host=resolved_host,
            enrollment_key=resolved_key,
            username=resolve_mdm_username(username),
            device_name=resolve_mdm_device_name(device_name),
        )
    except EnrollmentError as exc:
        typer.secho(f"Error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1) from None

    config = load_config()
    keyring_used = config.set_host_credentials(resolved_host, result.api_key)
    save_config(config)
    write_enrollment_marker(resolved_host)
    dest = "credential store" if keyring_used else "config file"
    typer.secho(
        f"Enrollment successful. API key saved to {dest} for {resolved_host}.",
        fg=typer.colors.GREEN,
        err=True,
    )
