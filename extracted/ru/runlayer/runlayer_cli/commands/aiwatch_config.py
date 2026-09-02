"""Inspect AI Watch config and trigger privileged scheduler units."""

from __future__ import annotations

import ctypes
from datetime import datetime, timezone
from enum import Enum
import json
import os
import platform
from pathlib import Path
import subprocess
import sys
from typing import Literal, TypedDict

import typer

from runlayer_cli import aiwatch_config_cache, mdm_config
from runlayer_cli.aiwatch_config_sync import sync_backend_config


app = typer.Typer(help="Inspect or synchronize resolved AI Watch configuration.")

_LINUX_UPDATE_SCRIPT = Path("/usr/lib/runlayer/run-aiwatch-update.sh")
# Linux `config sync` kicks the scan wrapper: its first step is the root
# `aiwatch config refresh`, so one run both refreshes the snapshot and applies
# it to the immediately following scan fan-out.
_LINUX_SCAN_SCRIPT = Path("/usr/lib/runlayer/run-aiwatch-scan.sh")
# Both Linux wrappers exit EX_TEMPFAIL when another cycle holds their lock —
# nothing ran, so the kick must not be reported as started.
_EX_TEMPFAIL = 75

CacheState = Literal["valid", "rejected", "missing", "unverified", "unsupported"]


class BackendCacheStatus(TypedDict):
    """Operator-safe status for the backend settings cache."""

    status: CacheState
    location: str | None
    modified_at: str | None


@app.callback(invoke_without_command=True)
def _config_callback(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


def _redact_config(config: mdm_config.ManagedConfig) -> dict[str, object]:
    redacted: dict[str, object] = {}
    for key, value in config.items():
        if key in mdm_config.SECRET_FIELDS:
            redacted[key] = (
                f"****{value[-4:]}" if isinstance(value, str) and value else "not set"
            )
        else:
            redacted[key] = value
    return redacted


def _posix_cache_details(path: Path) -> tuple[bool, str | None]:
    try:
        stat = path.stat()
    except (FileNotFoundError, OSError):
        return False, None
    modified_at = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()
    return True, modified_at


def _windows_cache_present() -> bool:
    winreg = aiwatch_config_cache.winreg
    if winreg is None:
        return False
    try:
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            aiwatch_config_cache.WINDOWS_REG_KEY_PATH,
            0,
            winreg.KEY_READ,
        ) as key:
            winreg.QueryValueEx(key, aiwatch_config_cache.WINDOWS_CONFIG_VALUE)
    except OSError:
        return False
    return True


def _backend_cache_status(
    managed: mdm_config.ManagedConfig,
) -> BackendCacheStatus:
    system = platform.system()
    present = False
    location: str | None = None
    modified_at: str | None = None
    if system == "Darwin":
        location = str(aiwatch_config_cache.MACOS_CACHE_PATH)
        present, modified_at = _posix_cache_details(
            aiwatch_config_cache.MACOS_CACHE_PATH
        )
    elif system == "Windows":
        location = (
            "HKLM\\"
            f"{aiwatch_config_cache.WINDOWS_REG_KEY_PATH}\\"
            f"{aiwatch_config_cache.WINDOWS_CONFIG_VALUE}"
        )
        present = _windows_cache_present()
    elif system == "Linux":
        location = str(aiwatch_config_cache.LINUX_CACHE_PATH)
        present, modified_at = _posix_cache_details(
            aiwatch_config_cache.LINUX_CACHE_PATH
        )
    else:
        return {
            "status": "unsupported",
            "location": None,
            "modified_at": None,
        }

    status: CacheState
    if not present:
        status = "missing"
    else:
        org_api_key = managed.get("org_api_key")
        if not org_api_key and system == "Linux":
            # Linux delivers the key via the root-only credentials env, not
            # the world-readable managed config (see mdm_config).
            org_api_key = os.environ.get("RUNLAYER_API_KEY")
        if not org_api_key:
            status = "unverified"
        elif aiwatch_config_cache.read_backend_config(org_api_key) is None:
            status = "rejected"
        else:
            status = "valid"
    return {
        "status": status,
        "location": location,
        "modified_at": modified_at,
    }


def _human_value(value: object) -> str:
    if isinstance(value, Enum):
        return str(value.value)
    if isinstance(value, str):
        return value
    return json.dumps(value, sort_keys=True)


