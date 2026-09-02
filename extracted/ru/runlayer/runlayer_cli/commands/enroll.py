"""``aiwatch enroll`` typer command (idempotent; exits 0 ok or no-key non-interactive no-op, 1 endpoint, 2 missing input)."""

from __future__ import annotations

import sys
from typing import Optional

import structlog
import typer

from runlayer_cli.cli_persistence import (
    complete_device_enrollment,
    credential_dest,
)
from runlayer_cli.config import load_config
from runlayer_cli.enrollment import (
    EnrollmentError,
    exchange_enrollment_key,
    resolve_enrollment_key,
    resolve_host,
    resolve_mdm_device_name,
    resolve_mdm_username,
    write_enrollment_marker,
)

logger = structlog.get_logger(__name__)


def _operator_is_watching() -> bool:
    """True when run interactively (a human at a terminal), False under launchd.

    Manual ``aiwatch enroll`` in a terminal has a TTY on stderr; the packaged
    enroll LaunchAgent (and any non-interactive / scripted invocation) does not.
    Gates whether a missing-enrollment-key configuration surfaces as an error
    (exit 2) or is silently skipped (exit 0): launchd must stay silent so
    org-key-only / unconfigured fleets don't log spurious failures, while an
    operator running it by hand gets actionable feedback.
    """
    try:
        return sys.stderr.isatty()
    except (AttributeError, ValueError):
        return False


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
    # Self-gate: no-op when no enrollment key is configured (no flag, no
    # RUNLAYER_ENROLLMENT_API_KEY, no managed EnrollmentKey). The packaged
    # enroll LaunchAgent invokes this signed binary directly, so the gate lives
    # here rather than in a `defaults read EnrollmentKey || exit 0` shell wrapper
    # in the plist (which would register an unmanaged "sh" background item and
    # re-prompt the user). Under launchd / non-interactive runs exit 0 silently
    # so org-key-only / unconfigured fleets don't surface a spurious failure; an
    # operator running it by hand instead gets an actionable exit-2 error.
    resolved_key = resolve_enrollment_key(enrollment_key)
    if not resolved_key:
        if _operator_is_watching():
            typer.secho(
                "Error: no enrollment key configured (pass --enrollment-key, set "
                "RUNLAYER_ENROLLMENT_API_KEY, or push MDM EnrollmentKey).",
                fg=typer.colors.RED,
                err=True,
            )
            raise typer.Exit(2)
        raise typer.Exit(0)

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
        _submit_validation_checkins(resolved_host, existing)
        typer.secho(
            f"Already enrolled for {resolved_host}; pass --force to re-enroll.",
            fg=typer.colors.GREEN,
            err=True,
        )
        raise typer.Exit(0)

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
    dest = credential_dest(
        complete_device_enrollment(
            config, resolved_host, result.api_key, subject="enrollment API key"
        )
    )
    _submit_validation_checkins(resolved_host, result.api_key)
    typer.secho(
        f"Enrollment successful. API key saved to {dest} for {resolved_host}.",
        fg=typer.colors.GREEN,
        err=True,
    )


def _submit_validation_checkins(host: str, secret: str) -> None:
    """Best-effort Enforce + Sessions check-ins after (re-)enrollment.

    Delegates to the shared orchestrator so the enroll path reports feature
    health (and isolates/logs failures) the same way the scan path does.

    Runs only after enrollment has already succeeded, so the whole body is
    guarded: the orchestrator isolates each individual check-in, but the setup
    before it (client construction, device context, installed-tool enumeration,
    even the local imports) is not. An unexpected failure there must not mask
    the enrollment success message or flip the exit code non-zero — mirrors the
    scan path, where check-ins run inside its general ``try/except``.
    """
    try:
        from runlayer_cli.aiwatch_checkin import (  # noqa: PLC0415
            _make_device_context,
            submit_validation_checkins,
        )
        from runlayer_cli.api import RunlayerClient  # noqa: PLC0415
        from runlayer_cli.scan.device import get_installed_tools  # noqa: PLC0415

        client = RunlayerClient(hostname=host, secret=secret)
        submit_validation_checkins(
            client, ctx=_make_device_context(), tools=get_installed_tools()
        )
    except Exception as exc:
        logger.warning(
            "aiwatch_enroll_checkin_failed",
            error=str(exc),
            error_type=type(exc).__name__,
            exc_info=True,
        )
