"""a message from another agent session, with its sender resolved to a session to exclude."""

from __future__ import annotations
import os
import re
import time
from collections import OrderedDict
from collections.abc import Callable
from pathlib import Path
#: Only a session id is excluded for a peer's message: a name could match any doc id.
_SESSION_ID = re.compile(r"[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}")
#: A peer's address in its event's `command`: `<name> (uds:<socket>)`.
_ADDRESS = re.compile(r"\((uds:[^()]+)\)\s*\Z")
#: Claude Code's socket for a session, `<pid>.sock` (`/run/user/<uid>/cc-socks/`,
#: older builds `/tmp/cc-socks/`), and its record of the session, `<pid>.json`.
_SOCKET_PID = re.compile(r"(\d+)\.sock")
#: Claude Code's session records looked through for one socket, at most, and
#: the size of one (a few hundred bytes).
MAX_SESSION_FILES = 512
MAX_SESSION_FILE_BYTES = 64 * 1024
#: A sender found is remembered this long (a pid, and so a socket, is reused
#: only by a later process); one not found is looked for again after SENDER_MISS_S.
SENDER_KEEP_S = 10 * 60.0
SENDER_MISS_S = 30.0
MAX_SENDERS = 256


def sender_of(event) -> str | None:
    """A peer message's sender as the harness gave it: `uds:<socket>` (another
    Claude Code session), a session id, or a helper agent's id or path."""
    args = event.tool_input or {}
    sender = args.get("from") if isinstance(args.get("from"), str) else None
    if not sender:
        command = event.command() or ""
        hit = _ADDRESS.search(command)
        sender = hit.group(1) if hit else command
    return sender.strip() or None


# -- a peer's session ----------------------------------------------------------


def claude_sessions_dir(env: dict) -> Path:
    """Where Claude Code keeps a record of each running session (`<pid>.json`:
    its `sessionId`, its `messagingSocketPath`), for a session with `env`."""
    base = env.get("CLAUDE_CONFIG_DIR") or os.path.join(env.get("HOME") or str(Path.home()), ".claude")
    return Path(base) / "sessions"


class Senders:
    """A peer message's sender to the session id that sent it. Another Claude
    Code session's message names its socket (`uds:<path>`), never its session:
    the session is the record whose `messagingSocketPath` is that path, else the
    record of the socket's pid (`<pid>.sock` -> `<pid>.json`, a build that
    records no path). A sender that is a session id already is one; a helper
    agent (its id, a Codex agent path) is none. Remembered per address."""

    def __init__(self, sessions_dir: Callable[[dict], Path] = claude_sessions_dir,
                 clock: Callable[[], float] = time.monotonic) -> None:
        self._dir_of = sessions_dir
        self.clock = clock
        #: address -> (session id or None, until when it holds)
        self._known: OrderedDict = OrderedDict()

    def resolve(self, sender: str, env: dict) -> str | None:
        if _SESSION_ID.fullmatch(sender):
            return sender
        if not sender.startswith("uds:"):
            return None
        address = sender[len("uds:"):]
        now = self.clock()
        hit = self._known.get(address)
        if hit is not None and now < hit[1]:
            return hit[0]
        try:
            sid = self._look(self._dir_of(env), address)
        except Exception:  # noqa: BLE001 -- unknown: nothing excluded
            sid = None
        self._known[address] = (sid, now + (SENDER_KEEP_S if sid else SENDER_MISS_S))
        self._known.move_to_end(address)
        while len(self._known) > MAX_SENDERS:
            self._known.popitem(last=False)
        return sid

    @staticmethod
    def _look(folder: Path, address: str) -> str | None:
        from ...mail.watch import read_json

        try:
            names = sorted(os.listdir(folder))[:MAX_SESSION_FILES]
        except OSError:
            return None
        for name in names:
            if not name.endswith(".json"):
                continue
            data = read_json(str(folder / name), MAX_SESSION_FILE_BYTES)
            if isinstance(data, dict) and data.get("messagingSocketPath") == address:
                sid = data.get("sessionId")
                return sid if isinstance(sid, str) and _SESSION_ID.fullmatch(sid) else None
        pid = _SOCKET_PID.fullmatch(os.path.basename(address))
        if pid is None:
            return None
        data = read_json(str(folder / f"{pid.group(1)}.json"), MAX_SESSION_FILE_BYTES)
        if not isinstance(data, dict):
            return None
        recorded = data.get("messagingSocketPath")
        if isinstance(recorded, str) and recorded and recorded != address:
            return None  # that pid's session listens elsewhere: not this sender
        sid = data.get("sessionId")
        return sid if isinstance(sid, str) and _SESSION_ID.fullmatch(sid) else None
