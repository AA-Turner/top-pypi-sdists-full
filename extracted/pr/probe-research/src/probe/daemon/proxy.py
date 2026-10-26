"""`probe daemon worker` started by an old tap: its session's run goes to the daemon host (plan P1).

A tap older than 0.10.5 (and a `tap watch` the service does not host) spawns
`probe daemon worker` itself and supervises that process by its exit codes. This
process stays what the tap expects -- the same command line, alive exactly as
long as the run, SIGTERM meaning "finish your queue", its exit code the run's --
but the work runs in the Probe service's daemon host instead of a ~150 MB process
of its own:

    tap supervisor --spawns--> proxy (stdlib, ~20 MB) --host.sock--> daemon host
                                 SIGTERM/SIGINT -> stop          the run (this connection owns it)
                                 its parent gone -> it leaves    the run's owner is gone
                                 exited {code}  -> that code     <-

`main` returns None when there is no host to reach (no service, an older one,
the host off, Windows): `probe daemon worker` then runs the worker in this
process, as before. A worker the service starts itself as a process (its own
fallback when the host is unavailable: it names itself its supervisor) is never
sent back to the host.

Stdlib only: imported before the CLI (`probe._entry`).
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import select
import signal
import socket
import sys
import time
import uuid
from pathlib import Path

#: `probe.daemon.worker.SUPERVISOR_PID_ENV` / `ENTER_CWD_ENV`: set on every worker
#: process the service starts itself.
SUPERVISOR_PID_ENV = "PROBE_DAEMON_SUPERVISOR"
ENTER_CWD_ENV = "PROBE_DAEMON_ENTER_CWD"
KILL_ENV = "PROBE_DAEMON_HOST"
#: `server.DAEMON_HOST_METHOD`.
METHOD = "daemon.host"
ASK_S = 15.0
ACK_S = 10.0


#: `worker.EXIT_CRASHED`: what a per-process worker exits with after a crash (a test keeps them equal).
EXIT_CRASHED = 4


def eligible(env: dict | None = None) -> bool:
    env = os.environ if env is None else env
    if os.name != "posix":
        return False
    if (env.get(KILL_ENV) or "").strip().lower() in ("off", "0", "false", "no"):
        return False
    return not env.get(SUPERVISOR_PID_ENV) and env.get(ENTER_CWD_ENV) != "1"


def _address() -> dict | None:
    """Where the service's daemon host listens (started if need be), or None."""
    try:
        from probe import __version__
        from probe.service import client
    except Exception:  # noqa: BLE001 -- no service client: in-process
        return None
    try:
        with client.Connection.open(1.0) as conn:
            conn.hello("cli", str(__version__))
            conn.sock.settimeout(ASK_S)
            answer = conn.call(METHOD, {})
    except Exception:  # noqa: BLE001 -- no service, an older one, a refusal: in-process
        return None
    if not isinstance(answer, dict) or not isinstance(answer.get("socket"), str):
        return None
    return answer


def _default_source() -> str:
    """The default `--source`: the registry's default harness, which the worker's
    own parser names too (a test keeps them equal)."""
    from probe.harness import registry

    return registry.load().default


def _daemon_dir() -> Path:
    xdg = os.environ.get("XDG_STATE_HOME")
    base = Path(xdg) if xdg else Path.home() / ".local" / "state"
    return base / "probe" / "daemon"


def _readline(sock: socket.socket, buf: bytearray, timeout: float) -> dict | None:
    """The next message within `timeout`, or None (nothing yet). EOFError: closed."""
    end = time.monotonic() + timeout
    while b"\n" not in buf:
        left = end - time.monotonic()
        if left <= 0:
            return None
        ready, _, _ = select.select([sock], [], [], left)
        if not ready:
            return None
        chunk = sock.recv(65536)
        if not chunk:
            raise EOFError
        buf += chunk
    line, _, rest = bytes(buf).partition(b"\n")
    buf[:] = rest
    try:
        msg = json.loads(line)
    except ValueError:
        return {}
    return msg if isinstance(msg, dict) else {}


def main(argv: list[str]) -> int | None:
    parser = argparse.ArgumentParser(prog="probe daemon worker")
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--transcript", required=True)
    parser.add_argument("--cwd", required=True)
    parser.add_argument("--source", default=None)
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return None  # the CLI's own parser says what was wrong
    if not eligible():
        return None
    parent = os.getppid()
    address = _address()
    if address is None:
        return None
    try:
        from probe.service import paths

        paths.require_private(Path(address["socket"]).parent)  # never a listener in a folder another user made
    except (OSError, ImportError):
        return None
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    buf = bytearray()
    try:
        sock.settimeout(ACK_S)
        sock.connect(address["socket"])
        sock.sendall(b'{"op":"hello","role":"proxy"}\n')
        hello = _readline(sock, buf, ACK_S)
        if not hello or hello.get("op") != "hello" or (address.get("pid") and hello.get("pid") != address["pid"]):
            sock.close()
            return None
        run_id = uuid.uuid4().hex
        cwd = os.path.abspath(args.cwd)
        start = {"op": "start", "run": run_id, "sid": args.session_id, "transcript": os.path.abspath(args.transcript),
                 "cwd": cwd, "source": args.source or _default_source(), "daemon_dir": str(_daemon_dir()),
                 "env": dict(os.environ)}
        sock.sendall((json.dumps(start, separators=(",", ":")) + "\n").encode())
        answer = _readline(sock, buf, ACK_S)
    except (OSError, EOFError):
        with contextlib.suppress(OSError):
            sock.close()
        return None
    if not answer:
        sock.close()
        return None
    if answer.get("op") == "exited":
        # Refused before it ran (a host that takes no new run, a stale one, a start
        # it found invalid): this worker runs in-process instead, never an exit code
        # the old tap would act on (0 respawns into the same host, 2 gives up).
        sock.close()
        return None
    if answer.get("op") != "started":
        sock.close()
        return None
    stop = {"asked": False}

    def _stop(_sig, _frame) -> None:
        stop["asked"] = True

    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)
    sent_stop = False
    print(f"probe daemon worker: session {args.session_id} runs in the daemon host (pid {hello.get('pid')})",
          file=sys.stderr)
    try:
        while True:
            if stop["asked"] and not sent_stop:
                sock.sendall((json.dumps({"op": "stop", "run": run_id}) + "\n").encode())
                sent_stop = True
            if os.getppid() != parent:
                return 0  # its supervisor is gone: closing tells the run so (the run's owner left)
            try:
                msg = _readline(sock, buf, 1.0)
            except InterruptedError:
                continue
            if msg and msg.get("op") == "exited" and msg.get("run") == run_id:
                code = msg.get("code")
                return code if isinstance(code, int) else 0
    except (OSError, EOFError):
        # The host went away under the run. After a stop it had nothing left to do;
        # else it died with the run going, maybe of this run: a crash, so the tap
        # backs this session off instead of starting it into the next host at once
        # (a run that kills its host would otherwise take every session down again).
        return 0 if sent_stop else EXIT_CRASHED
    finally:
        with contextlib.suppress(OSError):
            sock.close()
