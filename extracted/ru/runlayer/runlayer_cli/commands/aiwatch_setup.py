"""``aiwatch setup`` typer subapp — hook install/check for MDM bundles (see cli/AGENTS.md)."""

from __future__ import annotations

from typing import Optional

import typer

from runlayer_cli.config import load_config
from runlayer_cli.enrollment import resolve_host
from runlayer_cli.hook_install import (
    Client,
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
from runlayer_cli.install_window import InstallWindowState, install_window_state
from runlayer_cli.mdm_config import (
    read_managed_config,
    resolve_include_pipeline,
    resolve_install_hooks,
)
from runlayer_cli.symbols import FAIL, OK, WARN

# Exit codes (in sync with Intune detect scripts; see cli/AGENTS.md):
EXIT_OK = 0
EXIT_PARTIAL_FAILURE = 1
EXIT_DRIFT = 1
EXIT_MISCONFIG = 2
EXIT_NO_CLIENTS = 2
EXIT_NO_CREDENTIAL = 4


app = typer.Typer(help="Configure on-disk hook integrations for AI coding clients.")
hooks_app = typer.Typer(
    help="Install or verify Runlayer hook configs for installed AI clients."
)
app.add_typer(hooks_app, name="hooks")


def _client_from_str(name: Optional[str]) -> Optional[Client]:
    if name is None:
        return None
    try:
        return Client(name)
    except ValueError as exc:
        raise typer.BadParameter(
            f"unknown client {name!r}; expected one of "
            f"{', '.join(c.value for c in iter_supported_clients())}"
        ) from exc


def _targets_from_client(name: Optional[str]) -> tuple[Client, ...]:
    selected = _client_from_str(name)
    return (selected,) if selected else iter_supported_clients()


def _benign_uninstall_skip(reason: str | None) -> bool:
    return (
        reason is None or reason == "client not installed" or reason.startswith("no ")
    )


def _uninstall_targets(targets: tuple[Client, ...], *, scope: InstallScope) -> None:
    any_failed = False
    changed_any = False
    for target in targets:
        try:
            result = uninstall_client(target, scope=scope)
        except OSError as exc:
            any_failed = True
            typer.secho(
                f"{FAIL} {target.value}: uninstall failed ({exc}).",
                fg=typer.colors.RED,
                err=True,
            )
            continue

        if result.changed:
            changed_any = True
            typer.secho(
                f"{OK} {target.value}: Runlayer hooks removed from {result.config_path}.",
                fg=typer.colors.GREEN,
                err=True,
            )
        elif not _benign_uninstall_skip(result.skipped_reason):
            any_failed = True
            typer.secho(
                f"{FAIL} {target.value}: uninstall skipped ({result.skipped_reason}).",
                fg=typer.colors.RED,
                err=True,
            )

    if any_failed:
        raise typer.Exit(EXIT_PARTIAL_FAILURE)
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
            f"{FAIL} {result.client.value}: {result.status.value} "
            f"({result.detail or 'no detail'}).",
            fg=typer.colors.RED,
            err=True,
        )
    if drift:
        raise typer.Exit(EXIT_DRIFT)
    typer.secho(
        f"{OK} scan-only deployment (Enforcement + Sessions disabled); "
        "no Runlayer hooks present.",
        fg=typer.colors.GREEN,
        err=True,
    )


