"""The console's Station tab IS hugpy-fleet: a PTY running the real
`hugpy-fleet tui` in tmux, drawn by xterm.js over a websocket.

The Core arm hosts the shared terminal (`hugpy-fleet tui --base <this Core>`)
inside the named tmux session `hugpy-fleet`. The browser only
attaches a terminal client; closing it leaves that session running. Its journal
is Core's own /var/lib/hugpy-core/station directory. An explicit
HUGPY_STATION_WORKSPACE can share a journal; no Agent service is required.
Core owns only the terminal bridge:

    WS  /api/station/term?cols=&rows=     one tmux client per socket, as Core
    text frames  browser -> keystrokes; server -> terminal output (utf-8)
    "\\x00resize:<cols>x<rows>"            a resize control frame from the browser

Settings: HUGPY_STATION_FLEET_BIN (default the bundled Core venv command,
then /opt/hugpy-fleet/venv/bin/hugpy-fleet or PATH), HUGPY_STATION_FLEET_URL (else
HUGPY_CORE_URL, then http://127.0.0.1:7020), HUGPY_STATION_WORKSPACE (default /var/lib/hugpy-core/station),
HUGPY_STATION_SERVE_URL (set it to run the TUI as a client of a session server
instead — remote boxes). Access is the management gate the toolserver relay
uses (`KEYS.check(..., 'admin')`): a terminal is operator surface. The public
host adds its own auth_request in front, like it did for the station's old
wsterm.
"""
from __future__ import annotations

import fcntl
import logging
import os
import pty
import select
import shutil
import signal
import struct
import subprocess
import sys
import termios
import threading
from pathlib import Path

from flask import request

logger = logging.getLogger("hugpy_core.station_term")

DEFAULT_BIN = "/opt/hugpy-fleet/venv/bin/hugpy-fleet"
DEFAULT_FLEET = "http://127.0.0.1:7020"                  # this Core: the TUI's inference endpoint
FALLBACK_WORKSPACE = "/var/lib/hugpy-core/station"
RESIZE = "\x00resize:"
_LIVE = {"count": 0}
MAX_TERMINALS = 8


def harness_bin() -> str:
    pinned = (os.environ.get("HUGPY_STATION_FLEET_BIN") or os.environ.get("HUGPY_STATION_HARNESS_BIN", "")).strip()
    if pinned:
        return pinned
    bundled = str(Path(sys.executable).with_name('hugpy-fleet'))
    if os.access(bundled, os.X_OK):
        return bundled
    if os.access(DEFAULT_BIN, os.X_OK):
        return DEFAULT_BIN
    return shutil.which("hugpy-fleet") or DEFAULT_BIN


def fleet_url() -> str:
    return (os.environ.get("HUGPY_STATION_FLEET_URL") or os.environ.get("HUGPY_CORE_URL") or DEFAULT_FLEET).rstrip("/")


def serve_url() -> str:
    """Set HUGPY_STATION_SERVE_URL to run the TUI as a CLIENT of a session
    server instead (remote boxes). Unset = the harness in-process, the way it is."""
    return (os.environ.get("HUGPY_STATION_SERVE_URL") or "").rstrip("/")


def workspace() -> str:
    """Core owns its Harness journal; an explicit workspace can share sessions."""
    pinned = os.environ.get("HUGPY_STATION_WORKSPACE")
    if pinned:
        return pinned
    return FALLBACK_WORKSPACE


def tui_argv() -> list[str]:
    if serve_url():
        return [harness_bin(), "tui", "--serve", serve_url(), "--workspace", workspace()]
    return [harness_bin(), "tui", "--base", fleet_url(), "--workspace", workspace()]


def tmux_argv() -> list[str]:
    socket = os.environ.get("HUGPY_STATION_TMUX_SOCKET") or "/var/lib/hugpy-core/station-tmux.sock"
    return [shutil.which("tmux") or "tmux", "-S", socket, "new-session", "-A",
            "-s", "hugpy-fleet", "-c", workspace(), *tui_argv()]


def _winsize(fd: int, cols: int, rows: int) -> None:
    cols, rows = max(20, min(int(cols), 500)), max(5, min(int(rows), 200))
    fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", rows, cols, 0, 0))


