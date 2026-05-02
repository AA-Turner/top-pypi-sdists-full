"""Standalone cron scheduler daemon command."""

from __future__ import annotations

from argparse import ArgumentParser, Namespace, SUPPRESS
from pathlib import Path
from types import SimpleNamespace
from typing import Sequence

from apps.gateway.cron_service import build_cron_scheduler_service
from apps.gateway.gateway_main_runtime import (
    _gateway_runtime_environ,
    _run_logs,
    _run_restart,
    _run_start_detached,
    _run_status,
    _run_stop,
)
from apps.runtime_layout import (
    default_cli_state_dir,
    default_gateway_state_dir,
    default_profile_dir as runtime_default_profile_dir,
)


def command_main(
    argv: Sequence[str] | None = None,
    *,
    default_profile_dir: Path | None = None,
    default_state_dir: Path | None = None,
    default_control_profile_dir: Path | None = None,
    default_control_state_dir: Path | None = None,
) -> int:
    defaults = {
        "profile_dir": default_profile_dir or runtime_default_profile_dir(),
        "state_dir": default_state_dir or default_gateway_state_dir(),
        "cli_profile_dir": default_control_profile_dir or runtime_default_profile_dir(),
        "cli_state_dir": default_control_state_dir or default_cli_state_dir(),
    }
    parser = _build_parser(defaults=defaults)
    resolved_argv = list(argv) if argv is not None else None
    if resolved_argv == []:
        resolved_argv = ["status"]
    args = parser.parse_args(resolved_argv)
    action = getattr(args, "command_action", None) or "status"
    service = _build_service(args)
    if action == "status":
        return _run_status(args, service=service)
    if action == "stop":
        return _run_stop(args, service=service)
    if action == "restart":
        return _run_restart(args, service=service)
    if action == "logs":
        return _run_logs(args, service=service)
    if action == "run":
        return int(
            service.run_scheduler(
                interval_seconds=float(args.interval_seconds),
                once=bool(getattr(args, "once", False)),
            )
            or 0
        )
    target = service.configured_runtime_target()
    if getattr(args, "detach", False):
        return _run_start_detached(args, service=service, target=target)
    return int(service.run_scheduler(interval_seconds=float(args.interval_seconds), once=False) or 0)


def _build_parser(*, defaults: dict[str, Path]) -> ArgumentParser:
    common = ArgumentParser(add_help=False)
    common.add_argument("--profile-dir", type=Path, default=defaults["profile_dir"])
    common.add_argument("--state-dir", type=Path, default=defaults["state_dir"])
    common.add_argument("--cli-profile-dir", type=Path, default=defaults["cli_profile_dir"])
    common.add_argument("--cli-state-dir", type=Path, default=defaults["cli_state_dir"])
    common.add_argument("--workspace-id", default="workspace:gateway")

    parser = ArgumentParser(prog="aegis cron", description="Manage the Aegis cron scheduler daemon.")
    subparsers = parser.add_subparsers(dest="command")

    start = subparsers.add_parser("start", parents=[common], help="Start the cron scheduler.")
    _add_start_options(start)
    start.set_defaults(command_action="start")

    run = subparsers.add_parser("run", parents=[common], help="Run the cron scheduler in the foreground.")
    _add_start_options(run)
    run.add_argument("--once", action="store_true", help="Run one scheduler tick and exit.")
    run.set_defaults(command_action="run", detach=False)

    status = subparsers.add_parser("status", parents=[common], help="Show cron scheduler status.")
    _add_target_options(status)
    status.set_defaults(command_action="status")

    stop = subparsers.add_parser("stop", parents=[common], help="Stop the cron scheduler.")
    _add_stop_options(stop)
    stop.set_defaults(command_action="stop")

    restart = subparsers.add_parser("restart", parents=[common], help="Restart the cron scheduler.")
    _add_start_options(restart)
    restart.add_argument("--timeout", type=float, default=10.0, help=SUPPRESS)
    restart.add_argument("--force", action="store_true", help=SUPPRESS)
    restart.set_defaults(command_action="restart", detach=True)

    logs = subparsers.add_parser("logs", parents=[common], help="Show cron scheduler logs.")
    _add_logs_options(logs)
    logs.set_defaults(command_action="logs")
    parser.set_defaults(command_action="status")
    return parser


def _add_target_options(parser: ArgumentParser) -> None:
    parser.set_defaults(runtime_target="scheduler")
    parser.add_argument("--target", dest="runtime_target", choices=("configured", "scheduler"), default="scheduler", help=SUPPRESS)


def _add_start_options(parser: ArgumentParser) -> None:
    _add_target_options(parser)
    parser.add_argument("--detach", action="store_true", help="Start in a background process and return immediately.")
    parser.add_argument("--interval-seconds", type=float, default=60.0, help="Seconds between scheduler ticks.")


def _add_stop_options(parser: ArgumentParser) -> None:
    _add_target_options(parser)
    parser.add_argument("--timeout", type=float, default=10.0, help="Seconds to wait before failing or forcing.")
    parser.add_argument("--force", action="store_true", help="Send SIGKILL when the process does not exit.")


def _add_logs_options(parser: ArgumentParser) -> None:
    _add_target_options(parser)
    parser.add_argument("--tail", type=int, default=80, help="Show the last N log lines.")
    parser.add_argument("--follow", action="store_true", help="Keep streaming appended log output.")
    parser.add_argument("--path", action="store_true", help="Print the resolved log file path and exit.")


def _build_service(args: Namespace):
    args.state_dir.mkdir(parents=True, exist_ok=True)
    app = SimpleNamespace(profile_dir=str(args.profile_dir), state_dir=str(args.state_dir))
    return build_cron_scheduler_service(
        app=app,
        default_cli_profile_dir=str(args.cli_profile_dir),
        default_cli_state_dir=str(args.cli_state_dir),
        environ=_gateway_runtime_environ(args.state_dir, cli_state_dir=args.cli_state_dir),
        runtime_state_dir=args.state_dir,
    )


def main(argv: Sequence[str] | None = None) -> int:
    return command_main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
