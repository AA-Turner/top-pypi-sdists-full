"""SDK -> Probe daemon: one local datagram when a run opens and when it ends.

Daemon v2 (plan R3.1, the S10 channel): runs start floating and the daemon
files them. The daemon learns about a run the instant it starts, from the run
itself, instead of guessing from the transcript: capture's supervisor
(`tap/companion_supervisor.py`) binds a UNIX datagram socket per session in the
`daemon` state and appends every message to the session's inbox, which the
worker reads.

FIRE AND FORGET, BY CONTRACT. :func:`announce` never raises, never waits more
than ~200 ms, and does nothing at all when there is no session, no socket, or
any error. No daemon listening means the run floats and is filed later from
the session tag; a training run must never fail, slow down or print because of
this. The daemon treats every message as a HINT and verifies it with a Probe
read before acting, because any local process can write to the socket.

Stdlib only, like `agent_session`: a Miles actor spilling metric batches
imports the SDK and must not drag anything heavier in.

The wire, one JSON object per datagram:

    {"event": "run started", "run_id", "session_id", "name", "description",
     "tags", "config" (capped at ~4 KB; "config_truncated": true when cut),
     "intent", "parent_run_id", "relation", "command" (`probe exec` only)}
    {"event": "run ended", "run_id", "session_id", "status"}
"""

from __future__ import annotations

import contextlib
import contextvars
import errno
import hashlib
import json
import os
import shlex
import socket
import stat
import time
from collections.abc import Iterator, Mapping
from pathlib import Path
from typing import Any

from . import agent_session

EVENT_RUN_STARTED = "run started"
EVENT_RUN_ENDED = "run ended"

#: A UNIX socket path is at most 108 bytes (104 on macOS). Same number as
#: `companion_supervisor.MAX_SOCKET_PATH`: the two sides must pick the same path.
MAX_SOCKET_PATH = 100

#: Where a too-long path falls back to: `<root>/probe-<uid>/<hash>.sock`. A
#: module constant so tests can point it at a temporary folder; the supervisor
#: hardcodes `/tmp`.
FALLBACK_ROOT = Path("/tmp")

#: The whole send, socket setup included.
TIMEOUT_S = 0.2

#: `config` is the one field that can be arbitrarily large (a whole Hydra tree).
#: The daemon reads the real one from Probe; the message only has to say what
#: the run is.
MAX_CONFIG_BYTES = 4096

#: Every free-text field (description, intent, command, name).
MAX_TEXT_CHARS = 2000

#: The supervisor reads at most 64 KiB per datagram; stay well under it.
MAX_DATAGRAM_BYTES = 60_000

#: Tags a message carries at most.
MAX_TAGS = 64

#: The command `probe exec` wraps, set around its run creation so the run's
#: "run started" message can say what the run executes.
_COMMAND: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "probe_daemon_channel_command", default=None
)


def _state_base() -> Path:
    """`<state>/probe`: the one definition is `session_marker.state_dir()`
    (stdlib only too; imported here, when a message is sent, not at import)."""
    from . import session_marker

    return session_marker.state_dir()


def _private_folder(folder: Path) -> bool:
    """Owned by this user, a real directory (not a symlink), no group/other bits."""
    try:
        st = folder.lstat()
    except OSError:
        return False
    return (
        stat.S_ISDIR(st.st_mode)
        and st.st_uid == os.getuid()
        and not stat.S_IMODE(st.st_mode) & 0o077
    )


def socket_path(session_id: str) -> Path:
    """`<state>/probe/sessions/<sid>.sock`, the daemon's listening socket.

    When that is too long for a UNIX socket: `/tmp/probe-<uid>/<sha256(sid)[:24]>.sock`,
    and only if that folder is this user's private folder (else OSError). The
    supervisor computes the same path (`companion_supervisor.socket_path`) --
    keep the two in step. This side never creates the folder: a sender with no
    listener has nothing to send to.
    """
    if not agent_session.valid_session_id(session_id):
        raise ValueError("not a session id")
    path = _state_base() / "sessions" / (session_id + ".sock")
    if len(str(path).encode()) <= MAX_SOCKET_PATH:
        return path
    folder = FALLBACK_ROOT / f"probe-{os.getuid()}"
    if not _private_folder(folder):
        raise OSError(f"{folder} is not a private folder of this user")
    return folder / (hashlib.sha256(session_id.encode()).hexdigest()[:24] + ".sock")


def current_session_id(env: Mapping[str, str] | None = None) -> str | None:
    """This process's agent session: the agent's own variables, else the one a
    launcher forwarded (`PROBE_AGENT_SESSION`)."""
    found = agent_session.session_id_from_env(env)
    if found:
        return found
    forwarded = agent_session.forwarded_agent_session(env)
    return forwarded[1] if forwarded else None


def _text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value)
    return text if len(text) <= MAX_TEXT_CHARS else text[:MAX_TEXT_CHARS] + "..."


