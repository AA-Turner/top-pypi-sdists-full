"""``aiwatch bootstrap`` — strict-ordered enroll-then-install-hooks (see cli/AGENTS.md)."""

from __future__ import annotations

import os
from typing import Optional

import typer

from runlayer_cli.cli_persistence import complete_device_enrollment
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
from runlayer_cli.hook_install import (
    ClientStatus,
    InstallScope,
    check_absent_all,
    check_all,
    credential_present,
    install_client,
    iter_supported_clients,
    resolve_hook_command,
    uninstall_client,
)
from runlayer_cli.mdm_config import (
    read_managed_config,
    resolve_include_pipeline,
    resolve_install_hooks,
)
from runlayer_cli.symbols import FAIL, OK, WARN

EXIT_OK = 0
EXIT_STEP_FAILED = 1
EXIT_MISCONFIG = 2
EXIT_DRIFT_CHECK = 4


def bootstrap(
    host: Optional[str] = typer.Option(
        None,
        "--host",
        "-H",
        envvar="RUNLAYER_HOST",
        help="Runlayer host URL; falls back to config / MDM Host.",
    ),
    check: bool = typer.Option(
        False,
        "--check",
        help="Non-mutating: report whether enroll + hook configs are current.",
    ),
    mdm: bool = typer.Option(
        True,
        "--mdm/--user",
        help=(
            "Hook install scope. --mdm (default) writes to enterprise config "
            "dirs; --user writes to per-user ~/.<client> dirs."
        ),
    ),
    all_events: bool = typer.Option(
        False,
        "--all-events",
        help="Register all event/session hooks in addition to enforcement hooks.",
    ),
) -> None:
    """Enroll then install hooks. Idempotent. Skips enroll when running as root/SYSTEM.

    Enforcement is sourced at hook-fire time from MDM managed config
    (``Enforcement`` key in ``com.runlayer.aiwatch``). In MDM scope, event/session
    hooks install by default unless the ``Sessions`` key is set to ``false``;
    ``--all-events`` always forces them on.
    """
    resolved_host = resolve_host(host)
    if not resolved_host:
        typer.secho(
            f"{FAIL} no host configured (pass --host, set RUNLAYER_HOST, or push MDM Host).",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(EXIT_MISCONFIG)

    scope = InstallScope.MDM if mdm else InstallScope.USER

    if check:
        _bootstrap_check(resolved_host, scope=scope)
        return

    _bootstrap_apply(
        resolved_host,
        scope=scope,
        all_events=all_events,
    )


def _benign_uninstall_skip(reason: str | None) -> bool:
    return (
        reason is None or reason == "client not installed" or reason.startswith("no ")
    )


def _uninstall_all(scope: InstallScope) -> None:
    any_failed = False
    changed_any = False
    for target in iter_supported_clients():
        try:
            result = uninstall_client(target, scope=scope)
        except OSError as exc:
            any_failed = True
            typer.secho(
                f"{FAIL} hooks: {target.value} uninstall failed ({exc}).",
                fg=typer.colors.RED,
                err=True,
            )
            continue

        if result.changed:
            changed_any = True
            typer.secho(
                f"{OK} hooks: {target.value} removed from {result.config_path}.",
                fg=typer.colors.GREEN,
                err=True,
            )
        elif not _benign_uninstall_skip(result.skipped_reason):
            any_failed = True
            typer.secho(
                f"{FAIL} hooks: {target.value} uninstall skipped "
                f"({result.skipped_reason}).",
                fg=typer.colors.RED,
                err=True,
            )

    if any_failed:
        raise typer.Exit(EXIT_STEP_FAILED)
    if not changed_any:
        typer.secho(
            f"{OK} scan-only deployment (Enforcement + Sessions disabled); "
            "no Runlayer hooks present.",
            fg=typer.colors.GREEN,
            err=True,
        )


def _check_absent(scope: InstallScope) -> None:
    results = check_absent_all(scope=scope)
    drift = False
    for result in results:
        if result.status == ClientStatus.OK:
            continue
        drift = True
        typer.secho(
            f"{FAIL} hooks: {result.client.value} {result.status.value} "
            f"({result.detail or 'no detail'}).",
            fg=typer.colors.RED,
            err=True,
        )
    if drift:
        raise typer.Exit(EXIT_STEP_FAILED)
    typer.secho(
        f"{OK} scan-only deployment (Enforcement + Sessions disabled); "
        "no Runlayer hooks present.",
        fg=typer.colors.GREEN,
        err=True,
    )


def _bootstrap_check(host: str, *, scope: InstallScope) -> None:
    managed = read_managed_config()
    if not resolve_install_hooks(managed):
        _check_absent(scope)
        return

    present, _ = credential_present(load_config(), host, scope)
    if not present:
        typer.secho(
            f"{FAIL} enroll: missing credential for {host}.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(EXIT_DRIFT_CHECK)
    typer.secho(f"{OK} enroll: credential present.", fg=typer.colors.GREEN, err=True)

    results = check_all(
        scope=scope,
        include_pipeline=resolve_include_pipeline(False, managed),
    )
    if scope == InstallScope.USER:
        installed = [
            r for r in results if r.status != ClientStatus.CLIENT_NOT_INSTALLED
        ]
        if not installed:
            typer.secho(
                f"{WARN} hooks: no supported AI clients installed; nothing to verify.",
                fg=typer.colors.YELLOW,
                err=True,
            )
            return
    else:
        installed = list(results)

    drift = False
    for result in installed:
        if result.status == ClientStatus.OK:
            typer.secho(
                f"{OK} hooks: {result.client.value} ok.",
                fg=typer.colors.GREEN,
                err=True,
            )
            continue
        drift = True
        typer.secho(
            f"{FAIL} hooks: {result.client.value} {result.status.value} "
            f"({result.detail or 'no detail'}).",
            fg=typer.colors.RED,
            err=True,
        )

    if drift:
        raise typer.Exit(EXIT_STEP_FAILED)


def _enroll_step(host: str, scope: InstallScope) -> None:
    """Enroll half of bootstrap; skips when running as root/SYSTEM in MDM scope."""
    if read_managed_config().get("org_api_key"):
        # Org-key mode: hooks authenticate with the single managed OrgApiKey
        # directly (backend resolves device identity), so there's no per-user
        # enroll step to run.
        typer.secho(
            f"{OK} enroll: skipped — using managed org api key for {host}.",
            fg=typer.colors.GREEN,
            err=True,
        )
        return

    config = load_config()
    if config.get_secret_for_host(host):
        # Self-migration for pre-marker-file enrollments.
        write_enrollment_marker(host)
        typer.secho(
            f"{OK} enroll: credential already present for {host}.",
            fg=typer.colors.GREEN,
            err=True,
        )
        return

    if scope == InstallScope.MDM and _running_as_root_or_system():
        typer.secho(
            f"{WARN} enroll: skipped — running as root/SYSTEM cannot write to "
            "the per-user keychain. Trigger enroll via the user-context "
            "LaunchAgent / bootstrap.ps1.",
            fg=typer.colors.YELLOW,
            err=True,
        )
        return

    enrollment_key = resolve_enrollment_key()
    if not enrollment_key:
        typer.secho(
            f"{FAIL} no enrollment key (push MDM EnrollmentKey or set "
            "RUNLAYER_ENROLLMENT_API_KEY); cannot bootstrap.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(EXIT_MISCONFIG)

    try:
        result = exchange_enrollment_key(
            host=host,
            enrollment_key=enrollment_key,
            username=resolve_mdm_username(),
            device_name=resolve_mdm_device_name(),
        )
    except EnrollmentError as exc:
        typer.secho(f"{FAIL} enroll: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(EXIT_STEP_FAILED) from None

    config = load_config()
    complete_device_enrollment(
        config,
        host,
        result.api_key,
        subject="enroll: API key",
        exit_code=EXIT_STEP_FAILED,
        fail_prefix=FAIL,
    )
    typer.secho(
        f"{OK} enroll: credential stored for {host}.",
        fg=typer.colors.GREEN,
        err=True,
    )


def _bootstrap_apply(
    host: str,
    *,
    scope: InstallScope,
    all_events: bool,
) -> None:
    managed = read_managed_config()
    if not all_events and not resolve_install_hooks(managed):
        typer.secho(
            f"{OK} scan-only deployment (Enforcement + Sessions disabled); "
            "removing Runlayer hooks.",
            fg=typer.colors.GREEN,
            err=True,
        )
        _uninstall_all(scope)
        return

    _enroll_step(host, scope)

    present, _ = credential_present(load_config(), host, scope)
    if not present:
        typer.secho(
            f"{FAIL} no per-user credential for {host} after enroll; refusing "
            "to install hooks (strict-ordering guardrail).",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(EXIT_DRIFT_CHECK)

    try:
        hook_command = resolve_hook_command()
    except FileNotFoundError as exc:
        typer.secho(
            f"{FAIL} cannot find aiwatch binary on disk: {exc}.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(EXIT_MISCONFIG) from None

    include_pipeline = resolve_include_pipeline(all_events, managed)

    any_failed = False
    wrote_any = False
    for target in iter_supported_clients():
        try:
            result = install_client(
                target,
                scope=scope,
                include_pipeline=include_pipeline,
                hook_command=hook_command,
            )
        except OSError as exc:
            any_failed = True
            typer.secho(
                f"{FAIL} hooks: {target.value} write failed ({exc}).",
                fg=typer.colors.RED,
                err=True,
            )
            continue

        if result.written:
            wrote_any = True
            typer.secho(
                f"{OK} hooks: {target.value} configured at {result.config_path}.",
                fg=typer.colors.GREEN,
                err=True,
            )
        else:
            typer.secho(
                f"{OK} hooks: {target.value} skipped ({result.skipped_reason}).",
                fg=typer.colors.GREEN,
                err=True,
            )

    if any_failed:
        raise typer.Exit(EXIT_STEP_FAILED)
    if not wrote_any:
        typer.secho(
            f"{WARN} hooks: no supported AI clients installed; nothing to write.",
            fg=typer.colors.YELLOW,
            err=True,
        )


def _running_as_root_or_system() -> bool:
    """True when this process can't write to the per-user keychain."""
    if os.name == "posix":
        try:
            return os.geteuid() == 0  # type: ignore[attr-defined]
        except AttributeError:
            return False
    if os.name == "nt":
        profile = os.environ.get("USERPROFILE", "")
        return "system32" in profile.lower() or "systemprofile" in profile.lower()
    return False
