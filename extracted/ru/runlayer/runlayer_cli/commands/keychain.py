"""macOS keychain migration commands for the packaged Runlayer CLI."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional

import typer

from runlayer_cli.config import load_config, normalize_url, url_to_host_key
from runlayer_cli.credential_store import ReadoptResult, readopt_entry
from runlayer_cli.paths import get_runlayer_dir
from runlayer_cli.runtime import is_frozen_runlayer_bundle

KEYCHAIN_ADOPTION_MARKER_PREFIX = ".keychain-adopted-"
_AUTO_ADOPT_SKIPPED_COMMANDS = frozenset(
    {
        "keychain",
        "run",
        "scan",
        "status",
        "__handle-url",
        "__self-update-root",
    }
)
_MARKER_RESULTS = frozenset({"adopted", "nothing", "denied", "lost"})

app = typer.Typer(help="Manage macOS keychain access")


def adoption_marker_path(host_key: str) -> Path:
    """Return the one-time adoption marker path for a keychain account."""
    return get_runlayer_dir() / f"{KEYCHAIN_ADOPTION_MARKER_PREFIX}{host_key}"


def _write_adoption_marker(host_key: str) -> None:
    """Best-effort marker write; adoption itself remains authoritative."""
    path = adoption_marker_path(host_key)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)
    except OSError:
        pass


def _adopt_host(host_key: str) -> ReadoptResult:
    result = readopt_entry(host_key)
    if result in _MARKER_RESULTS:
        _write_adoption_marker(host_key)
    return result


def _require_supported_runtime() -> None:
    if not is_frozen_runlayer_bundle():
        typer.secho(
            "Error: Keychain adoption is only available in the packaged macOS "
            "Runlayer CLI.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(1)


def _host_key_from_url(host: str) -> str:
    host_key = url_to_host_key(normalize_url(host))
    if not host_key:
        typer.secho(
            "Error: --host must be a full URL, such as https://app.runlayer.com.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(1)
    return host_key


def _print_manual_result(host_key: str, result: ReadoptResult) -> bool:
    failed = result in {"denied", "failed", "lost"}
    if result == "adopted":
        typer.secho(
            f"Adopted keychain credential for {host_key}.",
            fg=typer.colors.GREEN,
            err=True,
        )
    elif result == "nothing":
        typer.echo(f"No keychain credential found for {host_key}.", err=True)
    elif result == "denied":
        typer.secho(
            f"Keychain access denied for {host_key}; credential left unchanged.",
            fg=typer.colors.YELLOW,
            err=True,
        )
    elif result == "lost":
        typer.secho(
            f"Error: The keychain credential for {host_key} was removed but "
            "could not be recreated. Run 'runlayer login' to restore it.",
            fg=typer.colors.RED,
            err=True,
        )
    else:
        typer.secho(
            f"Failed to adopt keychain credential for {host_key}.",
            fg=typer.colors.RED,
            err=True,
        )
    return failed


@app.callback(invoke_without_command=True)
def keychain_callback(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


@app.command()
def adopt(
    host: Optional[str] = typer.Option(
        None,
        "--host",
        "-H",
        help="Host URL to adopt (defaults to all configured hosts)",
    ),
) -> None:
    """Recreate legacy keychain entries under the packaged CLI identity."""
    _require_supported_runtime()
    config = load_config()
    host_keys = [_host_key_from_url(host)] if host else sorted(config.hosts)
    if not host_keys:
        typer.echo("No configured hosts found.", err=True)
        return

    failed = False
    for host_key in host_keys:
        result = _adopt_host(host_key)
        failed = _print_manual_result(host_key, result) or failed
    if failed:
        raise typer.Exit(1)


def _running_as_root() -> bool:
    geteuid = getattr(os, "geteuid", None)
    return callable(geteuid) and geteuid() == 0


def maybe_auto_adopt(invoked_subcommand: str | None) -> None:
    """Best-effort one-time adoption before interactive packaged CLI commands."""
    # Adoption must stay in user context: as root (e.g. a sudo re-exec such as
    # the privileged self-update continuation) it would target root's keychain
    # and config, never the user's login-keychain item.
    if (
        not is_frozen_runlayer_bundle()
        or not sys.stderr.isatty()
        or _running_as_root()
        or invoked_subcommand is None
        or invoked_subcommand in _AUTO_ADOPT_SKIPPED_COMMANDS
    ):
        return

    # Broad catch: adoption is best-effort and runs before unrelated
    # subcommands, so an unexpected keychain/filesystem failure must degrade
    # to a warning rather than abort the command the user invoked (mirrors
    # the defensive probe in credential_store.get_keyring_store).
    try:
        config = load_config()
        for host_key in sorted(config.hosts):
            if adoption_marker_path(host_key).exists():
                continue
            typer.echo(
                f"Checking saved keychain access for {host_key}; macOS may ask "
                "you to allow access once.",
                err=True,
            )
            result = _adopt_host(host_key)
            if result == "denied":
                typer.secho(
                    "Access was not granted; the credential was left unchanged. "
                    "Retry with 'runlayer keychain adopt'.",
                    fg=typer.colors.YELLOW,
                    err=True,
                )
            elif result == "lost":
                typer.secho(
                    f"Warning: The keychain credential for {host_key} was "
                    "removed but could not be recreated. Run 'runlayer login' "
                    "to restore it.",
                    fg=typer.colors.RED,
                    err=True,
                )
            elif result == "failed":
                typer.secho(
                    f"Warning: Could not adopt the keychain credential for "
                    f"{host_key}. Retry with 'runlayer keychain adopt'.",
                    fg=typer.colors.YELLOW,
                    err=True,
                )
    except Exception:
        typer.secho(
            "Warning: Skipped the keychain adoption check. "
            "Retry with 'runlayer keychain adopt'.",
            fg=typer.colors.YELLOW,
            err=True,
        )