def _capped_config(config: Any) -> tuple[dict | None, bool]:
    """The config, or as many of its top-level keys as fit in MAX_CONFIG_BYTES."""
    if not isinstance(config, Mapping) or not config:
        return None, False
    try:
        whole = json.dumps(config, default=str, separators=(",", ":"))
    except (TypeError, ValueError):
        return None, True
    if len(whole.encode()) <= MAX_CONFIG_BYTES:
        return json.loads(whole), False
    kept: dict = {}
    used = 2
    for key, value in config.items():
        piece = json.dumps({str(key): value}, default=str, separators=(",", ":"))
        size = len(piece.encode()) - 1  # its `{`/`}` become one `,`
        if used + size > MAX_CONFIG_BYTES:
            continue
        kept[str(key)] = json.loads(piece)[str(key)]
        used += size
    return kept, True


#: Dropped in this order when a message does not fit: the daemon reads the full
#: run from Probe anyway, so what must survive is the run id and the session.
_BULKY = ("config", "config_truncated", "command", "description", "intent", "tags", "name")


def _encodings(message: dict) -> list[bytes]:
    """The message as JSON, then smaller and smaller, each under MAX_DATAGRAM_BYTES.

    More than one because the OS decides the real limit: Linux takes a 60 KB
    datagram, macOS refuses one past its UNIX-datagram buffer (a few KB by
    default) with EMSGSIZE / ENOBUFS, and the sender then retries smaller."""
    body = {k: v for k, v in message.items() if v is not None}
    out: list[bytes] = []
    for bulky in (None, *_BULKY):
        if bulky is not None:
            if bulky not in body:
                continue
            body.pop(bulky)
        data = json.dumps(body, default=str, separators=(",", ":")).encode()
        if len(data) <= MAX_DATAGRAM_BYTES:
            out.append(data)
    return out


def announce(event: str, *, env: Mapping[str, str] | None = None, **fields: Any) -> bool:
    """Send one message to this session's daemon. True when it was handed over.

    Never raises and never blocks the run for more than TIMEOUT_S: no session,
    no socket, an unsafe fallback folder, a full queue or any other error is a
    silent False, and the run carries on floating.
    """
    started = time.monotonic()
    try:
        family = getattr(socket, "AF_UNIX", None)
        if family is None:
            return False
        session_id = fields.pop("session_id", None) or current_session_id(env)
        if not session_id:
            return False
        path = socket_path(session_id)
        try:
            if not stat.S_ISSOCK(path.stat().st_mode):
                return False
        except OSError:
            return False
        sock = socket.socket(family, socket.SOCK_DGRAM)
        try:
            with contextlib.suppress(OSError):
                # macOS caps a UNIX datagram at the SENDER's buffer (2 KB by
                # default); raising it lets a full message through. Linux
                # already allows far more, so this changes nothing there.
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, MAX_DATAGRAM_BYTES + 4096)
            for data in _encodings({"event": event, "session_id": session_id, **fields}):
                remaining = TIMEOUT_S - (time.monotonic() - started)
                if remaining <= 0:
                    return False
                sock.settimeout(remaining)
                try:
                    sock.sendto(data, str(path))
                    return True
                except OSError as exc:
                    if exc.errno not in (errno.EMSGSIZE, errno.ENOBUFS):
                        return False
            return False
        finally:
            sock.close()
    except Exception:  # noqa: BLE001 -- the channel must never touch the run
        return False


@contextlib.contextmanager
def launch_command(argv: list[str] | None) -> Iterator[None]:
    """Name the command a run is opened for (`probe exec`), for its "run started"
    message. Scrubbed like the process span: a token on the command line must
    not reach the daemon's queue."""
    command = None
    if argv:
        try:
            from . import launch as _launch

            scrubbed, _ = _launch.scrub_argv(list(argv))
            command = _text(shlex.join(scrubbed))
        except Exception:  # noqa: BLE001
            command = None
    token = _COMMAND.set(command)
    try:
        yield
    finally:
        _COMMAND.reset(token)


def run_started(row: Mapping[str, Any] | None) -> bool:
    """Announce a run this process just opened, from the row the server returned."""
    try:
        if not isinstance(row, Mapping) or not row.get("id"):
            return False
        config, truncated = _capped_config(row.get("config"))
        metadata = row.get("metadata") if isinstance(row.get("metadata"), Mapping) else {}
        tags = row.get("tags") if isinstance(row.get("tags"), list) else None
        return announce(
            EVENT_RUN_STARTED,
            run_id=str(row["id"]),
            name=_text(row.get("name")),
            description=_text(row.get("description")),
            tags=[str(t) for t in tags[:MAX_TAGS]] if tags else None,
            config=config,
            config_truncated=True if truncated else None,
            intent=_text(metadata.get("intent")),
            parent_run_id=str(row["parent_run_id"]) if row.get("parent_run_id") else None,
            relation=row.get("parent_relation") if row.get("parent_run_id") else None,
            command=_COMMAND.get(),
        )
    except Exception:  # noqa: BLE001
        return False


def run_ended(run_id: str, status: str) -> bool:
    """Announce that this process closed a run, with the status it wrote."""
    try:
        return announce(EVENT_RUN_ENDED, run_id=str(run_id), status=str(status))
    except Exception:  # noqa: BLE001
        return False
