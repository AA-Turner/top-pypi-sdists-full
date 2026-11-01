"""track server inbox messages here: where each is, which were shown, return the unshown."""

from __future__ import annotations
import json
import os
import time
from pathlib import Path

from probe.foundation.compat.compat import StrEnum


class Where(StrEnum):
    """Where a message is in the mailbox (`where`)."""

    WAITING = "waiting"  # published, not delivered (a service claim not received included)
    CLAIMED = "claimed"  # a deliverer moved it into claimed/ under its own name: shown


def where(session_id: str, message_id: str) -> "Where | None":
    """Where message `message_id` is in this session's mailbox, until the sweep:
    waiting, claimed (a hook took it, its receipt done), or None (never
    published, or gone)."""
    if claimed_dir(session_id).is_dir():
        names = [p.name for p in claimed_dir(session_id).glob(f"*-{message_id}*.json")]
        if any(message_id_of(Path(n)) == message_id and n.count(".") == 1 for n in names):
            return Where.CLAIMED
        if any(message_id_of(Path(n)) == message_id for n in names):
            return Where.WAITING  # the service claimed it for a deliverer that has not shown it yet
    if messages_dir(session_id).is_dir():
        if any(message_id_of(p) == message_id for p in messages_dir(session_id).glob(f"*-{message_id}.json")):
            return Where.WAITING
    return None


def waiting_inbox_ids(session_id: str) -> "list[str]":
    """The server ids of the inbox messages still waiting here (published, not
    taken by a hook): the copies the poll asks Probe whether to keep."""
    import uuid

    out = set()
    folder = messages_dir(session_id)
    if folder.is_dir():
        for path in folder.glob(f"*-{INBOX_ID_PREFIX}*.json"):
            message_id = message_id_of(path)
            try:
                out.add(str(uuid.UUID(message_id[len(INBOX_ID_PREFIX):])))
            except ValueError:
                continue
    return sorted(out)


def inbox_server_id(message_id: str) -> "str | None":
    """The server id (a uuid) of inbox message `message_id` (`inbox_message_id`), or None."""
    import uuid

    if not message_id.startswith(INBOX_ID_PREFIX):
        return None
    try:
        return str(uuid.UUID(hex=message_id[len(INBOX_ID_PREFIX):]))
    except ValueError:
        return None


#: An inbox message a deliverer that writes `shown` lines claimed, and never
#: marked shown this long after its claim, goes back to waiting: its hook died,
#: or its output never went out, between the claim and the handoff (review of
#: #3530). A live hook marks it within milliseconds of the claim.
UNSHOWN_RETURN_S = 60.0
#: How much of the claim log and the shown log the inbox rule reads (their tails).
INBOX_LOG_TAIL_BYTES = 256 * 1024


def _log_tail(path: Path) -> "list[dict]":
    """The JSON lines of `path`'s last INBOX_LOG_TAIL_BYTES (a partial first line skipped)."""
    try:
        with path.open("rb") as handle:
            size = os.fstat(handle.fileno()).st_size
            handle.seek(max(0, size - INBOX_LOG_TAIL_BYTES))
            tail = handle.read().decode("utf-8", "replace")
    except OSError:
        return []
    out = []
    for line in tail.splitlines():
        try:
            entry = json.loads(line)
        except ValueError:
            continue
        if isinstance(entry, dict) and isinstance(entry.get("id"), str):
            out.append(entry)
    return out


class InboxClaims:
    """What the logs say about the inbox messages claimed in one session: the
    `shown` lines (written by a deliverer only once its output went out) and
    the claim lines. Decided PER CLAIM (review of #3530): a current hook or pi
    marks every claim it makes of an inbox message (`shows: 1` on its own claim
    line, and on a receipt line after a Probe service claimed it for it); an
    older deliverer (before `shown` lines, #3467) marks none."""

    def __init__(self, session_id: str) -> None:
        self.shown = {e["id"] for e in _log_tail(shown_log_path(session_id))}
        self.claims: dict[str, list[dict]] = {}
        for entry in _log_tail(claim_log_path(session_id)):
            self.claims.setdefault(entry["id"], []).append(entry)

    def shown_here(self, message_id: str) -> bool:
        """Was inbox message `message_id`, claimed here, handed to the agent?
        Its latest claim line decides: one with the marker (`shows: 1`, a
        deliverer that writes `shown` lines) only when a `shown` line names the
        message; one without it (a deliverer from before them, or a service
        claim no current hook received) at its claim, as before."""
        if message_id in self.shown:
            return True
        lines = self.claims.get(message_id)
        return not (lines and lines[-1].get("shows") == 1)

    def claimed_at(self, message_id: str, path: Path) -> float:
        """When it was claimed: its latest claim line, else the file's change time."""
        stamps = [float(e["at"]) for e in self.claims.get(message_id, [])
                  if isinstance(e.get("at"), (int, float))]
        if stamps:
            return max(stamps)
        try:
            return path.stat().st_ctime
        except OSError:
            return time.time()


