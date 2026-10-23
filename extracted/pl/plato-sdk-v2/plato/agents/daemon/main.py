"""``plato-agent-daemon`` entry point.

Subcommands:
  serve   — run the RPC daemon (foreground under systemd; ``--daemonize`` for
            the world's bootstrap SSH, which self-daemonizes via double-fork).
  status  — check whether a daemon is already running (pidfile + /healthz).

``serve`` is idempotent: if a live daemon is already bound, it exits 0 without
starting a second one, so the world's bootstrap SSH command can be re-run
safely. The pidfile is claimed only after the port is bound, so a losing racer
never clobbers the live daemon's pidfile.
"""

from __future__ import annotations

import argparse
import asyncio
import errno
import os
import secrets
import signal
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


def _mint_token_if_missing(token_path: Path) -> None:
    """Boot-time mint: write a fresh random token unless one already exists.

    O_EXCL, so a token delivered concurrently by a world bootstrap is adopted,
    never clobbered — whichever writer wins, both sides read the same file.
    """
    token_path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    try:
        fd = os.open(str(token_path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        return
    try:
        os.write(fd, secrets.token_urlsafe(32).encode())
    finally:
        os.close(fd)


def _serve(args: argparse.Namespace) -> int:
    state_dir = Path(args.state_dir)
    pid_path = state_dir / "daemon.pid"

    if _already_running(pid_path):
        # Idempotent bootstrap: a live daemon already owns the port.
        return 0

    if args.mint_token:
        _mint_token_if_missing(Path(args.token_file))
    token = read_token_file(Path(args.token_file))

    if args.daemonize:
        _daemonize()
    if args.daemonize or not sys.stdout.isatty():
        # Bootstrap-started (daemonized) and systemd-started (foreground, no
        # tty) daemons both log to daemon.log — the bootstrap's diagnostics
        # tail that file on a failed start, whichever way the daemon came up.
        _redirect_stdio(Path(args.log_file))

    state_dir.mkdir(parents=True, exist_ok=True)
    app = build_app(state_dir=state_dir, token=token)
    return asyncio.run(_serve_app(app, host=args.bind, port=args.port, pid_path=pid_path))


def _redirect_stdio(log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_fd = os.open(str(log_path), os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    os.dup2(log_fd, sys.stdout.fileno())
    os.dup2(log_fd, sys.stderr.fileno())


async def _serve_app(app: web.Application, *, host: str, port: int, pid_path: Path) -> int:
    """Bind, THEN claim the pidfile, then serve until SIGTERM/SIGINT.

    The pidfile is written only after the listening socket is bound: a second
    ``serve`` racing a live daemon for the port used to overwrite the live
    daemon's pidfile before failing on EADDRINUSE, then unlink it on the way
    out — leaving the live daemon invisible to ``_already_running`` so every
    later ``serve`` (systemd restarts included) repeated the collision.
    """
    runner = web.AppRunner(app)
    await runner.setup()
    try:
        await web.TCPSite(runner, host, port).start()
    except OSError as exc:
        await runner.cleanup()
        if exc.errno == errno.EADDRINUSE and await _winner_claimed(pid_path):
            return 0  # lost the bind race to a live daemon: same idempotent exit as the pidfile check
        raise
    pid_path.write_text(str(os.getpid()))
    stop = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, stop.set)
    try:
        await stop.wait()
    finally:
        await runner.cleanup()
        try:
            if _read_pidfile(pid_path) == os.getpid():
                pid_path.unlink()
        except OSError:
            pass
    return 0


async def _winner_claimed(pid_path: Path, wait_s: float = 2.0) -> bool:
    """Whether a live daemon claims the pidfile within ``wait_s`` (it writes it right after binding)."""
    deadline = asyncio.get_running_loop().time() + wait_s
    while not _already_running(pid_path):
        if asyncio.get_running_loop().time() > deadline:
            return False
        await asyncio.sleep(0.1)
    return True


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
    serve.add_argument(
        "--mint-token",
        action="store_true",
        help="Mint the token file if absent (boot-time start, before any world contact)",
    )
    serve.set_defaults(func=_serve)

    status = sub.add_parser("status", help="Check if a daemon is running")
    status.add_argument("--state-dir", default=STATE_DIR)
    status.set_defaults(func=_status)

    args = parser.parse_args()
    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()
