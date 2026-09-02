"""Single entrypoint for the AI Watch frozen executable (see cli/AGENTS.md).

One ``aiwatch`` binary serves both the typer CLI (scan / enroll / setup hooks /
bootstrap), the MCP guardrail hook, and the per-user hook daemon. The module top
stays standard-library-only so hot hook dispatch branches pay no CLI import tax.
"""

# Keep annotations eager so the callback can use the lazily imported typer.Context.
import os
import sys
import time
from pathlib import Path
from typing import Any

from runlayer_cli.hook import TRANSCRIPT_STREAM_WORKER_SENTINEL

# Earliest Python-side stamp for end-to-end hook latency: import of this
# entry module is the first thing a frozen `aiwatch` process executes, so
# everything after it (truststore, imports, dispatch) is startup overhead
# the in-hook flow timer cannot see. The Go shim's stamp (env var on exec
# fallback, frame field over IPC) is earlier still and wins when present.
_CLIENT_START_MS = int(time.time() * 1000)

HOOK_SUBCOMMAND = "hook"
DAEMON_SUBCOMMAND = "daemon"
DAEMON_STATUS_SUBCOMMAND = "status"
DAEMON_SERVICE_SUBCOMMAND = "daemon-service"
NATIVE_HOST_SUBCOMMAND = "native-host"
NATIVE_HOST_BASENAME = "aiwatch-native-messaging-host"

_app: Any | None = None


def _inject_truststore() -> None:
    from runlayer_cli.truststore_init import (  # noqa: PLC0415 - branch-local
        inject,
    )

    inject()


def _build_app() -> Any:
    """Build the typer surface lazily for non-hook invocations and tests."""
    global _app
    if _app is not None:
        return _app

    _inject_truststore()

    import typer  # noqa: PLC0415 - cold CLI branch only

    from runlayer_cli import __version__  # noqa: PLC0415
    from runlayer_cli.commands.aiwatch_config import (  # noqa: PLC0415
        app as aiwatch_config_app,
        update_now,
    )
    from runlayer_cli.commands.aiwatch_setup import (  # noqa: PLC0415
        app as aiwatch_setup_app,
    )
    from runlayer_cli.commands.aiwatch_update import self_update  # noqa: PLC0415
    from runlayer_cli.commands.auth import login, logout  # noqa: PLC0415
    from runlayer_cli.commands.bootstrap import bootstrap  # noqa: PLC0415
    from runlayer_cli.commands.enroll import enroll  # noqa: PLC0415
    from runlayer_cli.commands.logs import logs  # noqa: PLC0415
    from runlayer_cli.commands.org_api_key import (  # noqa: PLC0415
        app as org_api_key_app,
    )
    from runlayer_cli.commands.scan import app as scan_app  # noqa: PLC0415
    from runlayer_cli.tls import set_ca_bundle_path  # noqa: PLC0415

    built = typer.Typer(
        help="Runlayer AI Watch — scan and protect MCP client configurations"
    )

    def version_callback(value: bool) -> None:
        if value:
            typer.echo(f"aiwatch version {__version__}")
            raise typer.Exit()

    @built.callback(invoke_without_command=True)
    def root(
        ctx: typer.Context,
        version: bool | None = typer.Option(
            None,
            "--version",
            "-v",
            callback=version_callback,
            is_eager=True,
            help="Show version and exit.",
        ),
        ca_bundle: str | None = typer.Option(
            None,
            "--ca-bundle",
            help="Path to a PEM CA bundle for TLS inspection proxies.",
        ),
    ) -> None:
        set_ca_bundle_path(ca_bundle)
        if ctx.invoked_subcommand is None:
            typer.echo(ctx.get_help())
            raise typer.Exit()

    built.add_typer(scan_app, name="scan")
    built.add_typer(org_api_key_app, name="org-api-key", hidden=True)
    built.add_typer(aiwatch_setup_app, name="setup")
    built.add_typer(aiwatch_config_app, name="config")
    built.command(hidden=True)(login)
    built.command(hidden=True)(logout)
    built.command(hidden=True)(logs)
    built.command(hidden=True)(enroll)
    built.command(hidden=True)(bootstrap)
    built.command(name="self-update", hidden=True)(self_update)
    built.command(name="update-now")(update_now)
    _app = built
    return built


def __getattr__(name: str) -> Any:
    """Preserve ``from runlayer_cli.aiwatch import app`` without eager typer."""
    if name == "app":
        return _build_app()
    raise AttributeError(name)


