"""``aiwatch setup`` typer subapp — hook install/check for MDM bundles (see cli/AGENTS.md)."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Optional

import structlog
import typer

from runlayer_cli.aiwatch_config_sync import sync_backend_config
from runlayer_cli.config import load_config, normalize_url
from runlayer_cli.enrollment import resolve_host
from runlayer_cli.hook_install import (
    Client,
    ClientStatus,
    InstallScope,
    ManagedPathError,
    check_absent_all,
    check_all,
    credential_present,
    install_client,
    iter_supported_clients,
    resolve_hook_command,
    uninstall_client,
)
from runlayer_cli.hook_install.browser_extensions import (
    BrowserExtensionMisconfiguration,
    check_browser_extension,
    install_browser_extension,
    should_report_browser_extension_skip,
)
from runlayer_cli.hook_install.daemon_lifecycle import (
    check_daemon_unit,
    check_scan_unit,
    ensure_daemon_unit,
    ensure_scan_unit,
)
from runlayer_cli.install_window import InstallWindowState, install_window_state
from runlayer_cli.mdm_config import (
    ManagedConfig,
    daemon_gate_open,
    read_managed_config,
    resolve_include_pipeline,
    resolve_install_hooks,
    resolve_mcp_usage_metadata_only,
    resolve_mode,
)
from runlayer_cli.symbols import FAIL, OK, WARN
from runlayer_cli.macos_test_device_config import (
    AIWATCH_LOCAL_CONFIG_PATH,
    TestDeviceConfigError,
    configure_aiwatch_test_device,
)

logger = structlog.get_logger(__name__)

# Exit codes. Consumed by the supervisors that run `aiwatch setup hooks install`:
# the macOS bootstrap LaunchDaemon's KeepAlive (exit 4 fast-retries within the
# install window, exit 0 idles after) and the Windows AIWatchHooks scheduled
# task's LastTaskResult. NOT read by detect-install.ps1, which always exits 0 per
# Intune's custom-detection STDOUT contract. See cli/AGENTS.md.
EXIT_OK = 0
EXIT_PARTIAL_FAILURE = 1
EXIT_DRIFT = 1
EXIT_MISCONFIG = 2
EXIT_NO_CLIENTS = 2
EXIT_NO_CREDENTIAL = 4

_DEFAULT_PROJECT_DEPTH = 7
_DEFAULT_PROJECT_TIMEOUT = 60
_BOOTSTRAP_FAILURE_COUNT_PATH = Path("/var/db/com.runlayer.aiwatch/.bootstrap-failures")
_BOOTSTRAP_FAILURE_THRESHOLD = 5


app = typer.Typer(help="Configure on-disk hook integrations for AI coding clients.")
hooks_app = typer.Typer(
    help="Install or verify Runlayer hook configs for installed AI clients."
)
app.add_typer(hooks_app, name="hooks")


@app.callback(invoke_without_command=True)
def _setup_callback(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


def _reset_bootstrap_failure_count() -> None:
    """Best-effort reset; state I/O never changes the install outcome."""
    try:
        _BOOTSTRAP_FAILURE_COUNT_PATH.unlink()
    except FileNotFoundError:
        pass
    except OSError:
        pass


def _increment_bootstrap_failure_count() -> int | None:
    """Atomically increment persisted state, or return ``None`` if unavailable."""
    path = _BOOTSTRAP_FAILURE_COUNT_PATH
    try:
        try:
            current = int(path.read_text(encoding="ascii").strip())
        except FileNotFoundError:
            current = 0
        except (UnicodeError, ValueError):
            current = 0

        if current >= _BOOTSTRAP_FAILURE_THRESHOLD:
            return _BOOTSTRAP_FAILURE_THRESHOLD
        count = min(_BOOTSTRAP_FAILURE_THRESHOLD, max(0, current) + 1)
        path.parent.mkdir(mode=0o755, parents=True, exist_ok=True)
        fd, temp_name = tempfile.mkstemp(prefix=f"{path.name}.", dir=path.parent)
        temp_path = Path(temp_name)
        try:
            with os.fdopen(fd, "w", encoding="ascii") as temp_file:
                temp_file.write(f"{count}\n")
                temp_file.flush()
                os.fsync(temp_file.fileno())
            os.chmod(temp_path, 0o600)
            os.replace(temp_path, path)
        finally:
            try:
                temp_path.unlink()
            except FileNotFoundError:
                pass
        return count
    except OSError:
        return None


def _bootstrap_install_exit_code(
    scope: InstallScope,
    exit_code: int,
    *,
    window_state: InstallWindowState | None = None,
) -> int:
    """Bound launchd retries without changing non-MDM install semantics."""
    if scope != InstallScope.MDM:
        return exit_code

    if exit_code == EXIT_OK:
        _reset_bootstrap_failure_count()
        return exit_code

    state = window_state if window_state is not None else install_window_state()
    if state is InstallWindowState.INSIDE:
        _reset_bootstrap_failure_count()
        return exit_code
    if state is not InstallWindowState.OUTSIDE or exit_code not in {
        EXIT_PARTIAL_FAILURE,
        EXIT_MISCONFIG,
    }:
        return exit_code

    count = _increment_bootstrap_failure_count()
    if count is not None and count >= _BOOTSTRAP_FAILURE_THRESHOLD:
        return EXIT_OK
    return exit_code


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


def _uninstall_targets(targets: tuple[Client, ...], *, scope: InstallScope) -> bool:
    any_failed = False
    changed_any = False
    for target in targets:
        try:
            result = uninstall_client(target, scope=scope)
        except ManagedPathError as exc:
            any_failed = True
            typer.secho(
                f"{FAIL} {target.value}: configuration invalid ({exc}).",
                fg=typer.colors.RED,
                err=True,
            )
            continue
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

    if not any_failed and not changed_any:
        typer.secho(
            f"{OK} scan-only deployment (hooks and MCP usage metadata disabled); "
            "no Runlayer hooks present.",
            fg=typer.colors.GREEN,
            err=True,
        )
    return any_failed


def _check_absent(scope: InstallScope) -> bool:
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
    if not drift:
        typer.secho(
            f"{OK} scan-only deployment (hooks and MCP usage metadata disabled); "
            "no Runlayer hooks present.",
            fg=typer.colors.GREEN,
            err=True,
        )
    return drift


def _install_browser_extension_step(managed: ManagedConfig) -> tuple[bool, bool]:
    any_failed = False
    wrote_any = False
    try:
        ext = install_browser_extension(managed)
    except BrowserExtensionMisconfiguration as exc:
        any_failed = True
        typer.secho(
            f"{FAIL} browser_extension: configuration failed ({exc}).",
            fg=typer.colors.RED,
            err=True,
        )
    except OSError as exc:
        any_failed = True
        typer.secho(
            f"{FAIL} browser_extension: write failed ({exc}).",
            fg=typer.colors.RED,
            err=True,
        )
    else:
        if ext.written:
            wrote_any = True
            policy_path = ext.policy_path or ext.force_policy_path
            typer.secho(
                f"{OK} browser_extension: browser policies reconciled at {policy_path}.",
                fg=typer.colors.GREEN,
                err=True,
            )
        elif should_report_browser_extension_skip(ext):
            typer.secho(
                f"{WARN} browser_extension: skipped ({ext.skipped_reason}).",
                fg=typer.colors.YELLOW,
                err=True,
            )
    return any_failed, wrote_any


def _check_browser_extension_step(managed: ManagedConfig) -> bool:
    ext_ok, ext_detail = check_browser_extension(managed)
    if ext_ok:
        return False
    typer.secho(
        f"{FAIL} browser_extension: drifted ({ext_detail}).",
        fg=typer.colors.RED,
        err=True,
    )
    return True


def _install_daemon_lifecycle_step(
    managed: ManagedConfig,
    *,
    restart_windows_service: bool = False,
) -> tuple[bool, bool]:
    try:
        result = ensure_daemon_unit(
            managed,
            restart_windows_service=restart_windows_service,
        )
    except OSError as exc:
        typer.secho(
            f"{FAIL} daemon: lifecycle repair failed ({exc}).",
            fg=typer.colors.RED,
            err=True,
        )
        return True, False
    if not result.ok:
        typer.secho(
            f"{FAIL} daemon: unhealthy ({result.detail}).",
            fg=typer.colors.RED,
            err=True,
        )
        return True, result.changed
    if result.changed:
        typer.secho(
            f"{OK} daemon: supervisor reconciled ({result.detail}).",
            fg=typer.colors.GREEN,
            err=True,
        )
    return False, result.changed


def _check_daemon_lifecycle_step(managed: ManagedConfig) -> bool:
    result = check_daemon_unit(managed)
    if result.ok:
        return False
    typer.secho(
        f"{FAIL} daemon: drifted ({result.detail}).",
        fg=typer.colors.RED,
        err=True,
    )
    return True


def _install_scan_lifecycle_step() -> tuple[bool, bool]:
    try:
        result = ensure_scan_unit()
    except OSError as exc:
        typer.secho(
            f"{FAIL} scan: lifecycle repair failed ({exc}).",
            fg=typer.colors.RED,
            err=True,
        )
        return True, False
    if not result.ok:
        typer.secho(
            f"{FAIL} scan: unhealthy ({result.detail}).",
            fg=typer.colors.RED,
            err=True,
        )
        return True, result.changed
    if result.changed:
        typer.secho(
            f"{OK} scan: scheduler reconciled ({result.detail}).",
            fg=typer.colors.GREEN,
            err=True,
        )
    return False, result.changed


def _check_scan_lifecycle_step() -> bool:
    result = check_scan_unit()
    if result.ok:
        return False
    typer.secho(
        f"{FAIL} scan: drifted ({result.detail}).",
        fg=typer.colors.RED,
        err=True,
    )
    return True


def _effective_backend_settings(managed: ManagedConfig) -> dict[str, object]:
    """Comparable values for the settings owned by the backend snapshot."""
    return {
        "mode": resolve_mode(managed),
        "sessions": resolve_include_pipeline(False, managed),
        "detect_processes": bool(managed.get("detect_processes", False)),
        "detect_containers": bool(managed.get("detect_containers", False)),
        "detect_disguised_skills": bool(managed.get("detect_disguised_skills", False)),
        "project_depth": managed.get("project_depth", _DEFAULT_PROJECT_DEPTH),
        "project_timeout": managed.get("project_timeout", _DEFAULT_PROJECT_TIMEOUT),
        "daemon_enabled": bool(managed.get("daemon_enabled", False)),
        "llm_routing": bool(managed.get("llm_routing", False)),
        "llm_routing_base_url": managed.get("llm_routing_base_url", ""),
    }


def _submit_config_change_checkins(*, host: str, key: str) -> None:
    """Best-effort validation report after a backend config change."""
    try:
        from runlayer_cli.aiwatch_checkin import (  # noqa: PLC0415
            _make_device_context,
            submit_validation_checkins,
        )
        from runlayer_cli.api import RunlayerClient  # noqa: PLC0415
        from runlayer_cli.scan.device import get_installed_tools  # noqa: PLC0415

        ctx = _make_device_context()
        if not ctx["username"]:
            logger.warning("aiwatch_config_change_checkin_skipped_no_console_user")
            return
        submit_validation_checkins(
            RunlayerClient(hostname=host, secret=key),
            ctx=ctx,
            tools=get_installed_tools(),
        )
    except Exception as exc:
        # Refresh + reconciliation own the command outcome; reporting cannot
        # turn either a success or an existing local failure into another exit.
        logger.warning(
            "aiwatch_config_change_checkin_failed",
            error=str(exc),
            error_type=type(exc).__name__,
            exc_info=True,
        )


@hooks_app.callback(invoke_without_command=True)
def _hooks_callback(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


@app.command("config", hidden=True)
def configure_test_device(
    host: str = typer.Option(
        ...,
        "--host",
        "-H",
        help="Runlayer tenant host URL.",
    ),
    org_api_key: str = typer.Option(
        ...,
        "--org-api-key",
        help="Organization API key (rl_org_...).",
    ),
) -> None:
    """Configure a package-only macOS Test Device and reconcile hooks."""
    try:
        config_result = configure_aiwatch_test_device(host, org_api_key)
    except TestDeviceConfigError as exc:
        typer.secho(f"{FAIL} {exc}.", fg=typer.colors.RED, err=True)
        raise typer.Exit(EXIT_MISCONFIG) from None

    typer.secho(
        f"{OK} AI Watch configured at {AIWATCH_LOCAL_CONFIG_PATH}.",
        fg=typer.colors.GREEN,
        err=True,
    )
    exit_code = _reconcile_hooks(
        client=None,
        host=config_result["host"],
        mdm=True,
        all_events=False,
    )
    if not config_result["flushed"] and exit_code == EXIT_OK:
        exit_code = EXIT_PARTIAL_FAILURE
    if exit_code != EXIT_OK:
        typer.secho(
            f"{WARN} AI Watch configuration was written, but hook reconciliation "
            "is incomplete; the hourly bootstrap daemon will retry.",
            fg=typer.colors.YELLOW,
            err=True,
        )
        raise typer.Exit(exit_code)


def _reconcile_hooks(
    *,
    client: Optional[str],
    host: Optional[str],
    mdm: bool,
    all_events: bool,
) -> int:
    """Reconcile Runlayer hook configs and return the corresponding exit code."""
    scope = InstallScope.MDM if mdm else InstallScope.USER

    managed = read_managed_config()
    # Self-gate (MDM scope): with no managed OrgApiKey this deployment isn't
    # configured for hooks, so exit 0 silently before any host check. The
    # packaged bootstrap LaunchDaemon invokes this signed binary directly with
    # KeepAlive(SuccessfulExit=false); a non-zero exit on an unconfigured fleet
    # would relaunch every ThrottleInterval forever. This replaces the prior
    # `defaults read OrgApiKey || exit 0` shell wrapper in the plist (which
    # registered an unmanaged "sh" background item). --user (dev / manual) scope
    # is never gated.
    if scope == InstallScope.MDM and not managed.get("org_api_key"):
        return EXIT_OK

    effective_host = resolve_host(host)
    if not effective_host:
        typer.secho(
            f"{FAIL} no host configured (pass --host, set RUNLAYER_HOST, or push MDM Host).",
            fg=typer.colors.RED,
            err=True,
        )
        return EXIT_MISCONFIG

    config_changed = False
    restart_windows_service = False
    checkin_host = ""
    checkin_key = ""
    if scope == InstallScope.MDM:
        org_api_key = managed.get("org_api_key")
        managed_host = managed.get("host")
        if org_api_key and managed_host:
            normalized_managed_host = normalize_url(managed_host)
            initial_settings = _effective_backend_settings(managed)
            daemon_was_enabled = daemon_gate_open(managed)
            refreshed = sync_backend_config(
                host=normalized_managed_host,
                org_api_key=org_api_key,
            )
            managed = read_managed_config()
            restart_windows_service = (
                refreshed and not daemon_was_enabled and daemon_gate_open(managed)
            )
            config_changed = (
                refreshed and _effective_backend_settings(managed) != initial_settings
            )
            checkin_host = normalized_managed_host
            checkin_key = org_api_key

    targets = _targets_from_client(client)
    if not all_events and not resolve_install_hooks(managed):
        typer.secho(
            f"{OK} scan-only deployment (hooks and MCP usage metadata disabled); "
            "removing Runlayer hooks.",
            fg=typer.colors.GREEN,
            err=True,
        )
        any_failed = _uninstall_targets(targets, scope=scope)
        if scope == InstallScope.MDM:
            ext_failed, _ = _install_browser_extension_step(managed)
            # Keep the macOS supervisor installed for its hourly gate check.
            # Windows reconciliation removes the service while the gate is closed.
            daemon_failed, _ = _install_daemon_lifecycle_step(
                managed,
                restart_windows_service=restart_windows_service,
            )
            scan_failed, _ = _install_scan_lifecycle_step()
            any_failed = any_failed or ext_failed or daemon_failed or scan_failed
            if config_changed:
                _submit_config_change_checkins(
                    host=checkin_host,
                    key=checkin_key,
                )
        if any_failed:
            return EXIT_PARTIAL_FAILURE
        return EXIT_OK

    present, detail = credential_present(load_config(), effective_host, scope)
    if not present:
        typer.secho(
            f"{FAIL} no user credential for {effective_host} ({detail}). "
            "Run `aiwatch enroll` first (exit 4 = strict-ordering guardrail).",
            fg=typer.colors.RED,
            err=True,
        )
        # macOS-only soft-fail: the bootstrap LaunchDaemon's KeepAlive needs an
        # exit-0 to stop fast-retrying once the 10-min install window closes.
        # install_window_state() returns NO_STAMP off macOS, so Windows (and
        # everywhere else) always takes the strict exit-4 branch — the Windows
        # AIWatchHooks task has no KeepAlive, it just records LastTaskResult and
        # waits for the next hourly tick, so there is no retry storm to soften.
        if install_window_state() is InstallWindowState.OUTSIDE:
            return EXIT_OK
        return EXIT_NO_CREDENTIAL

    try:
        hook_command = resolve_hook_command()
    except FileNotFoundError as exc:
        typer.secho(
            f"{FAIL} cannot find aiwatch binary on disk: {exc}.",
            fg=typer.colors.RED,
            err=True,
        )
        return EXIT_MISCONFIG

    include_pipeline = resolve_include_pipeline(all_events, managed)
    metadata_only = not all_events and resolve_mcp_usage_metadata_only(managed)

    any_failed = False
    wrote_any = False
    for target in targets:
        try:
            result = install_client(
                target,
                scope=scope,
                include_pipeline=include_pipeline,
                metadata_only=metadata_only,
                hook_command=hook_command,
                skip_when_missing=True,
            )
        except ManagedPathError as exc:
            any_failed = True
            typer.secho(
                f"{FAIL} {target.value}: configuration invalid ({exc}).",
                fg=typer.colors.RED,
                err=True,
            )
            continue
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

    if scope == InstallScope.MDM:
        ext_failed, ext_wrote = _install_browser_extension_step(managed)
        daemon_failed, daemon_wrote = _install_daemon_lifecycle_step(
            managed,
            restart_windows_service=restart_windows_service,
        )
        scan_failed, scan_wrote = _install_scan_lifecycle_step()
        any_failed = any_failed or ext_failed or daemon_failed or scan_failed
        wrote_any = wrote_any or ext_wrote or daemon_wrote or scan_wrote

    if config_changed:
        _submit_config_change_checkins(
            host=checkin_host,
            key=checkin_key,
        )

    if any_failed:
        return EXIT_PARTIAL_FAILURE
    if not wrote_any:
        typer.secho(
            f"{WARN} no client config dirs detected; nothing to install.",
            fg=typer.colors.YELLOW,
            err=True,
        )
    return EXIT_OK


@hooks_app.command("install")
def install(
    client: Optional[str] = typer.Option(
        None,
        "--client",
        "-c",
        help=(
            "Configure a single client (cursor / vscode / claude_code / codex / "
            "hermes / goose / github-copilot-cli / windsurf); defaults to all "
            "installed."
        ),
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

    Desired settings resolve from the backend cache, then MDM managed config.
    Event/session hooks require resolved ``Sessions=true``; missing capability
    settings fail closed to no hooks. Monitor can instead install the
    metadata-only MCP profile when ``MCPUsageMetadata`` is true;
    ``--all-events`` forces the full profile.
    """
    # Retry-bounding applies only at this CLI boundary (the launchd bootstrap
    # daemon / AIWatchHooks task entrypoint): the Test Device flow calls
    # _reconcile_hooks directly so real failures are never mapped to exit 0
    # and don't touch the bootstrap failure counter.
    exit_code = _bootstrap_install_exit_code(
        InstallScope.MDM if mdm else InstallScope.USER,
        _reconcile_hooks(
            client=client,
            host=host,
            mdm=mdm,
            all_events=all_events,
        ),
    )
    if exit_code != EXIT_OK:
        raise typer.Exit(exit_code)


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
        drift = _check_absent(scope)
        if scope == InstallScope.MDM:
            drift = _check_browser_extension_step(managed) or drift
            drift = _check_daemon_lifecycle_step(managed) or drift
            drift = _check_scan_lifecycle_step() or drift
        if drift:
            raise typer.Exit(EXIT_DRIFT)
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
        metadata_only=resolve_mcp_usage_metadata_only(managed),
    )

    installed_results = [
        r for r in results if r.status != ClientStatus.CLIENT_NOT_INSTALLED
    ]
    drift = (
        _check_daemon_lifecycle_step(managed) if scope == InstallScope.MDM else False
    )
    if scope == InstallScope.MDM:
        drift = _check_browser_extension_step(managed) or drift
        drift = _check_scan_lifecycle_step() or drift
    if not installed_results:
        typer.secho(
            f"{WARN} no supported AI clients installed.",
            fg=typer.colors.YELLOW,
            err=True,
        )
        if drift:
            raise typer.Exit(EXIT_DRIFT)
        raise typer.Exit(EXIT_NO_CLIENTS)

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