@hooks_app.callback(invoke_without_command=True)
def _hooks_callback(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


@hooks_app.command("install")
def install(
    client: Optional[str] = typer.Option(
        None,
        "--client",
        "-c",
        help="Configure a single client (cursor / claude_code / codex / hermes); defaults to all installed.",
    ),
    host: Optional[str] = typer.Option(
        None,
        "--host",
        "-H",
        envvar="RUNLAYER_HOST",
        help="Runlayer host URL; falls back to config / MDM Host.",
    ),
    mdm: bool = typer.Option(
        True,
        "--mdm/--user",
        help=(
            "Write to enterprise (MDM) config dirs by default. Pass --user to "
            "write per-user ~/.<client> dirs instead (dev / manual use)."
        ),
    ),
    all_events: bool = typer.Option(
        False,
        "--all-events",
        help="Register all event/session hooks in addition to enforcement hooks.",
    ),
) -> None:
    """Install Runlayer hook configs (exit 4 if ``aiwatch enroll`` hasn't run).

    Enforcement is sourced at hook-fire time from MDM managed config
    (``Enforcement`` key in ``com.runlayer.aiwatch``). In MDM scope, event/session
    hooks install by default unless the ``Sessions`` key is set to ``false``;
    ``--all-events`` always forces them on.
    """
    scope = InstallScope.MDM if mdm else InstallScope.USER

    effective_host = resolve_host(host)
    if not effective_host:
        typer.secho(
            f"{FAIL} no host configured (pass --host, set RUNLAYER_HOST, or push MDM Host).",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(EXIT_MISCONFIG)

    managed = read_managed_config()
    targets = _targets_from_client(client)
    if not all_events and not resolve_install_hooks(managed):
        typer.secho(
            f"{OK} scan-only deployment (Enforcement + Sessions disabled); "
            "removing Runlayer hooks.",
            fg=typer.colors.GREEN,
            err=True,
        )
        _uninstall_targets(targets, scope=scope)
        raise typer.Exit(EXIT_OK)

    present, detail = credential_present(load_config(), effective_host, scope)
    if not present:
        typer.secho(
            f"{FAIL} no user credential for {effective_host} ({detail}). "
            "Run `aiwatch enroll` first (exit 4 = strict-ordering guardrail).",
            fg=typer.colors.RED,
            err=True,
        )
        if install_window_state() is InstallWindowState.OUTSIDE:
            raise typer.Exit(EXIT_OK)
        raise typer.Exit(EXIT_NO_CREDENTIAL)

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
    for target in targets:
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
                f"{FAIL} {target.value}: write failed ({exc}).",
                fg=typer.colors.RED,
                err=True,
            )
            continue

        if result.written:
            wrote_any = True
            typer.secho(
                f"{OK} {target.value}: hooks installed at {result.config_path}.",
                fg=typer.colors.GREEN,
                err=True,
            )
        else:
            typer.secho(
                f"{WARN} {target.value}: skipped ({result.skipped_reason}).",
                fg=typer.colors.YELLOW,
                err=True,
            )

    if any_failed:
        raise typer.Exit(EXIT_PARTIAL_FAILURE)
    if not wrote_any:
        typer.secho(
            f"{WARN} no client config dirs detected; nothing to install.",
            fg=typer.colors.YELLOW,
            err=True,
        )


@hooks_app.command("check")
def check(
    host: Optional[str] = typer.Option(
        None,
        "--host",
        "-H",
        envvar="RUNLAYER_HOST",
        help="Runlayer host URL; falls back to config / MDM Host.",
    ),
    mdm: bool = typer.Option(
        True,
        "--mdm/--user",
        help="Inspect enterprise config dirs by default; pass --user for per-user dirs.",
    ),
) -> None:
    """Report installed clients' hook config compliance (exits 0 ok, 1 drift, 2 no clients, 4 no creds)."""
    scope = InstallScope.MDM if mdm else InstallScope.USER

    effective_host = resolve_host(host)
    if not effective_host:
        typer.secho(f"{FAIL} no host configured.", fg=typer.colors.RED, err=True)
        raise typer.Exit(EXIT_MISCONFIG)

    managed = read_managed_config()
    if not resolve_install_hooks(managed):
        _check_absent(scope)
        raise typer.Exit(EXIT_OK)

    present, detail = credential_present(load_config(), effective_host, scope)
    if not present:
        typer.secho(
            f"{FAIL} no user credential for {effective_host} ({detail}).",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(EXIT_NO_CREDENTIAL)

    results = check_all(
        scope=scope,
        include_pipeline=resolve_include_pipeline(False, managed),
    )

    if scope == InstallScope.USER:
        installed_results = [
            r for r in results if r.status != ClientStatus.CLIENT_NOT_INSTALLED
        ]
        if not installed_results:
            typer.secho(
                f"{WARN} no supported AI clients installed.",
                fg=typer.colors.YELLOW,
                err=True,
            )
            raise typer.Exit(EXIT_NO_CLIENTS)
    else:
        installed_results = list(results)

    drift = False
    for result in installed_results:
        if result.status == ClientStatus.OK:
            typer.secho(
                f"{OK} {result.client.value}: ok.",
                fg=typer.colors.GREEN,
                err=True,
            )
            continue
        drift = True
        typer.secho(
            f"{FAIL} {result.client.value}: {result.status.value} ({result.detail or 'no detail'}).",
            fg=typer.colors.RED,
            err=True,
        )

    if drift:
        raise typer.Exit(EXIT_DRIFT)
