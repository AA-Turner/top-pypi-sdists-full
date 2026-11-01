"""the reads/ folder layout (per thread root, per session folders) and whole-file JSON reads and writes."""

from __future__ import annotations
import json
import os
import secrets
import threading
import time
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

#: The env switch that turns the reader on for a session before the wizard's
#: daemon profile exists (plan T8 makes the profile the switch).
ENV_READS = "PROBE_DAEMON_READS"


#: The Probe service serves sessions whose state folders differ from its own:
#: on its mailbox thread, `rooted` points every path here at the session's.
_ROOTED = threading.local()


def root() -> Path:
    override = getattr(_ROOTED, "root", None)
    if override is not None:
        return override
    base = os.environ.get("XDG_STATE_HOME") or str(Path.home() / ".local" / "state")
    return Path(base) / "probe" / "reads"


class Late(Exception):
    """The Probe service's step reached its request's deadline before an
    irreversible write: nothing was written, and its caller writes it."""


def check_deadline() -> None:
    """On the service's thread (`rooted` with a deadline): raise `Late` once
    the request's deadline has passed. Called right before every `os.replace`,
    so a step that ran long never writes after its caller gave up and wrote."""
    deadline = getattr(_ROOTED, "deadline", None)
    if deadline is not None and time.monotonic() > deadline:
        raise Late()


@contextmanager
def rooted(state_dir: "str | Path", *, deadline: "float | None" = None) -> Iterator[None]:
    """Every path here under `<state_dir>/reads`, on this thread only (the
    Probe service's mailbox thread, acting for a session; `state_dir` is its
    `<XDG_STATE_HOME>/probe`), and no write past `deadline` (monotonic:
    `check_deadline`). A post from inside never goes to the service."""
    previous = (getattr(_ROOTED, "root", None), getattr(_ROOTED, "deadline", None))
    _ROOTED.root = Path(state_dir) / "reads"
    _ROOTED.deadline = deadline
    try:
        yield
    finally:
        _ROOTED.root, _ROOTED.deadline = previous


def _safe(session_id: str) -> str:
    return "".join(c for c in session_id if c.isalnum() or c in "-_") or "session"


def asks_dir(session_id: str) -> Path:
    return root() / "asks" / _safe(session_id)


def messages_dir(session_id: str) -> Path:
    return root() / "messages" / _safe(session_id)


def claimed_dir(session_id: str) -> Path:
    return root() / "claimed" / _safe(session_id)


def turn_path(session_id: str) -> Path:
    return root() / "turns" / _safe(session_id)


def heartbeat_path(session_id: str, ask_id: str) -> Path:
    return asks_dir(session_id) / f"{ask_id}.alive"


def _write_json(path: Path, data: dict, *, exclusive: bool = False) -> None:
    """Write `data` to `path` whole: a temp file, then `os.replace` (or, when
    `exclusive`, `os.link`, which fails if the name is taken)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.{secrets.token_hex(3)}.tmp")
    tmp.write_text(json.dumps(data, sort_keys=True), encoding="utf-8")
    try:
        check_deadline()
        if exclusive:
            os.link(tmp, path)
        else:
            os.replace(tmp, path)
    finally:
        if exclusive or tmp.exists():
            tmp.unlink(missing_ok=True)


#: A mailbox file larger than this is not read (a message is a few KB).
MAX_FILE_BYTES = 4 * 1024 * 1024


def _read_json(path: Path) -> "dict | None":
    """A regular file's JSON object, opened without blocking (a FIFO where a
    message goes is no message, never a read that hangs: the Probe service
    reads these for every session)."""
    import stat

    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOCTTY", 0))
    except OSError:
        return None
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode) or st.st_size > MAX_FILE_BYTES:
            return None
        chunks = []
        while True:
            chunk = os.read(fd, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        data = json.loads(b"".join(chunks).decode("utf-8"))
    except (OSError, ValueError, RecursionError):
        return None
    finally:
        os.close(fd)
    return data if isinstance(data, dict) else None


#: The folders under `root`, one per kind of mailbox file. A run's read
#: recorder keeps its own folders beside them (`probe.sdk.capture.lineage.spool.spool.state_dir`).
FOLDERS = ("asks", "messages", "claimed", "requests", "turns", "status", "alerts", "alive", "hints")
#: In each of `FOLDERS`, empty, read by nothing: what keeps an SDK's dead-run
#: recovery from deleting the folder. Every SDK since recovery began leaves a
#: folder holding a `*.jsonl` its `<host>.<pid>` rule does not parse
#: (`inputs._clear_dead_folder`), and one from #3616 on takes no folder
#: without a run's own file (`inputs._sdk_owned`).
KEEP_FILE = "probe-mailbox.jsonl"


def keep_folders() -> None:
    """Each of `FOLDERS`, made if missing, with its `KEEP_FILE`: an SDK from
    before #3616, in a training venv nobody updates, takes any folder under
    `root` unchanged for 10 minutes for a dead run's and deletes it whole,
    every session's asks, requests and messages with it, whether or not a
    worker runs. Called by the running worker at its start and every poll, and
    by `probe ask` before it files anything. Best effort."""
    base = root()
    for name in FOLDERS:
        path = base / name / KEEP_FILE
        try:
            if not path.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch()
        except OSError:
            pass  # the next caller makes it
