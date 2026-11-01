"""remove expired messages, old claims and taken asks, and whole stale sessions."""

from __future__ import annotations
import time
#: Claimed messages and taken asks are kept this long, then swept.
KEEP_CLAIMED_S = 7 * 24 * 3600
#: A turn's unasked-delivery slot file is swept after this long.
UNASKED_SLOT_KEEP_S = 24 * 3600


def open_asks(session_id: str, *, now: "float | None" = None) -> list[str]:
    """Ask and request ids still waiting for their end (an answer, nothing
    found, or failed): filed or taken, younger than ANSWER_TTL_S, and with no
    ending message claimed yet. The Stop hook's wake waits for their answers
    while one is open (and for run alerts while the session's worker runs)."""
    now = time.time() if now is None else now
    asked: dict[str, float] = {}
    for folder, pattern in ((asks_dir(session_id), "a*.json"), (asks_dir(session_id) / ".taken", "a*.json"),
                            (requests_dir(session_id), "w*.json"),
                            (requests_dir(session_id) / ".taken", "w*.json")):
        if not folder.is_dir():
            continue
        for path in folder.glob(pattern):
            data = _read_json(path)
            ask = (Ask.from_dict(data) if pattern.startswith("a") else Request.from_dict(data)) if data else None
            if ask is not None and now - ask.asked_at < ANSWER_TTL_S:
                asked[ask.id] = ask.asked_at
    folder = claimed_dir(session_id)
    if folder.is_dir():
        for path in folder.glob("*.json"):
            if path.name.count(".") > 1:
                continue  # a service claim not received yet: its ask is still open
            data = _read_json(path)
            if data and data.get("ask") and data.get("kind") != Kind.MESSAGE:
                asked.pop(str(data["ask"]), None)
    return sorted(asked, key=lambda i: (asked[i], i))


def sweep(session_id: str, *, now: "float | None" = None) -> int:
    """Remove expired messages, and claimed messages and taken asks past KEEP_CLAIMED_S."""
    now = time.time() if now is None else now
    removed = 0
    for path, msg in [(p, Message.from_dict(_read_json(p) or {})) for p in messages_dir(session_id).glob("*.json")]:
        if msg is not None and msg.expires_at and msg.expires_at < now:
            path.unlink(missing_ok=True)
            removed += 1
    for path in asks_dir(session_id).glob("*.alive") if asks_dir(session_id).is_dir() else ():
        try:  # a killed `probe ask --wait` leaves its heartbeat behind
            if now - path.stat().st_mtime > UNASKED_SLOT_KEEP_S:
                path.unlink(missing_ok=True)
                removed += 1
        except OSError:
            pass
    for folder in (claimed_dir(session_id), asks_dir(session_id) / ".taken", requests_dir(session_id) / ".taken"):
        if not folder.is_dir():
            continue
        for path in folder.glob("*.json"):
            try:
                if now - path.stat().st_mtime > KEEP_CLAIMED_S:
                    path.unlink(missing_ok=True)
                    removed += 1
            except OSError:
                pass
    # A turn's unasked-delivery slots (`turns/<sid>.unasked-<token>`, `.hint-`): the
    # prompt hook clears old ones only when Python runs; past a day none is current.
    turn = turn_path(session_id)
    slots = [path for slot in (SLOT_UNASKED, SLOT_HINT) for path in turn.parent.glob(f"{turn.name}.{slot}-*")] \
        if turn.parent.is_dir() else []
    for path in slots:
        try:
            if now - path.stat().st_mtime > UNASKED_SLOT_KEEP_S:
                path.unlink(missing_ok=True)
                removed += 1
        except OSError:
            pass
    return removed


def sweep_stale_sessions(keep: str, *, now: "float | None" = None, max_age: float = KEEP_CLAIMED_S) -> int:
    """Remove every file of sessions whose mailbox has not changed in `max_age`
    (the worker's start-up sweep; `keep` is its own session), except a live
    worker's. One listing per folder kind; best effort."""
    import shutil

    now = time.time() if now is None else now
    base = root()
    removed = 0
    for kind in ("asks", "messages", "claimed", "requests"):
        folder = base / kind
        if not folder.is_dir():
            continue
        for sub in folder.iterdir():
            if sub.name == _safe(keep) or not sub.is_dir():
                continue
            if accepts_requests(sub.name):
                continue  # a live worker's session, however quiet (its marker is in requests/)
            try:
                newest = max([sub.stat().st_mtime] + [p.stat().st_mtime for p in sub.rglob("*")])
            except OSError:
                continue
            if now - newest > max_age:
                shutil.rmtree(sub, ignore_errors=True)
                removed += 1
    for kind in ("turns", "status", "alerts", "alive", "hints"):
        folder = base / kind
        if not folder.is_dir():
            continue
        for path in folder.iterdir():
            if path.name == KEEP_FILE:
                continue  # the folder's own (`keep_folders`), not a session's
            if path.name.startswith(_safe(keep)) or accepts_requests(path.name.split(".", 1)[0]):
                continue  # a live worker's status says what it is doing, however old
            try:
                if now - path.stat().st_mtime > max_age:
                    path.unlink(missing_ok=True)
                    removed += 1
            except OSError:
                pass
    return removed
from probe.shared.mailbox.asks import Ask, Request, requests_dir  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.mailbox.layout import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    KEEP_FILE,
    _read_json,
    _safe,
    asks_dir,
    claimed_dir,
    messages_dir,
    root,
    turn_path,
)
from probe.shared.mailbox.mailbox import ANSWER_TTL_S, Kind, Message  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.mailbox.poster import SLOT_HINT, SLOT_UNASKED  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.mailbox.worker_marker import accepts_requests  # noqa: E402 -- pieces need each other; the front door loads this one first