def read_managed_config() -> Any:
    """Lazy compatibility seam for command tests and managed env injection."""
    from runlayer_cli.mdm_config import (  # noqa: PLC0415 - cold CLI branch only
        read_managed_config as read,
    )

    return read()


def _apply_managed_config() -> None:
    """Populate host/secret env vars from MDM-managed config (CLI flags / env still win)."""
    managed = read_managed_config()
    host = managed.get("host")
    org_api_key = managed.get("org_api_key")
    if host and not os.environ.get("RUNLAYER_HOST"):
        os.environ["RUNLAYER_HOST"] = host
    if org_api_key and not os.environ.get("RUNLAYER_API_KEY"):
        os.environ["RUNLAYER_API_KEY"] = org_api_key
    project_depth = managed.get("project_depth")
    if project_depth is not None and not os.environ.get("RUNLAYER_PROJECT_DEPTH"):
        os.environ["RUNLAYER_PROJECT_DEPTH"] = str(project_depth)
    project_timeout = managed.get("project_timeout")
    if project_timeout is not None and not os.environ.get("RUNLAYER_PROJECT_TIMEOUT"):
        os.environ["RUNLAYER_PROJECT_TIMEOUT"] = str(project_timeout)
    cpu_cores = managed.get("cpu_cores")
    if cpu_cores is not None and not os.environ.get("RUNLAYER_CPU_CORES"):
        os.environ["RUNLAYER_CPU_CORES"] = str(cpu_cores)
    max_cpu_percent = managed.get("max_cpu_percent")
    if max_cpu_percent is not None and not os.environ.get("RUNLAYER_MAX_CPU_PERCENT"):
        os.environ["RUNLAYER_MAX_CPU_PERCENT"] = str(max_cpu_percent)
    memory_limit_mb = managed.get("memory_limit_mb")
    if memory_limit_mb is not None and not os.environ.get("RUNLAYER_MEMORY_LIMIT_MB"):
        os.environ["RUNLAYER_MEMORY_LIMIT_MB"] = str(memory_limit_mb)
    detect_processes = managed.get("detect_processes")
    if detect_processes is not None and not os.environ.get("RUNLAYER_DETECT_PROCESSES"):
        os.environ["RUNLAYER_DETECT_PROCESSES"] = (
            "true" if detect_processes else "false"
        )
    detect_containers = managed.get("detect_containers")
    if detect_containers is not None and not os.environ.get(
        "RUNLAYER_DETECT_CONTAINERS"
    ):
        os.environ["RUNLAYER_DETECT_CONTAINERS"] = (
            "true" if detect_containers else "false"
        )
    detect_disguised_skills = managed.get("detect_disguised_skills")
    if detect_disguised_skills is not None and not os.environ.get(
        "RUNLAYER_DETECT_DISGUISED_SKILLS"
    ):
        os.environ["RUNLAYER_DETECT_DISGUISED_SKILLS"] = (
            "true" if detect_disguised_skills else "false"
        )
    artifact_lookup_cache = managed.get("artifact_lookup_cache")
    if artifact_lookup_cache is not None and not os.environ.get(
        "RUNLAYER_ARTIFACT_LOOKUP_CACHE"
    ):
        os.environ["RUNLAYER_ARTIFACT_LOOKUP_CACHE"] = (
            "true" if artifact_lookup_cache else "false"
        )
    detect_renamed_plugin_caches = managed.get("detect_renamed_plugin_caches")
    if detect_renamed_plugin_caches is not None and not os.environ.get(
        "RUNLAYER_DETECT_RENAMED_PLUGIN_CACHES"
    ):
        os.environ["RUNLAYER_DETECT_RENAMED_PLUGIN_CACHES"] = (
            "true" if detect_renamed_plugin_caches else "false"
        )


