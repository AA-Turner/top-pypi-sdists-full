"""The daemon writer's request files, in ONE format: `probe ask --writer` files them (through
`probe.shared.mailbox.asks`), and so does a run waiting for its session's project. Imports only
the stdlib and `probe.foundation`, so a training script with no CLI can write them."""

from __future__ import annotations

import json
import os
import secrets
import time
from collections.abc import Callable
from dataclasses import asdict, dataclass
from pathlib import Path

from probe.foundation.durable import homedir

#: Under the reads root, one folder per session: `<root>/requests/<session>/<id>.json`.
REQUESTS_FOLDER = "requests"
#: A request id is this letter and 12 hex digits; its file is `<id>.json`.
ID_PREFIX = "w"


@dataclass
class WriterRequest:
    """One request for a session's daemon writer, as its file holds it."""

    id: str
    session: str
    text: str
    asked_at: float
    wait: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> "WriterRequest | None":
        try:
            return cls(id=str(data["id"]), session=str(data["session"]), text=str(data["text"]),
                       asked_at=float(data["asked_at"]), wait=bool(data.get("wait", False)))
        except (KeyError, TypeError, ValueError):
            return None


def get_reads_root() -> Path:
    """`<XDG_STATE_HOME>/probe/reads`, where the daemon's mailbox lives (`~` from `homedir`: a
    process with no HOME and no passwd entry gets the SDK's stand-in, not a crash)."""
    base = os.environ.get("XDG_STATE_HOME") or str(homedir.home() / ".local" / "state")
    return Path(base) / "probe" / "reads"


def to_folder_name(session_id: str) -> str:
    """A session id as a folder name: letters, digits, `-` and `_` only."""
    return "".join(c for c in session_id if c.isalnum() or c in "-_") or "session"


def get_requests_dir(session_id: str, root: "Path | None" = None) -> Path:
    """The session's request folder under `root` (default `get_reads_root()`)."""
    return (root if root is not None else get_reads_root()) / REQUESTS_FOLDER / to_folder_name(session_id)


def make_request_id() -> str:
    return ID_PREFIX + secrets.token_hex(6)


def write_writer_request(session_id: str, text: str, *, wait: bool = False, now: "float | None" = None,
                         root: "Path | None" = None,
                         before_write: "Callable[[], None] | None" = None) -> WriterRequest:
    """File a request for the session's daemon writer; its id is never reused while the file
    exists. `before_write` runs right before the file appears (the Probe service's deadline)."""
    folder = get_requests_dir(session_id, root)
    for _ in range(32):
        req = WriterRequest(id=make_request_id(), session=session_id, text=text,
                            asked_at=time.time() if now is None else now, wait=wait)
        try:
            _write_new(folder / f"{req.id}.json", asdict(req), before_write)
            return req
        except FileExistsError:
            continue
    raise RuntimeError("could not find a free request id")


def _write_new(path: Path, data: dict, before_write: "Callable[[], None] | None") -> None:
    """Write `data` to `path` whole, only if the name is free: a temp file, then `os.link`
    (which fails when the name is taken)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.{secrets.token_hex(3)}.tmp")
    tmp.write_text(json.dumps(data, sort_keys=True), encoding="utf-8")
    try:
        if before_write is not None:
            before_write()
        os.link(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)
