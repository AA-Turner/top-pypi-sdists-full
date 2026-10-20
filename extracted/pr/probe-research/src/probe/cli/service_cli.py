"""`probe service ...`: the machine-wide Probe service, by hand (plan T3).

    probe service status [--json]   is it running; its sessions, state and pid
    probe service start             start it (whatever PROBE_SERVICE says) and
                                    wait up to 2 s for it to answer
    probe service stop              ask it to stop now
    probe service check-now         ask it to check for updates now (starting it if
                                    needed): what the plugin hook runs instead of
                                    an updater of its own while the switch is on

Thin on purpose: everything is `probe.service.client` over the socket, the
same calls a tap or the desktop app makes. The service itself never starts
through this CLI (`python -m probe.service`, stdlib only, plan S1).
"""

from __future__ import annotations

import json
import os
import sys
import time

import typer

service_app = typer.Typer(
    no_args_is_help=True,
    help="the machine-wide Probe service (one per user; started by agent sessions, exits when idle)",
)

#: `probe service start` waits this long for the new service to answer.
START_WAIT_S = 2.0
#: `probe service stop` waits this long for it to be gone.
STOP_WAIT_S = 2.0


def _version() -> str:
    from probe import __version__

    return __version__


def _status() -> dict | None:
    from probe.service import client
    from probe.service.protocol import Client, Method

    try:
        answer = client.call(Method.STATUS, client=Client.CLI, client_version=_version())
    except OSError:
        return None
    return answer if isinstance(answer, dict) else None


@service_app.command("status")
def status_cmd(
    as_json: bool = typer.Option(False, "--json", help="service.status as one JSON object"),
) -> None:
    """Is the Probe service running here, and what does it hold? Exit 1 when it is not running."""
    from probe.service import paths

    status = _status()
    if as_json:
        typer.echo(json.dumps(status if status is not None else {"running": False}))
    elif status is None:
        typer.echo(f"probe service: not running (socket {paths.socket_path()})")
    else:
        typer.echo(
            f"probe service {status.get('service_version')}: {status.get('state')}, pid {status.get('pid')}, "
            f"{status.get('sessions')} live session(s), {status.get('app_clients')} app window(s)"
        )
        typer.echo(f"  updates: {update_line(status.get('update'))}")
    if status is None:
        raise typer.Exit(1)


def _when(epoch: object) -> str:
    if not isinstance(epoch, (int, float)) or isinstance(epoch, bool):
        return "never"
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(epoch))


def update_line(update: object) -> str:
    """The updater's state in one line (`service.status`'s `update`)."""
    if not isinstance(update, dict):
        return "unknown"
    if update.get("in_progress"):
        step = update.get("step") or "starting"
        return f"updating now ({step})"
    parts = []
    if not update.get("enabled"):
        parts.append("automatic updates off")
    last = update.get("last_result")
    if isinstance(last, dict):
        verdict = "ok" if last.get("ok") else "failed"
        parts.append(f"last check {_when(update.get('last_check'))} ({verdict})")
    else:
        parts.append(f"last check {_when(update.get('last_check'))}")
    deferred = update.get("deferred")
    if isinstance(deferred, dict):
        parts.append(f"deferred {_when(deferred.get('at'))}: {deferred.get('reason')}")
    if update.get("enabled") and update.get("next_check") is not None:
        parts.append(f"next {_when(update.get('next_check'))}")
    return ", ".join(parts)


@service_app.command("start")
def start_cmd() -> None:
    """Start the Probe service if it is not running, and wait for it to answer."""
    from probe.service import client, paths

    record_runtime(force=True)
    outcome = client.ensure(wait=START_WAIT_S)
    status = _status()
    if status is None:
        typer.echo(f"probe service: did not start ({outcome}); see {paths.log_path()}", err=True)
        raise typer.Exit(1)
    typer.echo(f"probe service: {status.get('state')}, pid {status.get('pid')}")


@service_app.command("stop")
def stop_cmd() -> None:
    """Ask the Probe service to stop now. Agent sessions start it again when they need it."""
    from probe.service import client
    from probe.service.protocol import Client, Method

    try:
        client.call(Method.STOP, client=Client.CLI, client_version=_version())
    except OSError:
        typer.echo("probe service: not running")
        return
    except client.ServiceError as exc:
        typer.echo(f"probe service: refused to stop: {exc.message}", err=True)
        raise typer.Exit(1) from None
    deadline = time.monotonic() + STOP_WAIT_S
    while time.monotonic() < deadline and _status() is not None:
        time.sleep(0.05)
    typer.echo("probe service: stopped")


@service_app.command("check-now")
def check_now_cmd(
    trigger: str = typer.Option("cli", "--trigger", help="what asks: app, cli, session or schedule"),
) -> None:
    """Ask the Probe service to check for updates now, starting it if needed.

    Applied only while automatic updates are on, and only on a quiet machine
    (no daemon recording, no run, no setup): otherwise it is deferred.
    """
    from probe.service import client
    from probe.service.protocol import CHECK_TRIGGERS

    if trigger not in CHECK_TRIGGERS:
        raise typer.BadParameter(f"--trigger must be one of {', '.join(sorted(CHECK_TRIGGERS))}")
    try:
        answer = client.check_now(trigger, client_version=_version())
    except OSError:
        typer.echo("probe service: not running and could not be started", err=True)
        raise typer.Exit(1) from None
    except client.ServiceError as exc:
        typer.echo(f"probe service: {exc.message}", err=True)
        raise typer.Exit(1) from None
    outcome = answer.get("outcome")
    reason = answer.get("reason")
    typer.echo(f"probe service: update check {outcome}" + (f" ({reason})" if reason else ""))


def record_runtime(*, force: bool = False) -> None:
    """Write `runtime.json` (`{"python", "cli_version"}`) when this CLI runs from
    its uv tool env, so a tap or pi can spawn the service with the CLI's own
    interpreter (plan X2). One small read when nothing changed; never raises.

    `force` (`probe service start`, run on purpose) also records a checkout's or
    a venv's interpreter, but only where no usable one is recorded: the uv tool
    env's own CLI runs rewrite it on their next start either way.
    """
    try:
        prefix = sys.prefix.replace(os.sep, "/")
        from_tool_env = "/uv/tools/probe-research" in prefix
        if not from_tool_env and not force:
            return
        from probe.service import client

        if not from_tool_env and client.runtime_python() is not None:
            return
        client.write_runtime(sys.executable, _version())
    except Exception:  # noqa: BLE001 -- a missing runtime.json only means the fallback path
        pass