def main() -> None:
    from runlayer_cli.runtime import mark_aiwatch_runtime  # noqa: PLC0415

    mark_aiwatch_runtime()

    if len(sys.argv) >= 2 and sys.argv[1] == TRANSCRIPT_STREAM_WORKER_SENTINEL:
        _inject_truststore()
        from runlayer_cli.hook import _transcript_stream_worker  # noqa: PLC0415

        sys.argv = [sys.argv[0], *sys.argv[2:]]
        _transcript_stream_worker.main()
        return

    if Path(sys.argv[0]).stem == NATIVE_HOST_BASENAME or (
        len(sys.argv) >= 2 and sys.argv[1] == NATIVE_HOST_SUBCOMMAND
    ):
        _inject_truststore()
        from runlayer_cli.native_messaging import (  # noqa: PLC0415
            run_native_messaging_host,
        )

        raise SystemExit(run_native_messaging_host())

    if len(sys.argv) >= 2 and sys.argv[1] == HOOK_SUBCOMMAND:
        sys.argv = [sys.argv[0], *sys.argv[2:]]
        _run_hook_daemon_first()
        return

    if len(sys.argv) >= 2 and sys.argv[1] == DAEMON_SERVICE_SUBCOMMAND:
        from runlayer_cli.daemon.windows_service import run_service  # noqa: PLC0415

        exit_code = run_service()
        if exit_code:
            raise SystemExit(exit_code)
        return

    if len(sys.argv) >= 2 and sys.argv[1] == DAEMON_SUBCOMMAND:
        if len(sys.argv) >= 3:
            daemon_action = sys.argv[2]
            if daemon_action == DAEMON_STATUS_SUBCOMMAND:
                from runlayer_cli.daemon.status import run_status  # noqa: PLC0415

                raise SystemExit(run_status())
            sys.stderr.write("Usage: aiwatch daemon [status]\n")
            raise SystemExit(0 if daemon_action in {"--help", "-h"} else 2)
        _inject_truststore()
        _apply_managed_config()
        from runlayer_cli.command_metrics import (  # noqa: PLC0415
            run_with_command_metrics,
        )
        from runlayer_cli.daemon.server import run_daemon  # noqa: PLC0415

        # Only survivable exits flush this metric; supervisor kills, logoff,
        # SIGTERM, and crashes do not. It is diagnostics, not a liveness SLO.
        run_with_command_metrics(run_daemon)
        return

    _inject_truststore()
    _apply_managed_config()

    # Best-effort per-command perf telemetry (command time, CPU, peak memory).
    # Deferred import keeps it off the fast hook-dispatch branches above.
    from runlayer_cli.command_metrics import (  # noqa: PLC0415
        run_with_command_metrics,
    )

    run_with_command_metrics(_build_app())


def _client_start_ms() -> int:
    """Shim env stamp when exec'd as its fallback, else this module's import stamp."""
    from runlayer_cli.hook.daemon_protocol import (  # noqa: PLC0415 - stdlib-only
        CLIENT_START_ENV,
    )

    value = os.environ.get(CLIENT_START_ENV, "")
    try:
        parsed = int(value)
    except ValueError:
        parsed = 0
    return parsed if parsed > 0 else _CLIENT_START_MS


def _run_hook_daemon_first() -> None:
    """Use daemon IPC when gated on; preserve consumed stdin for inline fallback."""
    from runlayer_cli.hook import daemon_client  # noqa: PLC0415 - stdlib-only

    client_start_ms = _client_start_ms()
    stdin_text: str | None = None
    stdin_error: BaseException | None = None
    response = None
    try:
        daemon_enabled = daemon_client.daemon_is_enabled()
    except Exception:
        daemon_enabled = False
    if daemon_enabled:
        try:
            stdin_text = sys.stdin.read()
        except Exception as exc:
            stdin_error = exc
        else:
            response = daemon_client.try_daemon_hook(
                stdin_text,
                client_start_ms=client_start_ms,
                _gate_checked=True,
            )

    if response is not None:
        sys.stdout.write(response["stdout"])
        sys.stdout.flush()
        sys.stderr.write(response["stderr"])
        sys.stderr.flush()
        raise SystemExit(response["exit_code"])

    _inject_truststore()
    from runlayer_cli.hook import hook_io  # noqa: PLC0415
    from runlayer_cli.hook.dispatch import run_hook  # noqa: PLC0415

    if stdin_text is None and stdin_error is None:
        with hook_io.scoped(hook_io.HookIO(client_start_ms=client_start_ms)):
            run_hook()
        return

    # stdin is spent either way: replay the text we read, or the failure that
    # consumed an unknown prefix of it. Re-reading would hand the hook a
    # truncated payload to decide on.
    with hook_io.scoped(
        hook_io.HookIO(
            stdin_text=stdin_text,
            stdin_error=stdin_error,
            daemon_fallback=daemon_enabled and stdin_text is not None,
            client_start_ms=client_start_ms,
        )
    ):
        run_hook()


if __name__ == "__main__":
    main()