def _spawn(cols: int, rows: int):
    """Fork the TUI on a fresh PTY -> (pid, master fd)."""
    ws = Path(workspace())
    ws.mkdir(parents=True, exist_ok=True, mode=0o770)
    argv = tmux_argv()
    core_env = os.environ
    env = {k: v for k, v in os.environ.items() if not k.startswith(("HUGPY_CORE_", "SOLCATCHER_", "HUGPY_ROUTER_"))}
    env.update(TERM="xterm-256color", COLORTERM="truecolor", LANG=env.get("LANG") or "C.UTF-8",
               HOME=env.get("HOME") or "/var/lib/hugpy-core",
               HUGPY_FLEET_URL=fleet_url())
    # Reuse Core's pre-split journal without moving or rewriting its history.
    if (ws / '.hugpy_wrapper/chat').is_dir() and not (ws / '.hugpy_fleet/chat').exists():
        env.setdefault('HUGPY_SESSION_STATE_DIR', '.hugpy_wrapper/chat')
    # the harness's toolserver tools: Core's own operator token for the host's
    # toolserver node, under the names the harness reads
    if core_env.get("HUGPY_CORE_TOOLSERVER_TOKEN"):
        env.setdefault("HUGPY_TOOLSERVER_TOKEN", core_env["HUGPY_CORE_TOOLSERVER_TOKEN"])
    if core_env.get("HUGPY_CORE_TOOLSERVER_URL"):
        env.setdefault("HUGPY_TOOLSERVER_URL", core_env["HUGPY_CORE_TOOLSERVER_URL"])
    # openpty + Popen rather than pty.fork(): Core is a threaded server, and a
    # bare fork in a multi-threaded process is the deadlock the stdlib warns
    # about; Popen's exec path is safe there and gives a proper handle.
    master, slave = pty.openpty()
    _winsize(slave, cols, rows)
    try:
        # umask 0007: files the TUI creates in the SHARED workspace (session
        # locks, drafts) stay group-writable for the sessions service; Core's
        # own unit runs at 0077, which would make them owner-only.
        proc = subprocess.Popen(argv, cwd=str(ws), env=env, stdin=slave, stdout=slave, stderr=slave,
                                start_new_session=True, close_fds=True, umask=0o007)
    finally:
        os.close(slave)
    return proc, master


def _pump(ws, fd: int, pid: int, closed: threading.Event) -> None:
    """PTY output -> websocket, until the TUI exits or the socket closes."""
    try:
        while not closed.is_set():
            ready, _, _ = select.select([fd], [], [], 0.5)
            if not ready:
                continue
            try:
                data = os.read(fd, 65536)
            except OSError:
                break
            if not data:
                break
            ws.send(data.decode("utf-8", "replace"))
    except Exception as exc:  # noqa: BLE001 — a closed socket is the normal end
        logger.debug("station term pump ended: %s", exc)
    finally:
        closed.set()
        try:
            ws.close()
        except Exception:  # noqa: BLE001
            pass


def terminal(ws):
    """One websocket = one tmux client; the real harness session survives it."""
    from hugpy_core.router.observability import store as routing

    class RequestView:
        client_address = (request.remote_addr or "", 0)
        headers = request.headers
        request = request.environ.get("werkzeug.socket")
    denied = routing.KEYS.check(RequestView(), "admin")
    if denied:
        status, body = denied
        text = "hugpy-fleet: %s (HTTP %s)" % (body.get("error") or "not permitted", status)
        ws.send("\r\n  " + text + "\r\n")
        ws.close(reason=1008, message=text[:120])          # the close frame carries the reason too
        return
    if _LIVE["count"] >= MAX_TERMINALS:
        ws.send("\r\n  hugpy-fleet: too many open terminals on this core; close one first\r\n")
        ws.close()
        return
    try:
        cols = int(request.args.get("cols") or 120)
        rows = int(request.args.get("rows") or 36)
    except ValueError:
        cols, rows = 120, 36
    try:
        proc, fd = _spawn(cols, rows)
    except OSError as exc:
        ws.send("\r\n  hugpy-fleet: cannot start the TUI: %s\r\n" % exc)
        ws.close()
        return
    _LIVE["count"] += 1
    closed = threading.Event()
    threading.Thread(target=_pump, args=(ws, fd, proc.pid, closed), name="station-term-pump", daemon=True).start()
    try:
        while not closed.is_set():
            try:
                frame = ws.receive(timeout=1)
            except Exception:  # noqa: BLE001 — socket gone
                break
            if frame is None:
                continue
            if isinstance(frame, bytes):
                frame = frame.decode("utf-8", "replace")
            if frame.startswith(RESIZE):
                try:
                    c, r = frame[len(RESIZE):].split("x", 1)
                    _winsize(fd, int(c), int(r))
                except (ValueError, OSError):
                    pass
                continue
            try:
                os.write(fd, frame.encode("utf-8"))
            except OSError:
                break
    finally:
        closed.set()
        _LIVE["count"] -= 1
        if proc.poll() is None:
            proc.send_signal(signal.SIGHUP)              # detach this client; keep the tmux TUI running
            try:
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                proc.terminate()
                try:
                    proc.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()
        try:
            os.close(fd)
        except OSError:
            pass


def attach(app) -> bool:
    """Mount the websocket route; False (and a log line) when flask-sock is
    not installed, so Core still serves everything else."""
    try:
        from flask_sock import Sock
    except ImportError:
        logger.warning("station terminal disabled: flask-sock is not installed")
        return False
    sock = Sock(app)
    sock.route("/api/station/term")(terminal)

    def terminal_bare(ws):        # the same bridge without the /api prefix (dual mount, distinct endpoint)
        return terminal(ws)
    sock.route("/station/term")(terminal_bare)
    return True
