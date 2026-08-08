"""``plato-agent-daemon`` entry point.

Subcommands:
  serve   — run the RPC daemon (optionally self-daemonizing via double-fork).
  status  — check whether a daemon is already running (pidfile + /healthz).

``serve --daemonize`` is idempotent: if a live daemon is already bound, it
exits 0 without starting a second one, so the world's bootstrap SSH command can
be re-run safely.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from aiohttp import web

from plato.agents.daemon.app import build_app
from plato.agents.daemon.state import read_token_file
from plato.rpc.protocol import (
    DEFAULT_PORT,
    LOG_FILE,
    STATE_DIR,
    TOKEN_FILE,
)


def _pid_is_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _read_pidfile(pid_path: Path) -> int | None:
    try:
        pid = int(pid_path.read_text().strip())
    except (OSError, ValueError):
        return None
    return pid if _pid_is_alive(pid) else None


def _already_running(pid_path: Path) -> bool:
    return _read_pidfile(pid_path) is not None


def _daemonize() -> None:
    """Double-fork + setsid so the daemon survives its SSH parent closing."""
    if os.fork() > 0:
        os._exit(0)
    os.setsid()
    if os.fork() > 0:
        os._exit(0)
    sys.stdin.close()


def _serve(args: argparse.Namespace) -> int:
    state_dir = Path(args.state_dir)
    pid_path = state_dir / "daemon.pid"

    if _already_running(pid_path):
        # Idempotent bootstrap: a live daemon already owns the port.
        return 0

    token = read_token_file(Path(args.token_file))

    if args.daemonize:
        _daemonize()
        log_path = Path(args.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_fd = os.open(str(log_path), os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
        os.dup2(log_fd, sys.stdout.fileno())
        os.dup2(log_fd, sys.stderr.fileno())

    state_dir.mkdir(parents=True, exist_ok=True)
    pid_path.write_text(str(os.getpid()))
    try:
        app = build_app(state_dir=state_dir, token=token)
        web.run_app(app, host=args.bind, port=args.port, print=None)
    finally:
        try:
            if _read_pidfile(pid_path) == os.getpid():
                pid_path.unlink()
        except OSError:
            pass
    return 0


def _status(args: argparse.Namespace) -> int:
    pid = _read_pidfile(Path(args.state_dir) / "daemon.pid")
    if pid is None:
        print("stopped")
        return 1
    print(f"running pid={pid}")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(prog="plato-agent-daemon")
    sub = parser.add_subparsers(dest="command", required=True)

    serve = sub.add_parser("serve", help="Run the agent RPC daemon")
    serve.add_argument("--port", type=int, default=DEFAULT_PORT)
    serve.add_argument("--bind", default="0.0.0.0")
    serve.add_argument("--token-file", default=TOKEN_FILE)
    serve.add_argument("--state-dir", default=STATE_DIR)
    serve.add_argument("--log-file", default=LOG_FILE)
    serve.add_argument("--daemonize", action="store_true")
    serve.set_defaults(func=_serve)

    status = sub.add_parser("status", help="Check if a daemon is running")
    status.add_argument("--state-dir", default=STATE_DIR)
    status.set_defaults(func=_status)

    args = parser.parse_args()
    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()