@app.command("show")
def show_config(
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit machine-readable JSON.",
    ),
) -> None:
    """Show resolved managed configuration and backend cache status."""
    managed = mdm_config.read_managed_config()
    redacted = _redact_config(managed)
    cache_status = _backend_cache_status(managed)
    if json_output:
        typer.echo(
            json.dumps(
                {
                    "config": redacted,
                    "backend_cache": cache_status,
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        typer.echo("Resolved config:")
        for key in sorted(redacted):
            typer.echo(f"  {key}: {_human_value(redacted[key])}")
        typer.echo("Backend cache:")
        for key, value in cache_status.items():
            typer.echo(f"  {key}: {_human_value(value)}")


def _require_root(command: str) -> None:
    get_euid = getattr(os, "geteuid", None)
    if get_euid is None or get_euid() != 0:
        typer.secho(
            f"Root privileges required. Re-run with: sudo {command}",
            err=True,
        )
        raise typer.Exit(1)


def _require_windows_admin(command: str) -> None:
    if sys.platform != "win32":
        is_admin = False
    else:
        try:
            is_admin = bool(ctypes.windll.shell32.IsUserAnAdmin())
        except (AttributeError, OSError):
            is_admin = False
    if not is_admin:
        _show_windows_admin_hint(command)
        raise typer.Exit(1)


def _show_windows_admin_hint(command: str) -> None:
    typer.secho(
        "Administrator privileges required. "
        f"Re-run `{command}` from an elevated prompt.",
        err=True,
    )


def _scheduler_unit_missing(result: subprocess.CompletedProcess[str]) -> bool:
    output = f"{result.stdout or ''}\n{result.stderr or ''}".lower()
    return any(
        marker in output
        for marker in (
            "could not find service",
            "cannot find the file",
            "cannot find the path",
            "does not exist",
            "not found",
        )
    )


def _scheduler_access_denied(result: subprocess.CompletedProcess[str]) -> bool:
    output = f"{result.stdout or ''}\n{result.stderr or ''}".lower()
    return "access is denied" in output or "access denied" in output


def _kick_unit(
    *,
    macos_label: str,
    windows_task: str,
    windows_requires_admin: bool,
    operator_command: str,
    success_message: str,
    linux_script: Path | None = None,
) -> None:
    system = platform.system()
    command: list[str]
    if system == "Darwin":
        _require_root(operator_command)
        command = ["launchctl", "kickstart", f"system/{macos_label}"]
    elif system == "Windows":
        if windows_requires_admin:
            _require_windows_admin(operator_command)
        command = ["schtasks", "/Run", "/TN", windows_task]
    elif system == "Linux" and linux_script is not None:
        _require_root(operator_command)
        if not linux_script.is_file():
            typer.secho(
                "AI Watch package not installed: wrapper script not found.",
                err=True,
            )
            raise typer.Exit(1)
        command = [str(linux_script)]
    else:
        typer.secho(f"Unsupported platform: {system}", err=True)
        raise typer.Exit(1)

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        typer.secho(f"Failed to start scheduler unit: {exc}", err=True)
        raise typer.Exit(1) from exc
    if result.returncode != 0:
        if system == "Linux" and result.returncode == _EX_TEMPFAIL:
            # The wrapper skipped: another cycle holds the lock, so nothing
            # ran on this invocation. Report honestly instead of "started".
            typer.secho(
                "Another AI Watch cycle is already running; nothing was "
                f"started. Re-run `{operator_command}` once it finishes.",
                err=True,
            )
        elif system == "Windows" and _scheduler_access_denied(result):
            _show_windows_admin_hint(operator_command)
        elif _scheduler_unit_missing(result):
            typer.secho(
                "AI Watch package not installed: scheduler unit not found.",
                err=True,
            )
        elif system == "Darwin" and "already" in (
            f"{result.stdout or ''}\n{result.stderr or ''}".lower()
        ):
            typer.echo("Cycle already running.")
            return
        else:
            detail = (result.stderr or result.stdout or "unknown error").strip()
            typer.secho(f"Failed to start scheduler unit: {detail}", err=True)
        raise typer.Exit(1)
    typer.echo(success_message)


@app.command("refresh", hidden=True)
def refresh_config() -> None:
    """Fetch backend settings into the root-owned snapshot (Linux cron step).

    Linux has no privileged hook-reconcile unit, so the root cron scan wrapper
    runs this before the per-user fan-out. Quiet exit 0 when unconfigured; a
    fetch failure keeps the last-known-good snapshot and also exits 0 so a
    transient backend error never blocks the scan fan-out.
    """
    managed = mdm_config.read_managed_config()
    host = os.environ.get("RUNLAYER_HOST") or managed.get("host")
    org_api_key = managed.get("org_api_key") or os.environ.get("RUNLAYER_API_KEY")
    if not host or not org_api_key:
        raise typer.Exit(0)

    if sync_backend_config(host=host, org_api_key=org_api_key):
        typer.echo("Backend settings snapshot refreshed.")
    else:
        typer.echo("Backend settings refresh skipped; kept last-known-good.")


@app.command("sync")
def sync_config() -> None:
    """Run backend config sync and hook reconciliation now."""
    _kick_unit(
        macos_label="com.runlayer.aiwatch.bootstrap",
        windows_task=r"\Runlayer\AIWatchHooks",
        windows_requires_admin=False,
        linux_script=_LINUX_SCAN_SCRIPT,
        operator_command="aiwatch config sync",
        success_message="Configuration sync started.",
    )


def update_now() -> None:
    """Run the managed AI Watch self-update cycle now."""
    _kick_unit(
        macos_label="com.runlayer.aiwatch.update",
        windows_task=r"\Runlayer\AIWatchUpdate",
        windows_requires_admin=True,
        linux_script=_LINUX_UPDATE_SCRIPT,
        operator_command="aiwatch update-now",
        success_message="Update cycle started.",
    )
