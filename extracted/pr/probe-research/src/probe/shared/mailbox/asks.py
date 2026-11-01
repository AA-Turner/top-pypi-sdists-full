"""file asks (for the reader) and requests (for the writer) and let the worker take them."""

from __future__ import annotations
import os
import secrets
import textwrap
import time
from dataclasses import asdict, dataclass
from pathlib import Path

#: `probe ask --wait` touches its heartbeat this often...
HEARTBEAT_S = 5.0
#: ...and a heartbeat older than this means nobody is waiting any more.
HOLD_FRESH_S = 15.0
#: `probe ask --wait` gives up after this long; the answer then goes out as a message.
WAIT_MAX_S = 2 * 3600
#: The most a request to the writer may carry (`probe ask --writer`): room for a
#: phase handover or a branch's conclusion, and under the 20,000 characters the
#: writer is shown of one (`bite.TEXT_SHOWN_CHARS`).
REQUEST_MAX_CHARS = 16_000
#: What a worker whose marker names no `request_chars` takes (it cuts the rest).
LEGACY_REQUEST_MAX_CHARS = 4000


# ---------------------------------------------------------------------------
# Asks.
# ---------------------------------------------------------------------------


@dataclass
class Ask:
    id: str
    session: str
    question: str
    asked_at: float
    wait: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> "Ask | None":
        try:
            return cls(id=str(data["id"]), session=str(data["session"]), question=str(data["question"]),
                       asked_at=float(data["asked_at"]), wait=bool(data.get("wait", False)))
        except (KeyError, TypeError, ValueError):
            return None


def new_ask_id() -> str:
    return "a" + secrets.token_hex(6)


def write_ask(session_id: str, question: str, *, wait: bool = False, now: "float | None" = None) -> Ask:
    """File a new ask for the reader; its id is never reused while the file exists."""
    keep_folders()  # it may wait for the next worker a while (`ASK_NO_WORKER`)
    for _ in range(32):
        ask = Ask(id=new_ask_id(), session=session_id, question=question,
                  asked_at=time.time() if now is None else now, wait=wait)
        try:
            _write_json(asks_dir(session_id) / f"{ask.id}.json", asdict(ask), exclusive=True)
            return ask
        except FileExistsError:
            continue
    raise RuntimeError("could not find a free ask id")


def pending_asks(session_id: str) -> list[Ask]:
    """Asks the worker has not taken yet, oldest first."""
    out = []
    folder = asks_dir(session_id)
    if not folder.is_dir():
        return out
    for path in folder.glob("a*.json"):
        data = _read_json(path)
        ask = Ask.from_dict(data) if data else None
        if ask is not None:
            out.append(ask)
    return sorted(out, key=lambda a: (a.asked_at, a.id))


def take_ask(session_id: str, ask_id: str) -> None:
    """The worker has stored the ask: move its file out of the way (kept a while)."""
    src = asks_dir(session_id) / f"{ask_id}.json"
    dst = asks_dir(session_id) / ".taken" / f"{ask_id}.json"
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.replace(src, dst)
    except FileNotFoundError:
        pass


def touch_heartbeat(session_id: str, ask_id: str) -> None:
    path = heartbeat_path(session_id, ask_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()


def held(session_id: str, ask_id: "str | None", *, now: "float | None" = None) -> bool:
    """Is a `probe ask --wait` still waiting for this ask's answer?"""
    if not ask_id:
        return False
    try:
        age = (time.time() if now is None else now) - heartbeat_path(session_id, ask_id).stat().st_mtime
    except OSError:
        return False
    return age < HOLD_FRESH_S


# ---------------------------------------------------------------------------
# Requests to the writer.
# ---------------------------------------------------------------------------


def requests_dir(session_id: str) -> Path:
    return root() / "requests" / _safe(session_id)


@dataclass
class Request:
    id: str
    session: str
    text: str
    asked_at: float
    wait: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> "Request | None":
        try:
            return cls(id=str(data["id"]), session=str(data["session"]), text=str(data["text"]),
                       asked_at=float(data["asked_at"]), wait=bool(data.get("wait", False)))
        except (KeyError, TypeError, ValueError):
            return None


def new_request_id() -> str:
    return "w" + secrets.token_hex(6)


def request_text(value: str) -> str:
    """A request to the writer as it is filed and shown: its line breaks and
    indentation kept (a handover reads as the lists, paragraphs and code it was
    written in), every kind of line end read as one, each line's trailing space,
    the blank lines at either end and the indentation every line shares
    dropped, and a run of blank lines kept as one. `probe ask --writer` files
    it so (its length is the one checked against REQUEST_MAX_CHARS) and the
    worker reads it so (a CLI before this one filed one line)."""
    lines: list[str] = []
    for line in value.splitlines():
        line = line.rstrip()
        if line or (lines and lines[-1]):
            lines.append(line)
    while lines and not lines[-1]:
        lines.pop()
    return textwrap.dedent("\n".join(lines))


def write_request(session_id: str, text: str, *, wait: bool = False, now: "float | None" = None) -> Request:
    """File a request for the daemon's writer; its id is never reused while the file exists."""
    keep_folders()  # it may wait for the next worker a while (`ASK_NO_WORKER`)
    for _ in range(32):
        req = Request(id=new_request_id(), session=session_id, text=text,
                      asked_at=time.time() if now is None else now, wait=wait)
        try:
            _write_json(requests_dir(session_id) / f"{req.id}.json", asdict(req), exclusive=True)
            return req
        except FileExistsError:
            continue
    raise RuntimeError("could not find a free request id")


def pending_requests(session_id: str) -> list[Request]:
    """Requests the worker has not taken yet, oldest first."""
    folder = requests_dir(session_id)
    if not folder.is_dir():
        return []
    out = [req for path in folder.glob("w*.json") if (req := Request.from_dict(_read_json(path) or {})) is not None]
    return sorted(out, key=lambda r: (r.asked_at, r.id))


def take_request(session_id: str, request_id: str) -> None:
    """The worker has stored the request: move its file out of the way (kept a while)."""
    src = requests_dir(session_id) / f"{request_id}.json"
    dst = requests_dir(session_id) / ".taken" / f"{request_id}.json"
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.replace(src, dst)
    except FileNotFoundError:
        pass
from probe.shared.mailbox.layout import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _read_json,
    _safe,
    _write_json,
    asks_dir,
    heartbeat_path,
    keep_folders,
    root,
)