def _claimed_inbox(session_id: str, now: float) -> "list[tuple[str, str, Path]]":
    """(server id, message id, file) of each inbox message claimed here under
    the plain name (its receipt done) that Probe still serves (not past its
    INBOX_TTL_S)."""
    out = []
    folder = claimed_dir(session_id)
    if folder.is_dir():
        for path in sorted(folder.glob(f"*-{INBOX_ID_PREFIX}*.json")):
            if path.name.count(".") != 1:
                continue  # a service claim its deliverer has not received: not shown yet
            message_id = message_id_of(path)
            server_id = inbox_server_id(message_id)
            msg = read_message(path) if server_id else None
            if msg is None or not msg.from_inbox or (msg.expires_at and msg.expires_at < now):
                continue
            out.append((server_id, message_id, path))
    return out


def shown_inbox_ids(session_id: str, *, now: "float | None" = None) -> "list[str]":
    """The server ids of the inbox messages handed to the agent here
    (`InboxClaims.shown_here`) that Probe still serves: the ones the daemon
    reports `delivered_to_agent`, a restarted one before it polls again."""
    now = time.time() if now is None else now
    claims = InboxClaims(session_id)
    return sorted({server_id for server_id, message_id, _path in _claimed_inbox(session_id, now)
                   if claims.shown_here(message_id)})


def inbox_shown(session_id: str, message_id: str) -> bool:
    """Was inbox message `message_id` handed to the agent here (claimed and
    shown, `InboxClaims.shown_here`)? False while it waits or is gone."""
    return where(session_id, message_id) is Where.CLAIMED and InboxClaims(session_id).shown_here(message_id)


def return_unshown_inbox(session_id: str, *, now: "float | None" = None,
                         after: "float | None" = None) -> "list[str]":
    """Put back to waiting every inbox message claimed here more than `after`
    (UNSHOWN_RETURN_S) ago that was never shown (`InboxClaims.shown_here`), so
    the next prompt or tool call shows it. Their mailbox ids."""
    now = time.time() if now is None else now
    after = UNSHOWN_RETURN_S if after is None else after
    claims = InboxClaims(session_id)
    out = []
    for _server_id, message_id, path in _claimed_inbox(session_id, now):
        if claims.shown_here(message_id) or now - claims.claimed_at(message_id, path) < after:
            continue
        if unclaim(session_id, message_id):
            out.append(message_id)
    return out


def unclaim(session_id: str, message_id: str) -> bool:
    """Move inbox message `message_id` from claimed/ (its plain name) back to
    waiting: a deliverer took it and never handed it over. True when it moved.
    Only an inbox message: every other kind keeps its claim."""
    folder = claimed_dir(session_id)
    for path in folder.glob(f"*-{message_id}.json") if folder.is_dir() else ():
        if path.name.count(".") != 1 or message_id_of(path) != message_id:
            continue
        msg = read_message(path)
        if msg is None or not msg.from_inbox:
            return False
        target = messages_dir(session_id) / path.name
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.rename(path, target)
        except OSError:
            return False
        return True
    return False


def drop_waiting(session_id: str, message_id: str) -> bool:
    """Remove message `message_id` while it still waits (another Probe daemon of
    the session holds its delivery). True when a file went; a claimed one stays."""
    folder = messages_dir(session_id)
    gone = False
    if folder.is_dir():
        for path in folder.glob(f"*-{message_id}.json"):
            if message_id_of(path) == message_id:
                try:
                    path.unlink()
                    gone = True
                except FileNotFoundError:
                    pass  # a hook took it first
    return gone
from probe.shared.mailbox.delivery import claim_log_path, shown_log_path  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.mailbox.layout import claimed_dir, messages_dir  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.mailbox.mailbox import INBOX_ID_PREFIX, message_id_of, read_message  # noqa: E402 -- pieces need each other; the front door loads this one first
